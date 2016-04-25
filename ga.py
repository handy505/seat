#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

import random
import seat

class GA(object):
    
    def __init__(self, func=None):
    
        self.__pool = []
        for i in range(0, 10):
            ss = func()
            self.__pool.append(ss)
        
    def next_generation(self):
        """ eliminate, mating, mutation  """
        self.__generation += 1
        
        # eliminating
        min = 9999
        idxmin = 0
        for i in self.__pool:
            #print("i:", self.__pool.index(i)) # debug
            if i.score < min:
                min = i.score
                idxmin = self.__pool.index(i)
        print("[eliminating...] pool[{0}] is min".format(idxmin))
        
        del self.__pool[idxmin]
        print(self.info(), "(debugging)")
        
        
        # mating ..... not complete
        rnd1 = 0
        rnd2 = 0
        while rnd1 == rnd2:
            rnd1 = random.randint(0, len(self.__pool))
            rnd2 = random.randint(0, len(self.__pool))
            
        print("[mating...] select two is {0}, {1}".format(rnd1, rnd2))
        student_table, exclusion_table = seat.generate_student_table_16()
        
        ss1 = self.__pool[rnd1]
        ss2 = self.__pool[rnd2]
        for r in range(0, seat.ROW_MAX):
            for c in range(0, seat.COLUMN_MAX):
                if ss1.table[r, c].number == ss2.table[r, c].number:
                    string = "the same in {0} {1}, {2} {3}".format(r, c, ss1.table[r, c].number, ss2.table[r, c].number)
                    print(string) 
            
        # mutation
        
        
    __generation = 0
    @property
    def generation(self):
        return self.__generation
    
    def info(self):
        score = []
        scoreStr = ""
        for i in self.__pool:
            scoreStr += str(i.score) + " "
        string = "[GA {0}] {1}".format(self.generation, scoreStr)
        return string
        
        
def rand_gen():
    rnd = random.randint(0, 10)
    print(rnd)
    return rnd
            
        
if __name__ == '__main__':
    
    print("GA unit test")
    gaSimu = GA(rand_gen)
    print(gaSimu.info())
    
    
    