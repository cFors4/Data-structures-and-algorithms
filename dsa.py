# for random number generation
import random

#################
# list methods
#################

def head(L): 
    '''
    Returns the first element of the list L (or None if L is empty). 
    '''
    if L:
        return L[0]
    else: 
        return None

def tail(L): 
	'''
	Returns the list L without its first element. 
	'''
	return L[1:]

def empty(L): 
	'''
	Checks whether the list L is empty or not. 
	'''
	return len(L) == 0

def cons(e,L): 
	'''
	Adds element e to the front of the list L. 
	'''
	return [e] + L

def conc(L1,L2): 
	'''
	Concatenates the two lists L1 and L2 (in this order).
	'''
	return L1 + L2

#################
# stack methods
#################
def top(S): 
	'''
	Returns the top element of the stack. 
	'''
	return head(S)

def pop(S):
	'''
	Removes the top element of the stack.
	'''
	return tail(S)

def push(e,S): 
	'''
	Adds element e on the top of the stack S.
	'''
	return cons(e,S)

#################
# queue methods
#################
def enqueue(e,Q): 
	'''
	Adds element e at the back of the queue Q.
	'''
	return Q+[e]

def dequeue(Q):
	'''
	Removes the first element from a queue.
	'''
	return tail(Q)

# also use head(Q) to get the next element in the queue.

################################
# tree access functions
################################

def new_tree(element, children_list, label=None): 
    '''
    Creates a new tree node, with the specified value and children. 
    '''
    return (element, children_list, label)

def new_leaf(element, label=None):
    ''' 
    Creates a new leaf node with the specified value. 
    (a label can optionally be provided)
    '''
    return new_tree(element, [], label)    

def value(T): 
    '''
    Returns the value of a node. 
    If a tree is provided, returns the value of the root node. 
    '''
    if T: return T[0]
    else: return None

def children(T):
    '''
    Returns a list of children for a node
    '''
    if(T): return T[1] 
    else: return None
    
def label(T): 
    '''
    Returns the label of a node 
    (this can be used optionally to store additional information in your tree)
    '''
    if(T): return T[2] 
    else: return None

def add_child(T,C): 
    ''' 
    Adds a new child to a node. 
    '''
    if children(T): 
        return new_tree(value(T), children(T) + [C], label(T))
    else: 
        return new_tree(value(T), [C], label(T))
    
def count_tree_nodes(T): 
    '''
    Count the number of nodes in a tree.
    '''
    nb = 1
    for c in children(T): 
        nb+=count_tree_nodes(c)
    return nb

def leaves(T): 
    '''
    Return all leaf nodes of T.
    '''
    if not children(T): 
        return [T]
    else:
        L = []
        for c in children(T): 
            L += leaves(c)
            
    return L

def count_leaves(T): 
    '''
    Return the number of leaf nodes of T. 
    '''
    return len(leaves(T))
