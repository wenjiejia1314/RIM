#alpha-RIM, beta-RIM gamma-RIM 
#accuracy of identifier tested by real networks 
import pandas as pd
import os
import numpy as np
from scipy import stats
from itertools import combinations
import warnings
warnings.filterwarnings('ignore')


__all__ = ['identifier', 'graph_ids', 'graph_names','get_Hs']

result_path = os.getcwd() + "\\" 




graph_names = ['twitter','slashdot','pokec',
               'HepPh','HepTh','patent',
               'epinions','bitcoinOTC','advogato',
               'NotreDame','Stanford','BerkStan',
               'p2p-1','p2p-2','p2p-3']

graph_ids = {'twitter':11,'slashdot':12,'pokec':13,
             'HepPh':21,'HepTh':22,'patent':23,
             'epinions':31,'bitcoinOTC':32,'advogato':33,
             'NotreDame':41,'Stanford':42,'BerkStan':43,
             'p2p-1':51,'p2p-2':52,'p2p-3':53}

categories4indentifier = [{'twitter':[11]},{'slashdot':[12]},{'pokec':[13]},
                          {'HepPh':[21]},{'HepTh':[22]},{'patent':[23]},
                          {'epinions':[31]},{'bitcoinOTC':[32]},{'advogato':[33]},
                          {'NotreDame':[41]},{'Stanford':[42]},{'BerkStan':[43]},
                          {'p2p-1':[51]},{'p2p-2':[52]},{'p2p-3':[53]}]





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
        
    


def get_orignal_net_RIMs(netid, r_max = 9):
    data_path = result_path + "results-0.csv"
    data = pd.read_csv(data_path)
    data_called = data[data.nid == netid]
    prs = {}
    rs = list(range(3, r_max + 1))
    for r in rs:
        temp = data_called[data_called.r == r]
        temp = temp['mean(pr)']
        prs[r] = temp.mean()
    
    betas = {}
    for r in rs:
        betas[r] = 1 - prs[r]
    
    alphas = {}
    for r in rs:
        alphas[r] = 0 - np.log(prs[r])
    
    gammas = {}
    
    
    for h in range(1, r_max - 2):
        temp = {}       
        X = np.array(list(range(3, 4 + h )))
        Y = [alphas[r] for r in range(3, 4 + h)]
        Y = np.array(Y)
        slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
        gammas[h] = slope

    return [alphas,betas,gammas]



#graph_quad (netid, alpha>0, sampleId, task)
def get_RIMs(graph_quad, r_max = 9):
    if graph_quad[1] == 0:
        return get_orignal_net_RIMs(graph_quad[0], r_max)
    else:
        def get_prs(graph_quad):
            net = graph_quad[0]
            alpha = graph_quad[1]
            sampleId = graph_quad[2]
            task = graph_quad[3]

            data_path = result_path + r"results-%s.csv" % task

            data = pd.read_csv(data_path)

            data_called = data[(data.nid == net) & (data.alpha == alpha) & (data.sampleId == sampleId) ]

            res = {}
            rs = list(range(3, r_max + 1))
            for r in rs:
                temp = data_called[data_called.r == r]
                prs = temp['mean(pr)']
                res[r] = prs.mean()
            return res

        prs = get_prs(graph_quad)

        betas = {}
        for r in prs.keys():
            betas[r] = 1 - prs[r]

        alphas = {}
        for r in prs.keys():
            alphas[r] = 0 - np.log(prs[r])

        gammas = {}
        h_max = r_max - 3

        for h in range(1, h_max + 1):
            temp = {}       
            X = np.array(list(range(3, 4 + h )))
            Y = [alphas[r] for r in range(3, 4 + h)]
            Y = np.array(Y)
            slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
            gammas[h] = slope

        return [alphas,betas,gammas]


def get_center_RIMs(netids, r_max = 9):
    alpha,beta,gamma = get_orignal_net_RIMs(netids[0], r_max)
    
    res1 = {}
    res2 = {}
    res3 = {}
    
    for key in alpha.keys():
        res1[key] = 0
    for key in beta.keys():
        res2[key] = 0
    for key in gamma.keys():
        res3[key] = 0
    
    
    for net in netids:
        temp1,temp2,temp3 = get_orignal_net_RIMs(net, r_max)   
        
        for key in res1.keys():
            res1[key] += temp1[key]/len(netids)
            
            
        for key in res2.keys():
            res2[key] += temp2[key]/len(netids)
            
        for key in res3.keys():
            res3[key] += temp3[key]/len(netids)
    
    return [res1,res2,res3]


def classifier(graph_quad,categories,x,hs):
    graph_rims = get_RIMs(graph_quad)
    g_F = np.array([graph_rims[x][h] for h in hs])
    center_Fs = {}
    for cate in categories:
        cate_name = list(cate.keys())
        cate_name = cate_name[0]
        temp = get_center_RIMs(list(cate.values())[0])
        center_Fs[cate_name] = np.array([temp[x][h] for h in hs])
    d = {}
    for cate_name in center_Fs.keys():
        d[cate_name] = np.linalg.norm(g_F - center_Fs[cate_name])
    d_order = sorted(d.items(),key=lambda x:x[1],reverse = False) 
    return d_order[0]


def identifier(graph_quad,x,H):
    return classifier(graph_quad,categories4indentifier,x,H)