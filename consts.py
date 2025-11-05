import numpy as np

N = 1000
MOON_OBLIQ = np.radians(1.543)
SOUTHPOLEANGLE = 7
R_MOON = 1737.4*1.02
D_0 = 2451544.5000000 #J2000 date
NUM_STEPS = 30
RHO_PARTICLE = 3 #grams/cm**3
R_PARTICLE = 0.12 #cm
SEC_PER_DAY = 86400
SEC_PER_YEAR = 3.154e+7
T_MOON_ECLIPTIC = 27.2122
W_MOON = 2*np.pi/T_MOON_ECLIPTIC
DAYS = np.linspace(0, T_MOON_ECLIPTIC, NUM_STEPS)

RUN_DIR = 'C:/Users/matth/Dropbox/github_repos/lunar_impacts/'
#RUN_DIR = 'C:/Users/Matthew/Dropbox/github_repos/lunar_impacts/'
MEM3_DIR = RUN_DIR+"MEM3_Windows/"
OPTIONS_IN = MEM3_DIR+"options_template.txt"
OPTIONS_OUT = MEM3_DIR+"options.txt"
DATA_FOLDER = "data_1000_m1.16/"
DATA_DIR = MEM3_DIR+DATA_FOLDER
LOG_MIN_MASS = -1.16
TRAJECTORY_FILE_NAME = "trajectory.txt"
MEM3_COMMAND = "MEM3Windows.exe"
FAILED_CHECK_FILE = "HiDensity/cube_avg.txt"
#m = log_min_mass(RHO_PARTICLE, R_PARTICLE)


BASE_LENGTH = 100
BASE_WIDTH = 100
BASE_HEIGHT = 10
BASE_SURF_AREA = 2*BASE_HEIGHT*(BASE_WIDTH+BASE_LENGTH) + BASE_WIDTH*BASE_LENGTH
