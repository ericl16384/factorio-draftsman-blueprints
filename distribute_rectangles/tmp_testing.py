import numpy as np

import belt_pathfinding as bp



number = 0b1111  # Decimal 15
bit_position = 1 # Clear the second bit from the right (0-indexed)

# 1. Create a mask and invert it, then apply bitwise AND
mask = ~(1 << bit_position)
result = number & mask

print(bin(result))  # Output: 0b1101 (Decimal 13)




occu_bm = np.zeros((20, 20), dtype=int)
belt_bm = np.zeros((20, 20), dtype=int)



occu_bm[:, 10] = 1
occu_bm[10, :] = 1

# print(occu_bm)
# print(occu_bm[0, 10:13])
# print(occu_bm[0, 10:13] & 0b111)

# print(np.logical_and(occu_bm[0, 10:13], [7, 9, 0]))
# print(np.logical_and(occu_bm[0, 10:13], [7, 9, 0]).any())

# print(np.ones((5, 1)))
# print(np.ones((5, 1)).ravel())
# print(np.ones((1, 3)))
# print(np.ones((1, 3)).ravel())

num = int.from_bytes(np.packbits([True, False, False, True, True], bitorder="little").tobytes())

print(f"0b{num:08b}")



for nxy in bp.neighbors((0, 12), occu_bm, belt_bm, (1000, 1000), 0):
    # print(nxy)
    pass

