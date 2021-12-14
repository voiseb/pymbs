# -*- coding: utf-8 -*-
'''
This file is part of PyMbs.

PyMbs is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

PyMbs is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with PyMbs.
If not, see <http://www.gnu.org/licenses/>.

Copyright 2011, 2012 Carsten Knoll, Christian Schubert,
                     Jens Frenkel, Sebastian Voigt
'''

'''
Created on 02.07.2009

@author: Christian Schubert
'''

import PyMbs.Symbolics as Symbolics
import numpy
import scipy


def sqrt(arg):
    return arg**0.5



def sin(arg):
    """
    calculate sine
    """
    if isinstance(arg, (int,float)):
        return scipy.sin(arg)
    else:
        return Symbolics.sin(arg)



def asin(arg):
    """
    calculate arc sine
    """
    if isinstance(arg, (int,float)):
        return scipy.arcsin(arg)
    else:
        return Symbolics.asin(arg)



def cos(arg):
    """
    calculate cosine
    """
    if isinstance(arg, (int,float)):
        return scipy.cos(arg)
    else:
        return Symbolics.cos(arg)



def acos(arg):
    """
    calculate arc cosine
    """
    if isinstance(arg, (int,float)):
        return scipy.arccos(arg)
    else:
        return Symbolics.acos(arg)



def tan(arg):
    """
    calculate tangent
    """
    if isinstance(arg, (int,float)):
        return scipy.tan(arg)
    else:
        return Symbolics.tan(arg)



def atan(arg):
    """
    calculate arc tangent
    """
    if isinstance(arg, (int,float)):
        return scipy.arctan(arg)
    else:
        return Symbolics.atan(arg)



def atan2(arg1, arg2):
    """
    calculate arc tangent with two arguments
    """
    if isinstance(arg1, (int,float)) and isinstance(arg2, (int,float)):
        return scipy.arctan2(arg1,arg2)
    else:
        return Symbolics.atan2(arg1,arg2)



def outer(arg1, arg2):
    """
    outer or dyadic product
    """
    return Symbolics.outer(arg1, arg2)



def der(arg):
    """
    Derivative
    """
    if isinstance(arg, (int,float)):
        return 0
    else:
        return Symbolics.der(arg)



def diag(vect):
    """
    PyMbs.Symbolics diagonal matrix
    """
    if (isinstance(vect, list)):
        L=len(vect)
    elif (isinstance(vect, Symbolics.Matrix)):
        assert(len(vect.shape()) == 1)
        L=vect.shape()[0]
    else:
        raise ValueError('vect should be a list or a vector (PyMbs.Symbolics.Matrix) but an %s was encountered'%str(vect.__class__))
    M=Symbolics.Matrix((L,L))
    for i in range(L):
        v = vect[i]
        M[i,i] = v
    return M



def norm(vec):
    """
    Calculate norm
    """

    if (isinstance(vec, Symbolics.zeros)):
        return 0

    assert isinstance(vec, Symbolics.Basic), "vec must be a symbolic type not a %s"%vec.__class__
    assert (vec.shape() in ((3,), (3,1))), "vec must be a 3x1 vector but has shape %s"%vec.shape()

    n = sqrt(vec[0]**2+vec[1]**2+vec[2]**2)
    if (isinstance(n, Symbolics.Basic)):
        n.simplify()

    return n



def symmetricMatrix(seq):
    """
    creates a symmetric 3x3 matrix from
    a sequence (list, tuple, Matrix)
    with 6 elements
    """

    assert isinstance(seq, (list, tuple, Symbolics.Matrix))
    M=Symbolics.Matrix([[seq[0], seq[1], seq[3]],
                        [seq[1], seq[2], seq[4]],
                        [seq[3], seq[4], seq[5]]])

    return M



def blockMatrix(elements):
    """
    generates a matrix from a given list of elements, i.e. A = blockMatrix([[A,B], [C,D]])
    """

    # Type Check
    assert isinstance(elements, list), "elements must be a list, not %s (%s)"%\
                                            (elements, elements.__class__)
    assert len(elements) > 0, "element list must not be empty"
    for i in elements:
        assert isinstance(i, list), "elements in elements must be lists, not %s (%s)"%\
                                            (i, i.__class__)
        assert len(i) > 0, "element list must not be empty"

        for a in i:
            assert isinstance(a, (Symbolics.Matrix, Symbolics.Variable, Symbolics.zeros)), \
                "only Matrices and Variables are allowed, not %s (%s)"%(a, a.__class__)
            assert len(a.shape())==2, "Elements must be matrices themselves, but %s has shape %s"%\
                                            (a, a.shape())

    # Calculate Shape
    rows = 0   # Rows
    cols = 0   # Columns
    for i in range(len(elements)):
        shape = elements[i][0].shape()
        rows += shape[0]
    for i in range(len(elements[0])):
        shape = elements[0][i].shape()
        cols += shape[1]

    # Set up Matrix
    M = Symbolics.Matrix((rows,cols))

    # Fill it
    m = 0
    for row in elements:
        n = 0
        rowCheck = (row[0].shape())[0]
        for A in row:
            # A is the current element
            shape = A.shape()
            assert rowCheck == shape[0], "Row size does not match! Expected %s but got %s"%\
                                            (rowCheck, shape[0])
            # copy it
            for i in range(shape[0]):
                for j in range(shape[1]):
                    M[m+i,n+j] = A[i,j]
            # advance to the next column
            n += shape[1]

        # After copying all elements, advance row and check columncount
        assert cols == n, "Column count does not match! Expected %s but got %s"%\
                                (cols, n)
        m += rowCheck

    # Finally check number of rows
    assert rows == m, "Row count does not match! Expected %s but got %s"%\
                            (rows, m)

    return M



def blockVector(elements):
    """
    generates a vector from a given list of elements, i.e. v = blockVector([a,b])
    """

    # Type Check
    assert isinstance(elements, list), "elements must be a list, not %s (%s)"%\
                                            (elements, elements.__class__)
    assert len(elements) > 0, "element list must not be empty"
    for a in elements:
        assert isinstance(a, (Symbolics.Matrix, Symbolics.Variable, Symbolics.zeros)), \
            "only Matrices and Variables are allowed, not %s (%s)%"(a, a.__class__)
        assert len(a.shape())==1, "Elements must be vectors themselves, but %s has shape %s"%\
                                    (a, a.shape())

    # Calculate Shape
    rows = 0   # Rows
    for i in range(len(elements)):
        shape = elements[i].shape()
        rows += shape[0]

    # Set up Matrix
    v = Symbolics.Matrix((rows,))

    # Fill it
    m = 0
    for a in elements:
        # a is the current element
        shape = a.shape()
        # copy it
        for i in range(shape[0]):
            v[m+i] = a[i]
        m += (a.shape())[0]

    # Finally check number of rows
    assert rows == m, "Row count does not match! Expected %s but got %s"%\
                            (rows, m)

    return v



# Class used for Symbolic Calculations only
def transpose(arg):
    '''
    Transpose of an expression
    '''

    if isinstance(arg, (int,float)):
        return arg
    elif isinstance(arg, Symbolics.Basic):
        return Symbolics.transpose(arg)
    else:
        raise TypeError("Type %s not supported in transpose!"%str(arg.__class__))



# Class used for Symbolic Calculations only
def skew(arg):
    '''
    w=skew(v) returns a w, such that w*p = v x p
    '''

    if isinstance(arg, Symbolics.Matrix):
        v = arg
        assert v.shape() == (3,)

        # we already know the what the skew thing is:
        return Symbolics.Matrix([[0, -v[2], v[1]],
                                 [v[2], 0, -v[0]],
                                 [-v[1], v[0], 0]])

    if (isinstance(arg, Symbolics.Basic)):
        return Symbolics.skew(arg)

    raise TypeError("skew is not defined for %s (%s)"%(arg, str(arg.__class__)))

def skew_numpy(arg):
    '''
    w=skew(v) returns a w, such that w*p = v x p
    numpy matrices only
    '''
    if isinstance(arg, numpy.matrix):
        v = arg
        assert v.shape == (3,1)

        return numpy.matrix([[0, -v[2], v[1]],
                                 [v[2], 0, -v[0]],
                                 [-v[1], v[0], 0]])



# Class used for Symbolic Calculations only
def scalar_if_possible(arg):
    '''
    Try to make the given expression scalar, i.e. if it is a matrix
    '''
    if (isinstance(arg, Symbolics.Matrix)):
        if (arg.shape() == (1,)):
            return arg[0]
        elif (arg.shape() == (1,1)):
            return arg[0,0]
    elif (isinstance(arg, Symbolics.Basic)):
        if ((arg.shape() == (1,)) or (arg.shape() == (1,1))):
            return scalar(arg)

    return arg



def vector_if_possible(arg):
    '''
    Try to make the given expression a vector, i.e. if it is a matrix
    '''
    if (isinstance(arg, numpy.matrix)):
        if (arg.shape[1] == 1):
            arg = [el[0] for el in arg.tolist()]

    return arg



def scalar(arg):
    '''
    scalar, converts an expression to a scalar
    '''

    if (isinstance(arg, (int,float))):
        return arg
    else:
        return Symbolics.scalar(arg)




# Class used for Symbolic Calculations only
def solve(A,b):
    '''
    Given Ax=b, one can write x = solve(A,b)
    '''
    return Symbolics.solve(A,b)



# Class used for Symbolic Calculations only
def element(A,row,col):
    '''
    Returns a special element from a vector/matrix
    '''
    return Symbolics.element(A,row,col)



def rotMat(angle, axis):
    # x-Axis
    if (axis in (1, 'x', 'X', 'Rx')):
        return Symbolics.Matrix([[1,           0,          0],
                       [0,  cos(angle), sin(angle)],
                       [0, -sin(angle), cos(angle)]])
    # y-Axis
    if (axis in (2, 'y', 'Y', 'Ry')):
        return Symbolics.Matrix([[cos(angle), 0, -sin(angle)],
                                 [         0, 1,           0],
                                 [sin(angle), 0,  cos(angle)]])
    # z-Axis
    if (axis in (3, 'z', 'Z', 'Rz')):
        return Symbolics.Matrix([[ cos(angle), sin(angle), 0],
                                 [-sin(angle), cos(angle), 0],
                                 [          0,          0, 1]])

    raise ValueError('axis must either be x,y or z')