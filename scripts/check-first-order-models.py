from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root=Path(__file__).resolve().parents[1]
out=root/"output/figures"
out.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,
                     "axes.spines.top":False,"axes.spines.right":False})
teal="#16766e"; orange="#ad6b1d"
fig=plt.figure(figsize=(7.2,3.5),layout="constrained")
ax=fig.add_subplot(121)
x=np.linspace(-2.6,2.6,400)
for a in [-1.9,-1,-.55,.55,1,1.9]:
    ax.plot(x,(2*a-x)/a**2,color="#9ebfba",lw=.9)
for interval in [(-2.6,-.39),(.39,2.6)]:
    q=np.linspace(*interval,250);ax.plot(q,1/q,color=teal,lw=2.1)
ax.set(xlim=(-2.6,2.6),ylim=(-2.6,2.6),xlabel="x1",ylabel="x2",
       title="Line envelope: x1 x2 = 1")
ax.set_aspect("equal")
ax=fig.add_subplot(122,projection="3d")
q=np.linspace(-1.1,1.1,35);X,Y=np.meshgrid(q,q);Z=-X*X-Y*Y
ax.plot_surface(X,Y,Z,color=teal,alpha=.7,linewidth=0)
a1,a2=.55,.3
q1=np.linspace(-a1-.4,-a1+.4,10);q2=np.linspace(-a2-.4,-a2+.4,10)
XX,YY=np.meshgrid(q1,q2)
ax.plot_surface(XX,YY,2*a1*XX+2*a2*YY+a1*a1+a2*a2,
                color=orange,alpha=.65)
ax.set(xlabel="x1",ylabel="x2",zlabel="x3",
       title="Plane envelope: x3 = -x1²-x2²")
ax.view_init(24,-45)
fig.savefig(out/"ch03-envelopes.pdf")
fig.savefig(out/"ch03-envelopes.png",dpi=180);plt.close(fig)

fig,axs=plt.subplots(1,2,figsize=(7.2,3.4),layout="constrained")
for ax in axs:
    ax.set(xlabel="x",ylabel="t",ylim=(0,2),xlim=(-2.2,4.2))
ax=axs[0]
for x0 in np.linspace(-2,0,8):
    t=np.linspace(0,min(2,-x0),80);ax.plot(x0+2*t,t,color=teal,lw=.9)
for x0 in np.linspace(0,2,8):
    t=np.linspace(0,min(2,x0),80);ax.plot(np.full_like(t,x0),t,color=teal,lw=.9)
t=np.linspace(0,2,100);ax.plot(t,t,color=orange,lw=2.4)
ax.set_title("Compression: 2 to 0")
ax.text(1.8,1.5,"shock x=t",color=orange,fontsize=9)
ax=axs[1]
for x0 in np.linspace(-2,-.2,6):
    ax.plot([x0,x0],[0,2],color=teal,lw=.9)
for x0 in np.linspace(.2,2,6):
    ax.plot([x0,x0+4],[0,2],color=teal,lw=.9)
for v in np.linspace(0,2,9):ax.plot(v*t,t,color=orange,lw=.9)
ax.set_title("Rarefaction: 0 to 2")
ax.text(.75,1.6,"u=x/t",fontsize=10,color=orange)
fig.savefig(out/"ch03-riemann-characteristics.pdf")
fig.savefig(out/"ch03-riemann-characteristics.png",dpi=180);plt.close(fig)

T=(2+np.sqrt(2))**2
def fronts(t):
    left=-1+t/2 if t<=2 else t-np.sqrt(2*t)
    right=1+t if t<=1 else 2*np.sqrt(t)
    return (1+t/2,1+t/2) if t>=T else (left,right)
def solution(x,t):
    x=np.asarray(x)
    if t>=T:return np.where(x<1+t/2,1.,0.)
    left,right=fronts(t)
    fan=(x>max(0,left))&(x<min(2*t,right))
    u=np.where(x<left,1.,0.)
    u=np.where(fan,x/t,u)
    if t<1:u=np.where((x>=2*t)&(x<right),2.,u)
    return u

fig,axs=plt.subplots(1,2,figsize=(7.5,3.6),layout="constrained",
                     gridspec_kw={"width_ratios":[1,1.25]})
ax=axs[0]
t=np.linspace(0,T,500)
left=np.where(t<=2,-1+t/2,t-np.sqrt(2*t))
right=np.where(t<=1,1+t,2*np.sqrt(t))
ax.plot(left,t,color=orange,lw=2);ax.plot(right,t,color=orange,lw=2)
tt=np.linspace(T,T+3,80);ax.plot(1+tt/2,tt,color=orange,lw=2)
for v in np.linspace(0,2,13):
    tau=np.linspace(.001,T,500);xx=v*tau
    l=np.where(tau<=2,-1+tau/2,tau-np.sqrt(2*tau))
    rr=np.where(tau<=1,1+tau,2*np.sqrt(tau))
    mask=(xx>l)&(xx<rr)
    ax.plot(xx[mask],tau[mask],color=teal,lw=.6)
ax.scatter([0,2*np.sqrt(T)],[0,T],s=15,color=teal)
ax.set(xlabel="x",ylabel="t",title="Problem 20: interactions",
       ylim=(0,T+3),xlim=(-1.8,9))
ax.text(2.1*np.sqrt(T),T-.8,"merge",fontsize=9,color=orange)
ax=axs[1]
x=np.linspace(-3,12,2400)
for t,c in zip([.5,1.5,4,14],["#16766e","#ad6b1d","#675393","#375c9a"]):
    ax.plot(x,solution(x,t),label=f"t={t:g}",color=c,lw=1.4)
ax.set(xlabel="x",ylabel="u",ylim=(-.1,2.15),title="Entropy-solution profiles")
ax.legend(fontsize=8,loc="upper right",frameon=False)
fig.savefig(out/"ch03-interacting-waves.pdf")
fig.savefig(out/"ch03-interacting-waves.png",dpi=180);plt.close(fig)

# Independently minimize Hopf--Lax for the four affine primitive pieces.
pieces=[(-np.inf,-1,1,1),(-1,0,0,0),(0,1,2,0),(1,np.inf,0,2)]
checks=[]
for t in [.2,.8,1.3,2.5,5.,10.,14.,30.]:
    x=np.linspace(-4,max(12,t+4),1401)
    candidates=[];costs=[]
    for lo,hi,a,b in pieces:
        y=np.clip(x-t*a,lo,hi)
        candidates.append(y);costs.append((x-y)**2/(2*t)+a*y+b)
    costs=np.array(costs);candidates=np.array(candidates)
    best=np.argmin(costs,axis=0)
    y=candidates[best,np.arange(x.size)]
    residual=np.abs((x-y)/t-solution(x,t))
    # Multiple descriptions of the same endpoint are harmless; exclude
    # only genuinely different minimizing points at shocks.
    tie=np.zeros(x.size,dtype=bool)
    for j in range(4):
        tie|=(np.abs(costs[j]-costs[best,np.arange(x.size)])<1e-9)&(np.abs(candidates[j]-y)>1e-7)
    err=float(residual[~tie].max())
    assert err<1e-10,(t,err)
    checks.append({"time":t,"hopf_lax_profile_error":err})
assert abs((T-np.sqrt(2*T))-2*np.sqrt(T))<1e-12
assert abs((1+T/2)-2*np.sqrt(T))<1e-12
checks.append({"merger_time":float(T),"merger_location":float(2*np.sqrt(T))})
results=root/"tmp/pdfs";results.mkdir(parents=True,exist_ok=True)
(results/"ch03-model-checks.json").write_text(json.dumps(checks,indent=2),encoding="utf-8")
print(json.dumps(checks))
