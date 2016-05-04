#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
import random
import collections

ROW_MAX = 7
COLUMN_MAX = 7

class SeatSheet(object):
    def __init__(self, row=ROW_MAX, column=COLUMN_MAX, students=None):
        self.__table = collections.OrderedDict()
        self.__row = row
        self.__column = column
        self.__students = students
        
        for i in range(0, self.__row):
            for j in range(0, self.__column):
                if self.__students:
                    rnd = random.randint(0, len(self.__students)-1)
                    self.__table[(i, j)] = self.__students[rnd]
                    self.__students.pop(rnd)
                else:
                    self.__table[(i, j)] = None
        
        self.__score = 0
        self.__hscore = 0
        self.__dscore = 0
        self.__xscore = 0
    
    @property
    def row(self):
        return self.__row
        
    @property
    def column(self):
        return self.__column
        
    @property
    def table(self):
        return self.__table
        
    @table.setter
    def table(self, key, val):
        self.__table[key] = val

    def calc_score(self):
        """ weight adjusting """
        DUTY_WEIGHT = 1000
        EXCLUSION_WEIGHT = 100
        HEIGHT_WEIGHT = 10
        self.__hscore = self.height_score()
        self.__dscore = self.duty_score()
        self.__xscore = self.exclusion_score()
        self.__score = (self.__hscore*HEIGHT_WEIGHT) + (self.__dscore*DUTY_WEIGHT) - (self.__xscore*EXCLUSION_WEIGHT)

    @property
    def score(self):
        return self.__score
    
    @property
    def hscore(self):
        return self.__hscore
    
    @property
    def dscore(self):
        return self.__dscore
    
    @property
    def xscore(self):
        return self.__xscore
        
    def info(self):
        """ information """
        string = ""
        for i in range(0, self.__row):
            for j in range(0, self.__column):
                st = self.__table[(i, j)].info() if self.__table[(i, j)] else "xxxx" 
                #print(i, j, st)
                string += "({0}, {1}) {2}\n".format(i, j, st)
        return string
        
    def height_score(self):
        """ height score """
        IGNORE_ERROR = 0
        hscore = 0
        for r, c in self.__table:
            st = self.__table[(r, c)]

            #print("check location:{0}".format((r, c))) # debug
            if st and (r != 0):
                # valid seat
                curHeight = self.__table[(r, c)].height
                for before in range(0, r):
                    if self.__table[(before, c)]:
                        beforeHeight = self.__table[(before, c)].height
                        hscore += (curHeight - beforeHeight) if beforeHeight > (curHeight + IGNORE_ERROR) else 0
                        #print("hscore:{0} at {1} scan {2}".format(hscore, (r, c), (before, c))) # debug
        return hscore

    def duty_score(self):
        col_score = []
        for c in range(0, self.__column):
            rcount = 0
            for r in range(0, self.__row):
                st = self.__table[(r, c)]
                if st:
                    rcount = rcount + (1 if st.duty == True else 0)
            if rcount <=2:
                col_score.append(rcount) 
            else:
                col_score.append(2)
        return sum(col_score)
        
    def __location_valid(self, loc):
        x = loc[0]
        y = loc[1]
        if (0 <= x < self.__row) and (0 <= y < self.__column):
            return True
        else:
            return False
    
    def exclusion_score(self):
        xscore = 0
        xloc = (0,0)
        
        self.__xtable = []
        for st in self.__students:
            if st.exclusive:
                self.__xtable.append(st)
        
        for xstudent in self.__xtable:
            for loc in self.__table:
                if self.__table[loc] and (self.__table[loc].number == xstudent.number):
                    xloc = loc
            #print("excloc:", xloc) # debug
            
            near = (xloc[0]-1, xloc[1]-1)
            if self.__location_valid(near):
                #print("--valid") # debug
                xscore = xscore + (1 if self.__table[near] in self.__xtable else 0)
                
            near = (xloc[0]-1, xloc[1])    
            if self.__location_valid(near):
                #print("-0valid") # debug
                xscore = xscore + (1 if self.__table[near] in self.__xtable else 0)
                
            near = (xloc[0]-1, xloc[1]+1)
            if self.__location_valid(near):
                #print("-+valid") # debug
                xscore = xscore + (1 if self.__table[near] in self.__xtable else 0)
                
            near = (xloc[0], xloc[1]-1)
            if self.__location_valid(near):
                #print("0-valid") # debug
                xscore = xscore + (1 if self.__table[near] in self.__xtable else 0)

            near = (xloc[0], xloc[1]+1)
            if self.__location_valid(near):
                #print("0+valid") # debug
                xscore = xscore + (1 if self.__table[near] in self.__xtable else 0)
                
            near = (xloc[0]+1, xloc[1]-1)
            if self.__location_valid(near):
                #print("+-valid") # debug
                xscore = xscore + (1 if self.__table[near] in self.__xtable else 0)
                
            near = (xloc[0]+1, xloc[1])
            if self.__location_valid(near):
                #print("+0valid") # debug
                xscore = xscore + (1 if self.__table[near] in self.__xtable else 0)
                
            near = (xloc[0]+1, xloc[1]+1)
            if self.__location_valid(near):
                #print("++valid") # debug
                xscore = xscore + (1 if self.__table[near] in self.__xtable else 0)
        #print("xscore:", xscore) # debug
        return xscore


if __name__ == '__main__':
    pass
