This is a well-framed problem. Let me evaluate Strategy 1 and then offer a genuinely different alternative, then give my recommendation.

---

## Evaluation of Strategy 1

The core idea is solid, but the precomputed 2D move array has a subtle trap: **its update cost isn't really O(1)**. When you force an existing belt to take an underground, that belt's surrounding cells may now have new options (or lose options), which means adjacency needs updating not just at the conflict point but at the new underground entry and exit too. This cascades. For a prototype, that bookkeeping will bite you.

The other issue is that storing the *set of possible moves* per cell per direction complicates your neighbor function significantly before you've even confirmed the rest of the system works.

---

## Strategy 2: Underground-Aware Single-Pass A* (with Lazy Conflict Resolution)

Don't precompute anything. Instead, expand the **search state** to carry underground context, and handle conflicts inside the neighbor function itself — computed on-the-fly, never cached.

### State becomes `(x, y, direction, underground_remaining)`

Instead of `(x, y, direction)`, your node is:

```python
(x, y, incoming_direction, underground_remaining)
# underground_remaining: 0 = on surface, 1–4 = tiles left in current underground run
```

### Neighbor generation handles three cases

```python
def neighbors(x, y, direction, underground_remaining, grid, belt_map):
    for dx, dy, new_dir in cardinal_moves(x, y, direction):
        nx, ny = x + dx, y + dy
        cell = belt_map[ny][nx]

        if underground_remaining > 0:
            # Currently underground — can pass through anything, must surface or continue
            yield surface_or_continue(nx, ny, new_dir, underground_remaining - 1)

        elif cell is None:
            # Empty cell — normal belt move
            yield (nx, ny, new_dir, 0), cost_normal(dx, dy, new_dir, direction)

        elif cell.direction == new_dir:
            # Blocked by a PARALLEL belt — can force it underground (insert a conflict)
            # Check if underground insertion is geometrically valid at this spot
            if can_insert_underground(nx, ny, new_dir, belt_map):
                conflict_cost = cost_normal(...) + len_of_forced_segment(nx, ny, new_dir, belt_map) * CONFLICT_PENALTY
                yield (nx, ny, new_dir, 0), conflict_cost  # tagged as conflict move

        else:
            # Blocked by a CROSSING belt — must go underground to pass through
            for reach in range(1, MAX_UNDERGROUND + 1):
                ex, ey = x + dx * reach, y + dy * reach  # underground exit
                if not in_bounds(ex, ey) or is_wall(ex, ey):
                    break
                yield (ex, ey, new_dir, 0), cost_underground(reach, new_dir, direction)
```

The key insight: **the search itself handles the three-way split** (empty, parallel-blocked, cross-blocked) without precomputing anything. You only compute conflict costs for cells the frontier actually reaches.

### After path is found

Walk the chosen path. Anywhere a "conflict move" edge was used, insert the underground retroactively into the existing belt's segment data. This is the only mutation step, and it's deferred until you're sure the path is chosen.

### Why this is better for a prototype

| | Strategy 1 | Strategy 2 |
|---|---|---|
| Precomputation | O(W×H×4) upfront + updates | None |
| Update after path commit | O(1) per cell? (actually more) | O(path length) walk |
| Neighbor function complexity | Simple lookup, complex maintenance | Slightly more logic, zero maintenance |
| Underground-during-conflict | Requires encoding in the move set | Falls out naturally from state |
| Incorrect-state risk | High (cascading updates) | None (computed fresh each search) |

---

## My Recommendation

**Use Strategy 2, but add one priority layer from Strategy 1's spirit:**

Give your cost function **three tiers of conflict moves**, ordered by disruption:

```
1. Underground through existing belt (geometrically valid)         → +SMALL_PENALTY (e.g. 0.5)
2. Force existing belt to take an underground (parallel conflict)  → +MEDIUM_PENALTY (e.g. 2.0 * segment_length)
3. Flag existing belt for full replanning                          → +LARGE_PENALTY (e.g. 20.0)
```

A* naturally selects the least disruptive conflict resolution that still yields the shortest total path. You don't need to special-case anything — the cost weighting does the prioritization for you.

For the "prefer 1 tile of space between belts" constraint you mentioned: add a small surcharge to the neighbor function when `belt_map[ny±1][nx]` or `belt_map[ny][nx±1]` is occupied. This also falls out naturally without precomputation.

The one place a precomputed structure **does** help: keep a fast `segment_id_at[y][x]` lookup so that `len_of_forced_segment()` is O(1) rather than requiring a scan. A simple integer array mapping every belt tile to its segment's index (into a segment list) is cheap to maintain and update.