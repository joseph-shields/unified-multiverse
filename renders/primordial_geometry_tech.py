import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

phi = (1 + np.sqrt(5)) / 2

def r_n(n):
    phi_n = (n + np.sqrt(n**2 + 4)) / 2
    return 1 / (2 * phi_n)

def channels(n):
    r = r_n(n)
    WM = r**2
    WB = 2*r*(1-r)
    WL = (1-r)**2
    return WL, WB, WM

# continuous n range
n_cont = np.linspace(-2, 6, 1000)
r_cont = np.array([r_n(n) for n in n_cont])
kappa_actual = 2*r_cont - 1
WL_cont = (1 - r_cont)**2
kappa_obs = WL_cont * kappa_actual
kappa_dark = kappa_actual - kappa_obs

# discrete values for markers
n_disc = np.array([-1, 0, 1, 2, 3, 4])
r_disc = np.array([r_n(n) for n in n_disc])
ka_disc = 2*r_disc - 1
WL_disc = (1-r_disc)**2
ko_disc = WL_disc * ka_disc
kd_disc = ka_disc - ko_disc
WB_disc = np.array([channels(n)[1] for n in n_disc])
WM_disc = np.array([channels(n)[2] for n in n_disc])

fig = plt.figure(figsize=(18, 11), facecolor='#06060f')

# ── PANEL 1: curvature landscape ────────────────────────────────────
ax1 = fig.add_axes([0.04, 0.12, 0.42, 0.78], facecolor='#06060f')

# geometry regions
ax1.axhspan(-1.0, 0.0, alpha=0.06, color='#4488ff', zorder=0)   # hyperbolic
ax1.axhspan( 0.0, 1.0, alpha=0.06, color='#ff4444', zorder=0)   # spherical
ax1.axhline(0, color='#ffffff', linewidth=0.6, alpha=0.2)        # Euclidean

# dark curvature shading (the gap = dark energy/dark matter)
ax1.fill_between(n_cont, kappa_obs, kappa_actual,
                 where=(kappa_actual < kappa_obs),
                 color='#ff4444', alpha=0.18, label='_nolegend_')
ax1.fill_between(n_cont, kappa_obs, kappa_actual,
                 where=(kappa_actual >= kappa_obs),
                 color='#4488ff', alpha=0.18, label='_nolegend_')

# actual vs observable curvature
ax1.plot(n_cont, kappa_actual, color='#ffffff', linewidth=2.2,
         label=r'$\kappa_{\rm actual} = 2r_n - 1$')
ax1.plot(n_cont, kappa_obs,    color='#FFD700', linewidth=2.2, linestyle='--',
         label=r'$\kappa_{\rm obs} = W_L \cdot \kappa_{\rm actual}$')
ax1.plot(n_cont, kappa_dark,   color='#FF6B6B', linewidth=1.4, linestyle=':',
         label=r'$\kappa_{\rm dark} = \kappa_{\rm actual}(1-W_L)$')

# markers
colors_disc = ['#FF6B6B','#4ECDC4','#FFD700','#A78BFA','#98FB98','#87CEEB']
labels_disc = ['$n=-1$\nPrimordial','$n=0$\nParent','$n=1$\nOurs',
               '$n=2$\nSilver','$n=3$\nBronze','$n=4$']
for nd, ka, ko, kd, dc, lb in zip(n_disc, ka_disc, ko_disc, kd_disc,
                                    colors_disc, labels_disc):
    ax1.plot(nd, ka, 'o', markersize=8, color=dc, zorder=6,
             markeredgecolor='white', markeredgewidth=0.7)
    ax1.plot(nd, ko, 'D', markersize=6, color=dc, zorder=6, alpha=0.7)
    if nd in [-1, 0, 1]:
        ax1.annotate(lb, xy=(nd, ka), xytext=(nd+0.18, ka+0.07),
                     color=dc, fontsize=7.5)

# cosmological constant arrow at n=1
kobs1 = WL_disc[2] * ka_disc[2]
kact1 = ka_disc[2]
ax1.annotate('', xy=(1, kobs1), xytext=(1, kact1),
             arrowprops=dict(arrowstyle='<->', color='#FF6B6B', lw=1.5))
ax1.text(1.35, (kobs1+kact1)/2,
         r'$\kappa_{\rm dark} \propto \Lambda$' '\n(dark energy)',
         color='#FF6B6B', fontsize=8)

# geometry labels
ax1.text(-1.8, 0.72, 'SPHERICAL\n$\\kappa > 0$', color='#ff7777',
         fontsize=9, alpha=0.7, va='top')
ax1.text(-1.8, -0.08, 'EUCLIDEAN\n$\\kappa = 0$  ($n=0$ only)',
         color='#4ECDC4', fontsize=9, alpha=0.9)
ax1.text(-1.8, -0.45, 'HYPERBOLIC\n$\\kappa < 0$', color='#7799ff',
         fontsize=9, alpha=0.7)

ax1.set_xlim(-2, 6); ax1.set_ylim(-1.05, 1.05)
ax1.set_xlabel('Recursion depth $n$', color='#cccccc', fontsize=11)
ax1.set_ylabel('Curvature', color='#cccccc', fontsize=11)
ax1.set_title('Primordial Geometry: curvature landscape\n'
              r'The gap between $\kappa_{\rm actual}$ and $\kappa_{\rm obs}$ is dark energy',
              color='white', fontsize=12, pad=8)
ax1.tick_params(colors='#888888'); ax1.set_xticks(range(-2,7))
ax1.set_xticklabels([str(i) for i in range(-2,7)], color='#aaaaaa')
for sp in ax1.spines.values(): sp.set_color('#222233')
leg = ax1.legend(facecolor='#0d0d1a', labelcolor='white', fontsize=9,
                 loc='lower right', framealpha=0.8)

# ── PANEL 2: channel weight landscape ───────────────────────────────
ax2 = fig.add_axes([0.54, 0.55, 0.43, 0.36], facecolor='#06060f')

WL_c = (1-r_cont)**2
WB_c = 2*r_cont*(1-r_cont)
WM_c = r_cont**2

ax2.stackplot(n_cont, WL_c, WB_c, WM_c,
              colors=['#FFD700','#4ECDC4','#FF6B6B'],
              labels=[r'$W_L = (1-r)^2$  light',
                      r'$W_B = 2r(1-r)$  boundary',
                      r'$W_M = r^2$  matter'],
              alpha=0.85)

ax2.axvline(1, color='white', linewidth=1.2, linestyle='--', alpha=0.5)
ax2.text(1.08, 0.5, 'our\nuniverse', color='white', fontsize=8)
ax2.axvline(0, color='#4ECDC4', linewidth=1.0, linestyle=':', alpha=0.6)

ax2.set_xlim(-2, 6); ax2.set_ylim(0, 1)
ax2.set_xlabel('Recursion depth $n$', color='#cccccc', fontsize=10)
ax2.set_ylabel('Channel weight', color='#cccccc', fontsize=10)
ax2.set_title(r'Channel weights: $W_L + W_B + W_M = 1$', color='white', fontsize=11)
ax2.tick_params(colors='#888888'); ax2.set_xticks(range(-2,7))
ax2.set_xticklabels([str(i) for i in range(-2,7)], color='#aaaaaa')
for sp in ax2.spines.values(): sp.set_color('#222233')
ax2.legend(facecolor='#0d0d1a', labelcolor='white', fontsize=8.5,
           loc='upper right', framealpha=0.8)

# ── PANEL 3: G_eff = G/W_L ──────────────────────────────────────────
ax3 = fig.add_axes([0.54, 0.12, 0.43, 0.35], facecolor='#06060f')

Geff = 1.0 / WL_c   # in units of G
ax3.plot(n_cont, Geff, color='#FF6B6B', linewidth=2.2,
         label=r'$G_{\rm eff} = G / W_L$')
ax3.axhline(1, color='white', linewidth=0.7, linestyle='--', alpha=0.3,
            label='$G$ (GR limit, $\\lambda=1$)')

# mark key levels
for nd, dc in zip([-1,0,1,2,3], colors_disc):
    wl = channels(nd)[0]
    ge = 1/wl
    ax3.plot(nd, ge, 'o', markersize=8, color=dc, zorder=6,
             markeredgecolor='white', markeredgewidth=0.7)

geff1 = 1/channels(1)[0]
geff0 = 1/channels(0)[0]
ax3.text(0.3, geff1 + 0.15,
         f'$G_{{eff}}^{{(n=1)}} \\approx {geff1:.2f}G$',
         color='#FFD700', fontsize=8.5)
ax3.text(-0.7, geff0 + 0.3,
         f'$G_{{eff}}^{{(n=0)}} \\approx {geff0:.1f}G$',
         color='#4ECDC4', fontsize=8.5)

ax3.fill_between(n_cont, 1, Geff, where=(Geff > 1),
                 color='#FF6B6B', alpha=0.15)
ax3.text(3.5, 3.5, 'enhanced gravity\n(dark matter halos)',
         color='#FF6B6B', fontsize=8, ha='center', alpha=0.8)

ax3.set_xlim(-2, 6); ax3.set_ylim(0, 7)
ax3.set_xlabel('Recursion depth $n$', color='#cccccc', fontsize=10)
ax3.set_ylabel(r'$G_{\rm eff}$ (units of $G$)', color='#cccccc', fontsize=10)
ax3.set_title(r'Effective gravity: $G_{\rm eff} = G / W_L$ — dark matter without particles',
              color='white', fontsize=11)
ax3.tick_params(colors='#888888'); ax3.set_xticks(range(-2,7))
ax3.set_xticklabels([str(i) for i in range(-2,7)], color='#aaaaaa')
for sp in ax3.spines.values(): sp.set_color('#222233')
ax3.legend(facecolor='#0d0d1a', labelcolor='white', fontsize=9, framealpha=0.8)

fig.text(0.5, 0.005,
         'Primordial Geometry  ·  J. Shields (2026)  ·  '
         'k_obs = W_L * k_actual  ·  k_n = 2r_n - 1  ·  G_eff = G/W_L',
         color='#555566', fontsize=8, ha='center')

plt.savefig('/home/joe/Desktop/UNIFIED_MULTIVERSE/renders/primordial_geometry_tech.png',
            dpi=160, bbox_inches='tight', facecolor='#06060f')
plt.close()
print("tech saved")
