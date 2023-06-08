import os
from astropy import units as u
from os.path import isfile, join

from CoAl import theta_ap_0
import graph as plot
from plasmapy.particles import Particle
import pandas as pd
import pickle

def load_pkl(
        path,
):
    with open(path, 'rb') as file:
        return pickle.load(file)

def load_csv(
        path,
):
        return pd.read_csv(path)

path = os.getcwd() + "/Data/"

files = [f for f in os.listdir(path) if isfile(join(path, f))]
csv_files = []
pkl_files = []
for file in files:
    if ".csv" in file:
        csv_files.append(file)
    elif ".pkl" in file:
        pkl_files.append(file)

ds = []
df = {}
for file in pkl_files:
    df[file.split(".")[0]] = load_pkl(path + file)
    ds.append(file.split(".")[0])

for file in csv_files:
    df[file.split(".")[0]] = load_csv(path + file)
    ds.append(file.split(".")[0])


au_con = 0.00465047
psp = {"proton": df['span_psp'], "alpha": df['he_span_psp']}
solo = {"proton": df['pas_solo'], "alpha": df['he_pas_solo']}


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
L = len(n_1)
for i in range(L):
    theta.append(T_2[i]/T_1[i])
    x.append(theta_ap_0(psp_r, 1.0, n_1[i], n_[i], v_1[i], T_1[i], T_2[i]/T_1[i]))
    print('\r', f"{(i / L) * 100:.2f} %", end="")


plot.plot_hist(theta, 35, 15)
plot.plot_hist(x, 35, 15)

