
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 15:27:03 2018

@author: Vaiva

Longest path antichain partition. Size scalings
"""

import networkx as nx
import random
import matplotlib.pyplot as plt
from collections import defaultdict
from alg_height import *
import numpy as np


def random_dag(n, m, seed=None):
    """Return random graph using Price cummulative advantage model. With p=0

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
    targets, G = complete_dag(m,m)

    # List of existing nodes, with nodes repeated once for each adjacent edge
    nodes=set()
    # Start adding the other n-m nodes. The first node is m.
    source=m
    while source<n:
        # Add edges to m nodes from the source.
        G.add_edges_from(zip(targets,[source]*m))
        
        # Add one node to the list for each new edge just created.
        nodes.update(targets)
        # And the new node "source" has c times  to add to the list.

        nodes.add(source)
        # Now choose m unique nodes from the existing nodes
        # Pick uniformly from repeated_nodes (preferential attachement)
        targets = _random_subset(nodes,m)
        source += 1
    return G
