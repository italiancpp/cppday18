#!python
#cython: language_level=3

from libcpp.vector cimport vector
from libcpp cimport bool as CBOOL

import cython

from copy import copy

cdef extern from "Rule.hpp" namespace "GoL":
    cdef cppclass Rule[T]:
        Rule() except +
        Rule(vector[size_t]&, vector[size_t]&)
        T apply(size_t, T)
        vector[size_t] getBirth() const
        vector[size_t] getStay() const

cdef class PyRule:
    cdef Rule[CBOOL] c_rule      # hold a C++ instance which we're wrapping
    def __cinit__(self, B, S):
        cdef vector[size_t] cB, cS;
        for b in B:
            cB.push_back(b)
        for s in S:
            cS.push_back(s)
        self.c_rule = Rule[CBOOL](cB, cS)
    def __init__(self, B, S):
        pass
    def apply(self, full_slots, state):
        return self.c_rule.apply(full_slots, bool(state))
    def getBirth(self):
        return set(self.c_rule.getBirth())
    def getStay(self):
        return set(self.c_rule.getStay())
    def __copy__(self):
        return PyRule(self.getBirth(), self.getStay())


cdef extern from "GoLEngine.hpp" namespace "GoL":
    cdef cppclass GoLEngine[T]:
        GoLEngine() except +
        GoLEngine(size_t, size_t, Rule[T] &)
        void setRule(Rule[T] &)
        void run(size_t)
        #Rule[T] getRule() const
        T get(int, int) const
        void set(size_t, size_t, T)
        void reset()
        unsigned long long int getGen() const
        size_t getXMax() const
        size_t getYMax() const

cdef class PyGoLEngine:
    cdef GoLEngine[CBOOL] c_gol
    cdef PyRule pyruleobj
    cdef size_t _x
    cdef size_t _y
    def __cinit__(self, max_x, max_y, PyRule rule):
        self.c_gol = GoLEngine[CBOOL](max_x, max_y, rule.c_rule)
    def __init__(self, max_x, max_y, PyRule rule):
        self.pyruleobj = copy(rule)
    def setRule(self, PyRule rule):
        self.pyruleobj = copy(rule)
        self.c_gol.setRule(rule.c_rule)
    def run(self, n=1):
        self.c_gol.run(n)
    def getRule(self):
        return self.pyruleobj
    def get(self, x, y):
        return bool(self.c_gol.get(x,y))
    def set(self, x, y, state):
        self.c_gol.set(x, y, <CBOOL>state)
    def reset(self):
        self.c_gol.reset()
    def getGen(self):
        return self.c_gol.getGen()
    def getXMax(self):
        return self.c_gol.getXMax()
    def getYMax(self):
        return self.c_gol.getYMax()

