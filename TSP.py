# -*- coding: utf-8 -*-
"""
ECM1414: Data Structures and Algorithms 2018
CA: The Travelling Salesman Problem
"""

# this package is used to generate random TSP instances
from random import randint

# this package contains the functions for list, queues, stacks and trees seen in class. 
from dsa import *

# this is used for drawing the graphs
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

from pprint import pprint
from collections import deque


# uncomment the following if you are using a Jupyter Notebook and want the figures inline rather than on a separate window
#%matplotlib inline


########################
## PROVIDED FUNCTIONS 
########################

def print_tree(T, prefix='', branch='+--', increment='|  ', width=10): 
    '''
    Simple ASCII display of a tree. Each node is marked as value:label using standard
    python string conversions. 
    
    PARAMETERS: 
    T: the tree structure to print. 
    prefix: the prefix of the current lines to be printed. 
    branch: the symbols to print when a new child is printed. 
    increment: the increment to prefix when tree depth increases. 
    width: the estimated maximal length of a node text (default:10). 
    '''
    print(prefix+branch+(str(value(T))+':'+str(label(T))).ljust(width))    
    
    for c in children(T): 
        print_tree(c,prefix=prefix+increment, branch=branch, increment=increment, width=width)

def generate_problem( N, maxdist=100 ): 
    '''
    Generates a random TSP problem with N cities. 
    N: the number of cities. 
    Returns: a NxN symmetric matrix of distances between cities. 
    '''
    # generate an empty array to start
    distances = [[0 for i in range(N)] for j in range(N)]
    
    # fill with random numbers between 0 and 100
    for i in range(N): 
        for j in range(i+1,N): 
            distances[i][j] = randint(10,maxdist)
            
            # ensure symmetric distances
            distances[j][i] = distances[i][j]
            
    return distances

def plot_graph_nx(distances,path=None): 
    '''
    Display a graph using networkx and matplotlib. 
    distances: the matrix of distances between vertices. Vertices and edges are inferred from this. 
    path (optional, default: None): if provided also displays a circuit in red. 
    '''
    N = len(distances)
    
    # create the graph object using networkx
    g = nx.Graph()
    g.add_edges_from([(i,j, {'weight': distances[i][j]}) for i in range(N) for j in range(N)])
    
    # layout trying to mimic the edge weights
    # pos = nx.kamada_kawai_layout(g)
    pos = nx.spring_layout(g)
    
    # actally draw the graph
    nx.draw(g, pos, style='dashed', with_labels=True)
    
    # if a path is given, highlight it in red
    if path and len(path)>1: 
        elist = [(path[i], path[i+1]) for i in range(-1,len(path)-1)]
        nx.draw_networkx_edges(g, pos, edgelist=elist, edge_color='r')
        
    # display the graph
    plt.show()
    
########################
## COURSEWORK
########################


###### BRUTE FORCE #####
   

def build_TSP_tree(D,start):
    '''as 
    creates a search tree for all possible paths from a graph, taking an
    input the distances between cities. In this tree, each node contains a path as a list of nodes and
    the total cost of this path (ie, the sum of the costs between pairs of cities in the path). All of a
    node’s children extend this node’s path by exactly one unvisited city. For convenience, we will
    add to the cost of a leaf node the cost for travelling back to the first city. Note that the tree
    can be built with any city as the starting point as we are looking for a circuit (ie, you can start
    anywhere on a circle!).
    '''

    def construct(row, total=0, label=["c"+str(start+1)]): 
        """
        recursively builds tree by continuley creating subtrees by adding from a list previously pointed 
        to until that list is empty then unwinds acting as a base case when all n lists are all empty

        parameter row is a list that returns to previous row once empty
        parameter total keeps track of total during recursion creating the sum tree
        parameter label is the label of the node as a list ["c1"","c2","c4","c3"]

        """

        #adding new subtree
        T = new_tree(total, [], label)
        i=0

        #while row isnt empty and the label isnt too big
        while row and len(label)<=len(D[start]):  
  
            #only go to the next row and add child if not self and not previously visited before
            if head(row)!=0 and "c"+str(i+1) not in label:

                #makes it so if its the last element adds the cost for going back to begining for the cost to leaf
                if len(label)<len(D[start])-1:
                    newTotal = total+head(row)
                else:
                    begining = int(str(label[0])[1])-1
                    newTotal = total+head(row)+D[i][begining]

                #adding children to subtree recurively
                T = add_child(T, construct(D[i], newTotal, conc(label,["c"+str(i+1)])))

            #take head off row once come back from the recursion
            row = tail(row)
            i+=1

        return T

    #start row is randomly generated row of D
    T = construct(D[start])
    return T


    
def evaluate_path(path,distances):
    '''
    which evaluate the total cost of a path (distance between all
    cities in the provided order, plus the cost for coming back from the last city to the first).
    '''
    #keep running total of cost
    cost = 0

    #path indecies from ["c1"","c2","c4","c3"] to [0,1,3,2]
    pathI = list(map(lambda x: int(str(x)[1:])-1,path.copy()))
    
    #adds cost from between cities 
    for i in range(len(path)-1):

        cost+=distances[pathI[i]][pathI[i+1]]

    #adds cost for coming back from the last city to the first
    cost+=distances[pathI[-1]][pathI[0]] 

    return cost



def depth_first(tree):
    '''
    which will search the tree depth-first and return the shortest circuit (as a
    list of cities, in the order they are visited).
    
    record the number of element comparisons
    '''
    global counterd
    global node

    #for children of current node
    for child in children(tree):
   
        #if child has children go deeper
        if child[1]!=[]:
            depth_first(child)

        #if child doesnt have children
        else:
            counterd+=1             #record comparisons
            if child[0]<node[0]:    #if currnent sum of dead end is less than globally
                node = child        #node = current smallest node
    
    #parent prints on the backtrack
    return node[2]



def breadth_first(tree):
    '''
    which will search the tree breadth-first and return the shortest circuit (as
    a list of cities, in the order they are visited).

    record the number of element comparisons
    '''

    global counterb
    global node

    #create deque with tree as root node
    rootNode = tree
    Q = deque()
    Q.append(rootNode)

    current_node = []

    #while Q is not empty 
    while len(Q) != 0:
        
        #current node to analyse children is popped off Q
        current_node = Q.popleft()
    
        #for children of current node
        for child in children(current_node):

            #if child has no children go compare all children to smallest
            #becuase paths all at end of tree e.g. leaves
            if child[1]==[]:
                counterb += 1           #record comparisons
                if child[0]<node[0] :  
                    node = child

            #add sibling to queue in order of visited
            sibling = child            
            Q.append(sibling)

    return node[2]
    


###### Greedy Strategy #######


def greedySearch(tree):

    global node
    global counterg

    #if tree has children
    if tree[1]!=[]:
        #node = children subtree
        node = tree[1]

        nextClosest = []

        #for child in find smallest
        for child in children(tree):
            nextClosest.append(child[0])
            nextClosest = [min(nextClosest)]
            counterg+=1
        
        #if child is smallest go there
        for child in children(tree):
            if child[0]==min(nextClosest):
                greedySearch(child)
                break
               
    return node[0][2]



####### TESTING ###########

## n = 5,7,10
def serachdemo(n):

    global node
    global maxDistance


    ##searching algorithms
    print("Search demo","\n","n=",n)


    node = new_leaf(maxDistance)
    shortestPath = depth_first(T)
    total_length = evaluate_path(shortestPath,D)
    print("Depth first found the path",shortestPath,"at a distance of",total_length,"in",counterd,"tries")

    node = new_leaf(maxDistance)
    shortestPath = breadth_first(T)
    total_length = evaluate_path(shortestPath,D)
    print("Breadth first found the path",shortestPath,"at a distance of",total_length,"in",counterb,"tries")


    node = new_leaf(maxDistance)
    greedyPath = greedySearch(T)
    total_length = evaluate_path(greedyPath,D)
    print("Greedy search found the path",greedyPath,"at a distance of",total_length,"in",counterg,"tries")



###### 2-opt algorithm #####

def invert(L,i,j):
    #invert L between i and j
    L[i:j-1] = list(reversed(L[i:j-1]))
    return L


def opt_2(path,D):
    global countero
    #followed pseudo code 
    continuee = True
    while continuee:
        continuee = False
        for i in range(len(path)-1):       
            for j in range(i+1,len(path)-1):
                new_path = invert(path.copy(),i,j)
                countero +=1
                if evaluate_path(new_path.copy(),D)<evaluate_path(path.copy(),D):
                    path = new_path.copy()
                    continuee = True
    return path



########################
## MAIN FUNCTION
########################

if __name__=='__main__': 


    #testing
    for n in [5,7,10]:
        #geneate problem  and tree with n cities
        D = generate_problem(n)
        T = build_TSP_tree(D,random.randint(0,len(D)-1))

        #base line comparisons in searches to be less than on first comparison
        maxDistance = max(leaves(T))[0]
        node = new_leaf(maxDistance)

        #global counters for individual searches
        counterd = 0
        counterb = 0
        counterg = 0

        serachdemo(n)

    #second experiment
    yPlot1 = []
    yPlot2 = []
    Ntrees = 10

    for n in range(5,11):
        
        averageDG = 0
        averageDO = 0

        for i in range(Ntrees):
            #global counters for individual searches
            counterd = 0
            counterg = 0
            countero = 0

            #geneate problem and tree with n cities
            D = generate_problem(n)
            T = build_TSP_tree(D,random.randint(0,len(D)-1))
            maxDistance = max(leaves(T))[0]

            #search with depth
            node = new_leaf(maxDistance)
            shortestPathD = depth_first(T)
            total_lengthD = evaluate_path(shortestPathD,D)
 
            #search with greedy
            node = new_leaf(maxDistance)
            shortestPathG = greedySearch(T)
            total_lengthG = evaluate_path(shortestPathG,D)

            
            shortestPathO = opt_2(shortestPathG.copy(),D)
            total_lengthO =evaluate_path(shortestPathO,D)


            #keep track of running total of difference
            averageDG += (total_lengthG - total_lengthD)
            averageDO += (total_lengthO - total_lengthD)

        #average the difference
        yPlot1.append(averageDG/10)
        yPlot2.append(averageDO/10)

    #x axis
    xPlot = [i for i in range(5,11)]

    #plot grpah
    plt.figure(1)
    
    
    plt.plot(xPlot,yPlot1,label="Greedy Search")
    plt.plot(xPlot,yPlot2,label="opt 2",)
    plt.xlabel("N")
    plt.ylabel("AVerage difference")




    #empirical estimation

    #empty np arrays
    DataD = np.array(np.zeros((6,3)))
    DataB = np.array(np.zeros((6,3)))
    DataG = np.array(np.zeros((6,3)))

    #for 5 to 10 trees
    for n in range(5,11):
        #global counters for individual searches
        counterd = 0
        counterb = 0
        counterg = 0

        #geneate problem and tree with n cities
        D = generate_problem(n)
        T = build_TSP_tree(D,random.randint(0,len(D)-1))
        maxDistance = max(leaves(T))[0]

        #generate arrays to plot as tables
        node = new_leaf(maxDistance)
        shortestPath = depth_first(T)
        total_length = evaluate_path(shortestPath,D)

        DataD[n-5][0]=n
        DataD[n-5][1]=counterd
        DataD[n-5][2]=total_length

        node = new_leaf(maxDistance)
        shortestPath = breadth_first(T)
        total_length = evaluate_path(shortestPath,D)

        DataB[n-5][0]=n
        DataB[n-5][1]=counterb
        DataB[n-5][2]=total_length

        node = new_leaf(maxDistance)
        greedyPath = greedySearch(T)
        total_length = evaluate_path(greedyPath,D)

        DataG[n-5][0]=n
        DataG[n-5][1]=counterg
        DataG[n-5][2]=total_length

  
    fig, ax = plt.subplots(3)

    #plot 3 arrays as tables
    for i in range(len(ax)):
        # hide axes
        fig.patch.set_visible(False)
        ax[i].axis('off')
        ax[i].axis('tight')

        #column headings for table
        headings = ["N","Comparisons","Total length"]

        if i ==0:
            ax[i].set_title("Depth first")
            df = pd.DataFrame(DataD, columns=headings)
        elif i ==1:
            ax[i].set_title("Breadth first")
            df = pd.DataFrame(DataB, columns=headings)
        else:
            ax[i].set_title("Greedy search")
            df = pd.DataFrame(DataG, columns=headings)

        #create table
        ax[i].table(cellText=df.values, colLabels=df.columns, loc='center')

    #plot table
    fig.tight_layout()

    #show all plots
    plt.show()

  
    
#############TO DO
"""
COMMENT
PRINT OUT ON 3

"""