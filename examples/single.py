# SPDX-Identifier: CC0-1.0
import torch

import tad_dftd3 as d3

numbers = d3.util.to_number(symbols="C C C C N C S H H H H H".split())
positions = torch.Tensor(
    [
        [-2.56745685564671, -0.02509985979910, 0.00000000000000],
        [-1.39177582455797, +2.27696188880014, 0.00000000000000],
        [+1.27784995624894, +2.45107479759386, 0.00000000000000],
        [+2.62801937615793, +0.25927727028120, 0.00000000000000],
        [+1.41097033661123, -1.99890996077412, 0.00000000000000],
        [-1.17186102298849, -2.34220576284180, 0.00000000000000],
        [-2.39505990368378, -5.22635838332362, 0.00000000000000],
        [+2.41961980455457, -3.62158019253045, 0.00000000000000],
        [-2.51744374846065, +3.98181713686746, 0.00000000000000],
        [+2.24269048384775, +4.24389473203647, 0.00000000000000],
        [+4.66488984573956, +0.17907568006409, 0.00000000000000],
        [-4.60044244782237, -0.17794734637413, 0.00000000000000],
    ]
)
param = dict(a1=0.49484001, s8=0.78981345, a2=5.73083694)

energy = d3.dftd3(numbers, positions, param)

torch.set_printoptions(precision=10)
print(energy)
# tensor([-0.0004075971, -0.0003940886, -0.0003817684, -0.0003949536,
#         -0.0003577212, -0.0004110279, -0.0005385976, -0.0001808242,
#         -0.0001563670, -0.0001503394, -0.0001577045, -0.0001764488])
