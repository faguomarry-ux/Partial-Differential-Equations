"""Chapter 10 exact models; these checks do not replace general proofs.

Requires SymPy and NumPy. Writes tmp/pdfs/ch10-model-checks.json.
"""
from pathlib import Path
import json
import re
import sympy as s
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
report={}
x,y,t,h=s.symbols('x y t h',real=True,positive=True)
# Quadratic infimal convolution: analytic minimizer, value, PDE and semigroup.
obj=(x-y)**2/(2*t)+y*y/2
ym=x/(1+t)
assert s.simplify(s.diff(obj,y).subs(y,ym))==0
q=s.simplify(obj.subs(y,ym))
assert s.simplify(q-x*x/(2*(1+t)))==0
assert s.simplify(s.diff(q,t)+s.diff(q,x)**2/2)==0
z=x*(1+t)/(1+t+h)
stage=(x-z)**2/(2*h)+z*z/(2*(1+t))
assert s.simplify(stage-x*x/(2*(1+t+h)))==0
report['quadratic_hopf_lax']='minimizer, PDE residual, and two-stage identity exact'
# Bounded two-well data used in T10.4: test the proximal minimizers of each branch.
def g(v):return np.minimum(np.minimum(np.abs(v-1),np.abs(v+1)),2)
def huber(d,tt):return np.where(d<=tt,d*d/(2*tt),d-tt/2)
maxerr=0.
for tt in [.1,.5,1,2]:
 for xx in np.linspace(-5,5,401):
  candidates=[a+np.sign(xx-a)*max(abs(xx-a)-tt,0) for a in [-1,1]]+[xx]
  direct=min((xx-v)**2/(2*tt)+g(v) for v in candidates)
  formula=min(huber(abs(xx-1),tt),huber(abs(xx+1),tt),2)
  maxerr=max(maxerr,abs(direct-formula))
assert maxerr<1e-12
for yy in [-.5,.5]:assert abs(yy*yy+g(yy)-.75)<1e-12
report['bounded_two_well_model']=dict(points=1604,max_error=float(maxerr),minimizers_at_zero=[-.5,.5],minimum=.75)
# Inspect the actual TikZ expressions on both signs of the plotting variable.
# Bare negative numeric substitutions before a power have different precedence.
contact=(ROOT/'figures/tikz/ch10-contact.tex').read_text(encoding='utf-8-sig')
expressions=re.findall(r'plot \(\\x,\{([^}]+)\}\)',contact)
assert len(expressions)==2
for xx in [-1,-.5,0,.5,1]:
 for expr,expected in zip(expressions,[1-.5*xx**2,-1+.5*xx**2]):
  got=s.sympify(expr.replace(r'\x',str(xx)).replace('^','**'))
  assert abs(float(got)-expected)<1e-12
hopf=(ROOT/'figures/tikz/ch10-hopf-lax.tex').read_text(encoding='utf-8-sig')
assert r'{(\x)^2+min' in hopf
report['tikz_negative_abscissae']='actual contact expressions checked on both sides; squared cost parenthesized'
# Pure pursuit: exact time solves the singular transport field off r=0.
a,b,X,Y=s.symbols('a b X Y',positive=True)
r=s.sqrt(X*X+Y*Y);value=(b*r+a*X)/(b*b-a*a)
res=s.simplify((a-b*X/r)*s.diff(value,X)-b*Y/r*s.diff(value,Y)+1)
assert res==0
assert s.simplify(value.subs(Y,0)-X/(b-a))==0
report['pursuit_time']='transport residual 0 and collinear limit exact'
# Shared time difference cancels in comparison; localization leaves only small momentum error.
eps,eta,d,x1,y1=s.symbols('eps eta d x1 y1',positive=True)
bu=eta+d/eps;bv=-eta+d/eps
assert s.simplify(bu-bv-2*eta)==0
report['doubling_time_cancellation']='exact gap 2 eta'
# Concave bounded-control Hamiltonian: min_{|a|<=1} (a p+a^2/2).
for pp in np.linspace(-4,4,161):
 aa=np.clip(-pp,-1,1)
 H=aa*pp+aa*aa/2
 exact=-pp*pp/2 if abs(pp)<=1 else .5-abs(pp)
 assert abs(H-exact)<1e-12
report['bounded_control_hamiltonian']='161 exact clipped minimizers; K=-H is convex Huber function'
# Degenerate elliptic trace sign for varied PSD matrices, including singular ones.
rng=np.random.default_rng(1031)
mins=[]
for k in range(100):
 A0=rng.normal(size=(3,2));B0=rng.normal(size=(3,2))
 A=A0@A0.T;B=B0@B0.T
 val=np.trace(A@B);mins.append(val);assert val>=-1e-10
report['positive_trace_order']=dict(singular_psd_cases=100,minimum_trace=float(min(mins)))
report['status']='all checks passed; not independent mathematical review'
p=ROOT/'tmp/pdfs/ch10-model-checks.json';p.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
