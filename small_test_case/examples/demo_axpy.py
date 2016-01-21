import numpy as np
from small_test_case import basic

m = n = 4
colptr = np.array([0, 3, 6, 8, 10], dtype=np.int32)
rowind = np.array([0, 1, 3, 1, 2, 3, 0, 2, 1, 3], dtype=np.int32)
values = np.array([4.5, 3.1, 3.5, 2.9, 1.7, 0.4, 3.2, 3.0, 0.9, 1.0], dtype=np.float32)
x = np.array([1, 2, 3, 4], dtype=np.float32)
y = np.ones(4, dtype=np.float32)

print 'y:'
print y

basic.axpy(m, n, colptr, rowind, values, x, y)

print 'y:'
print y
