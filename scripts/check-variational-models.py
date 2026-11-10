"""Chapter 8 polynomial identities and exact examples; not a general proof.

Requires SymPy and NumPy. Reports to tmp/pdfs/ch08-model-checks.json.
"""
from pathlib import Path
import json
import sympy as s
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
report={}
x,y,z,t=s.symbols('x y z t',real=True)
coords=(x,y,z)
u=s.Matrix([x*x+y*z,x*y+z*z,y*y+x*z])
jac=u.jacobian(coords); cof=jac.cofactor_matrix()
piola=[s.expand(sum(s.diff(cof[a,i],coords[i]) for i in range(3))) for a in range(3)]
assert piola==[0,0,0]
eta=1+sum(v*v for v in u)
weighted=[s.expand(sum(s.diff(eta*cof[a,i],coords[i]) for i in range(3))
                   -2*u[a]*jac.det()) for a in range(3)]
assert weighted==[0,0,0]
report['piola_polynomial_residuals']=[str(v) for v in piola]
report['weighted_null_lagrangian_residuals']=[str(v) for v in weighted]

# Check the conformal identity off shell, without imposing the wave equation.
v=t**3+x*x*y+t*y*z+x*z*z+x*y*z
grad=s.Matrix([s.diff(v,q) for q in coords]); vt=s.diff(v,t)
r2=x*x+y*y+z*z; n=3
e=(vt*vt+grad.dot(grad))/2
mult=(r2+t*t)*vt+2*t*s.Matrix(coords).dot(grad)+(n-1)*t*v
density=(r2+t*t)*e+2*t*s.Matrix(coords).dot(grad)*vt+(n-1)*t*v*vt-s.Rational(n-1,2)*v*v
flux=mult*grad+t*(vt*vt-grad.dot(grad))*s.Matrix(coords)
residual=s.expand(s.diff(density,t)-sum(s.diff(flux[i],coords[i]) for i in range(3))
                  -mult*(s.diff(v,t,2)-sum(s.diff(v,q,2) for q in coords)))
assert residual==0
report['conformal_current_off_shell_residual']=str(residual)

# Verify the square completion with general symbolic dimension.
r,nn,uu,ur,ut,tan2=s.symbols('r n u u_r u_t tangential_square',real=True)
alpha=(nn-1)/2
cc=(r*r+t*t)*(ut*ut+ur*ur+tan2)/2+2*t*r*ur*ut+(nn-1)*t*uu*ut-alpha*uu*uu
square=(t+r)**2*(ut+ur+alpha*uu/r)**2/4+(t-r)**2*(ut-ur-alpha*uu/r)**2/4
square+=(r*r+t*t)*(tan2+(nn-3)*(nn-1)*uu*uu/(4*r*r))/2
divz=2*(r*r+t*t)*uu*ur/r+(nn+(nn-2)*t*t/(r*r))*uu*uu
completion=s.factor(cc-square+alpha*divz/2)
assert completion==0
report['conformal_square_completion_residual']=str(completion)

# Obstacle data match at the free boundary, including the derivative.
h=1-s.Rational(4,3)*x*x
left=s.Rational(4,3)*(1+x);right=s.Rational(4,3)*(1-x)
matches=[s.simplify((h-left).subs(x,-s.Rational(1,2))),
         s.simplify((s.diff(h,x)-s.diff(left,x)).subs(x,-s.Rational(1,2))),
         s.simplify((h-right).subs(x,s.Rational(1,2))),
         s.simplify((s.diff(h,x)-s.diff(right,x)).subs(x,s.Rational(1,2)))]
assert matches==[0]*4
phi=(1-x*x)**2
lhs=s.integrate(s.diff(left,x)*s.diff(phi,x),(x,-1,-s.Rational(1,2)))
lhs+=s.integrate(s.diff(h,x)*s.diff(phi,x),(x,-s.Rational(1,2),s.Rational(1,2)))
lhs+=s.integrate(s.diff(right,x)*s.diff(phi,x),(x,s.Rational(1,2),1))
rhs=s.integrate(s.Rational(8,3)*phi,(x,-s.Rational(1,2),s.Rational(1,2)))
assert s.simplify(lhs-rhs)==0 and lhs>0
report['obstacle']={'value_and_slope_matching':[str(v) for v in matches],'reaction_pairing':str(rhs),
                    'variational_identity_residual':str(s.simplify(lhs-rhs))}

# Harmonic polynomial in two dimensions: frequency and monotonicity factors.
theta=s.symbols('theta',real=True)
polar=r*r*s.cos(2*theta)
H=s.integrate(polar*polar*r,(theta,0,2*s.pi))
D=2*s.pi*r**4
a=H/r;b=D
frequency=s.simplify(b/a)
boundary_radial=s.integrate(s.diff(polar,r)**2*r,(theta,0,2*s.pi))
assert frequency==2 and s.simplify(s.diff(b,r)-2*boundary_radial)==0
assert s.simplify(s.diff(a,r)-2*b/r)==0
report['harmonic_polynomial_frequency']=str(frequency)

# Weighted degree of the complex map w -> w^3, with a normalized C^1 density.
rr=s.symbols('radius',nonnegative=True)
m=3
degree=s.integrate(6*m*m*(1-rr**(2*m))**2*rr**(2*m-1),(rr,0,1))
assert degree==m
report['weighted_degree_z_cubed']=str(degree)

# Nonconvexity along full matrix lines, but affine determinant on rank-one lines.
tau=s.symbols('tau')
P=s.Matrix([[1,2],[3,4]]);aa=s.Matrix([2,-1]);bb=s.Matrix([1,3])
assert s.diff((P+tau*aa*bb.T).det(),tau,2)==0
report['rank_one_determinant_second_derivative']='0'
nodes=np.linspace(-1,1,1001)
mountain=(nodes*nodes-1)**2-1
assert abs(mountain.max())<1e-14 and mountain[0]==mountain[-1]==-1
report['finite_dimensional_mountain_pass_level']=float(mountain.max())
report['scope']='Exact identities and explicit models only; no general proof or independent mathematical review.'
out=ROOT/'tmp/pdfs/ch08-model-checks.json';out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
