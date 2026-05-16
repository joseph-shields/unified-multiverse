import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.colors import LightSource

phi = (1 + np.sqrt(5)) / 2

def r_n(n):
    phi_n = (n + np.sqrt(n**2 + 4)) / 2
    return 1 / (2 * phi_n)

def WL_n(n):
    return (1 - r_n(n))**2

levels = [
    (-1, r'$n=-1$' '\nPrimordial\n' r'$\kappa=+1/\varphi$', '#FF6B6B', 'SPHERICAL\n(hidden)'),
    ( 0, r'$n=0$'  '\nParent\n'    r'$\kappa=0$',           '#4ECDC4', 'EUCLIDEAN\n(exact)'),
    ( 1, r'$n=1$'  '\nOur universe\n' r'$\kappa=-1/\varphi^2$', '#FFD700', 'HYPERBOLIC\n(AdS)'),
    ( 2, r'$n=2$'  '\nSilver\n'    r'$\kappa\approx-0.59$', '#A78BFA', 'HYPERBOLIC\n(deeper)'),
]

fig = plt.figure(figsize=(20, 12), facecolor='#03030a')
fig.text(0.5, 0.96,
         'Primordial Geometry — the same object at different light coupling',
         color='white', fontsize=16, ha='center', fontweight='bold')
fig.text(0.5, 0.925,
         r'$\kappa_{\rm obs} = \lambda \cdot \kappa_{\rm actual}$'
         '     where     '
         r'$\lambda = W_L = (1-r_n)^2$'
         '     |     Standard GR is the special case $\\lambda = 1$',
         color='#aaaaaa', fontsize=11, ha='center')

u = np.linspace(0, 2*np.pi, 80)
v = np.linspace(0, np.pi, 80)
xy = np.linspace(-2, 2, 80)
XX, YY = np.meshgrid(xy, xy)

for i, (n, label, color, geom_label) in enumerate(levels):
    ax = fig.add_subplot(2, 4, i+1, projection='3d', facecolor='#03030a')

    kappa = 2*r_n(n) - 1
    wl    = WL_n(n)
    alpha = 0.3 + 0.65 * wl   # opacity = light coupling

    if n == -1:
        # sphere (positive curvature)
        R = 1.4
        xs = R * np.outer(np.cos(u), np.sin(v))
        ys = R * np.outer(np.sin(u), np.sin(v))
        zs = R * np.outer(np.ones(np.size(u)), np.cos(v))
        norm_z = (zs - zs.min()) / (zs.max() - zs.min())
        facecolors = plt.cm.RdPu(0.3 + 0.6*norm_z)
        facecolors[..., 3] = alpha * 0.85
        ax.plot_surface(xs, ys, zs, facecolors=facecolors,
                        linewidth=0, antialiased=True, shade=True)
        ax.set_zlim(-2, 2)

    elif n == 0:
        # flat plane
        ZZ = np.zeros_like(XX)
        norm_xy = (XX**2 + YY**2) / 8
        facecolors = plt.cm.cool(0.3 + 0.4*norm_xy)
        facecolors[..., 3] = alpha
        ax.plot_surface(XX, YY, ZZ, facecolors=facecolors,
                        linewidth=0, antialiased=True)
        ax.set_zlim(-2, 2)

    elif n == 1:
        # hyperbolic paraboloid (saddle) — gentle
        ZZ = kappa * (XX**2 - YY**2) * 0.5
        ZZ = np.clip(ZZ, -2, 2)
        norm_z = (ZZ - ZZ.min()) / (ZZ.max() - ZZ.min() + 1e-8)
        facecolors = plt.cm.plasma(0.1 + 0.8*norm_z)
        facecolors[..., 3] = alpha
        ax.plot_surface(XX, YY, ZZ, facecolors=facecolors,
                        linewidth=0, antialiased=True, shade=True)
        ax.set_zlim(-2, 2)

    else:
        # deeper hyperbolic saddle
        ZZ = kappa * (XX**2 - YY**2) * 0.5
        ZZ = np.clip(ZZ, -2, 2)
        norm_z = (ZZ - ZZ.min()) / (ZZ.max() - ZZ.min() + 1e-8)
        facecolors = plt.cm.cool(0.1 + 0.8*norm_z)
        facecolors[..., 3] = alpha
        ax.plot_surface(XX, YY, ZZ, facecolors=facecolors,
                        linewidth=0, antialiased=True, shade=True)
        ax.set_zlim(-2, 2)

    ax.set_xlim(-2, 2); ax.set_ylim(-2, 2)
    ax.set_title(label, color=color, fontsize=9, pad=4)
    ax.text2D(0.5, -0.08, geom_label, transform=ax.transAxes,
              color=color, fontsize=8, ha='center', fontweight='bold')
    ax.text2D(0.5, -0.17,
              rf'$W_L={wl:.3f}$  $\lambda={wl:.3f}$  opacity={alpha:.2f}',
              transform=ax.transAxes, color='#aaaaaa', fontsize=7.5, ha='center')
    ax.set_axis_off()
    ax.patch.set_alpha(0)

    # light coupling meter below
    ax2d = fig.add_axes([0.055 + i*0.245, 0.07, 0.18, 0.025])
    ax2d.set_facecolor('#0a0a18')
    ax2d.barh(0, wl, height=1, color=color, alpha=0.85)
    ax2d.barh(0, 1-wl, height=1, left=wl, color='#111122', alpha=0.5)
    ax2d.set_xlim(0, 1); ax2d.set_ylim(-0.5, 0.5)
    ax2d.axis('off')
    ax2d.text(wl/2, 0, f'  WL={wl:.1%}', color='white',
              fontsize=8, ha='center', va='center')
    ax2d.text(-0.02, 0, r'$\lambda$', color='#888888', fontsize=8,
              ha='right', va='center', transform=ax2d.transAxes)
    ax2d.text(1.02, 0, '1', color='#888888', fontsize=8,
              ha='left', va='center', transform=ax2d.transAxes)
    for sp in ax2d.spines.values(): sp.set_color('#333344')

# ── bottom strip: the key equation visually ─────────────────────────
ax_eq = fig.add_axes([0.04, 0.02, 0.92, 0.04])
ax_eq.set_facecolor('#0a0a18')
ax_eq.axis('off')

concepts = [
    (0.08, r'$\lambda=0.037$', '#FF6B6B', 'Primordial'),
    (0.22, r'$\Rightarrow\;\kappa_{\rm obs}=+0.023$', '#FF6B6B', 'appears nearly flat'),
    (0.40, r'$\lambda=0.250$', '#4ECDC4', 'Parent'),
    (0.52, r'$\Rightarrow\;\kappa_{\rm obs}=0$', '#4ECDC4', 'exactly flat'),
    (0.63, r'$\lambda=0.478$', '#FFD700', 'Our universe'),
    (0.76, r'$\Rightarrow\;\kappa_{\rm obs}=-0.182$', '#FFD700', 'hyperbolic, appears flat'),
    (0.91, r'$\kappa_{\rm dark}\propto\Lambda$', '#FF6B6B', 'dark energy'),
]
for xpos, formula, col, desc in concepts:
    ax_eq.text(xpos, 0.65, formula, color=col, fontsize=9,
               ha='center', va='center', transform=ax_eq.transAxes)
    ax_eq.text(xpos, 0.15, desc, color='#777788', fontsize=7.5,
               ha='center', va='center', transform=ax_eq.transAxes)

for sp in ax_eq.spines.values(): sp.set_color('#333344')

plt.savefig('/home/joe/Desktop/UNIFIED_MULTIVERSE/renders/primordial_geometry_visual.png',
            dpi=160, bbox_inches='tight', facecolor='#03030a')
plt.close()
print("visual saved")
