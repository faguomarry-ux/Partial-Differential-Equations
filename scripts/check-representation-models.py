"""Reproduce Chapter 4 figures and independent analytic model checks."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/figures"
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False})
teal, orange = "#16766e", "#ad6b1d"

J = np.array([[1., -2.], [2., -3.]])
diffusion = np.diag([.01, 1.])
roots = np.sort(np.roots([.01, -.97, 1.]))
fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.35), layout="constrained")
lam = np.linspace(0, 110, 700)
axes[0].plot(lam, .01*lam**2-.97*lam+1, color=teal)
axes[0].axhline(0, color="#777", lw=.7)
axes[0].axvspan(*roots, color=teal, alpha=.1)
for j in range(1, 11):
    axes[0].plot(j*j, 0, "|", color=orange, ms=10)
axes[0].set(xlabel="Laplacian eigenvalue", ylabel="det(J - lambda D)",
            title="Turing band and interval modes")
axes[0].text(15, -7, "unstable: determinant < 0", fontsize=8)
y = np.linspace(-5, 5, 700)
axes[1].plot(y, np.maximum(1-y*y/12, 0), color=teal,
             label="porous medium: m = 2")
axes[1].plot(y, (1+y*y/3)**-2, color=orange,
             label="fast diffusion: m = 1/2")
axes[1].set(xlabel="profile coordinate y", ylabel="V(y)",
            title="C = 1, t = 1 (different masses)")
axes[1].legend(fontsize=8, frameon=False)
for suffix in ("pdf", "png"):
    fig.savefig(OUT / f"ch04-modes-profiles.{suffix}", dpi=180)
plt.close(fig)

fig, axes = plt.subplots(1, 3, figsize=(8, 3.1), layout="constrained")
y = np.linspace(-1.8, 1.8, 800)
for eps, color in zip([.3, .1, .03], ["#8ba6b8", orange, teal]):
    mu = np.exp(-(y-.4)**2/(2*eps))/np.sqrt(2*np.pi*eps)
    axes[0].plot(y, mu, label=f"eps = {eps:g}", color=color)
axes[0].set(xlabel="y", title="Laplace concentration")
axes[0].legend(fontsize=7, frameon=False)
y = np.linspace(-2.5, 2.5, 1600)
axes[1].plot(y, np.exp(-y*y/2)*np.cos(y*y/(2*.07)), color=teal, lw=.8)
axes[1].axvline(0, color=orange, lw=1)
axes[1].set(xlabel="y", title="Quadratic oscillatory phase")
axes[1].text(-1.6, .75, "stationary at y = 0", fontsize=7)
ang = np.linspace(0, 2*np.pi, 300)
axes[2].plot(np.cos(ang), np.sin(ang), color="#adbfb9", lw=.8)
for theta in np.linspace(0, 2*np.pi, 14, endpoint=False):
    z = np.array([np.cos(theta), np.sin(theta)])
    axes[2].annotate("", xy=.1*z, xytext=z,
                     arrowprops={"arrowstyle": "->", "color": teal, "lw": .8})
axes[2].plot(0, 0, "o", color=orange, ms=4)
axes[2].text(-.5, -.12, "focus at t = 1", fontsize=7)
axes[2].set(title="Radial wave rays", xlabel="x1", ylabel="x2",
            xlim=(-1.25, 1.25), ylim=(-1.25, 1.25))
axes[2].set_aspect("equal")
for suffix in ("pdf", "png"):
    fig.savefig(OUT / f"ch04-concentration-rays.{suffix}", dpi=180)
plt.close(fig)

checks = {}
growth = np.linalg.eigvals(J-4*diffusion)
assert max(np.real(np.linalg.eigvals(J))) < 0
assert max(np.real(growth)) > 0
checks["turing_mode_2_eigenvalues"] = growth.tolist()
checks["turing_band"] = roots.tolist()

# Gaussian stationary phase: a(z)=exp(-z^2/2), exact Fresnel integral.
eps_values = [.2, .1, .05, .025]
qp = []
for eps in eps_values:
    integral = np.sqrt(2*np.pi/(1-1j/eps))
    leading = np.sqrt(2*np.pi*eps)*np.exp(1j*np.pi/4)
    error = abs(integral/leading-1)
    assert error < eps
    qp.append({"epsilon": eps, "relative_error": float(error)})
checks["quadratic_stationary_phase"] = qp

# Width equation for constant beta and fixed positive sigma.
beta = -.3
for t in [.1, .5, 2.]:
    gamma = 2*np.expm1(2*beta*t)/beta
    gamma_prime = 4*np.exp(2*beta*t)
    assert abs(gamma_prime-(4+2*beta*gamma)) < 1e-12
checks["plume_width_residual_bound"] = 1e-12

# Explicit 1D homogenization with a(y)=2+sin(2 pi y), f=1.
# Integer-cell midpoints give a separate quadrature implementation of the flux.
effective = np.sqrt(3.)
rows = []
for cells in [10, 20, 40, 80]:
    count = cells*400
    grid = (np.arange(count)+.5)/count
    b = 1/(2+np.sin(2*np.pi*cells*grid))
    constant = np.sum(b*grid)/np.sum(b)
    derivative = b*(constant-grid)
    numerical_u = np.r_[0, np.cumsum(derivative)/count]
    nodes = np.linspace(0, 1, count+1)
    exact_limit = nodes*(1-nodes)/(2*effective)
    err = float(np.max(np.abs(numerical_u-exact_limit)))
    assert err < .12/cells
    rows.append({"epsilon": 1/cells, "max_solution_error": err})
checks["homogenization_1d"] = rows

# Verify the scalar CK majorant by differentiation, independently of TeX.
r, C, m, d = 1.3, .8, 3, 2
residuals = []
for s, t in [(.02, .001), (-.03, .003), (.1, .002)]:
    N = m*(d+1)
    v = ((r-s)-np.sqrt((r-s)**2-2*N*C*r*t))/N
    vt = C*r/(r-s-N*v)
    vs = v/(r-s-N*v)
    residuals.append(float(abs(vt-C*r/(r-s-m*v)*(m*d*vs+1))))
assert max(residuals) < 1e-12
checks["ck_majorant_max_residual"] = max(residuals)

folder = ROOT / "tmp/pdfs"
folder.mkdir(parents=True, exist_ok=True)
(folder/"ch04-model-checks.json").write_text(
    json.dumps(checks, indent=2), encoding="utf-8")
print(json.dumps(checks))
