# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 10:20:54 2018

@author: Vaiva
"""

def price_fields(no_nodes, no_fields,M, p,fields_uniform=True, C=1):
    """
    
    Parameters
    ----------
    field_size - relative publication frequency in a research field. Can be:
            "uniform": Uniform frequency accross the fields
            "random": Random
            "custom": custom frequencies, fed in as a list of a variable "frequencies"
    size - value related to frequency type. Can be:
            for "uniform",None
            for "random" , max and min sizes (tuple)
            for "custom" a list of relative sizes
    p - prbability for a new node to connect to nodes within
            its research field respectively        
    no_node - number of nodes in a resulting DAG
    no_field - number of fields
    M-number outward stubs for each new node
    C - number of times a node with out-degree=0 is added to PA list.
    
    Returns
    -------
    G - networkx directed acyclic graph
    fields - dictionary indicating field to which nodes belong to
    
    """
    node_multiset = []
    fields = {}
    age = {}
    #C = 10 #number of communities
    G = nx.DiGraph()
    
    outside_edges=0
    field_list = [] # preferential attachment list for fields
    for f in range(no_fields):
        field_list.append(f)
    size = {F:len([f for f in field_list if f==F] ) for F in range(no_fields)} #current size of fields
    for n in range(no_fields): #add one sink node to each field
        node_multiset.append([n])
        G.add_node(n)
        fields[n] = n
    n = n+1
    while n<no_nodes:
        G.add_node(n)
        fn = random.choice(field_list)
        fields[n] = fn
        edgelist = []
        if fields_uniform ==False:
            field_list.append(fn)

        i =0
        while i<M:
            q=  random.random()
            connected = False
            count = 0
            while connected == False:
                count +=1
                if q<= p:

                    nodelist = node_multiset[fn]
                    m = random.choice(nodelist)
                    if (m,n) not in G.edges():

                        G.add_edge(m,n)
                        edgelist.append(m)
                        i+=1
                        connected = True
                else:
                    j = random.randint(0,no_fields-1)
                    while j == fn:
                        j = random.randint(0,no_fields-1)

                    nodelist = node_multiset[j]
                    m = random.choice(nodelist)
                    if (m,n) not in G.edges():
                        outside_edges +=1
                        G.add_edge(m,n)
                        edgelist.append(m)
                        i+=1
                        connected = True
            
                if count >100:
                    break
            if count > 100:
                break
        for c in range(C):
            edgelist.append(n)
        print(n,edgelist,[fields[m] for m in edgelist],fields[n])
        for m in edgelist:
            f = fields[m]
            node_multiset[f].append(m)
        node_multiset[fn].append(n)
        n+=1
    size = {F:len([f for f in field_list if f==F] ) for F in range(no_fields)}
    for n in G:
        fn = fields[fn]
        age[n] = n/size[fn]
        
    return G,fields,age,outside_edges 
