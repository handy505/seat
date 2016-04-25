#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
from tkinter import *
import random
import math
import collections
from operator import itemgetter, attrgetter
import copy


ROW_MAX = 3
COLUMN_MAX = 3

def generate_student_table():
    """ for debug """
	# genrate student table
    s1 = Student(1, 'Ada', 160, True)
    s2 = Student(2, 'Bess', 170)
    s3 = Student(3, 'Carol', 155, True)
    s4 = Student(4, 'Dale', 175)
    s5 = Student(5, 'Eileen', 154)
    s6 = Student(6, 'Florence', 158)
    s7 = Student(7, 'Gill', 153)
    s8 = Student(8, 'Hannah', 163, True)
    s9 = Student(9, 'Irma', 168)
    st_table = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
    exclusion_table = [s1, s9]
    #for s in student_table:
    #	print(s.info()) # debug
    return st_table, exclusion_table

class Student(object):
    """ student """
    def __init__(self, number=0, name="empty", height=150, duty=False):
        self.__number = number
        self.__name = name
        self.__duty = duty
        self.__height = height

    @property
    def number(self):
        """ doc string """
        return self.__number
        
    @property
    def height(self):
        """ empty """
        return self.__height
        
    @height.setter
    def height(self, height):
        """ empty """
        self.__height = height

    @property
    def name(self):
        """ empty """
        return self.__name
        
    @name.setter
    def name(self, name):
        """ empty """
        self.__name = name

    @property
    def duty(self):
        """ empty """
        return self.__duty
        
    @duty.setter
    def duty(self, arg):
        """ empty """
        self.__duty = arg

    def info(self):
        """ empty """
        return ("#{num},{name},{duty},{height}".format(
            num=self.__number, name=self.__name, duty=self.__duty, height=self.__height)
        )


class SeatSheet(object):
    """ empty """

    __table = collections.OrderedDict()
    def __init__(self, row=ROW_MAX, column=COLUMN_MAX, students=None):
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
                        
        self.height_score()
        self.duty_score()
        
          
    @property
    def table(self):
        """ empty """
        return self.__table
        
    @table.setter
    def table(self, key, val):
        """ empty """
        self.__table[key] = val

    def calc_score(self, exclusion_table):
        """ weight adjusting """
        HEIGHT_WEIGHT = 1
        DUTY_WEIGHT = 1000
        EXCLUSION_WEIGHT = 10
        self.__hscore = self.height_score()
        self.__dscore = self.duty_score()
        self.__xscore = self.exclusion_score(exclusion_table)
        self.__score = (self.__hscore*HEIGHT_WEIGHT) + (self.__dscore*DUTY_WEIGHT) - (self.__xscore*EXCLUSION_WEIGHT)

    __score = 0        
    @property
    def score(self):
        """ empty """
        return self.__score
    
    __hscore = 0
    @property
    def hscore(self):
        return self.__hscore

    __dscore = 0
    @property
    def dscore(self):
        return self.__dscore
    
    __xscore = 0
    @property
    def xscore(self):
        return self.__xscore
                
        
        
    def info(self):
        """ infomation """
        for i in range(0, self.__row):
            for j in range(0, self.__column):
                st = self.__table[(i, j)].info() if self.__table[(i, j)] else "xxxx" 
                print(i, j, st)

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
                    beforeHeight = self.__table[(before, c)].height
                    hscore += (curHeight - beforeHeight) if beforeHeight > (curHeight + IGNORE_ERROR) else 0
                    #print("hscore:{0} at {1} scan {2}".format(hscore, (r, c), (before, c))) # debug
        return hscore

    def duty_score(self):
        """ empty """
        col_score = []
        for c in range(0, self.__column):
            rcount = 0
            for r in range(0, self.__row):
                st = self.__table[(r, c)]
                if st:
                    rcount = rcount + (1 if st.duty == True else 0)
            #print("rcount", c, ":", rcount) # debug
            col_score.append(1) if rcount >=1 else col_score.append(0)
        #self.__rscore = sum(col_score) 
        #return self.__rscore
        return sum(col_score)
        

    def __location_valid(self, loc):
        if (0 <= loc[0] < self.__row) and (0 <= loc[1] < self.__column):
            return True
        else:
            return False
    
    def exclusion_score(self, exclusion_table):
        #print("in exclusion_score", self.__row, self.__column) # debug
        xscore = 0
        xloc = (0,0)
        
        for xstudent in exclusion_table:
            for loc in self.__table:
                if self.__table[loc] and (self.__table[loc].number == xstudent.number):
                    xloc = loc
            #print("excloc:", xloc) # debug
            
            near = (xloc[0]-1, xloc[1]-1)
            if self.__location_valid(near):
                #print("--valid") # debug
                xscore = xscore + (1 if self.__table[near] in exclusion_table else 0)
                
            near = (xloc[0]-1, xloc[1])    
            if self.__location_valid(near):
                #print("-0valid") # debug
                xscore = xscore + (1 if self.__table[near] in exclusion_table else 0)
                
            near = (xloc[0]-1, xloc[1]+1)
            if self.__location_valid(near):
                #print("-+valid") # debug
                xscore = xscore + (1 if self.__table[near] in exclusion_table else 0)
                
            near = (xloc[0], xloc[1]-1)
            if self.__location_valid(near):
                #print("0-valid") # debug
                xscore = xscore + (1 if self.__table[near] in exclusion_table else 0)

            near = (xloc[0], xloc[1]+1)
            if self.__location_valid(near):
                #print("0+valid") # debug
                xscore = xscore + (1 if self.__table[near] in exclusion_table else 0)
                
            near = (xloc[0]+1, xloc[1]-1)
            if self.__location_valid(near):
                #print("+-valid") # debug
                xscore = xscore + (1 if self.__table[near] in exclusion_table else 0)
                
            near = (xloc[0]+1, xloc[1])
            if self.__location_valid(near):
                #print("+0valid") # debug
                xscore = xscore + (1 if self.__table[near] in exclusion_table else 0)
                
            near = (xloc[0]+1, xloc[1]+1)
            if self.__location_valid(near):
                #print("++valid") # debug
                xscore = xscore + (1 if self.__table[near] in exclusion_table else 0)
        #print("xscore:", xscore) # debug
        return xscore

class GUIDemo(Frame):
    __bss = SeatSheet(ROW_MAX, COLUMN_MAX)
    
    def __init__(self, master=None, seatsheet=None):
        Frame.__init__(self, master)
        self.grid()
        self.seatInfo = dict()
        self.bestSeatInfo = dict()
        
        self.create_widgets(seatsheet)
        
    def create_widgets(self, seatsheet=None):
        Label(self, text="teacher").grid(row=0, column = math.floor(COLUMN_MAX/2))
        
        # random seat table
        for r, c in seatsheet.table:
            ststr = seatsheet.table[(r, c)].info() if seatsheet.table[(r, c)] else "xx" 
            self.seatInfo[r, c] = StringVar()
            self.seatInfo[r, c].set("[{0},{1}]\n{2}\n".format(r, c, ststr))
            Label(self, textvariable=self.seatInfo[r, c]).grid(row=(r+1), column=c, padx=4, pady=4)
    
        # seat score
        self.seatScore = StringVar()
        self.seatScore.set("suit score: " + str(seatsheet.score))
        Label(self, textvariable=self.seatScore, fg="red").grid(row=1+ROW_MAX, column=0, padx=2, pady=4, columnspan=COLUMN_MAX)
        
        # manual again buttno
        Button(self, text="manual", command=self.manualAgain).grid(row=2+ROW_MAX, column=0, padx=2, pady=4)
        
        # auto loop button 
        Button(self, text="auto", command=self.autoAgain).grid(row=2+ROW_MAX, column=1, padx=2, pady=4)
        
        # best score
        self.bestSeatScore = StringVar()
        self.bestSeatScore.set("best: " + str(self.__bss.score))        
        Label(self, textvariable=self.bestSeatScore, fg="red").grid(row=3+ROW_MAX, column=0, padx=2, pady=4, columnspan=COLUMN_MAX)        

        # best table
        for r, c in self.__bss.table:
            ststr = self.__bss.table[(r, c)].info() if self.__bss.table[(r, c)] else "xx" 
            self.bestSeatInfo[r, c] = StringVar()
            self.bestSeatInfo[r, c].set("[{0},{1}]\n{2}\n".format(r, c, ststr))
            Label(self, textvariable=self.bestSeatInfo[r, c]).grid(row=(3+ROW_MAX)+(r+1), column=c, padx=4, pady=4)        
        
        
        
    def update(self, seatsheet):
        # random table
        for r, c in seatsheet.table:
            ststr = seatsheet.table[(r, c)].info() if seatsheet.table[(r, c)] else "xx"
            string = "[{0},{1}]\n{2}\n".format(r, c, ststr) 
            self.seatInfo[r, c].set(string)
            
        # random score
        scoreStr = ("best:{0}({1}, {2}, {3})".format(
                seatsheet.score, seatsheet.hscore, seatsheet.dscore, seatsheet.xscore))
        self.seatScore.set(scoreStr)
        
        # whether best
        if seatsheet.score >= self.__bss.score:
            #self.__bss = seatsheet
            self.__bss = copy.deepcopy(seatsheet)
            string = ("best:{0}({1}, {2}, {3})".format(
                self.__bss.score, self.__bss.hscore, self.__bss.dscore, self.__bss.xscore))

            self.bestSeatScore.set(string)

            # best table
            for r, c in self.__bss.table:
                stStr = self.__bss.table[(r, c)].info() if self.__bss.table[(r, c)] else "xx" 
                self.bestSeatInfo[r, c].set("[{0},{1}]\n{2}\n".format(r, c, stStr))        
            
        
    def manualAgain(self):
        ss = gererage_seat_sheet()
        self.update(ss)
    
    def autoAgain(self):
        for autoloop in range(0, 100):
            ss = gererage_seat_sheet()
            self.update(ss)
    
def gererage_seat_sheet():
    """ seat sheet include 1) student table 2) score """
    student_table, exclusion_table = generate_student_table()
    ss = SeatSheet(ROW_MAX, COLUMN_MAX, students=student_table)
    ss.calc_score(exclusion_table)
    return ss
        
if __name__ == '__main__':
    
    print("--------------- main() ---------------")
    # genrate student table
    student_table, exclusion_table = generate_student_table()

    '''# sorted
    st2 = sorted(student_table, key = attrgetter('height'))
    for s in st2:
        print(s.height) # debug
    '''

    ss = SeatSheet(ROW_MAX, COLUMN_MAX, students=student_table)
    ss.info()
    ss.calc_score(exclusion_table)

    # gui
    root = Tk()
    app = GUIDemo(master=root, seatsheet=ss)
    app.mainloop()    
