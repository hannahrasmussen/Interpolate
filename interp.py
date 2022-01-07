import numba as nb
import numpy as np

@nb.jit(nopython=True)
def log_fix(y):
    log_y = np.zeros(len(y))
    for i in range(len(y)):
        if (y[i]==0):
            log_y[i] = -200
        else:
            log_y[i] = np.log(y[i])
    return log_y

@nb.jit(nopython=True)
def lin_int(X,x,y): 
    
    P00 = y[0]
    P11 = y[1]
    P22 = y[2]
    P33 = y[3]
    P44 = y[4]
    P55 = y[5]
    
    P01 = ((X-x[1])*P00 - (X-x[0])*P11)/(x[0]-x[1])
    P12 = ((X-x[2])*P11 - (X-x[1])*P22)/(x[1]-x[2])
    P23 = ((X-x[3])*P22 - (X-x[2])*P33)/(x[2]-x[3])
    P34 = ((X-x[4])*P33 - (X-x[3])*P44)/(x[3]-x[4])
    P45 = ((X-x[5])*P44 - (X-x[4])*P55)/(x[4]-x[5])
    
    P02 = ((X-x[2])*P01 - (X-x[0])*P12)/(x[0]-x[2])
    P13 = ((X-x[3])*P12 - (X-x[1])*P23)/(x[1]-x[3])
    P24 = ((X-x[4])*P23 - (X-x[2])*P34)/(x[2]-x[4])
    P35 = ((X-x[5])*P34 - (X-x[3])*P45)/(x[3]-x[5])
    
    P03 = ((X-x[3])*P02 - (X-x[0])*P13)/(x[0]-x[3])
    P14 = ((X-x[4])*P13 - (X-x[1])*P24)/(x[1]-x[4])
    P25 = ((X-x[5])*P24 - (X-x[2])*P35)/(x[2]-x[5])
    
    P04 = ((X-x[4])*P03 - (X-x[0])*P14)/(x[0]-x[4])
    P15 = ((X-x[5])*P14 - (X-x[1])*P25)/(x[1]-x[5])
    
    P05 = ((X-x[5])*P04 - (X-x[0])*P15)/(x[0]-x[5])
    
    return P05
    
@nb.jit(nopython=True)
def interp(X,x_full,y_full):
    if X > x_full[-1]:
        print("Error:  extrapolation required!")
        return 0
    
    j = np.where(x_full < X)[0][-1]
    if j < 3:
        return lin_int(X, x_full[:6], y_full[:6])
    elif (j > len(x_full) - 4):
        return lin_int(X, x_full[-6:], y_full[-6:])
    else:
        return lin_int(X, x_full[j-3:j+3], y_full[j-3:j+3])
    
@nb.jit(nopython=True)
def interp_log(X,p_array,y_full):
    log_y = log_fix(y_full)
    return np.exp(interp(X,p_array,log_y))

@nb.jit(nopython=True)
def linear_extrap(X,x,y):    
    return y[0] + (y[1] - y[0])/(x[1] - x[0]) * (X - x[0])

@nb.jit(nopython=True)
def log_linear_extrap(X,x,y):
    log_y = log_fix(y)
    return np.exp(linear_extrap(X,x,log_y))
