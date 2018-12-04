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

"""
def _random_subset(seq,m):
""" """ Return m unique elements from seq.

This differs from random.sample which can return repeated
elements if seq holds repeated elements."""
"""
targets=set()
while len(targets)<m:
    x=random.choice(seq)
    targets.add(x)
return targets
"""
def _random_subset(seq,m):
    """ Return m non-unique elements from seq.

    This differs from random.sample which can return repeated
    elements if seq holds repeated elements.
    """
    targets=random.sample(seq,m)
    return targets


def complete_dag(n,c):
    graph = nx.DiGraph()
    list_repeated_nodes  = []
    for i in range(n):
        graph.add_node(i)
        list_repeated_nodes.extend([i]*c)
        for j in range(i+1,n):
            graph.add_edge(i,j)
            list_repeated_nodes.append(i)
                       
    
    return list_repeated_nodes, graph

def price_dag(n, m, c, seed=None):
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
    while source<n:
        # Add edges to m nodes from the source.
        G.add_edges_from(zip(targets,[source]*m))
        # Add one node to the list for each new edge just created.
        repeated_nodes.extend(targets)
        # And the new node "source" has c times  to add to the list.
        
        repeated_nodes.extend([source]*c)
        # Now choose m unique nodes from the existing nodes
        # Pick uniformly from repeated_nodes (preferential attachement)
        targets = _random_subset(repeated_nodes,m)
        source += 1
    return G
    
    
if __name__ =="__main__":

  G = price_dag(1000,3,1)
