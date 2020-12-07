import snap
import copy

__all__ = ['get_edge_set','delta_discriminant']

def get_edge_set(directedpath):
    '''
    Return the set consisting of edges in the directed path. 
    Parameters
    ----------
    directedpath : list [V1,V2,...,Vn] representing V1->V2->...->Vn
    
    Returns
    -------
    edgeset : list [(V1,V2),(V2,V3),...m(V{n-1},Vn)]
    '''

    length = len(directedpath)-1
    edgelist = []
    for i in range(length):
        edge = (directedpath[i],directedpath[i+1])
        edgelist.append(edge)
    return edgelist


def _get_src_tar_nodes(edgeset):
    src_nodes = []
    tar_nodes = []
    for edge in edgeset:
        src_nodes.append(edge[0])
        tar_nodes.append(edge[1])
    return (src_nodes,tar_nodes)

def _get_1st_following(graph, nodei):
    nodeI = graph.GetNI(nodei)
    following = [nodeId for nodeId in nodeI.GetOutEdges()]
    return set(following)

def _get_1st_followers(graph, nodej):
    nodeJ = graph.GetNI(nodej)
    followers = [nodeId for nodeId in nodeJ.GetInEdges()]
    return set(followers)


def _check_2nd_follower(graph, nodei, nodej):
    #nodei is nodej's 2-follower return True; otherwise return False.
    if nodei == nodej:
        return False
    following = _get_1st_following(graph,nodei)
    if nodej in following:
        return False
    else:
        followers = _get_1st_followers(graph,nodej)
        cap = following & followers
        if len(cap) > 0:
            return True
        else: 
            return False

        
def _step1(graph, edgeset):
    src, tar = _get_src_tar_nodes(edgeset)
    for target in tar:
        flag = 0
        for source in src:
            flag += _check_2nd_follower(graph,source,target)
        if flag == 0:
            return target
    return -1

def _step2(graph, edgeset):
    to_remove_node = _step1(graph,edgeset)
    if to_remove_node == -1:
        new_edgeset = copy.deepcopy(edgeset)
        return new_edgeset
    else:
        #print('To remove',to_remove_node)
        new_edgeset = copy.deepcopy(edgeset)
        for edge in new_edgeset:
            if edge[1] == to_remove_node:
                new_edgeset.remove(edge)
    return new_edgeset

def _step3(graph, edgeset):
    new_edgeset = _step2(graph,edgeset)
    if (len(new_edgeset) == len(edgeset)) or (len(new_edgeset) == 0):
        return new_edgeset
    else:    
        return _step3(graph,new_edgeset)
        
    
def delta_discriminant(graph, edgeset):
    '''
    Return the set consisting of edges in the directed path. 
    Parameters
    ----------
    graph : snap.TNGraph
    edgeset : list [(V1,V2),(V2,V3),...m(V{n-1},Vn)]
    Returns
    -------
    Delta = 0 or 1 .
    Notes:
    Delta = 0 : edgeset does not have the delta-property.
    Delta = 1 : edgeset has the delta-property.
    '''
    delta_edgeset = _step3(graph,edgeset)
    if len(delta_edgeset) > 0:
        return (0,delta_edgeset)
    else:
        return (1,delta_edgeset)       