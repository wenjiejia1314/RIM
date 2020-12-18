# In this project, we measure the accuracy of the identifiers introduced in the paper "Interaction multiplexity revealed by an intelligent-agent network theory".
# Before runing this project, PROJECT1 should be completed first.

from BasicTools.identifier import get_Hs, classifier
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
    accuracy_of_identifier_alpha_RIM.csv:  task,H,tau,accuracy
                                                          E,[3],0.00,X
                                                          ...

    accuracy_of_identifier_beta_RIM.csv:   task,H,tau,accuracy
                                                          E,[3],0.00,X
                                                          ...

    accuracy_of_identifier_gamma_RIM.csv:  task,H,tau,accuracy
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


    output_file1 = open(output_path + 'accuracy_of_identifier_alpha_RIM.csv', 'w')
    output_file2 = open(output_path + 'accuracy_of_identifier_beta_RIM.csv', 'w')
    output_file3 = open(output_path + 'accuracy_of_identifier_gamma_RIM.csv', 'w')
    output_file1.write('task,H,tau,accuracy\n')
    output_file2.write('task,H,tau,accuracy\n')
    output_file3.write('task,H,tau,accuracy\n')
    output_file1.close()
    output_file2.close()
    output_file3.close()
    
    
    for x in [0,1,2]:
        if x == 0:
            Hs = get_Hs(rs)
            this_output_file = open(output_path + 'accuracy_of_identifier_alpha_RIM.csv', 'a')
        elif x == 1:
            Hs = get_Hs(rs)
            this_output_file = open(output_path + 'accuracy_of_identifier_beta_RIM.csv', 'a')
        else:
            Hs = get_Hs(hs)
            this_output_file = open(output_path + 'accuracy_of_identifier_gamma_RIM.csv', 'a')
        
        for task in ['E', 'N']:
            for tau in taus:
                for H in Hs:
                    nnt = 0.0
                    cnt = 0.0
                    for graph_name in graph_names:
                        netId = graph_ids[graph_name]
                        for subnetworkId in subnetworkIds:
                            inferred_category = classifier(netId, task, tau, subnetworkId, categories4indentifier, x, H)
                            if inferred_category == graph_name:
                                cnt += 1
                            nnt += 1
                    this_accuracy = cnt / nnt
                    this_output_file.write('%s,%s,%f,%f\n' % (task, H, tau, this_accuracy))
        this_output_file.close()


if __name__ == '__main__':
    main()


            
            

