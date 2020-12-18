# In this source file, the code for the classifiers introduced in the paper "Interaction multiplexity revealed by an intelligent-agent network theory" is provided.
# Before runing the functions in this source file, PROJECT1 should be completed first.
import pandas as pd
import numpy as np
from itertools import combinations
from os import getcwd
import warnings
warnings.filterwarnings('ignore')

__all__ = ['get_Hs', 'classifier']


temp_path = getcwd()
temp_path = temp_path.split('RIM')
temp_path = temp_path[0]
root = temp_path + 'RIM\\'


def combine(temp_list, n):
    temp_list2 = []
    for c in combinations(temp_list, n):
        temp_list2.append(c)
    return temp_list2


def get_Hs(hs):
    end_list = []
    for i in range(1, len(hs) + 1):
        end_list.extend(combine(hs, i))
        end_list = [list(el) for el in end_list]
    return end_list
        
    


def get_orignal_net_RIMs(netId):
    data1 = pd.read_csv(root + 'alpha_RIM_table.csv', sep = ',')
    data2 = pd.read_csv(root + 'beta_RIM_table.csv', sep = ',')
    data3 = pd.read_csv(root + 'gamma_RIM_table.csv', sep = ',')
    
    data_called1 = data1[(data1.NetId == netId) & (data1.task == 'N') & (data1.tau == 0.00)]
    data_called2 = data2[(data2.NetId == netId) & (data2.task == 'N') & (data2.tau == 0.00)]
    data_called3 = data3[(data3.NetId == netId) & (data3.task == 'N') & (data3.tau == 0.00)]
    
    rs = set(data_called1.r)
    hs = set(data_called3.h)
    
    alphas = {}
    for r in rs:
        temp1 = data_called1[data_called1.r == r]
        temp1 = temp1['alpha']
        alphas[r] = temp1.mean()
        
    betas = {}
    for r in rs:
        temp2 = data_called2[data_called2.r == r]
        temp2 = temp2['beta']
        betas[r] = temp2.mean()

    gammas = {}
    for h in hs:
        temp3 = data_called3[data_called3.h == h]
        temp3 = temp3['gamma']
        gammas[h] = temp3.mean()

    return [alphas,betas,gammas]



def get_RIMs(netId, task, tau, subnetworkId):
    data1 = pd.read_csv(root + 'alpha_RIM_table.csv', sep = ',')
    data2 = pd.read_csv(root + 'beta_RIM_table.csv', sep = ',')
    data3 = pd.read_csv(root + 'gamma_RIM_table.csv', sep = ',')
    
    data_called1 = data1[(data1.NetId == netId) & (data1.task == task) & (data1.tau == tau) & (data1.subnetworkId == subnetworkId)]
    data_called2 = data2[(data2.NetId == netId) & (data2.task == task) & (data2.tau == tau) & (data2.subnetworkId == subnetworkId)]
    data_called3 = data3[(data3.NetId == netId) & (data3.task == task) & (data3.tau == tau) & (data3.subnetworkId == subnetworkId)]
    
    rs = set(data_called1.r)
    hs = set(data_called3.h)
    
    alphas = {}
    for r in rs:
        temp1 = data_called1[data_called1.r == r]
        temp1 = temp1['alpha']
        alphas[r] = temp1.mean()
        
    betas = {}
    for r in rs:
        temp2 = data_called2[data_called2.r == r]
        temp2 = temp2['beta']
        betas[r] = temp2.mean()

    gammas = {}
    for h in hs:
        temp3 = data_called3[data_called3.h == h]
        temp3 = temp3['gamma']
        gammas[h] = temp3.mean()

    return [alphas,betas,gammas]



def get_RIM_centroid(netIds):
    alphas,betas,gammas = get_orignal_net_RIMs(netIds[0])
    
    res1 = {}
    res2 = {}
    res3 = {}
    
    for key in alphas.keys():
        res1[key] = 0
    for key in betas.keys():
        res2[key] = 0
    for key in gammas.keys():
        res3[key] = 0
    
    
    for netId in netIds:
        temp1, temp2, temp3 = get_orignal_net_RIMs(netId)
        
        for key in res1.keys():
            res1[key] += temp1[key] / len(netIds)
            
            
        for key in res2.keys():
            res2[key] += temp2[key] / len(netIds)
            
        for key in res3.keys():
            res3[key] += temp3[key] / len(netIds)
    
    return [res1,res2,res3]




def classifier(netId, task, tau, subnetworkId, categories, x = 0, H = [3]):
    '''
    Parameters
    ----------
    netId: int
    task: 'E' or 'N'
    subnetwork: int
    categories: a list of categories, for example: [{'social':[11,12,13]}, {'citation':[21,22,23]}, {'web':[41,42,43]}, {'internet':[51,52,53]}]
    x: 0: alpha; 1: beta, 2: gamma
    H: a list of positive integers, parameter of the classifier
    
    Outputs:
    -------
    inferred_category: str

    '''
    graph_rims = get_RIMs(netId, task, tau, subnetworkId)
    g_F = np.array([graph_rims[x][h] for h in H])
    center_Fs = {}

    for cate in categories:
        cate_name = list(cate.keys())
        cate_name = cate_name[0]
        temp = get_RIM_centroid(list(cate.values())[0])
        center_Fs[cate_name] = np.array([temp[x][h] for h in H])
    d = {}

    for cate_name in center_Fs.keys():
        d[cate_name] = np.linalg.norm(g_F - center_Fs[cate_name])
    d_order = sorted(d.items(),key = lambda x:x[1],reverse = False) 
    inferred_category = d_order[0]

    return inferred_category
