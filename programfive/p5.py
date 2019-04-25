# Programming Assignment 5
#
# Don't rename any functions, although feel free to implement any helper functions
# you find useful.
#
# 1) Implement the naive_string_matcher function as specified in its docstring.
#    This is a variation of the algorithm on page 988 of the textbook.
#    Read the docstring below carefully so you know what I've changed.
#
# 2) Implement the function print_results below.
#
# 3) Implement the p_naive_string_matcher function as specified in its docstring.
#
# 4) In the time_results function below, implement any code needed to compare the runtimes
#    of the sequential and parallel version on string of varying lengths and with varying number of matches.
#    You will need to figure out how to generate strings of varying lengths.  And with a varying number of matches.
#    This is not as hard as it might seem at first.  Recall that you can use the multiplication operator * with
#    a string and an integer as follows:  "abc" * 5 will evaluate to "abcabcabcabcabc"
#
# 5) Answer the following questions here in a comment based on #4:
#
#    Q1: After running time_results, fill in this table in this comment for whatever P and T lengths
#        you tried (make sure you vary lengths from short to longer:
#        T-length   P-Length   Sequential   Parallel
#
#    Q2: How do the times (of both versions) vary by string length?  If T is held constant, and pattern P length varied, how does
#        that affect runtime?  If P length is held constant, and text T length varied, how does that affect runtimes?
#
#    Q3: At what lengths of P and/or T is the sequential version faster?
#
#    Q4: At what lengths of P and/or T is the parallel version faster?
#
#    Q5: Are the results consistent with the speedup you computed in Problem Set 4?  If not, what do you think caused
#        the inconsistency with the theoretical speedup?


# These are imports you will likely need.  Feel free to add any other imports that are necessary.
from multiprocessing import Pool
from timeit import timeit
from functools import partial

def time_results() :
    """Write any code needed to compare the timing of the sequential and parallel versions
    with a variety of string lengths.  Have this print a table of the following form:

    T-length   P-Length   SequentialTime  ParallelTime
    """
    seqtime = timeit(lambda : naive_string_matcher("abc"*5,"abc"),number=1)
    partime = timeit(lambda : p_naive_string_matcher("abc"*5,"abc"),number=1)
    print("15","3","%.4E"%seqtime,"%.4E"%partime,sep="\t")

    seqtime = timeit(lambda : naive_string_matcher("abcde"*500,"abc"),number=1)
    partime = timeit(lambda : p_naive_string_matcher("abcde"*500,"abc"),number=1)
    print("2500","3","%.4E"%seqtime,"%.4E"%partime,sep="\t")

    seqtime = timeit(lambda : naive_string_matcher("abcdefghij"*50000,"abc"),number=1)
    partime = timeit(lambda : p_naive_string_matcher("abcdefghij"*50000,"abc"),number=1)
    print("500000","3","%.4E"%seqtime,"%.4E"%partime,sep="\t")
    
    seqtime = timeit(lambda : naive_string_matcher("abcde"*3,"abcde"),number=1)
    partime = timeit(lambda : p_naive_string_matcher("abc"*3,"abcde"),number=1)
    print("15","5","%.4E"%seqtime,"%.4E"%partime,sep="\t")

    seqtime = timeit(lambda : naive_string_matcher("abcde"*500,"abcde"*100),number=1)
    partime = timeit(lambda : p_naive_string_matcher("abcde"*500,"abcde"*100),number=1)
    print("2500","500","%.4E"%seqtime,"%.4E"%partime,sep="\t")

    seqtime = timeit(lambda : naive_string_matcher("abcdefghij"*50000,"abcdefghij"*100),number=1)
    partime = timeit(lambda : p_naive_string_matcher("abcdefghij"*50000,"abcdefghij"*100),number=1)
    print("500000","1000","%.4E" % seqtime,"%.4E"%partime,sep="\t")

def print_results(L) :
    """Prints the list of indices for the matches."""
    for i in L:
        print(i,end="  ")
    print()


def naive_string_matcher(T, P) :
    """Naive string matcher algorithm from textbook page 988.

    Slight variation of the naive string matcher algorithm from
    textbook page 988.  Specifically, the textbook version prints the
    results.  This python function does not print the results.
    Instead, it generates and returns a list of the indices at the start
    of each match.  For example, if T="abcabcabc" and P="def", this function
    will return the empty list [] since the pattern doesn't appear in T.
    For that same T, if the pattern P="abc", then this function will return
    the list [0, 3, 6] since the pattern appears 3 times, beginning on indices
    0, 3, and 6.

    Keyword arguments:
    T -- the text string to search for patterns.
    P -- the pattern string.
    """
    out = list()
    for i in range(len(T)-len(P)+1):
        if list(T[i:i+len(P)]) == list(P[:]) :
            out.append(i)

    return out
    
def _index_matches(T,P,i):
    if list(T[i:i+len(P)]) == list(P):
        return i

def p_naive_string_matcher(T, P, p=4) :
    """Parallel naive string matcher algorithm from Problem Set 4.

    This function implements the parallel naive string matcher algorithm that you specified in
    Problem Set 4.  You may assume in your implementation that there are 4 processor cores.
    If you want to write this more generally, you may add a parameter to the function for number
    of processes.  If you do, don't change the order of the existing parameters, and your new parameters
    must follow, and must have default values such that if the only parameters I pass are T and P, that
    you default to 4 processes.

    Like the sequential implementation from step 1 of assignment, this function should not
    print results.  Instead, have it return a list of the indices where the matches begin.
    For example, if T="abcabcabc" and P="def", this function
    will return the empty list [] since the pattern doesn't appear in T.
    For that same T, if the pattern P="abc", then this function will return
    the list [0, 3, 6] since the pattern appears 3 times, beginning on indices
    0, 3, and 6.

    You must use Process objects (or a Pool of processes) from the multiprocessing module and not Threads from threading because
    in the next step of the assignment, you're going to investigate performance relative to the sequential
    implementation.  And due to Python's global interpreter lock, you won't see any gain if you use threads.
    I recommend using a Pool, and its map method.

    Hints related to using Pool.map: 1) You'll need a function of one argument
    to pass to Pool.map, and a list of the values for that argument.  This list can be a list of the starting indices
    to check for matches (i.e., the indices from the outer loop of the naive string matcher).  The one argument function's
    one argument can be the index to check, and can then check if a match starts at that index. 2) But wait, wouldn't that
    function need 3 arguments, T, P, and the index? Yes. Start by creating a helper function with those 3 arguments, with
    index as the last argument.  Your helper can simply return a boolean indicating whether it is a match.
    Then, look up the documentation for a function named partial in the Python module functools.
    partial takes as arguments a function and some of the arguments for it, and returns to you a function where those arguments
    will be passed by default.  E.g., you can pass your helper function, and T and P to partial, and it will return to you a
    function that you simply need to pass index (the remaining argument).  3) Your last hint.  If you follow hints 1 and 2, you'll
    end up with a list of booleans, true if that corresponding index was a match and false otherwise.  The final step would
    be to use that to generate what this string matcher is actually supposed to return.

    Keyword arguments:
    T -- the text string to search for patterns.
    P -- the pattern string.
    """
    results = list()
    hits= list()
    map_func = partial(_index_matches,T,P)
    with Pool(processes=p) as pool:
        for i in range(len(T)-len(P)+1):
            if T[i] == P[0]:
                hits.append(i)

        results = pool.map_async(map_func,hits).get()

    
    return results
