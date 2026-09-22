import hashlib,json,time,math

def now_ns(): return time.time_ns()
def stable(obj): return json.dumps(obj,sort_keys=True,separators=(',',':'),default=str)
def digest(obj): return hashlib.sha256(stable(obj).encode()).hexdigest()
def cpair(z): return [float(z.real),float(z.imag)]
def cfrom(x): return complex(float(x[0]),float(x[1]))
def close(a,b,tol=1e-9): return abs(a-b)<=tol
