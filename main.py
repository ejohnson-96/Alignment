import os
from os.path import isfile, join
import pickle


def load_pkl(
        path,
):
    with open(path, 'rb') as file:
        return pickle.load(file)

path = os.getcwd() + "/Data/"

files = [f for f in os.listdir(path) if isfile(join(path, f))]
files.remove('.DS_Store')

ds = []
df = {}
for file in files:
    df[file.split(".")[0]] = load_pkl(path + file)
    ds.append(file.split(".")[0])

print(ds, df)






