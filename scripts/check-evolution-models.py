"""Exact identities and finite models for Chapter 7; not a general proof.

Requires NumPy and SymPy. Writes an explicit, reproducible JSON report.
"""
from pathlib import Path
import json
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
report = {}

# Verify the tensor identity used in the variable-coefficient Harnack proof.
# Time evolution of p is substituted from v_t = A:D^2v + A Dv.Dv;
# no particular function is falsely assumed to solve that nonlinear equation.
x, y, t = sp.symbols("x y t", real=True)
xs = (x, y)
A = sp.Matrix([[2+x*x+t/10, x*y/4], [x*y/4, 3+y*y+t/5]])
v = x**3+y**4+x*y*t+x*x*y/3
p = sp.Matrix([sp.diff(v, q) for q in xs])
hv = sp.hessian(v, xs)
z = (p.T*A*p)[0]
rhs = sum(A[i,j]*hv[i,j] for i in range(2) for j in range(2))+z
zt = (p.T*A.diff(t)*p)[0]+2*(p.T*A*sp.Matrix([sp.diff(rhs,q) for q in xs]))[0]
dz = zt-sum(A[k,l]*sp.diff(z,xs[k],xs[l])
            +2*A[k,l]*p[l]*sp.diff(z,xs[k]) for k in range(2) for l in range(2))
claimed = sum((sp.diff(A[i,j],t)-sum(A[k,l]*sp.diff(A[i,j],xs[k],xs[l])
             for k in range(2) for l in range(2)))*p[i]*p[j]
             for i in range(2) for j in range(2))
claimed += sum(2*A[i,j]*p[i]*sp.diff(A[k,l],xs[j])*hv[k,l]
               -4*A[k,l]*sp.diff(A[i,j],xs[k])*hv[i,l]*p[j]
               -2*A[i,j]*A[k,l]*hv[i,k]*hv[j,l]
               for i in range(2) for j in range(2)
               for k in range(2) for l in range(2))
residual = sp.expand(dz-claimed)
assert residual == 0
report["harnack_tensor_identity_polynomial_residual"] = str(residual)

# Unit disk: check the complete twice-integrated principal identity,
# including a nonconstant normal derivative and tangential flux.
u = (1-x*x-y*y)*(1+x/5+x*y/10)
a = sp.Matrix([[2+x*x/5, x*y/10], [x*y/10, 3+y*y/7]])
du = sp.Matrix([sp.diff(u,q) for q in xs]); hu = sp.hessian(u,xs)
principal = sum(a[i,j]*hu[i,j] for i in range(2) for j in range(2))*sp.trace(hu)
bulk = sum(a[i,j]*hu[i,k]*hu[j,k] for i in range(2) for j in range(2) for k in range(2))
errors = sum(sp.diff(a[i,j],xs[j])*hu[i,k]*du[k]
             -sp.diff(a[i,j],xs[k])*hu[i,j]*du[k]
             for i in range(2) for j in range(2) for k in range(2))
nodes, weights = np.polynomial.legendre.leggauss(48)
r = (nodes+1)/2; wr = weights/2
theta = np.linspace(0,2*np.pi,512,endpoint=False)
xx=r[:,None]*np.cos(theta); yy=r[:,None]*np.sin(theta)
def disk_integral(expr):
    vals=np.asarray(sp.lambdify((x,y),expr,"numpy")(xx,yy),dtype=float)
    return float(np.sum(vals*r[:,None]*wr[:,None])*(2*np.pi/len(theta)))
angle=sp.symbols("angle",real=True)
nu=sp.Matrix([sp.cos(angle),sp.sin(angle)])
tau=sp.Matrix([-sp.sin(angle),sp.cos(angle)])
sub={x:sp.cos(angle), y:sp.sin(angle)}
aa=a.subs(sub); q=(du.subs(sub).T*nu)[0]
# On the unit circle the shape operator is identity on tangent vectors.
a_tau=(tau.T*aa*nu)[0]
boundary_expr=q*q*(tau.T*aa*tau)[0]+q*a_tau*sp.diff(q,angle)
bvals=sp.lambdify(angle,boundary_expr,"numpy")(theta)
boundary=float(np.mean(bvals)*2*np.pi)
lhs=disk_integral(principal); interior=disk_integral(bulk+errors)
boundary_residual=abs(lhs-interior-boundary)
assert boundary_residual < 1e-10, boundary_residual
report["disk_boundary_identity"]={"principal_integral":lhs,
    "interior_integral":interior,"boundary_integral":boundary,
    "absolute_residual":boundary_residual}

# Finite-mode heat and wave orbits, exact semigroup composition and energy.
k=np.arange(1,13,dtype=float); g=1/k**2; h=(-1)**k/k
times=np.linspace(0,2,101)
energy=[]
for tt in times:
    disp=g*np.cos(k*tt)+h*np.sin(k*tt)/k
    vel=-k*g*np.sin(k*tt)+h*np.cos(k*tt)
    energy.append(float(np.sum(vel**2+k**2*disp**2)/2))
wave_error=max(abs(np.asarray(energy)-energy[0]))
assert wave_error<1e-12
composition_error=float(np.max(abs(np.exp(-k*k*.7)*np.exp(-k*k*.2)-np.exp(-k*k*.9))))
assert composition_error<1e-14
report["finite_modes"]={"wave_energy_max_drift":wave_error,
    "heat_semigroup_composition_error":composition_error}

# Yosida regularization for G=-diag(k^2): strong convergence on fixed data.
errors=[]
for lam in (10,100,1000,10000):
    approx=np.exp(-.3*lam*k*k/(lam+k*k))*g
    errors.append(float(np.linalg.norm(approx-np.exp(-.3*k*k)*g)))
assert all(b<a for a,b in zip(errors,errors[1:]))
report["yosida_fixed_vector_errors"]={str(l):e for l,e in zip((10,100,1000,10000),errors)}

# The anisotropic optical distance and the sign of the moving-cone flux.
rng=np.random.default_rng(7); coeff=np.diag([4.,1.]); excess=[]
for _ in range(200):
    point=rng.normal(size=2)
    distance=np.sqrt(point@np.linalg.solve(coeff,point))
    dq=np.linalg.solve(coeff,point)/distance
    assert abs(dq@coeff@dq-1)<1e-13
    normal=dq/np.linalg.norm(dq); grad=rng.normal(size=2); vel=rng.normal()
    flux=vel*(grad@coeff@normal)
    loss=(vel*vel+grad@coeff@grad)/(2*np.linalg.norm(dq))
    excess.append(float(flux-loss))
assert max(excess)<=1e-12
report["anisotropic_cone_max_flux_minus_loss"]=max(excess)
report["scope"]="Exact polynomial identities and finite models only; no independent mathematical review."
out=ROOT/"tmp/pdfs/ch07-model-checks.json";out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2))
