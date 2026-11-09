from pathlib import Path
import json
import numpy as np
import math
import mpmath as mp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parents[1]
results = root/"tmp/pdfs"
results.mkdir(exist_ok=True, parents=True)
out = root/"output/figures"
out.mkdir(exist_ok=True, parents=True)
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,
                     "axes.spines.top":False,"axes.spines.right":False})
fig, axes = plt.subplots(1,2,figsize=(7.1,3.5), constrained_layout=True)
th = np.linspace(0,2*np.pi,500)
ax=axes[0]
ax.fill(np.cos(th),np.sin(th),color="#d7e8e5")
ax.plot(np.cos(th),np.sin(th),color="#16766e",lw=2)
ax.plot([0,1],[0,0],color="#a56a19",lw=1.5)
ax.scatter([0],[0],color="#124b49",s=20,zorder=3)
ax.text(.3,.08,"radius r",fontsize=9)
ax.set(xlabel="space coordinate",ylabel="space coordinate",
       title="Harmonic mean: ball / sphere",xlim=(-1.2,1.2),ylim=(-1.2,1.2))
ax.set_aspect("equal")
ax=axes[1]
q=np.linspace(1e-6,1,700)
radius=np.sqrt(-q*np.log(q)/(2*np.pi))
ax.fill_betweenx(-q,-radius,radius,color="#d7e8e5")
ax.plot(radius,-q,color="#16766e",lw=2)
ax.plot(-radius,-q,color="#16766e",lw=2)
ax.scatter([0],[0],color="#a56a19",s=28,zorder=3)
ax.annotate("target (x,t)",xy=(0,0),xytext=(.09,.06),fontsize=9,
            arrowprops={"arrowstyle":"->","color":"#a56a19"})
ax.axhline(-1/np.e,color="#a56a19",ls=":",lw=1)
ax.text(.02,-.41,"largest slice",fontsize=8)
ax.set(xlabel="(y-x) / r",ylabel="(s-t) / [r²/(4π)]",
       title="Heat ball: spatial dimension n=1",
       ylim=(-1.08,.16),xlim=(-.31,.31))
fig.savefig(out/"ch02-mean-geometries.pdf")
fig.savefig(out/"ch02-mean-geometries.png",dpi=180)
plt.close(fig)

checks=[]
mp.mp.dps=35
for n in [1,2,3,5,10]:
    b=n/2
    omega=np.pi**b/math.gamma(b+1)
    a=1/(4*np.pi)
    c=n*omega/(4*(n+2))*(2*n)**(b+1)*a**b
    density=lambda z:mp.power(b,b+2)/mp.gamma(b+2)*z**(b+1)*mp.exp(-b*z)
    mass=float(mp.quad(lambda z:c*mp.exp(-b*z)*z**(b+1),[0,mp.inf]))
    et=float(mp.quad(lambda z:a*mp.exp(-z)*density(z),[0,mp.inf]))
    er2=float(mp.quad(lambda z:(n+2)/(n+4)*2*n*a*mp.exp(-z)*z*density(z),
                     [0,mp.inf]))
    exact=a*(n/(n+2))**(b+2)
    residual=er2-2*n*et
    assert abs(mass-1)<1e-10
    assert abs(et-exact)<1e-11
    assert abs(residual)<1e-11
    checks.append(dict(n=n,mass=mass,mean_time=et,
                       exact_mean_time=exact,heat_polynomial_residual=residual))
(results/"heatball-moment-checks.json").write_text(
    json.dumps(checks,indent=2),encoding="utf-8")
print(json.dumps(checks))
