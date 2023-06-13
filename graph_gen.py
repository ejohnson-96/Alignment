from main import load_files
from astropy import units as u
from CoAl import theta_ap_0
import graph as plot
from plasmapy.particles import Particle
import scalar_gen as sg
L=1000
clrs = ["black", "blue", "red"]
styles = ["-", "--", "-."]

k_B = 1.38 * 10**-23
mu = 1.67 * 10**-27

boxes = 35
range_value = 8

psp, solo, wind = load_files()

au_con = 0.00465047

psp_r = 13.5 * au_con
solo_r = 127 * au_con

n_1 = psp['proton'][1]
n_ = psp['proton'][2]
v_1 = psp['proton'][3]
T_1 = psp['proton'][4] * u.eV
T_1 = T_1.to(u.K, equivalencies=u.temperature_energy()).value
T_2 = psp['alpha'][2] * u.eV
T_2 = T_2.to(u.K, equivalencies=u.temperature_energy()).value
ions = [Particle("p+"), Particle("He-4++")]

theta = []
x = []
y = []
L = len(n_1)
for i in range(L):
    #print(n_1[i], n_[i], v_1[i], T_1[i], T_2[i] / T_1[i])
    theta.append(T_2[i]/T_1[i])
    x.append(theta_ap_0(psp_r, 1.0, n_1[i], n_[i], v_1[i], T_1[i], theta[i]))
    y.append(theta_ap_0(psp_r, solo_r, n_1[i], n_[i], v_1[i], T_1[i], theta[i]))
    print('\r', f"{(i / L) * 100:.2f} %", end="")

tle = "Parker Solar Probe (PSP)"
lbls = [r"$r = 0.0625 \, {\rm au}$", r"$r = 1.0 \, {\rm au}$ - Wind", r"$ r = 0.59 \, {\rm au}$ - SOLO"]
plot.plot_hist([theta, x, y], labels=lbls, color=clrs, style=styles, title=tle, box_n=boxes, range=range_value)

n_1 = solo['proton'][1]
n_ = sg.arr_fix(solo['alpha'][1])
v_1 = solo['proton'][2]
T_1 = solo['proton'][3] * u.eV
T_1 = T_1.to(u.K, equivalencies=u.temperature_energy()).value
T_2 = solo['alpha'][3] * u.eV
T_2 = sg.arr_fix(T_2.to(u.K, equivalencies=u.temperature_energy()).value)
ions = [Particle("p+"), Particle("He-4++")]

theta = []
x = []
y = []
L = len(n_1)
for i in range(L):
    #print(n_1[i], n_[i], v_1[i], T_1[i], T_2[i]/T_1[i])
    theta.append(T_2[i]/T_1[i])
    x.append(theta_ap_0(solo_r, 1.0, n_1[i], n_[i], v_1[i], T_1[i], T_2[i]/T_1[i]))
    y.append(theta_ap_0(solo_r, psp_r, n_1[i], n_[i], v_1[i], T_1[i], T_2[i] / T_1[i]))
    print('\r', f"{(i / L) * 100:.2f} %", end="")

tle = "Solar Orbiter SOLO"
lbls = [r"$ r = 0.59 \, {\rm au}$", r"$r = 1.0 \, {\rm au}$ - Wind", r"$r = 0.0625 \, {\rm au}$ - PSP" ]
plot.plot_hist([theta, x, y], labels=lbls, color=clrs, style=styles, title=tle, box_n=boxes, range=range_value)

n_1, n_2, v_1 = None, None, None
n_1 = wind["P+_DENSITY_cm^{-3}"]
n_2 = wind["HE++_DENSITY_NONLIN_cm^{-3}"]

wp_perp = wind["P+_WPERP_NONLIN_km/s"]
wp_par = wind["P+_WPAR_NONLIN_km/s"]

wa_perp = wind["HE++_WPERP_NONLIN_km/s"]
wa_par = wind["HE++_WPAR_NONLIN_km/s"]

wp_wind = sg.run_loop(wp_perp, wp_par, sg.temp_from_omega)
wa_wind =sg.run_loop(wa_perp, wa_par, sg.temp_from_omega)

v_1 = sg.mag(wind["P+_VX_GSE_NONLIN_km/s"], wind["P+_VY_GSE_NONLIN_km/s"], wind["P+_VZ_GSE_NONLIN_km/s"])
va_wind = sg.mag(wind["HE++_VX_GSE_NONLIN_km/s"], wind["HE++_VY_GSE_NONLIN_km/s"], wind["HE++_VZ_GSE_NONLIN_km/s"])

B_wind = sg.mag(wind["BX_nT"], wind["BY_nT"], wind["BZ_nT"])

theta = []
x = []
y = []
L = len(n_1)
for i in range(L):
    theta.append(4*wa_wind[i]**2/wp_wind[i]**2)
    T_1 = (2*(mu)*wp_wind[i]**2)/(3*k_B)
    print(n_1[i], n_[i], v_1[i], T_1, theta[i])
    x.append(theta_ap_0(1.0, solo_r, n_1[i], n_[i], v_1[i], T_1, theta[i]))
    y.append(theta_ap_0(1.0, psp_r, n_1[i], n_[i], v_1[i], T_1, theta[i]))
    print('\r', f"{(i / L) * 100:.2f} %", end="")



theta[:] = [arg for arg in theta if arg<= 100]
x[:] = [arg for arg in x if arg<= 100]
y[:] = [arg for arg in y if arg<= 100]


print(x, y)

tle = "Wind"
lbls = [r"$r = 1.0 \, {\rm au}$", r"$ r = 0.59 \, {\rm au}$ - SOLO", r"$r = 0.0625 \, {\rm au}$ - PSP" ]
plot.plot_hist([theta, x, y], labels=lbls, color=clrs, style=styles, title=tle, box_n=boxes, range=range_value)

