#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
import random
import copy
from operator import itemgetter, attrgetter
from fractions import Fraction
import bisect

import seat
import student

class GeneAlgorithm(object):
    def __init__(self):
        self.students = student.student_factory('config.txt')
        self.chromosomes = [seat.SeatTable(self.students) for _ in range(8)]
        self.chromosomes.sort(key=attrgetter('score'))


    def wheel_select(self):
        reciprocals = [Fraction(1, cs.score) for cs in self.chromosomes]
        total = sum(reciprocals)
        probabilities = [float(r/total) for r in reciprocals]

        cdf_vals = []
        cumsum = 0
        for p in probabilities:
            cumsum += p
            cdf_vals.append(cumsum)

        x = random.random()
        idx1 = bisect.bisect(cdf_vals, x)
        idx2 = idx1
        while idx2 == idx1:
            x = random.random()
            idx2 = bisect.bisect(cdf_vals, x)
        return (self.chromosomes[idx1], self.chromosomes[idx2])


    def next(self):
        a, b = self.wheel_select()
        seat_table = seat.SeatTable(self.students, (a,b))
    
        keys = [cs.score for cs in self.chromosomes]
        idx = bisect.bisect(keys, seat_table.score)
        self.chromosomes.insert(idx, seat_table)
        self.chromosomes.pop()
        

    def report(self):
        for cs in self.chromosomes:
            print(repr(cs))

    
def main():
    ga = GeneAlgorithm()

    for _ in range(300):
        ga.next()

    ga.report()
    
    
if __name__ == '__main__':    
    main()
