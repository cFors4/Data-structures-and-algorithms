# -*- coding: utf-8 -*-
"""
ECM1414: Data Structures and Algorithms 2018
Examples of using the provided tree functions
"""

from dsa import *

def split(L): 
    '''
    Splits a list in two around the middle. 
    
    PARAMETERS: 
    L: a list of items
    
    RETURNS: two lists L1,L2 such that len(L1)-len(L2) <= 1
    '''
    
    L1 = []
    L2 = L
    while len(L1) < len(L2): 
        L1 = conc( L1, [head(L2)] )
        L2 = tail(L2)
    return L1,L2

def split_tree(L): 
    '''
    Builds a binary tree according to the split function, as when using it for, eg, binary search or insertion. 
    
    PARAMETERS: 
    L: a list of items
    
    RETURNS: a tree of all splits. 
    '''

    T = new_tree(L, [])                 #new tree

    if not len(L) > 1:                  #L less than 1
        return T                        #return

    else: 
        L1,L2 = split(L)                # generate new lists to be added
        T = add_child(T, split_tree(L1)) #tree add child as the children being the function
        T = add_child(T, split_tree(L2))
        
        return T
    
def sum_tree(L, total=0, selected=[]): 
    '''
    Builds a sum tree from a list of numbers, as seen in class. 
    
    PARAMETERS: 
    L: a list of items
    
    RETURNS: a tree structure containing all possible sums. 
    '''
    T = new_tree(total, [], selected)
    while L:         
        T = add_child(T, sum_tree(tail(L), total+head(L), cons(head(L),selected)))
        L = tail(L)
    return T        

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
        
        
    
if __name__=='__main__': 
    print('\nEXAMPLE #1: Split Tree' )
    L = [1,2,3,4,5,6]
    print('Building split tree for list: {}'.format(L))
    T = split_tree(L)
    print('Generated tree structure: {}'.format(T))
    print('(you do not need to understand this structure, it is used by the provided tree functions)')
    print('Illustration of the tree structure:')
    print_tree(T)
    

    print('\nEXAMPLE #2: Sum Tree' )
    L = [1,2,3,4]
    print('Building sum tree for list: {}'.format(L))
    T = sum_tree( [1,2,3,4] )
    print('Generated tree structure: {}'.format(T))
    print('(you do not need to understand this structure, it is used by the provided tree functions)')
    print('Illustration of the tree structure:')
    print_tree(T)
