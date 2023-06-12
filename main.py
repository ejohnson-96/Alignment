import os
import numpy as np
from os.path import isfile, join

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

def mag(
        x,
        y,
        z
):
    return np.sqrt(x**2 + y**2 + z**2)

def load_files(

):
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

    psp = {"proton": df['span_psp'], "alpha": df['he_span_psp']}
    solo = {"proton": df['pas_solo'], "alpha": df['he_pas_solo']}
    wind = df["Wind"]
    return psp, solo, wind

psp, solo, wind = load_files()


