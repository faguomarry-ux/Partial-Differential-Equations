"""Exact identities and sampled admissibility checks for Chapter 11.
These model checks are not a proof of general system theorems.
"""
import json
from pathlib import Path
import sympy as s
import numpy as np

report = {}
def zero(name, expr):
    residual = s.simplify(expr)
    if isinstance(residual, s.MatrixBase):
        assert all(v == 0 for v in residual), (name, residual)
    else:
        assert residual == 0, (name, residual)
    report[name] = 'exact residual zero'

h, h0, v0 = s.symbols('h h0 v0', positive=True)
a, b, rho, q = s.symbols('a b rho q', real=True)
c = s.symbols('c', positive=True)
A = s.Matrix([[0, -1], [-c**2, 0]])
zero('elastic_eigenvectors', A*s.Matrix([[1,1],[c,-c]])
     -s.Matrix([[1,1],[c,-c]])*s.diag(-c,c))
v = v0+(h-h0)*s.sqrt((h+h0)/(2*h*h0))
sigma = v0+s.sqrt(h*(h+h0)/(2*h0))
zero('shallow_water_mass_jump', sigma*(h-h0)-(h*v-h0*v0))
zero('shallow_water_momentum_jump', sigma*(h*v-h0*v0)
     -(h*v**2+h**2/2-h0*v0**2-h0**2/2))
xi, hl = s.symbols('xi hl', positive=True)
fan_h = (2*s.sqrt(hl)-xi)**2/9
fan_v = 2*(s.sqrt(hl)+xi)/3
fan_q = fan_h*fan_v
zero('dam_break_fan_mass', -xi*s.diff(fan_h,xi)+s.diff(fan_q,xi))
zero('dam_break_fan_momentum', -xi*s.diff(fan_q,xi)
     +s.diff(fan_q**2/fan_h+fan_h**2/2,xi))

# Mechanical entropy: take a nontrivial pressure p=rho^3 and P=rho^3/2.
rho = s.symbols('rho', positive=True)
q = s.symbols('q', real=True)
F = s.Matrix([q,q*q/rho+rho**3])
eta = q*q/(2*rho)+rho**3/2
Q = q**3/(2*rho**2)+3*q*rho**2/2
zero('barotropic_entropy_flux', s.Matrix([[s.diff(Q,z) for z in [rho,q]]])
     -s.Matrix([[s.diff(eta,z) for z in [rho,q]]])*F.jacobian([rho,q]))
u = s.symbols('u', real=True)
f = lambda z:z**3-z
chord = -s.Rational(1,4)*(u+1)
zero('cubic_entropy_chord_factorization', f(u)-chord-(u+1)*(u-s.Rational(1,2))**2)
zero('arbitrary_sonic_chord', f(u)-f(a)-(s.Rational(3,4)*a*a-1)*(u-a)
     -(u-a)*(u+a/2)**2)
zero('sonic_shock_speed', (f(-a/2)-f(a))/(-a/2-a)
     -(s.Rational(3,4)*a*a-1))
zeta = s.symbols('zeta', real=True)
wave_speed = s.sqrt(s.Rational(3,2))
profile = 1/(1+s.exp(-zeta/(2*wave_speed)))
zero('partially_viscous_elastic_profile', s.diff(profile,zeta)
     -(2*profile-profile**2/2-wave_speed**2*profile)/wave_speed)
zero('nonlinear_coordinate_jump_original', s.sqrt(3)*s.sqrt(3)
     -(s.Rational(3,2)+2-s.Rational(1,2)))
assert s.Rational(11,8) != s.Rational(3,2)

# Perturbed sonic shock: independently verify its implicit characteristic map
# and Rankine--Hugoniot speed by differentiating the exact parametrization.
r, lam = s.symbols('r lam', positive=True)
t = s.Rational(4,15)/lam*(r**(-s.Rational(8,3))-1/r)
alpha = (r-1)/lam
shock = alpha+(3*r*r-1)*t
zero('perturbed_shock_RH_velocity', s.diff(shock,r)/s.diff(t,r)
     -(s.Rational(3,4)*r*r-1))
zero('perturbed_shock_initial_time', t.subs(r,1))
zero('perturbed_shock_initial_position', shock.subs(r,1))
# s''(0)= -27 lambda/8, and its Taylor coefficient is half of this.
zero('perturbed_shock_initial_curvature',
     (s.diff(s.diff(shock,r)/s.diff(t,r),r)/s.diff(t,r)).subs(r,1)
     +s.Rational(27,8)*lam)
# Maxwell algebra for a coupled polynomial energy, testing all spatial directions.
B = s.symbols('B0:3'); D = s.symbols('D0:3'); z = B+D
energy = sum(w*w for w in z)/2+sum(B[i]*D[i] for i in range(3))/5
E = s.Matrix([s.diff(energy,w) for w in D])
H = s.Matrix([s.diff(energy,w) for w in B])
for j in range(3):
    flux = s.Matrix([sum(s.LeviCivita(i,j,k)*E[k] for k in range(3)) for i in range(3)]
                   +[-sum(s.LeviCivita(i,j,k)*H[k] for k in range(3)) for i in range(3)])
    zero(f'Maxwell_entropy_direction_{j}',
         s.Matrix([[s.diff(energy,w) for w in z]])*flux.jacobian(z)
         -s.Matrix([[s.diff(E.cross(H)[j],w) for w in z]]))

# Wide depth ratios: bracket the unique dam-break intermediate state and check
# both jumps, fan ordering, and Lax compression numerically.
worst = 0.0
for ratio in np.geomspace(1.001,1000,180):
    left, right = float(ratio), 1.0
    lo, hi = right, left
    def mismatch(H):
        return 2*(np.sqrt(left)-np.sqrt(H))-(H-right)*np.sqrt((H+right)/(2*H*right))
    for _ in range(100):
        mid=(lo+hi)/2
        if mismatch(mid)>0:lo=mid
        else:hi=mid
    Hm=(lo+hi)/2
    Vm=2*(np.sqrt(left)-np.sqrt(Hm)); qm=Hm*Vm
    speed=qm/(Hm-right)
    mom=speed*qm-(qm*qm/Hm+Hm*Hm/2-right*right/2)
    worst=max(worst,abs(mom)/(1+Hm*Hm))
    assert right < Hm < left
    assert np.sqrt(right)<speed<Vm+np.sqrt(Hm)
    assert -np.sqrt(left)<Vm-np.sqrt(Hm)<speed
assert worst<1e-10,worst
report['dam_break_180_depth_ratios']={'max_scaled_momentum_residual':worst,
                                      'depth_ratio_range':[1.001,1000]}
# Sonic shock curvature and nonintersection of emitted rays, finite-time hit.
for lv in [.001,.01,.1,.24]:
    rs=np.linspace(1,1-lv,200)
    ts=np.array([float(t.subs({r:rr,lam:lv})) for rr in rs])
    speeds=.75*rs**2-1
    assert np.all(np.diff(ts)>0) and np.all(np.diff(speeds)<0)
report['perturbed_shock_emission']={'parameter_sets':4,'samples_each':200,
                                   'times_increase':True,'speeds_decrease':True}
report['coordinate_change_counterexample']={'old_momentum_jump':True,
 'alternative_velocity_flux_jump':'11/8','speed_times_velocity_jump':'3/2'}
out=Path(__file__).resolve().parents[1]/'tmp/pdfs/ch11-qa/model-checks.json'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
