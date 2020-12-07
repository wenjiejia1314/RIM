from BasicTools.rsm import rsm
from BasicTools.delta_discriminant import *
from os import getcwd
from scipy import stats
import numpy
import math



__all__ = ['get_pr', 'get_alpha_RIM', 'get_beta_RIM', 'get_gamma_RIM']




def get_pr(graph, r, rsm_n = 5000, trials = 30):
    '''
    Measure the p_r value of a graph.
    Parameters
    ----------
    graph : snap.TNGraph
    r : int, length of sample paths
    rsm_n : int, number of random sample paths
    trials: int, number of trials

    Returns
    -------
    [mean(pr), sem(pr)]  
    '''
    prs = []
    for trial in range(trials):
        simple_paths = rsm(graph = graph, r = r, rsm_n = rsm_n)
        nnt = len(simple_paths)
        if nnt > 0:
            cnt = 0
            for simple_path in simple_paths:
                edgeset = get_edge_set(simple_path)
                cnt += delta_discriminant(graph,edgeset)[0]
            pr = cnt / nnt
        else:
            pr = numpy.NaN
        prs.append(pr)
    prs = numpy.array(prs)
    return [prs.mean(), prs.std()]




def get_alpha_RIM(graph, r, rsm_n = 5000, trials = 30):
    '''
    Measure the alpha-RIM of a graph.
    Parameters
    ----------
    graph : snap.TNGraph
    r : int, length of sample paths
    rsm_n : int, number of random sample paths
    trials: int, number of trials

    Returns
    -------
    alpha: float number 
    '''
    pr = get_pr(graph, r, rsm_n, trials)
    pr = pr[0]
    alpha = 0.0 - math.log(pr)
    return alpha


def get_beta_RIM(graph, r, rsm_n = 5000, trials = 30):
    '''
    Measure the beta—RIM of a graph.
    Parameters
    ----------
    graph : snap.TNGraph
    r : int, length of sample paths
    rsm_n : int, number of random sample paths
    trials: int, number of trials

    Returns
    -------
    beta: float number 
    '''
    pr = get_pr(graph, r, rsm_n, trials)
    pr = pr[0]
    beta = 1.0 - pr
    return beta



def get_gamma_RIM(graph, h, rsm_n = 5000, trials = 30):
    '''
    Measure the gamma—RIM of a graph.
    Parameters
    ----------
    graph : snap.TNGraph
    h : int
    rsm_n : int, number of random sample paths
    trials: int, number of trials

    Returns
    -------
    gamma: float number 
    '''

    X = numpy.array(list(range(3, 4 + h )))
    Y = [get_alpha_RIM(graph, r, rsm_n, trials) for r in range(3, 4 + h)]
    Y = numpy.array(Y)
    gamma, intercept, r_value, p_value, std_err = stats.linregress(X, Y)
    return gamma

    
