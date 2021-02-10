# COMPSCI 365
# Spring 2020
# NATHAN NG
# Assignment 1

# Complete the following functions, and make
# sure to test your implementations.

import math

def sum(x, y):
    """
    Description: Return sum of x and y.
    Input: integer x, integer y
    Output: single integer = sum of x and y
    Example: sum(5, 8) = 13
    """
    return x+y

def divide(x, y, trunc=True):
    """
    Description: Return x/y, and truncate to an integer if trunc is true.
    Input: integer x, integer y, boolean trunc
    Output: single float = x/y, OR single integer = x/y
    Example: divide(3, 2, False) = 1.5; divide(3, 2) = 1
    """
    if trunc:
        return x/y
    else:
        return x//y

def equiv_val(x, y):
    """
    Description: Return true IFF x and y are equal in value; false otherwise.
    Input: object x, object y
    Output: single boolean
    Example: equiv_val("a", "A") = False; equiv_val("a", "a") = True
    """
    return x==y

def equiv_mem(x, y):
    """
    Description: Return true IFF x and y point to the same object in memory; false otherwise.
    Input: object x, object y
    Output: single boolean
    Example: equiv_mem(x, x) = True
    """
    return x is y

def concat(a, b):
    """
    Description: Return strings a and b joined by a space.
    Input: string a, string b
    Output: single string
    Example: concat("abc", "xy") = "abc xy"
    """
    return a + ' ' + b

def listinfo(x):
    """
    Description: Return a 3-tuple containing the first, last, and middle elements (in that order) in x.
    Input: list x; n(x) >= 3, and n(x) is odd
    Output: 3-tuple (object, object, object)
    Example: listinfo([1, 2, 3, 4, 5]) = (1, 5, 3)
    """
    return (x[0], x[len(x)-1], x[int((len(x)-1)/2)])
    

def mlast(x, m):
    """
    Description: Return the last m elements of x.
    Input: list x, integer m; assume n(x) >= m
    Output: list
    Example: mlast([1, 2, 3, 4], 2) = [3, 4]
    """
    theList = []
    if m > len(x):
        for i in range(0,len(x)):
            theList.append(x[i])
    else:
        for i in range(len(x)-m,len(x)):
            theList.append(x[i])
    return theList

def summation(x):
    """
    Description: Return the sum of all numbers in x; error if a non-number is encountered.
    Input: list x
    Output: number
    Example: summation([1, 2, 3.5]) = 6.5; summation([1, "a", 2]) -> TypeError
    """
    theSum = 0
    for i in x:
        theSum += i
    return theSum

def oddlist(x):
    """
    Description: Return true IFF all elements in x are odd numbers; return false otherwise
    Input: list x
    Output: boolean
    Example: oddlist([1, 3, 5]) = True; oddlist([1, 3, "a"]) = False
    """
    for i in x:
        if isinstance(i, int):
            if i % 2 == 0:
                return False
        else:
            return False
    return True


def lookup(d, k):
    """
    Description: Return the key k's associated value IFF k is in the dictionary d; return false otherwise
    Input: dictionary d, object k
    Output: object OR boolean
    Example: lookup({"a": 1, "b": 5}, "b") = 5; lookup({"a": 1, "b": 5}, "c") = False
    """
    if k in d:
        return d[k]
    else:
        return False

def factorialdict(n):
    """
    Description: Return a dictionary d containing the first n factorials from 0, such that d[n] = n!
    Input: integer n
    Output: dictionary of format {integer: integer}
    Example: factorialdict(1) = {0: 1}; factorialdict(4) = {0: 1, 1: 1, 2: 2, 3: 6}
    """
    theDict= {}
    start = 0
    while start < n:
        theDict[start] = math.factorial(start)
        start+=1
    return theDict

def read_numbers():
    """
    Description: Read and return the contents of numbers.txt as a string.
    Output: string
    Example: read_numbers() = "9104\n12873\n..."
    """
    File_object = open(r"numbers.txt","r")
    return File_object.read()

def list_numbers():
    """
    Description: Read and return the contents of numbers.txt as a list of numbers, where newlines indicate a new number.
    Output: list of integers
    Example: read_numbers() = [9104, 12873, ...]
    """
    File_object = open(r"numbers.txt","r")
    theObj = File_object.read().splitlines()

    theList = []
    for i in theObj:
        theList.append(int(i))
    return theList
    

def convert_bases():
    """
    Description: Read and return the contents of numbers.txt as a list of 3-tuples, where each 3-tuple is the number in three bases: (base 2, base 10, base 16)
    Output: list of 3-tuples; where each 3-tuple has integers OR strings, i.e. (number in base 2, number in base 10, number in base 16)
    NOTE: You can give the number as a base-specific integer, which Python stores with the prefix "0b" or "0x" for binary and hex, respectively; OR you can give it as a string. Both are acceptable. EX: We will evaluate "1011" and 0b1011 as the same.
    Example: convert_bases() = [(0b10001110010000, 9104, 0x2390), ("11001001001001", 12873, "3249"), ...]
    """
    File_object = open(r"numbers.txt","r")
    theObj = File_object.read().splitlines()

    theList = []
    for i in theObj:
        i = int(i)
        theList.append((bin(i), i, hex(i)))
    return theList

# print(mlast([1, 2, 3, 4], 5))



