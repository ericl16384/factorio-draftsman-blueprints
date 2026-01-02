

from draftsman.blueprintable import *
from draftsman.constants import Direction
from draftsman.entity import *

import draftsman





bp_string = "0eNqdlttuwyAMQH9l4plUgUBuv1JVE0lph0RIBLRbVeXfR1Ktt7EO8ohjHxvHF86gkQc+aKEsqM9AtL0yoF6fgRF7xeQkU6zjoAbMGN41Uqh90rH2QyieIDBCINSWf4EajdBjZDVTZui1TRou7Z06flS3p2FSPwptD04Cf+wvGg+OsihLfGdJxg0EXFlhBb9ccj6c3tWha7h2d7ha75ixiVCGa+s+QDD0xln1avLoSDlaUQhOoE4wXlHnYSs0by8K5RTfExjDPxLym5xeydkzGWEPOgtHo0g0uSWzY1ImXDp1Ldpk6CX38PFDUjxAGh4rjow1D0dnkegiuCpIXFWU4TGTyJircDSNRKMUvhwJr+ou9dcFQrFI8i8Sx/cyKkP+GsqWtsXM9xFJfIUFxkoXDB5UPKOJD50vGDyB6GLBnAhElwvmRCC6WtDOYWicLmhnH9rtv093npbfmkAKXS3TjRMKyzsHvz0FIJDMOZj3aDdI/tZqtpvER67NDKM5rkhV0aIgeV5W4/gN/Tevhg=="

bp = Blueprint.from_string(bp_string)

# import json
# print(json.dumps(bp.to_dict(), indent=2))
print(bp)
# print(bp.entities[0].filters)

# bp.entities[0].filters.append(draftsman.signatures.ItemFilter(index=0, name="iron-plate", quality=None))
# bp.entities[0].filters.append(draftsman.signatures.ItemFilter(index=1, name="iron-plate", quality=None))

# bp.entities[0].filters[0].name = "copper-plate"

# bp.entities[0].filters.append("iron-plate")
# bp.entities[0].filters.append("iron-plate")

# print(bp.entities[0].filters)

print(bp)

print(bp.to_string())

# print(bp.entities[0].filters[0])

# draftsman.signatures.ItemFilter()






# with open("reference_blueprint_book.txt") as f:
#     bp_string = f.read()

# book = BlueprintBook.from_string(bp_string)





# for bp in book.blueprints:
#     print(bp.label)

# # print(book.blueprints[1])

# g = Group()
# g.entities = book.blueprints[1].entities

# new_bp = Blueprint()
# for i in range(5):
#     new_bp.groups.append(g, position=(i*3, 0))

# print(new_bp.to_string())

# # print(g)

