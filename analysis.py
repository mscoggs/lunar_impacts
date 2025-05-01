import pandas as pd
import os
import numpy as np
from scipy.interpolate import griddata
from scipy.interpolate import Rbf
from consts import *
import glob

def get_flux_avg(dir_):
    flux_file = dir_+"/HiDensity/flux_avg.txt"
    colnames = ["phi", "theta"]+[str(x) for x in list(np.arange(80))]
    df = pd.read_csv(flux_file, skiprows=8,names = colnames,delim_whitespace=True)
    return df

def get_cube_avg(dir_):
    cube_avg_file = dir_+"/HiDensity/cube_avg.txt"
    names = ["velocity", "+x", "-x", "+y", "-y", "+z", "-z", "Earth", "Sun", "anti-Sun", "rot (x)", "rot (y)", "rot (z)"]
    df = pd.read_csv(cube_avg_file, skiprows=9,delim_whitespace=True,names=names)
    return df

def get_density_profile(dir_):
    density_profile_file = dir_+"/hidensity.txt"
    colnames = ["rho_min", "rho_max",   "fraction"]
    df = pd.read_csv(density_profile_file, skiprows=2,names = colnames,delim_whitespace=True)
    return df

def get_avg_flux(dir_):
    local = 1
    cube_avg_file = dir_+"/HiDensity/cube_avg.txt"
    file = open(cube_avg_file, 'r')
    lines = file.readlines()
    for line in lines:
        if "total cross-sectional flux" in line:
            return float(line.split()[-2])

def get_impact_rate(dir_,std=False):
    l,w,h = BASE_LENGTH, BASE_WIDTH, BASE_HEIGHT
    cube_avg_file = dir_+"/HiDensity/cube_avg.txt"
    if(std): cube_avg_file = dir_+"/HiDensity/cube_std.txt"
    if(not os.path.exists(cube_avg_file)): return -1
    names = ["velocity", "+x", "-x", "+y", "-y", "+z", "-z", "Earth", "Sun", "anti-Sun", "rot (x)", "rot (y)", "rot (z)"]
    df = pd.read_csv(cube_avg_file, skiprows=9,delim_whitespace=True,names=names)
    xtot, ytot, ztot =  np.sum(df["+x"])+np.sum(df["-x"]), np.sum(df["+y"])+np.sum(df["-y"]), np.sum(df["+z"])

    top_sum = ztot*l*w
    side_sum = l*h*(ytot+xtot)
    if(std):
        num = top_sum**2*l*w+ side_sum**2  * h*w*4
        denom = l*w + 4*w*h
        return np.sqrt(num/denom)

    return top_sum+side_sum

def get_all_sim_dirs():
    return list(glob.iglob(DATA_DIR+"*"))

def pull_phi_theta(fname):
    tail = fname.split("\\")[-1]
    phi = float((tail.split("phi_")[-1]).split("_")[0])
    theta = float(tail.split("_")[-1])
    return phi,theta


def consolidate_sims(save_name):
    data_folders = get_all_sim_dirs()


    phis, thetas, flux=[],[],[]
    for folder in data_folders:
        phi, theta = pull_phi_theta(save_name)

        avg_flux = get_impact_rate(run_name,std=True)

        if(avg_flux == -1):
            print(run_name, "failed")
            continue
        phis.append(phi)
        thetas.append(theta)
        flux.append(avg_flux)


    thetas,phis, flux = np.array(thetas),np.array(phis), np.array(flux)
    df = pd.DataFrame(data={'theta': thetas, 'phi': phis, 'flux': flux})
    df.to_csv("flux_files/"+save_name)

def read_flux_file(name):
    df = pd.read_csv("flux_files/"+name)
    thetas = np.array(df["theta"])
    phis = np.array(df["phi"])
    impact_rate = np.array(df["flux"])
    return thetas, phis, impact_rate


def interp_impact_rates(phi,theta,name):
    thetas, phis, impact_rate = read_flux_file(name)
    rbf3 = Rbf(thetas, phis, impact_rate, function="multiquadric", smooth=2)
    impact_rate = rbf3(theta, phi)
    return impact_rate
