import json
from draftsman.data import recipes

# print(json.dumps(recipes.raw["iron-plate"], indent=4))

print(json.dumps(list(recipes.categories.keys())))