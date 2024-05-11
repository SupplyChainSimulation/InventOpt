# This script does the following

# sample x% points from whole data
# fit a metamodel (GPR/NN) with some metamodel parameter values
# do optimization
# calculate mse (goodness of fit)
# calculate dist(actual optimum and obtained optimum)

# to build a metamodel
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from sklearn.neural_network import MLPRegressor
#import pickle # to save a metamodel

# to optimize
from scipy import optimize
from scipy.interpolate import Rbf

# general operations
from csv import writer
import pandas as pd
import numpy as np
import random
import time
import os

# to parallelize the script
import multiprocessing as mp
#from joblib import parallel_backend

# load whole data (exhaustive eval)
data_fx = pd.read_csv("../data/supplychain_datav2_720_60_llel.csv")
data_fx = data_fx[['S_R1','s_R1', 'S_R2', 's_R2', 'S_D1', 's_D1', 'S_D2', 's_D2', 'avg_net_profit']]

# some global variables
metamodel_regr = None # this is to save the metamodel
x_fx_arr = [] # this global array is created for estimating the number of iterations
# an optimizer will take before converging to a maxima/minima

# decorated objective fucntion for optimizers
def obj_fun(x):
    global metamodel_regr, x_fx_arr
    pad = [300,100,300,100,600,350,600,350]
    gx = metamodel_regr.predict([x,pad])
    gx = -gx[0]
    # save iterations and the min found till now
    min_found = 0
    if(len(x_fx_arr)>0):
        min_found = x_fx_arr[-1][1]
    if(gx<min_found):
        min_found = gx
    x_fx_arr.append([len(x_fx_arr),min_found])
    return gx

# function calculates mean squared error
def mse(x1,x2):
    if(len(x1)!=len(x2)):
        print("lengths do not match")
        return
    squared_sum = 0
    for i in range(0,len(x1)):
        squared_sum = (x1[i]-x2[i])**2
    return (1/len(x1))*np.sqrt(squared_sum)

# function samples x% data points from whole data
# fits a metamodel
# calculate mse
# fits optimizer
# calculates dist(act optimum, obtained optimum)
def fit_with_x_perc(in_params): #[train_data_perc, name, optimizer_name]
    global data_fx, metamodel_regr, x_fx_arr
    filename = "../data/opti_using_meta_stats.csv"
    filename_est_n_itr_opti = "../data/"+str(in_params[0])+in_params[1][0]+in_params[2]+"_est_n_itr_opti.csv"
    num_samples_percent = in_params[0]/100 # num of sample points is num_samples_percent % of whole data we created above
    # randomly sample some K training points
    k = int(data_fx.shape[0]*num_samples_percent)
    indices = random.sample(range(0, data_fx.shape[0]), k)
    X_train = data_fx.values[indices,:8]
    y_train = data_fx.values[indices,8]
    print(f"Training Data shape X = {X_train.shape}, shape y = {y_train.shape}")

    if(in_params[1][0]=="gpr"):
        # let us fit a GPR metamodel with RBF kerneli
        start_time = time.time()
        #with parallel_backend('threading', n_jobs=2):
        # Your scikit-learn code here
        kernel = RBF(length_scale=in_params[1][1],length_scale_bounds=in_params[1][2])
        regr = GaussianProcessRegressor(kernel=kernel,random_state=0).fit(X_train,y_train)

    elif(in_params[1][0]=="nn"):
        # let us fit a MLP
        start_time = time.time()
        #with parallel_backend('threading', n_jobs=2):
        # Your scikit-learn code here
        regr = MLPRegressor(hidden_layer_sizes=in_params[1][1],
                            activation='relu',
                            solver='lbfgs',
                            random_state=1,
                            max_iter=3000).fit(X_train, y_train)
    
    print("train data = ",in_params[0],"exe time for fitting ",in_params[1][0]," = ",time.time()-start_time)
    exe_time = time.time()-start_time
    # predict for remaining points and calculate mse
    gx = regr.predict(data_fx[['S_R1','s_R1', 'S_R2', 's_R2', 'S_D1', 's_D1', 'S_D2', 's_D2']].values)
    fx_gx_mse = mse(gx,data_fx['avg_net_profit'].values)
    
    # save the metamodel to global variable
    metamodel_regr = regr
    # optimization
    # generate for N random starting points (x0)
    N = 20
    optimum_arr = []
    for i in range(N):
        x_fx_arr.clear()
        x0 = [np.random.randint(300, 450), #SR1
            np.random.randint(100, 250), #sR1
            np.random.randint(300, 450), #SR2
            np.random.randint(100, 250), #sR2
            np.random.randint(600, 750), #SD1
            np.random.randint(350, 500), #sD1
            np.random.randint(600, 750), #SD2
            np.random.randint(350, 500)] #sD2
        result = optimize.minimize(obj_fun,x0,method=in_params[2])
        optimum_arr.append([*result.x, result.fun])
        x_fx_arr = np.array((x_fx_arr)).T
        with open(filename_est_n_itr_opti, 'a', newline='') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow(x_fx_arr[1,:])
            f_object.close()
        x_fx_arr = []
        
    # save stats to csv file
    optimum_arr = np.array((optimum_arr))
    opti_id = np.argmin(optimum_arr[:,-1])
    optimum_x_gx = optimum_arr[opti_id]
    # saving format/columnnames are
    # (1) train data %, (2) metamodel name, (3-4) metamodel parameters, (5) mse (goodness of fit), (6) exe_time to fit metamodel,
    # (7) optimization method name, (8-17) optimum x found and g(x), (18-.) predictions on all data
    with open(filename, 'a', newline='') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow([num_samples_percent, *in_params[1], fx_gx_mse, exe_time, in_params[2], *optimum_x_gx, *gx])
        f_object.close()
    return 1

#pool = mp.Pool()
#pool = mp.Pool(processes=2)

#input_arr = [[80,"gpr"],[90,"gpr"]]
#pool.map(fit_with_x_perc,input_arr)
fit_with_x_perc([25,["gpr",1,(30,60)],"COBYLA"])