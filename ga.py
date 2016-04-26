#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

import random
import seat
import copy


class GA(object):
    
    def __init__(self, func=None):
        self.POOLSIZE = 6
        self.__pool = []
        for i in range(0, self.POOLSIZE):
            print("--------")
            ss = func()
            self.__pool.append( copy.deepcopy(ss))
            
 
        for i in range(0, self.POOLSIZE):
            print("--------")
            print("pool: " + str(self.__pool[i]))
            print(self.__pool[i].info())
        


    def __eliminating(self):
        min = 99999
        idxmin = 0
        for i in self.__pool:
            #print("i:", self.__pool.index(i)) # debug
            if i.score < min:
                min = i.score
                idxmin = self.__pool.index(i)
        print("[eliminating...] pool[{0}] is min".format(idxmin))
        
        del self.__pool[idxmin]
        print(self.info(), "(after del)")
        
    def __mating(self):
        rnd1 = 0
        rnd2 = 0
        while rnd1 == rnd2:
            rnd1 = random.randint(0, len(self.__pool)-1)
            rnd2 = random.randint(0, len(self.__pool)-1)
        print("[mating...] select two is {0}, {1}".format(rnd1, rnd2)) # debug
        
        # gererate empty seat sheet
        student_table, exclusion_table = seat.generate_student_table_16()
        ss = seat.SeatSheet(seat.ROW_MAX, seat.COLUMN_MAX, students=None, xtable=None)
        print(ss.info())        
        
        # copy the same student in sheetA and sheetB to new sheet
        ss1 = self.__pool[rnd1]
        ss2 = self.__pool[rnd2]
        for r in range(0, seat.ROW_MAX):
            for c in range(0, seat.COLUMN_MAX):
                st1 = ss1.table[r, c]
                st2 = ss2.table[r, c]
                if st1.number == st2.number:
                    string = "the same in {0} {1}, {2} {3}".format(r, c, st1.info(), st2.info())
                    print(string)
                    
                    # find index of the same student in student_table
                    for x in student_table:
                        if x.number == st1.number:
                            idx = student_table.index(x)
                    ss.table[(r, c)] = copy.deepcopy(student_table[idx])
                    del student_table[idx]
        print(ss.info()) # debug

        # fill students to the other empty seats by ranodm, new sheet complete
        for r in range(0, seat.ROW_MAX):
            for c in range(0, seat.COLUMN_MAX):
                if ss.table[(r, c)] == None:
                    rnd = random.randint(0, len(student_table)-1) 
                    ss.table[(r, c)] = student_table[rnd]
                    del student_table[rnd]
        print(ss.info()) # debug
        return ss
    
    def __mutation(self, ss=None):
        ''' not complete '''
    
    
    def next_generation(self):
        """ eliminate, mating, mutation  """
        self.__generation += 1
        
        # 1) eliminating
        self.__eliminating()
        
        
        # 2) mating ..... not complete
        
        while len(self.__pool) < self.POOLSIZE:
            print("pool len:", len(self.__pool))
            ss = self.__mating()
            # mutation
            ss = self.__mutation(ss)    
            self.__pool.append(ss)
                    
        
        
        
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
            
