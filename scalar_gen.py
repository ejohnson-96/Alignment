import numpy as np


def temp_from_omega(
        w_perp,
        w_par,
):
    return (2*(w_perp**2) + (w_par**2))/3


def run_loop(
        a,
        b,
        function,
):
    res = []
    if len(a) != len(b):
        raise ValueError(
            f"Arguments must be equal in length, received {len(a)}"
            f"and {len(b)}."
        )
    else:
        for i in range(len(a)):
            res.append(function(a[i], b[i]))
        return res

def theta_gen(
        Ta,
        Tp,
):
    return 4*Ta/Tp

def mag(
        x,
        y,
        z
):
    res = []
    for i in range(len(x)):
        res.append(np.sqrt(x[i]**2 + y[i]**2 + z[i]**2))
    return res


def arr_fix(
        data,
):
    res = []
    for i in range(len(data)):
        res.append(data[i][0])
    return res
