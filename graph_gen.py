from main import load_files
from astropy import units as u
from CoAl import theta_ap_0
import graph as plot
from plasmapy.particles import Particle
import scalar_gen as sg

clrs = ["black", "blue", "red"]
styles = ["-", "--", "-."]

boxes = 35
range_value = 15

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
    theta.append(T_2[i]/T_1[i])
    x.append(theta_ap_0(psp_r, 1.0, n_1[i], n_[i], v_1[i], T_1[i], T_2[i]/T_1[i]))
    y.append(theta_ap_0(psp_r, solo_r, n_1[i], n_[i], v_1[i], T_1[i], T_2[i] / T_1[i]))
    print('\r', f"{(i / L) * 100:.2f} %", end="")

tle = ""
lbls = ["", "", ""]
plot.plot_hist([theta, x, y], labels=lbls, color=clrs, style=styles, title=tle, box_n=boxes, range=range_value)


n_1 = solo['proton'][1]
n_ = solo['alpha'][1]
v_1 = solo['proton'][2]
T_1 = solo['proton'][3] * u.eV
T_1 = T_1.to(u.K, equivalencies=u.temperature_energy()).value
T_2 = solo['alpha'][3] * u.eV
T_2 = T_2.to(u.K, equivalencies=u.temperature_energy()).value
ions = [Particle("p+"), Particle("He-4++")]

theta = []
x = []
L = 100 #= len(n_1)
for i in range(L):
    theta.append(T_2[i]/T_1[i])
    x.append(theta_ap_0(solo_r, 1.0, n_1[i], n_[i], v_1[i], T_1[i], T_2[i]/T_1[i]))
    print('\r', f"{(i / L) * 100:.2f} %", end="")

lbls = ["", "", ""]
plot.plot_hist([theta, x, y], labels=lbls, color=clrs, style=styles, box_n=35, range=15)

print(wind.keys())

np_w = wind["P+_DENSITY_cm^{-3}"]
na_w = wind["HE++_DENSITY_NONLIN_cm^{-3}"]

wp_perp = wind["P+_WPERP_NONLIN_km/s"]
wp_par = wind["P+_WPAR_NONLIN_km/s"]

wa_perp = wind["HE++_WPERP_NONLIN_km/s"]
wa_par = wind["HE++_WPAR_NONLIN_km/s"]

wp_wind = sg.run_loop(wp_perp, wp_par, sg.temp_from_omega)
wa_wind =sg.run_loop(wa_perp, wa_par, sg.temp_from_omega)

vp_wind = sg.mag(wind["P+_VX_GSE_NONLIN_km/s"], wind["P+_VY_GSE_NONLIN_km/s"], wind["P+_VZ_GSE_NONLIN_km/s"])
va_wind = sg.mag(wind["HE++_VX_GSE_NONLIN_km/s"], wind["HE++_VY_GSE_NONLIN_km/s"], wind["HE++_VZ_GSE_NONLIN_km/s"])

B_wind = sg.mag(wind["BX_nT"], wind["BY_nT"], wind["BZ_nT"])

theta_w = sg.run_loop(wa_wind, wp_wind, sg.theta_gen)

theta = []
x = []
L = 10 #= len(n_1)
for i in range(L):
    theta.append(T_2[i]/T_1[i])
    x.append(theta_ap_0(solo_r, 1.0, n_1[i], n_[i], v_1[i], T_1[i], T_2[i]/T_1[i]))
    print('\r', f"{(i / L) * 100:.2f} %", end="")



theta_w[:] = [x for x in theta_w if x<= 100]
print(theta_w)
plot.plot_hist(theta_w, 35, 10)


