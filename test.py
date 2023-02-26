import numpy as np

def make_sym(a):
    w, h, c = a.shape
    a[w - w // 2 :, :] = np.flipud(a[:w // 2, :])
    a[:, h - h // 2:] = np.fliplr(a[:, :h // 2])


m = (np.random.rand(3, 3, 3) * 10).astype(int)
print(m)
make_sym(m)
print(m)
