"""Exact Chapter 9 models and algebraic identities, not general PDE proofs.

Requires SymPy and NumPy; writes tmp/pdfs/ch09-model-checks.json.
"""
from pathlib import Path
import json
import sympy as s
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
report={}
x,y,z=s.symbols('x y z',real=True)
r,n=s.symbols('r n',positive=True)
# Radial Laplacian at arbitrary dimension, not only a sampled plot.
u=(1+r*r)**(-(n-2)/2)
res=s.simplify(-s.diff(u,r,2)-(n-1)/r*s.diff(u,r)-n*(n-2)*(1+r*r)**(-(n+2)/2))
assert res==0
report['critical_bubble_radial_residual']=str(res)
# Every plotted ordered iterate has the claimed forcing and zero traces.
lower=(1-s.cosh(2*x-1)/s.cosh(1))/4
upper=x*(1-x)-lower
exact=x*(1-x)/2
assert s.simplify(-s.diff(lower,x,2)+4*lower-1)==0
assert s.simplify(-s.diff(upper,x,2)+4*upper-(1+4*x*(1-x)))==0
assert all(s.simplify(v.subs(x,e))==0 for v in [lower,upper,exact] for e in [0,1])
grid=np.linspace(0,1,1001)
l=s.lambdify(x,lower,'numpy')(grid);h=s.lambdify(x,upper,'numpy')(grid);q=.5*grid*(1-grid)
assert np.min(l)>=-1e-14 and np.min(q-l)>=-1e-14 and np.min(h-q)>=-1e-14
assert np.min(grid*(1-grid)-h)>=-1e-14
report['ordered_first_iterates']='exact residuals and traces zero; 1001-point plot order verified'
# The local Pohozaev divergence identity for a mixed polynomial.
coords=[x,y,z];p=x**3+x*y+2*y*z+z**2+x*z
D=s.Matrix([s.diff(p,c) for c in coords]);X=s.Matrix(coords)
Q=(X.dot(D))*D-X*D.dot(D)/2
lhs=sum(s.diff(Q[i],coords[i]) for i in range(3))
rhs=X.dot(D)*sum(s.diff(p,c,2) for c in coords)-D.dot(D)/2
assert s.simplify(lhs-rhs)==0
report['pohozaev_divergence_residual']='0 (mixed polynomial in dimension 3)'
# Bochner identity used in total-variation calculation, away from zero gradient.
p=s.exp(x)+y*y+z*z
D=s.Matrix([s.diff(p,c) for c in coords]);H=s.hessian(p,coords)
g=s.sqrt(D.dot(D));lap=sum(s.diff(p,c,2) for c in coords)
res=sum(s.diff(g,c,2) for c in coords)-D.dot(s.Matrix([s.diff(lap,c) for c in coords]))/g
res-=sum(v*v for v in H)/g-(H*D).dot(H*D)/g**3
assert s.simplify(res)==0
report['bochner_total_variation_residual']='0'
# Reciprocal Riccati solution with its stated positive-time singularity.
t,lam,a=s.symbols('t lam a',positive=True)
eta=lam*a*s.exp(-lam*t)/(lam-a*(1-s.exp(-lam*t)))
assert s.simplify(s.diff(eta,t)-(eta**2-lam*eta))==0
report['riccati_residual']='0'
# Firm resolvent identity and exact soft-threshold graph inclusion.
for ell in [.1,.5,1,2]:
 for v in np.linspace(-3,3,61):
  j=np.sign(v)*max(abs(v)-ell,0);aa=(v-j)/ell
  assert (abs(aa)<=1+1e-12 if abs(j)<1e-12 else abs(aa-np.sign(j))<1e-12)
  for w in np.linspace(-3,3,61):
   k=np.sign(w)*max(abs(w)-ell,0);bb=(w-k)/ell
   assert (j-k)**2+ell**2*(aa-bb)**2<=(v-w)**2+1e-12
report['absolute_value_resolvent']='graph inclusion and firm estimate on 14884 pairs'
report['status']='all model checks passed; not independent mathematical review'
out=ROOT/'tmp/pdfs/ch09-model-checks.json';out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
