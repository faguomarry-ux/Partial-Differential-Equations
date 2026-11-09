"""Chapter 6: reproducible explanatory figures and exact-model checks.

These finite-dimensional/explicit checks are supplements, not proofs of the
general elliptic theorems.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"output/figures"
OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,
                     "axes.spines.top":False,"axes.spines.right":False})
teal,orange="#16766e","#ad6b1d"
fig,axes=plt.subplots(1,2,figsize=(7.2,3.15),layout="constrained")
ax=axes[0]
t=np.linspace(0,np.pi,240)
ax.plot(np.cos(t),np.sin(t),color=teal,lw=1.5)
ax.plot([-1.08,1.08],[0,0],color="#555",lw=1.4)
ax.fill_between(np.cos(t),np.sin(t),0,color=teal,alpha=.05)
ax.scatter([-.25],[.35],s=18,color=teal)
ax.annotate("",xy=(.3,.35),xytext=(-.25,.35),
            arrowprops={"arrowstyle":"->","color":teal,"lw":2})
ax.text(-.08,.43,"tangential step",ha="center",fontsize=9,color=teal)
ax.annotate("",xy=(-.68,-.2),xytext=(-.68,.15),
            arrowprops={"arrowstyle":"->","color":orange,"lw":2})
ax.text(-.5,-.2,"normal step may exit",fontsize=8.5,color=orange)
ax.text(.05,.83,"half-ball",ha="center",fontsize=10)
ax.text(0,-.09,"zero trace on flat face",ha="center",fontsize=9)
ax.set(xlim=(-1.15,1.15),ylim=(-.33,1.1),title="Legal boundary difference quotients")
ax.set_aspect("equal")
ax.axis("off")
ax=axes[1]
ax.add_patch(Circle((0,0),1,fill=False,color=teal,lw=1.5))
ax.add_patch(Circle((0,0),.5,fill=False,color=orange,ls="--"))
ax.add_patch(Wedge((0,0),1,0,360,width=.5,color=teal,alpha=.06))
ax.plot([0,1],[0,0],color="#888",lw=.8)
ax.scatter([0,1],[0,0],s=18,color=teal)
ax.annotate("",xy=(1.32,0),xytext=(1,0),
            arrowprops={"arrowstyle":"->","color":orange,"lw":1.7})
ax.text(1.2,.1,r"$\nu$",color=orange)
ax.text(-.08,-.13,r"$y$")
ax.text(.96,-.17,r"$x_0$")
ax.text(0,.73,"barrier annulus",ha="center",fontsize=9)
ax.text(0,-1.2,r"$h=e^{-\alpha |x-y|^2}-e^{-\alpha r^2}$",ha="center",fontsize=10)
ax.set(xlim=(-1.15,1.45),ylim=(-1.32,1.1),title="Hopf: an interior tangent ball")
ax.set_aspect("equal")
ax.axis("off")
for ext in ("pdf","png"):
    fig.savefig(OUT/f"ch06-boundary-tools.{ext}",dpi=180)
plt.close(fig)

fig,axes=plt.subplots(1,2,figsize=(7.2,3.1),layout="constrained")
x=np.linspace(0,np.pi,500)
for j,color in zip((1,2,3),(teal,orange,"#5670a4")):
    axes[0].plot(x,np.sqrt(2/np.pi)*np.sin(j*x),label=f"j = {j}",color=color)
axes[0].axhline(0,color="#777",lw=.6)
axes[0].set(xlabel="x on (0, pi)",ylabel="normalized eigenfunction",
            title="First mode positive; higher modes oscillate")
axes[0].legend(fontsize=8,frameon=False,ncol=3,loc="lower center")
for a,b in ((-1,.96),(1.04,3.96),(4.04,8.96),(9.04,11)):
    lam=np.linspace(a,b,220)
    dist=np.min(np.abs(lam[:,None]-np.array([1.,4.,9.,16.])),axis=1)
    axes[1].semilogy(lam,1/dist,color=teal)
for eig in (1,4,9):
    axes[1].axvline(eig,color=orange,lw=.8,ls="--")
axes[1].set(xlabel="real parameter lambda",ylabel="L2 inverse norm",
            title="Resolvent grows near resonance",ylim=(.2,35),xlim=(-1,11))
for ext in ("pdf","png"):
    fig.savefig(OUT/f"ch06-modes-resonance.{ext}",dpi=180)
plt.close(fig)

# Uniform second-order consistency and spectral checks at independent grid sizes.
fd=[]
for N in (31,63,127):
    h=np.pi/(N+1)
    xx=np.arange(1,N+1)*h
    uu=np.sin(xx)
    padded=np.r_[0,uu,0]
    residual=(-padded[:-2]+2*padded[1:-1]-padded[2:])/h**2-uu
    vals=4/h**2*np.sin(np.arange(1,5)*np.pi/(2*(N+1)))**2
    fd.append({"N":N,"h":h,"poisson_residual_inf":float(np.max(np.abs(residual))),
               "first_four_eigenvalue_relative_error":float(np.max(np.abs(vals/np.arange(1,5)**2-1)))})
assert all(fd[i]["poisson_residual_inf"]/fd[i+1]["poisson_residual_inf"]>3.9 for i in (0,1))
assert all(fd[i]["first_four_eigenvalue_relative_error"]/fd[i+1]["first_four_eigenvalue_relative_error"]>3.9 for i in (0,1))

# Graph flattening: Ahat = J A J^T, with det J = 1.
rng=np.random.default_rng(2606)
A=np.array([[2.,.4],[.4,1.]])
theta=float(np.linalg.eigvalsh(A)[0])
J=np.array([[1.,0.],[-.7,1.]])
Ahat=J@A@J.T
assert abs(np.linalg.det(J)-1)<1e-14
vectors=rng.normal(size=(2000,2))
lhs=np.einsum("bi,ij,bj->b",vectors,Ahat,vectors)
lower=theta/np.linalg.norm(np.linalg.inv(J.T),2)**2*np.sum(vectors**2,axis=1)
assert np.all(lhs>=lower-1e-12)

# Drift conjugacy: u=e^(bx/2) sin(kx), L=-d2+b*d+c.
b,c,k=1.3,.4,2
xx=np.linspace(.01,np.pi-.01,200)
e=np.exp(b*xx/2)
u=e*np.sin(k*xx)
du=e*(b/2*np.sin(k*xx)+k*np.cos(k*xx))
ddu=e*((b*b/4-k*k)*np.sin(k*xx)+b*k*np.cos(k*xx))
lam=k*k+b*b/4+c
drift_error=float(np.max(np.abs(-ddu+b*du+c*u-lam*u)))
assert drift_error<1e-12

# Hadamard for an interval: move only its right endpoint with unit speed.
ell,j=1.7,3
explicit=-2*(j*np.pi)**2/ell**3
boundary_flux=-(np.sqrt(2/ell)*j*np.pi/ell)**2
assert abs(explicit-boundary_flux)<1e-12

# Fredholm resonance on (0, pi): f=sin(2x) is orthogonal to sin(x).
xx=np.linspace(0,np.pi,10001)
compat=float(np.trapezoid(np.sin(xx)*np.sin(2*xx),xx))
incompat=float(np.trapezoid(np.sin(xx)**2,xx))
assert abs(compat)<1e-12 and abs(incompat-np.pi/2)<1e-12

report={"finite_difference":fd,"flattened_min_eigenvalue":float(np.linalg.eigvalsh(Ahat)[0]),
        "flattening_lower_bound":theta/np.linalg.norm(np.linalg.inv(J.T),2)**2,
        "drift_conjugacy_max_error":drift_error,"hadamard_derivative":explicit,
        "hadamard_boundary_flux":boundary_flux,"resonant_compatible_pairing":compat,
        "resonant_incompatible_pairing":incompat,
        "scope":"Explicit models only; not a proof or independent mathematical review."}
(ROOT/"tmp/pdfs").mkdir(parents=True,exist_ok=True)
(ROOT/"tmp/pdfs/ch06-model-checks.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
print(json.dumps(report,indent=2))