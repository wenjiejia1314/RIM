#In this project, we measure the alpha-, beta- and gamma- RIMs of real network in Supplementary Table S1.
from BasicTools.rim import get_pr
from os import getcwd
from scipy import stats
import numpy as np
import snap

temp_path = getcwd()
temp_path = temp_path.split('RIM')
temp_path = temp_path[0]
root = temp_path + 'RIM\\'

real_network_path = root + 'RealNetworkData\\'
output_path = root + 'Outputs\\'
real_network_Ids = [11,12,13,21,22,23,31,32,33,41,42,43,51,52,53]

def get_RIM_table(tasks = ['E', 'N'], taus = [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50], 
                subnetworks = 30,  rs = [3, 4, 5, 6, 7, 8, 9], rsm_n = 5000, trials = 30):
    '''
    Measure the alpha-, beta- and gamma- RIMs of real network in Supplementary Table S1.
    Parameters
    ----------
    tasks:  'E', removing a percentage (tau) of Edges
            'N', removing a percentage (tau) of Nodes
    taus:  a list of float numbers, a set of taus.
    subnetworks:  number of generated subnetworks 
    rs :  a list of integers, lengths of sample paths
    rsm_n :  int, number of random sample paths in measuring RIMs
    trials:  int, number of trials in measuring RIMs

    Outputs
    -------
    alpha_RIM_table.csv:  NetId, task, tau, subnetworkId, r, alpha
                   11,'E',0.00,0,3,X
                   ...
            
    beta_RIM_table.csv:  NetId, task, tau, subnetworkId, r, beta
                   11,'E',0.00,0,3,X
                   ...   

    gamma_RIM_table.csv:  NetId, task, tau, subnetworkId, h, gamma
                   11,'E',0.00,0,1,X
                   ...  

    '''
    
    output_file1 = open(output_path + "alpha_RIM_table.csv", 'w')
    output_file2 = open(output_path + "beta_RIM_table.csv", 'w')
    output_file3 = open(output_path + "gamma_RIM_table.csv", 'w')
    output_file1.write('NetId,task,tau,subnetworkId,r,alpha\n')
    output_file2.write('NetId,task,tau,subnetworkId,r,beta\n')
    output_file3.write('NetId,task,tau,subnetworkId,h,gamma\n')
    output_file1.close()
    output_file2.close()
    output_file3.close()

    for netId in real_network_Ids:
        graph_path = real_network_path + "%d.txt" % netId
        graph = snap.LoadEdgeList(snap.PNGraph, graph_path, 0, 1)
        for task in tasks:
            for tau in taus:
                for subnetworkId in range(subnetworks):
                    if task == 'N':
                        temp_subnetwork = snap.GetRndSubGraph(graph, int(graph.GetNodes() * (1.0 - tau)))
                    elif task == 'E':
                        temp_subnetwork = snap.GetRndESubGraph(graph, int(graph.GetEdges() * (1.0 - tau)))
                    
                    prs = {}
                    for r in rs:
                        temp_pr = get_pr(temp_subnetwork, r, rsm_n, trials)
                        prs[r] = temp_pr[0]
                    
                    betas = {}
                    for r in rs:
                        betas[r] = 1.0 - prs[r]
                    
                    alphas = {}
                    for r in rs:
                        alphas[r] = 0.0 - np.log(prs[r])
                    
                    gammas = {}
                    for h in range(1, len(rs)):
                        temp = {}       
                        X = np.array(list(range(3, 4 + h )))
                        Y = [alphas[r] for r in range(3, 4 + h)]
                        Y = np.array(Y)
                        slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
                        gammas[h] = slope
                    

                    output_file1 = open(output_path + "alpha_RIM_table.csv", 'a')
                    output_file2 = open(output_path + "beta_RIM_table.csv", 'a')
                    output_file3 = open(output_path + "gamma_RIM_table.csv", 'a')
                    for r in rs:
                        output_file1.write("%d,%s,%f,%d,%d,%f\n" % (netId, task, tau, subnetworkId, r, alphas[r])
                        output_file2.write("%d,%s,%f,%d,%d,%f\n" % (netId, task, tau, subnetworkId, r, betas[r])
                        
                    for h in range(1, len(rs)):
                        output_file3.write("%d,%s,%f,%d,%d,%f\n" % (netId, task, tau, subnetworkId, h, gammas[h])
                    output_file1.close()
                    output_file2.close()
                    output_file3.close()

                    
    


if __name__ == '__main__':
    get_RIM_table()
    
                    

