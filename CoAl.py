import math
import numpy as np

def theta_ap_0(r_0, r_1, n_p_1, eta_ap, v_p_1, t_p_1, theta_ap_1,
               n_step=100,):
    # Initialize the alpha-proton charge and mass ratios.
    z_a = 2.
    mu_a = 4.

    t_p_1 = t_p_1

    # Initialise.
    d_r = (r_0 - r_1) / (1. * n_step)

    theta_ap = theta_ap_1

    # Loop.
    for i in range(n_step):

        r = r_1 + ((i + 1) * d_r)

        a = -1.8
        b = -0.2
        c = -0.74

        n_p = n_p_1 * (r / r_1) ** a
        v_p = v_p_1 * (r / r_1) ** b
        t_p = t_p_1 * (r / r_1) ** c

        alpha = (theta_ap + mu_a)
        beta = theta_ap

        if alpha == 0:
            alpha = float('Nan')
        if beta == 0:
            beta = float('Nan')

        charlie = 1 + (z_a ** 2 * eta_ap / beta)

        if charlie < 0:
            charlie = 0

        arg_ = ((n_p ** 0.5 / t_p ** 1.5) * (z_a * (mu_a + 1) / alpha) *
                (charlie) ** 0.5)

        if arg_ == 0:
            arg_ = math.exp(9)
        elif type(arg_) is complex:
            arg_ = math.exp(9)
        else:
            pass

        lambda_ap = 9 + np.log(arg_)

        x = (v_p * t_p ** 1.5)
        y = (eta_ap + 1) ** 2.5

        if theta_ap == float('Nan'):
            z = float('Nan')
        else:
            z = (theta_ap + mu_a) ** 1.5

        if x == 0:
            x = float('Nan')
        if y == 0:
            y = float('Nan')
        if z == 0:
            z = float('Nan')
        elif z < 0:
            z = float('Nan')

        d_theta_ap = ((-2.60e7) * ((n_p /x)) * (mu_a ** 0.5 * z_a ** 2 / y) * ((theta_ap - 1.) * (eta_ap * theta_ap + 1.) ** 2.5 / z) * (lambda_ap) * (d_r))

        theta_ap = theta_ap + d_theta_ap

    return theta_ap