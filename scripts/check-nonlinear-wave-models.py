"""Exact identities and independent explicit-model checks for Chapter 12.
These checks do not replace general proofs or independent review.
"""
from pathlib import Path
import json
import sympy as s
import numpy as np

report={}
def zero(name,expr):
    residual=s.factor(s.simplify(expr))
    assert residual==0,(name,residual)
    report[name]='exact residual zero'

x,y,z,t,T=s.symbols('x y z t T',real=True)
coords=[x,y,z]
u=1+x*t+y*y+z*t*t
ut=s.diff(u,t); grad=s.Matrix([s.diff(u,v) for v in coords])
box=s.diff(u,t,2)-sum(s.diff(u,v,2) for v in coords)
e=(ut*ut+grad.dot(grad))/2+u**6/6
zero('local_quintic_energy_identity',s.diff(e,t)
     -sum(s.diff(ut*grad[j],coords[j]) for j in range(3))-ut*(box+u**5))
m=(t-T)*ut+s.Matrix(coords).dot(grad)+u
P=(t-T)*e+(s.Matrix(coords).dot(grad)+u)*ut
Q=m*grad+s.Matrix(coords)*((ut*ut-grad.dot(grad))/2-u**6/6)
zero('Morawetz_identity_off_shell',s.diff(P,t)
     -sum(s.diff(Q[j],coords[j]) for j in range(3))-m*(box+u**5)+u**6/3)
# On the cone, derive the null-square algebra before imposing a PDE.
r,U,V,W,Hpot=s.symbols('r U V W Hpot',real=True)
# U=u_t, V=u_r, W=|D_tan u|^2 and Hpot=u^6/6.
energy=(U*U+V*V+W)/2+Hpot
pcone=-r*energy+(r*V+u)*U
qnormal=(-r*U+r*V+u)*V+r*((U*U-V*V-W)/2-Hpot)
zero('null_Morawetz_boundary',pcone-qnormal-(-r*(U-V)**2+u*(U-V)))
zero('null_energy_flux_square',U*V-energy+((U-V)**2+W)/2+Hpot)

power=s.symbols('power',positive=True)
a=2/(power-1)
zero('power_scaling_match',2*a+2-3-(a*(power+1)-3))
zero('quintic_energy_scaling', (2*a+2-3).subs(power,5))
zero('critical_holder_reciprocals',s.Rational(1,6)+4*s.Rational(1,12)-s.Rational(1,2))
eps=s.symbols('eps',positive=True)
mu=(power-1)**2+eps*(4-power)
zero('Strauss_bootstrap_exponent',(4-power)*(power-1-eps)-3*(power-1)+mu)
zero('retarded_kernel_mass',s.integrate(r,(r,0,t))-t*t/2)
zero('Morawetz_weighted_integral',4*s.pi*s.integrate(r**s.Rational(1,2),(r,0,T))
     -8*s.pi*T**s.Rational(3,2)/3)

# Kelvin intertwining tested on a polynomial that is not a free wave.
q=x*x+y*y+z*z-t*t
trans=t**3/q**4+(x*x+y*z)/q**3
lhs=s.diff(trans,t,2)-sum(s.diff(trans,v,2) for v in coords)
zero('Kelvin_operator_intertwining_n3',lhs-(6*t/q-2)/q**3)
# Klein--Gordon descent kernel, using the Bessel ODE explicitly.
ss,mm=s.symbols('ss mm',positive=True)
zero('Klein_Gordon_Bessel_kernel',s.expand_func(s.diff(s.besselj(0,mm*ss),ss,2)
     +s.diff(s.besselj(0,mm*ss),ss)/ss+mm*mm*s.besselj(0,mm*ss)))
A=s.symbols('A',nonzero=True,real=True)
kink=4*s.atan(s.exp(A*t+x/A))
zero('Backlund_sine_Gordon_kink',s.diff(kink,x,t)-s.expand_trig(s.sin(kink)))
d=s.symbols('d',real=True)
f=s.Function('f')(x,t)
v=s.exp(d*t/2)*f
zero('damping_exponential_transform',s.diff(v,t,2)-s.diff(v,x,2)-d*d*v/4
     -s.exp(d*t/2)*(s.diff(f,t,2)-s.diff(f,x,2)+d*s.diff(f,t)))
# Galilean phase cancellation in all three spatial directions.
k=s.Matrix(s.symbols('k0:3',real=True));xi=s.Matrix(s.symbols('xi0:3',real=True))
zero('NLS_Galilean_dispersion',(k+xi/2).dot(k+xi/2)
     -(k.dot(k)+k.dot(xi)+xi.dot(xi)/4))
# Concavity transformation and the cubic virial coefficient.
I,Ip,Ipp,alpha=s.symbols('I Ip Ipp alpha',positive=True)
zero('concavity_transform',alpha*(alpha+1)*I**(-alpha-2)*Ip**2
     -alpha*I**(-alpha-1)*Ipp
     +alpha*I**(-alpha-2)*(I*Ipp-(alpha+1)*Ip**2))
K,L,n=s.symbols('K L n',real=True)
zero('focusing_cubic_virial',8*K-2*n*L-(8*(K-L/2)+(4-2*n)*L))

# Displacement amplification from the Poisson formula, independently integrated.
# t=3+epsilon probes the narrowing outer transition. Quadrature is checked
# at two resolutions; neither sample is treated as a proof of divergence.
values=[]
for ee in [.1,.03,.01,.003,.001]:
    estimates=[]
    for N in [400,600]:
        nodes,weights=np.polynomial.legendre.leggauss(N)
        rr=2+nodes
        gg=np.exp(-ee*(rr-2)**2/((rr-1)*(3-rr)))
        tt=3+ee
        estimates.append(float(-tt*np.sum(weights*rr*gg/(tt*tt-rr*rr)**1.5)))
    assert abs(estimates[0]-estimates[1])<1e-5*max(1,abs(estimates[1]))
    values.append({'epsilon':ee,'time':3+ee,'value':estimates[1]})
assert all(values[j+1]['value']<values[j]['value']<0 for j in range(len(values)-1))
report['two_dimensional_amplification']=values
# Negative-energy Gaussian data: a direct integral check for virial examples.
for dim in [2,3,4]:
    amp=8.0
    kinetic=dim*amp**2*np.pi**(dim/2)/2
    fourth=amp**4*(np.pi/2)**(dim/2)
    en=kinetic-fourth/2
    variance=dim*amp**2*np.pi**(dim/2)/2
    assert en<0 and 8*kinetic-2*dim*fourth<=8*en+1e-8
    report[f'cubic_NLS_Gaussian_n{dim}']={'energy':en,'variance':variance,
                                      'quadratic_contradiction_time':float(np.sqrt(variance/(-4*en)))}
# Verify the actual diagram formulas at their highlighted threshold/tangent.
zero('energy_scaling_diagram_threshold',(4/(power-1)-1).subs(power,5))
zero('blowup_diagram_tangent', (1-t-t*t/4).subs(t,s.Rational(2,5))
     -(s.Rational(26,25)-s.Rational(6,5)*s.Rational(2,5)))
zero('Strauss_diagram_threshold',((power-1)**2-2).subs(power,1+s.sqrt(2)))
root=Path(__file__).resolve().parents[1]
out=root/'tmp/pdfs/ch12-qa/model-checks.json'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
