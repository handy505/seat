#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
import random
import copy
import math
import sys
import getopt
from operator import itemgetter, attrgetter
from fractions import Fraction
import bisect

import seat
import student

class GeneAlgorithm(object):
    def __init__(self):
        self.students = student.student_factory('config.txt')
        self.chromosomes = [seat.SeatTable(self.students) for _ in range(8)]


    def wheel_select(self):
        reciprocals = [Fraction(1, cs.score) for cs in self.chromosomes]
        total = sum(reciprocals)
        probabilities = [float(r/total) for r in reciprocals]
        #print(probabilities)

        cdf_vals = []
        cumsum = 0
        for p in probabilities:
            cumsum += p
            cdf_vals.append(cumsum)
        #print(cdf_vals)

        x = random.random()
        idx1 = bisect.bisect(cdf_vals, x)
        idx2 = idx1
        while idx2 == idx1:
            x = random.random()
            idx2 = bisect.bisect(cdf_vals, x)
        return (self.chromosomes[idx1], self.chromosomes[idx2])


    def next(self):
        for _ in range(15):
            a, b = self.wheel_select()
            #print('a: {}, b: {}'.format(a.score, b.score))
            print('a:\n{}'.format(repr(a)))
            print('b:\n{}'.format(repr(b)))

            seat_table = seat.SeatTable(self.students, (a,b))
            print('c:\n{}'.format(repr(seat_table)))
        

    
def main():
    ga = GeneAlgorithm()

    #[print(repr(cs) + '\n') for cs in ga.chromosomes]
        
    print('----------------')
    cs2 = sorted(ga.chromosomes, key=attrgetter('score'))
    #[print(repr(cs) + '\n') for cs in cs2]
        

    ga.next()
    
    
if __name__ == '__main__':    
    main()
