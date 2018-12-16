import numpy as np

"""
Generate dummy point data for a unit cube.
The data is written one line per frame, in [x, y, z, x, y, z ...]
order. So,  in this case:
  8 * x, y, z = 24 float values per line.

"""

start = [[-0.500000, -0.500000,  0.500000],
         [0.500000, -0.500000,  0.500000],
         [-0.500000,  0.500000,  0.500000],
         [0.500000,  0.500000,  0.500000],
         [-0.500000,  0.500000, -0.500000],
         [0.500000,  0.500000, -0.500000],
         [-0.500000, -0.500000, -0.500000],
         [0.500000, -0.500000, -0.500000]]

n = 20
s = np.array(start)

with open('testdata.pts', 'w') as fid:
    for i in range(n):
        r = np.random.standard_normal(s.shape) * 0.05
        v = ' '.join([str(i) for i in (r + s).ravel()])
        fid.write(v)
        fid.write('\n')
