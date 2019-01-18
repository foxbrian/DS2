#!/usr/bin/python
#Brian Fox

import random
from math import floor

def is_sorted(A) :
    """Returns True if A is sorted in non-decreasing order,
    and returns False if A is not sorted.

    Keyword arguments:
    A - a Python list.
    """
    last = A[0]
    for element in A:
        if element >= last:
            last=element
        else:
            return False
    return True
    

def random_list(length, low_value=0, high_value=100) :
    """Generates and returns a Python list of random integer values.
    The integers in the list are generated uniformly at random from
    the interval [low_value, high_value].

    Keyword arguments:
    length - the length of the list.
    low_value - the lower bound for the random integers.
    high_value - the upper bound for the random integers.
    """

    return [random.randrange(low_value,high_value) for i in range(length)]

def insertion_sort(A) :
    """Implementation of the insertion sort algorithm
    as specified on page 18 of the textbook.

    Keyword arguments:
    A - a Python list.
    """
    
    for i in range(1,len(A)):
        element = A[i]
        for j in range(i-1,-1,-1):
            if element<A[j]:
                A[j+1],A[j]=A[j],A[j+1]
            else:
                break

    return A

def merge_sort(A) :
    """Implementation of the mergesort algorithm.

    Keyword arguments:
    A - a Python list.
    """
    
    _merge_sort(A,0,len(A)-1)
    return A


def _merge_sort(A, p, r) :
    """The mergesort algorithm as specified on page 34 of the textbook.

    Keyword arguments:
    A - a Python list
    p - left most index of portion of list to sort
    r - the right most index of portion of list to sort
    """
    
    if(p<r):
        q = floor((p+r)/2)
        _merge_sort(A,p,q)
        _merge_sort(A,q+1,r)
        _merge(A,p,q,r)


def _merge(A, p, q, r) :
    """The merge operation for mergesort, as specified on page 31
    of the textbook.

    Keyword arguments:
    A - a Python list
    p - left most index of left sublist
    q - right most index of left sublist
    r - right most index of right sublist
    """

    L = A[p:q+1]
    R = A[q+1:r+1]

    i,j,k=0,0,0

    while i<len(L) and j<len(R):
        if L[i]<R[j]:
            A[p+k] = L[i]
            i = i+1
        else:
            A[p+k] = R[j]
            j = j+1
        k=k+1
    while i<len(L):
        A[p+k] = L[i]
        i=i+1
        k=k+1
    while k<len(R):
        A[p+k] = R[j]
        j=j+1
        k=k+1
    
if __name__ == "__main__" :

    #1)
    A = [1,2,3,4,5,6,7]
    print("Expecting True:"," "," ")
    print(is_sorted(A))
    A = [1,4,3,4,5,6,7]
    print("Expecting False:"," "," ")
    print(is_sorted(A))
    A = [1,2,3,4,5,6,5]
    print("Expecting False: "," "," ")
    print(is_sorted(A))
    
    #2)
    print("testing insertion sort on 1000 random lists")
    for b in [is_sorted(insertion_sort(random_list(100))) for i in range(1000)]:
        if not b:
            print("failed")
            break
    else:
        print("passed")
    
    #3)
    print("testing merge sort on 1000 random lists")
    for b in [is_sorted(merge_sort(random_list(100))) for i in range(1000)]:
        if not b:
            print("failed")
            break
    else:
        print("passed")

