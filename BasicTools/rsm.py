from random import randint


__all__ = ['rsm', 'getRandomDirectedPathCenteredAtNode']

def getRandomDirectedPathCenteredAtNode(graph, node, r):
    nodeId = node.GetId()
    if r % 2 == 0:
        given_node_pos = r / 2
    else:
        given_node_pos = (r - 1) / 2

    leftSideCnt = given_node_pos
    rightSideCnt = r - leftSideCnt

    leftSides = []
    rightSides = []

    def getLeftSide(directedPath):
        if len(directedPath) - 1 == leftSideCnt:
            if directedPath not in leftSides:
                leftSides.append(directedPath)
        else:
            srcId = directedPath[0]
            src = graph.GetNI(srcId)
            inDeg = src.GetInDeg()
            if inDeg > 0:
                nextSrcIds = [nextSrcId for nextSrcId in src.GetInEdges()]
                nextSrcId = nextSrcIds[randint(0, inDeg - 1)]
                nextDirectedPath = [nextSrcId] + directedPath
                getLeftSide(nextDirectedPath)


    def getRightSide(directedPath):
        if len(directedPath) - 1 == rightSideCnt:
            if directedPath not in rightSides:
                rightSides.append(directedPath)
        else:
            dstId = directedPath[-1]
            dst = graph.GetNI(dstId)
            outDeg = dst.GetOutDeg()
            if outDeg > 0:
                nextDstIds = [nextDstId for nextDstId in dst.GetOutEdges()]
                nextDstId = nextDstIds[randint(0, outDeg -1)]
                nextDirectedPath = directedPath + [nextDstId]
                getRightSide(nextDirectedPath)
    
    directedPath = [nodeId]
    getLeftSide(directedPath)
    getRightSide(directedPath)
    if (len(leftSides) > 0) and (len(rightSides) > 0):
        newleftside = leftSides[0]
        newrightside = rightSides[0]
        newdirectedPath = newleftside + newrightside[1:]
        return newdirectedPath
    else:
        return []



def rsm(graph, r, rsm_n = 5000):
    '''
    use Ramdom Sampling Method (RSM) to gain simple paths.
    Parameters
    ----------
    graph : snap.TNGraph
    r : int 
    rsm_n : int

    Returns
    -------
    res : list of r-length dircted paths. 
    '''

    res = []
    N = graph.GetNodes()
    rsm_n = min(N,rsm_n)
    while len(res) < rsm_n:
        randNodeId = graph.GetRndNId()
        node = graph.GetNI(randNodeId)
        temp = getRandomDirectedPathCenteredAtNode(graph, node, r)
        if (len(temp) == r + 1) and (temp not in res):
            res.append(temp)
    return res