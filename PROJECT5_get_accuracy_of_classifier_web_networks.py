# In this project, we measure the accuracy of the classifiers introduced in the paper "An intelligent-agent network theory to and hidden interaction multiplexities of complex systems".
# The test sets used in this project are the web networks in Supplementary Table S1 or the subnetworks generated by these web networks.
# Before runing this project, PROJECT1 should be completed first.

from BasicTools.classifier import get_Hs, classifier
from os import getcwd
import pandas as pd

temp_path = getcwd()
temp_path = temp_path.split('RIM')
temp_path = temp_path[0]
root = temp_path + 'RIM\\'
output_path = root + 'Outputs\\'



def main():
    '''
    Outputs
    ----------
    accuracy_of_classifier_alpha_RIM_web_networks.csv:  task,H,tau,accuracy
                                                          E,[3],0.00,X
                                                          ...

    accuracy_of_classifier_beta_RIM_web_networks.csv:   task,H,tau,accuracy
                                                          E,[3],0.00,X
                                                          ...

    accuracy_of_classifier_gamma_RIM_web_networks.csv:  task,H,tau,accuracy
                                                          E,[1],0.00,X
                                                          ...
    '''

    data1 = pd.read_csv(root + 'alpha_RIM_table.csv', sep = ',')
    data3 = pd.read_csv(root + 'gamma_RIM_table.csv', sep = ',')
    rs = list(set(data1.r))
    hs = list(set(data3.h))
    rs.sort()
    hs.sort()
    subnetworkIds = set(data1.subnetworkId)
    taus = set(data1.tau)
    this_categories = [{'social':[11,12,13]}, {'citation':[21,22,23]}, {'web':[41,42,43]}, {'internet':[51,52,53]}]


    output_file1 = open(output_path + 'accuracy_of_classifier_alpha_RIM_web_networks.csv', 'w')
    output_file2 = open(output_path + 'accuracy_of_classifier_beta_RIM_web_networks.csv', 'w')
    output_file3 = open(output_path + 'accuracy_of_classifier_gamma_RIM_web_networks.csv', 'w')
    output_file1.write('task,H,tau,accuracy\n')
    output_file2.write('task,H,tau,accuracy\n')
    output_file3.write('task,H,tau,accuracy\n')
    output_file1.close()
    output_file2.close()
    output_file3.close()
    
    
    for x in [0,1,2]:
        if x == 0:
            Hs = get_Hs(rs)
            this_output_file = open(output_path + 'accuracy_of_classifier_alpha_RIM_web_networks.csv', 'a')
        elif x == 1:
            Hs = get_Hs(rs)
            this_output_file = open(output_path + 'accuracy_of_classifier_beta_RIM_web_networks.csv', 'a')
        else:
            Hs = get_Hs(hs)
            this_output_file = open(output_path + 'accuracy_of_classifier_gamma_RIM_web_networks.csv', 'a')
        
        for task in ['E', 'N']:
            for tau in taus:
                for H in Hs:
                    nnt = 0.0
                    cnt = 0.0
                    for netId in [41,42,43]:
                        for subnetworkId in subnetworkIds:
                            inferred_category = classifier(netId, task, tau, subnetworkId, this_categories, x, H)
                            if inferred_category == 'web':
                                cnt += 1
                            nnt += 1
                    this_accuracy = cnt / nnt
                    this_output_file.write('%s,%s,%f,%f\n' % (task, H, tau, this_accuracy))
        this_output_file.close()


if __name__ == '__main__':
    main()


            
            

