import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Circle, FancyBboxPatch
from matplotlib.patheffects import withStroke

phi = (1 + np.sqrt(5)) / 2

def r_n(n):
    phi_n = (n + np.sqrt(n**2 + 4)) / 2
    return 1 / (2 * phi_n)

def channels(n):
    r = r_n(n)
    return (1-r)**2, 2*r*(1-r), r**2   # WL, WB, WM

fig = plt.figure(figsize=(22, 13), facecolor='#02020a')

ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 22); ax.set_ylim(0, 13)
ax.axis('off')
ax.set_facecolor('#02020a')

# ── title ────────────────────────────────────────────────────────────
ax.text(11, 12.3, 'The Multiverse Chain', color='white',
        fontsize=20, ha='center', fontweight='bold',
        path_effects=[withStroke(linewidth=4, foreground='#02020a')])
ax.text(11, 11.75,
        r'Two operations  $\infty\,(x\to x+1)$  and  $\mathcal{O}\,(x\to 1/x)$'
        r'  generate every level.  Fixed point of $\infty^n\circ\mathcal{O}$: $\varphi_n$.',
        color='#888899', fontsize=10, ha='center')

# ── chain levels ─────────────────────────────────────────────────────
levels = [
    # (n,   x,    label,          sublabel,                   color,     geom,        size)
    (-2,  1.4,  'Matter\nSea',   'pure $\\infty$\nno fixed pt', '#cc4444', 'pre-time',   1.05),
    (-1,  3.8,  'Primordial\n$n=-1$', r'$\varphi=1/\varphi$' '\n' r'$\kappa=+1/\varphi$', '#FF6B6B', 'spherical\nhidden',  1.15),
    ( 0,  6.8,  'Parent\n$n=0$', r'$\varphi=1$' '\n' r'$\kappa=0$ exact',  '#4ECDC4', 'Euclidean\nexact',  1.25),
    ( 1, 10.2,  'Our Universe\n$n=1$', r'$\varphi=\phi$' '\n' r'$\kappa=-1/\phi^2$', '#FFD700', 'hyperbolic\nAdS',    1.45),
    ( 2, 14.0,  'Silver\n$n=2$', r'$\varphi=1+\sqrt{2}$' '\n' r'$\kappa\approx-0.59$', '#A78BFA', 'hyperbolic\ndeeper', 1.15),
    ( 3, 17.2,  'Bronze\n$n=3$', r'$\varphi\approx3.30$' '\n' r'$\kappa\approx-0.70$', '#98FB98', 'hyperbolic',        1.05),
    ( 4, 19.8,  'Light\nSea',    r'$n\to\infty$' '\n' r'$\kappa\to-1$', '#87CEEB', 'max\nhyperbolic', 1.0),
]

node_positions = {n: x for n, x, *_ in levels}
node_colors    = {n: c for n, _, __, ___, c, *__ in levels}

# vertical spine
ax.axhline(6.5, color='#1a1a2e', linewidth=60, solid_capstyle='round', zorder=0)

# ── draw connecting arrows ────────────────────────────────────────────
arrow_labels = [
    r'$\mathcal{O}$: self-contact',
    r'$\infty\circ\mathcal{O}$: bootstrap',
    r'interface\nrecursion',
    r'$\infty^1\circ\mathcal{O}$',
    r'$\infty^2\circ\mathcal{O}$',
    r'$\infty^3\circ\mathcal{O}$',
    '',
]

for i in range(len(levels)-1):
    x0 = levels[i][1]
    x1 = levels[i+1][1]
    col0 = levels[i][4]
    col1 = levels[i+1][4]
    lab  = arrow_labels[i]
    xmid = (x0+x1)/2

    # gradient arrow line
    for t in np.linspace(0, 1, 40):
        r_col = tuple(int(col0[j*2+1:j*2+3], 16)/255 * (1-t) +
                      int(col1[j*2+1:j*2+3], 16)/255 * t for j in range(3))
        xp = x0 + t*(x1-x0)
        if t < 0.98:
            ax.plot([xp, xp+((x1-x0)/40)], [6.5, 6.5],
                    color=r_col, linewidth=3.5, solid_capstyle='butt', zorder=1)

    ax.annotate('', xy=(x1-0.18, 6.5), xytext=(x1-0.5, 6.5),
                arrowprops=dict(arrowstyle='->', color=col1, lw=2.0), zorder=3)

    if lab:
        ax.text(xmid, 5.55, lab, color='#666677', fontsize=7.5,
                ha='center', va='top', style='italic')

# ── closing loop arrow (E=mc²) ────────────────────────────────────────
ax.annotate('', xy=(1.6, 4.8), xytext=(19.6, 4.8),
            arrowprops=dict(arrowstyle='->', color='#FF6B6B', lw=2.0,
                            connectionstyle='arc3,rad=0.0'))
ax.text(11, 4.4, r'$E=mc^2$ — light sea collapses back to matter sea — loop closes',
        color='#FF6B6B', fontsize=9.5, ha='center',
        bbox=dict(facecolor='#0a0008', edgecolor='#FF6B6B',
                  alpha=0.7, boxstyle='round,pad=0.3'))

# ── draw nodes ────────────────────────────────────────────────────────
for n, x, label, sublabel, color, geom, size in levels:
    # glow ring
    glow = Circle((x, 6.5), size*1.35, color=color, alpha=0.08, zorder=2)
    ax.add_patch(glow)
    glow2 = Circle((x, 6.5), size*1.15, color=color, alpha=0.12, zorder=2)
    ax.add_patch(glow2)

    # main circle
    circle = Circle((x, 6.5), size, color=color, alpha=0.92, zorder=4)
    ax.add_patch(circle)

    # channel weight pie inside circle
    if n not in [-2, 4]:
        wl, wb, wm = channels(n)
        wedge_colors = ['#FFD700', '#4ECDC4', '#FF6B6B']
        start = 90
        for w, wc in zip([wl, wb, wm], wedge_colors):
            angle = w * 360
            wedge = mpatches.Wedge((x, 6.5), size*0.72, start, start+angle,
                                   facecolor=wc, alpha=0.7, zorder=5)
            ax.add_patch(wedge)
            start += angle
    elif n == -2:
        # matter sea — solid red
        ax.add_patch(Circle((x, 6.5), size*0.72, color='#cc4444', alpha=0.7, zorder=5))
    else:
        # light sea — solid cyan
        ax.add_patch(Circle((x, 6.5), size*0.72, color='#87CEEB', alpha=0.7, zorder=5))

    # label above
    ax.text(x, 6.5+size+0.55, label, color=color, fontsize=9,
            ha='center', va='bottom', fontweight='bold',
            path_effects=[withStroke(linewidth=3, foreground='#02020a')])

    # sublabel below
    ax.text(x, 6.5-size-0.45, sublabel, color=color, fontsize=7.5,
            ha='center', va='top', alpha=0.85,
            path_effects=[withStroke(linewidth=2, foreground='#02020a')])

    # geometry label further below
    ax.text(x, 6.5-size-1.35, geom, color='#555566', fontsize=7,
            ha='center', va='top', style='italic')

# ── our universe highlight ────────────────────────────────────────────
x1 = node_positions[1]
ax.add_patch(Circle((x1, 6.5), 1.9, color='#FFD700', alpha=0.05, zorder=1,
                    linestyle='--'))
for r_ring in [2.1, 2.5]:
    ring = Circle((x1, 6.5), r_ring, fill=False, edgecolor='#FFD700',
                  linewidth=0.6, alpha=0.2, linestyle='--', zorder=1)
    ax.add_patch(ring)
ax.text(x1, 9.8, 'YOU ARE HERE', color='#FFD700', fontsize=8,
        ha='center', style='italic', alpha=0.6)

# ── dark matter arrows ────────────────────────────────────────────────
# n=0 pressing into n=1
ax.annotate('', xy=(9.5, 7.9), xytext=(7.8, 8.6),
            arrowprops=dict(arrowstyle='->', color='#4ECDC4', lw=1.5,
                            connectionstyle='arc3,rad=-0.2'))
ax.text(8.4, 9.0, 'dark matter\n(gravitational\nonly)',
        color='#4ECDC4', fontsize=7.5, ha='center', alpha=0.8)

# n=2 pressing into n=1
ax.annotate('', xy=(10.9, 7.9), xytext=(12.8, 8.6),
            arrowprops=dict(arrowstyle='->', color='#A78BFA', lw=1.5,
                            connectionstyle='arc3,rad=0.2'))
ax.text(13.2, 9.0, 'dark matter\n(gravitational\nonly)',
        color='#A78BFA', fontsize=7.5, ha='center', alpha=0.8)

# ── channel weight legend ─────────────────────────────────────────────
lx, ly = 0.35, 2.8
ax.text(lx, ly+0.5, 'Channel weights (pie):', color='#888899',
        fontsize=8, ha='left')
for wlab, wc, wy in [('Light $W_L$','#FFD700', 0.0),
                      ('Boundary $W_B$','#4ECDC4',-0.45),
                      ('Matter $W_M$','#FF6B6B',-0.9)]:
    ax.add_patch(Circle((lx+0.15, ly+wy-0.05), 0.12, color=wc, alpha=0.85, zorder=6))
    ax.text(lx+0.4, ly+wy, wlab, color=wc, fontsize=8, va='center')

# ── key equation box ──────────────────────────────────────────────────
ax.text(17.5, 2.8,
        r'$\kappa_n = 2r_n - 1$' '\n'
        r'$r_n = 1/(2\varphi_n)$' '\n'
        r'$\varphi_n = (n+\sqrt{n^2+4})/2$' '\n'
        r'$\varepsilon_n = r_n^3$  (braiding floor)',
        color='#aaaaaa', fontsize=8.5, ha='center', va='top',
        bbox=dict(facecolor='#0a0a18', edgecolor='#333344',
                  alpha=0.9, boxstyle='round,pad=0.5'))

fig.text(0.5, 0.01,
         'Primordial Loop Algebra  ·  J. Shields (2026)  ·  '
         'Pie segments show W_L / W_B / W_M at each level',
         color='#444455', fontsize=8, ha='center')

plt.savefig('/home/joe/Desktop/UNIFIED_MULTIVERSE/renders/multiverse_chain.png',
            dpi=160, bbox_inches='tight', facecolor='#02020a')
plt.close()
print("saved")
