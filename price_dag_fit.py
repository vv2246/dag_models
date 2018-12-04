# -*- coding: utf-8 -*-
"""
Created on Tue Dec 4 15:27:03 2018

@author: Vaiva

DAG with fit nodes (Price model)
"""




def price_dag_fit_nodes(n, m, c,f, seed=None,random_attachment = False):
    """Return random graph using Price cummulative advantage model.

    A graph of n nodes is grown by attaching new nodes each with m
    edges that are preferentially attached to existing nodes with high
    degree.

    Parameters
    ----------
    n : int
        Number of nodes
    m : int
        Number of edges to attach from a new node to existing nodes
    c: number of times a node with out-degree=0 is added to the target list
        c = 1 Price original model
        c = m Directed Barabasi-Albert
    seed : int, optional
        Seed for random number generator (default=None).
    f: fitness factor 
    Returns
    -------
    G : Graph

    Notes
    -----
    The initialization is a graph with with m nodes and no edges.

    References
    ----------
    .. [1] de-Solla Price Network of Scientific Publications
    """

    if m < 1 or  m >=n:
        raise nx.NetworkXError(\
              "Price network must have m>=1 and m<n, m=%d,n=%d"%(m,n))
    if seed is not None:
        random.seed(seed)

    # Add m initial nodes (m0 in barabasi-speak)
    targets, G = complete_dag(m,c)
    
    # List of existing nodes, with nodes repeated once for each adjacent edge
    repeated_nodes=[]
    # Start adding the other n-m nodes. The first node is m.
    source=m+1
    
    
    fit = [random.choice([0,1]) for n in range(len(G))]
    #extend targets 
    for n in range(len(fit)):
        if fit[n] == 1:
            repeated_nodes.extend([n]*f)
        else:
            repeated_nodes.extend([n])
    while source<n:
        # Add edges to m nodes from the source.
        G.add_edges_from(zip(targets,[source]*m))
        # Add one node to the list for each new edge just created.
        repeated_nodes.extend(targets)
        # And the new node "source" has c times  to add to the list.
        f = random.choice([0,1])
        fit.append(f)
        if f==1:
            repeated_nodes.extend([source]*c*f)
        else:
            repeated_nodes.extend([source]*c)
        # Now choose m unique nodes from the existing nodes
        # Pick uniformly from repeated_nodes (preferential attachement)
        targets = _random_subset(repeated_nodes,m)
        source += 1
    return G, fit
