import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(18, 10), facecolor='#050508')

# ── LEFT PANEL: iteration portrait ─────────────────────────────────
ax1 = fig.add_axes([0.03, 0.08, 0.44, 0.84], facecolor='#050508')

phi = (1 + np.sqrt(5)) / 2
x = np.linspace(0.05, 4.5, 2000)

colors_fn = ['#4ECDC4', '#FFD700', '#FF6B6B', '#A78BFA']
labels_fn = [r'$f_0(x)=1/x$  $(n=0,\;\varphi=1)$',
             r'$f_1(x)=1+1/x$  $(n=1,\;\varphi=\phi)$',
             r'$f_2(x)=2+1/x$  $(n=2,\;\varphi=1+\sqrt{2})$',
             r'$f_3(x)=3+1/x$  $(n=3)$']

for n, (c, lab) in enumerate(zip(colors_fn, labels_fn)):
    y = n + 1/x
    mask = (y > 0) & (y < 5)
    ax1.plot(x[mask], y[mask], color=c, linewidth=1.8, alpha=0.85, label=lab)

ax1.plot(x, x, color='#ffffff', linewidth=0.8, linestyle='--', alpha=0.25,
         label=r'$y=x$ (fixed-point locus)')

# cobweb for f_1 from several starts
starts = [0.15, 0.5, 0.9, 2.8, 4.2, 1.05]
cwcols = ['#FF6B6B','#FFA07A','#FFD700','#98FB98','#87CEEB','#DDA0DD']
for x0, cc in zip(starts, cwcols):
    xc = x0
    xs, ys = [xc], [0]
    for _ in range(28):
        yc = 1 + 1/xc
        xs += [xc, yc]; ys += [yc, yc]
        xc = yc
    ax1.plot(xs, ys, color=cc, linewidth=0.9, alpha=0.55)

phi_ns = [(n, (n+np.sqrt(n**2+4))/2) for n in range(4)]
for n, pn in phi_ns:
    ax1.plot(pn, pn, 'o', color=colors_fn[n], markersize=9, zorder=6,
             markeredgecolor='white', markeredgewidth=0.6)
    ax1.annotate(rf'$\varphi_{n}={pn:.3f}$', xy=(pn, pn),
                 xytext=(pn+0.12, pn-0.38),
                 color=colors_fn[n], fontsize=8.5,
                 arrowprops=dict(arrowstyle='->', color=colors_fn[n], lw=0.8))

ax1.set_xlim(0.05, 4.5); ax1.set_ylim(0.05, 4.5)
ax1.set_xlabel('x', color='#cccccc', fontsize=11)
ax1.set_ylabel(r'$f_n(x) = n + 1/x$', color='#cccccc', fontsize=11)
ax1.set_title('Primordial Loop Algebra — iteration portrait\n'
              r'Every cobweb forces itself to a metallic fixed point $\varphi_n$',
              color='white', fontsize=12, pad=10)
ax1.tick_params(colors='#888888')
for sp in ax1.spines.values(): sp.set_color('#222233')
ax1.legend(facecolor='#0d0d1a', labelcolor='white', fontsize=8.5,
           loc='upper right', framealpha=0.7)

# ── RIGHT PANEL: the loop on the real line ──────────────────────────
ax2 = fig.add_axes([0.52, 0.08, 0.46, 0.84], facecolor='#050508')
ax2.set_xlim(-0.3, 4.8); ax2.set_ylim(-2.4, 2.5)
ax2.axis('off')
ax2.set_title('Primordial Loop Algebra — the two operations & the loop',
              color='white', fontsize=12, pad=10)

# real line
ax2.axhline(0, color='#444455', linewidth=1.2, xmin=0.02, xmax=0.98)

# unit circle (inversion)
theta = np.linspace(0, 2*np.pi, 300)
ax2.plot(np.cos(theta)*0.9, np.sin(theta)*0.9,
         color='#4ECDC4', linewidth=1.2, alpha=0.4, linestyle=':')
ax2.text(0, 1.08, r'$\mathcal{O}$: unit circle of inversion $x\!\to\!1/x$',
         color='#4ECDC4', fontsize=8, ha='center', alpha=0.75)

# metallic ratios
phi_list = [(n, (n+np.sqrt(n**2+4))/2) for n in [-1, 0, 1, 2, 3]]
dot_colors = ['#FF6B6B','#4ECDC4','#FFD700','#A78BFA','#98FB98']
labels_phi = [r'$\varphi_{-1}=1/\varphi$  Primordial',
              r'$\varphi_0=1$  Parent',
              r'$\varphi_1=\varphi$  Our universe',
              r'$\varphi_2=1+\sqrt{2}$  Silver',
              r'$\varphi_3$  Bronze']
yoff = [0.28, -0.30, 0.28, -0.30, 0.28]

for (n, pn), dc, lab, yo in zip(phi_list, dot_colors, labels_phi, yoff):
    ax2.plot(pn, 0, 'o', markersize=11, color=dc, zorder=6,
             markeredgecolor='white', markeredgewidth=0.7)
    ax2.annotate(lab, xy=(pn, 0), xytext=(pn, yo),
                 color=dc, fontsize=8, ha='center',
                 arrowprops=dict(arrowstyle='->', color=dc, lw=0.7, alpha=0.8))

# infinity arrows (translation)
for x0 in [0.618, 1.0, 1.618, 2.414]:
    ax2.annotate('', xy=(x0+1, -0.58), xytext=(x0, -0.58),
                 arrowprops=dict(arrowstyle='->', color='#FFD700',
                                 lw=1.2, connectionstyle='arc3,rad=-0.3'))
ax2.text(1.8, -1.02, r'$\infty$: $x \to x+1$  (accumulate)',
         color='#FFD700', fontsize=9, ha='center')

# inversion arcs
for x0 in [1.618, 2.414, 3.303]:
    inv = 1/x0
    mid = (x0+inv)/2
    r   = abs(x0-inv)/2
    th  = np.linspace(0, np.pi, 80)
    ax2.plot(mid + r*np.cos(th), 0.62 + r*np.sin(th)*0.5,
             color='#4ECDC4', linewidth=1.1, alpha=0.6)
    ax2.annotate('', xy=(inv, 0.62), xytext=(x0, 0.62),
                 arrowprops=dict(arrowstyle='->', color='#4ECDC4', lw=0.8))
ax2.text(1.5, 1.55, r'$\mathcal{O}$: $x \to 1/x$  (invert)',
         color='#4ECDC4', fontsize=9, ha='center')

# the complete loop at bottom
loop_labels = ['Matter\nsea', 'Primordial\n$n=-1$', 'Parent\n$n=0$',
               'Our universe\n$n=1$', 'Silver\n$n=2$', 'Light\nsea']
loop_x = [0.0, 0.618, 1.0, 1.618, 2.414, 4.4]
loop_y = [-1.72]*6
lcols  = ['#888888','#FF6B6B','#4ECDC4','#FFD700','#A78BFA','#ffffff']

for lx, ly, ll, lc in zip(loop_x, loop_y, loop_labels, lcols):
    ax2.plot(lx, ly, 's', markersize=9, color=lc, zorder=6,
             markeredgecolor='white', markeredgewidth=0.5)
    ax2.text(lx, ly-0.27, ll, color=lc, fontsize=7, ha='center', va='top')

for i in range(len(loop_x)-1):
    ax2.annotate('', xy=(loop_x[i+1], loop_y[i+1]),
                 xytext=(loop_x[i], loop_y[i]),
                 arrowprops=dict(arrowstyle='->', color='#555577', lw=1.3))

# closing arrow E=mc2
ax2.annotate('', xy=(0.05, -1.72), xytext=(4.35, -1.72),
             arrowprops=dict(arrowstyle='->', color='#FF6B6B', lw=1.8,
                             connectionstyle='arc3,rad=0.5'))
ax2.text(2.3, -2.3, r'$E=mc^2$ — loop closes', color='#FF6B6B',
         fontsize=9, ha='center')

# continued fraction box
ax2.text(2.4, 2.3,
         r'$\varphi = 1 + \frac{1}{1+\frac{1}{1+\frac{1}{1+\cdots}}}$'
         '\n= the loop written as a formula',
         color='#FFD700', fontsize=11, ha='center', va='top',
         bbox=dict(facecolor='#0d0d1a', edgecolor='#FFD700',
                   alpha=0.75, boxstyle='round,pad=0.45'))

fig.text(0.5, 0.005,
         'Primordial Loop Algebra  ·  J. Shields (2026)  ·  '
         'Two operations: inf (x->x+1) and O (x->1/x)  ·  '
         'Fixed point of inf^n composed with O: metallic ratio phi_n',
         color='#666677', fontsize=8, ha='center')

plt.savefig('/home/joe/Desktop/UNIFIED_MULTIVERSE/renders/pla_loop.png',
            dpi=160, bbox_inches='tight', facecolor='#050508')
plt.close()
print("saved")
