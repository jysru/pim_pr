import numpy as np


def quality(x, y):
    return np.power(np.abs(np.sum(x * np.conjugate(y))) / np.sum(np.abs(x) * np.abs(y)), 2)


def internal_pr(b, xc, A, max_iter=50, max_Qint=0.99):
    x_est = xc
    Ap = np.linalg.pinv(A)

    for i in range(max_iter):
        if i > 0:
            y_store = y_est
        y_est = b * np.exp(1j*np.angle(np.dot(A, x_est)))
        x_est = np.dot(Ap, y_est)
        if i > 0 and quality(y_store, y_est) >= max_Qint:
            break

    return x_est


def internal_pr_svd(b, xc, A, max_iter=50, max_Qint=0.99):
    x_est = xc
    y_est = b * np.exp(1j*np.angle(np.dot(A, x_est)))
    U, S, Vh = np.linalg.svd(A, full_matrices=False)

    for i in range(max_iter):
        if i > 0:
            y_store = y_est
        y_est = b * np.exp(1j*np.angle( np.dot( U, np.dot(U.conj().T, y_est) ) ))
        x_est = np.dot(Vh.conj().T, np.dot(U.conj().T, y_est) / S)
        if i > 0 and quality(y_store, y_est) >= max_Qint:
            break

    return x_est



def pim_pr(x, xc, A, max_iter=50, max_Q=0.99):

    for _ in range(max_iter):
        b = np.abs(np.dot(A, x))
        x_est = internal_pr(b, xc, A)
        x = np.abs(x) * np.exp(1j * (np.angle(x) - np.angle(x_est) + np.angle(xc)))
        q = quality(x, xc)
        print(f"Quality: {q}")
        if q > max_Q:
            break

    return x



def pim_pr_svd(x, xc, A, max_iter=50, max_Q=0.99):

    for _ in range(max_iter):
        b = np.abs(np.dot(A, x))
        x_est = internal_pr_svd(b, xc, A)
        x = np.abs(x) * np.exp(1j * (np.angle(x) - np.angle(x_est) + np.angle(xc)))
        q = quality(x, xc)
        print(f"Quality: {q}")
        if q > max_Q:
            break

    return x


n = 16
m = 8*n

x = np.ones(shape=(n))*np.exp(1j*2*np.pi*np.random.rand(n))
x1 = x
xc = np.ones(shape=(n))*np.exp(1j*2*np.pi*np.random.rand(n))
A = np.random.rand(m,n)*np.exp(1j*2*np.pi*np.random.rand(m,n))

x = pim_pr(x, xc, A)
print('end x1')
x2 = pim_pr_svd(x1, xc, A)
print('end x2')
