import math
from .errors import ChannelValidationError,StateValidationError

def dagger(A): return [[complex(A[j][i]).conjugate() for j in range(len(A))] for i in range(len(A[0]))]
def matmul(A,B):
    if not A or not B or len(A[0])!=len(B): raise StateValidationError('shape mismatch')
    return [[sum(complex(A[i][k])*complex(B[k][j]) for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def matvec(A,v):
    if not A or len(A[0])!=len(v): raise StateValidationError('shape mismatch')
    return [sum(complex(A[i][k])*complex(v[k]) for k in range(len(v))) for i in range(len(A))]
def eye(n): return [[1+0j if i==j else 0j for j in range(n)] for i in range(n)]
def add(A,B): return [[complex(A[i][j])+complex(B[i][j]) for j in range(len(A[0]))] for i in range(len(A))]
def scalar(c,A): return [[c*complex(x) for x in row] for row in A]
def outer(v,w=None):
    w=v if w is None else w
    return [[complex(v[i])*complex(w[j]).conjugate() for j in range(len(w))] for i in range(len(v))]
def trace(A): return sum(complex(A[i][i]) for i in range(min(len(A),len(A[0]))))
def frob(A,B): return math.sqrt(sum(abs(complex(A[i][j])-complex(B[i][j]))**2 for i in range(len(A)) for j in range(len(A[0]))))
def is_unitary(U,tol=1e-9):
    if not U or len(U)!=len(U[0]): return False
    return frob(matmul(dagger(U),U),eye(len(U)))<=tol
def density_from_state(v): return outer(v)
def purity(rho):
    return float(trace(matmul(rho,rho)).real)
def coherence_l1(rho):
    return float(sum(abs(complex(rho[i][j])) for i in range(len(rho)) for j in range(len(rho)) if i!=j))
def tensor_vec(a,b): return [complex(x)*complex(y) for x in a for y in b]
def tensor(A,B):
    return [[complex(A[i][j])*complex(B[k][l]) for j in range(len(A[0])) for l in range(len(B[0]))] for i in range(len(A)) for k in range(len(B))]
def validate_kraus(ops,tol=1e-9):
    if not ops: raise ChannelValidationError('no Kraus operators')
    n=len(ops[0][0]); acc=[[0j for _ in range(n)] for _ in range(n)]
    for K in ops:
        if len(K)!=n or len(K[0])!=n: raise ChannelValidationError('Kraus shape')
        acc=add(acc,matmul(dagger(K),K))
    if frob(acc,eye(n))>tol: raise ChannelValidationError('not trace preserving')
    return True
