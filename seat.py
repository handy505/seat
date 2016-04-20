#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
from tkinter import *
import random
import math
import collections
from operator import itemgetter, attrgetter

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
    def __init__(self, number=0, name="empty", height=150, responsibility=False):
        self.__number = number
        self.__name = name
        self.__responsibility = responsibility
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
    def responsibility(self):
        """ empty """
        return self.__responsibility
    @responsibility.setter
    def responsibility(self, arg):
        """ empty """
        self.__responsibility = arg

    def info(self):
        """ empty """
        return "#" + str(self.__number) + "," + self.__name + "," + str(self.__responsibility) + "," + str(self.__height)


def distance(a, b):
    """ empty """
    return math.hypot(abs(a[0] - b[0]), abs(a[1] - b[1]))


class SeatSheet(object):
    """ empty """
    def __init__(self, row=ROW_MAX, column=COLUMN_MAX, students=None):
        self.__score = 0
        self.__row = row
        self.__column = column
        self.__table = collections.OrderedDict()
        self.__students = students
        if self.__students:
            for i in range(0, self.__row):
                for j in range(0, self.__column):
                    if students:
                        rnd = random.randint(0, len(students)-1)
                        self.__table[(i, j)] = students[rnd]
                        students.pop(rnd)
                    else:
                        self.__table[(i, j)] = None

    @property
    def table(self):
        """ empty """
        return self.__table
    @table.setter
    def table(self, k, val):
        """ empty """
        self.__table[k] = val


    @property
    def score(self):
        """ empty """
        self.__score = self.__hscore + self.__rscore
        return self.__score


    def info(self):
        """ infomation """
        for i in range(0, self.__row):
            for j in range(0, self.__column):
                st = self.__table[(i, j)].info() if self.__table[(i, j)] else "xxxx" 
                print(i, j, st)

    def height_score(self):
        """ height score """
        score = []
        for i in range(0, self.__row):
            for j in range(0, self.__column):
                st = self.__table[(i, j)]
                if st:
                    score.append(st.height * distance((i, j), (0, self.__column/2)))
        #print(score) # debug
        self.__hscore = sum(score)
        return self.__hscore

    def responsibility_score(self):
        """ empty """
        col_score = []
        for c in range(0, self.__column):
            rcount = 0
            for r in range(0, self.__row):
                st = self.__table[(r, c)]
                if st:
                    rcount = rcount + (1 if st.responsibility == True else 0)
            #print("rcount", c, ":", rcount) # debug
            col_score.append(1000) if rcount >=1 else col_score.append(0)
        self.__rscore = sum(col_score) 
        return self.__rscore


    def __location_valid(self, tp):
        if (0 <= tp[0] < self.__row) and (0 <= tp[1] < self.__column):
            return True
        else:
            return False
    
    def exclusion_score(self, exclusion_table):
        print("in exclusion_score", self.__row, self.__column)
        ex = (0,0)
        for loc in self.__table:
            if self.__table[loc].number == exclusion_table[0].number:
                ex = loc
        print("excloc:", ex) 
        if self.__location_valid((ex[0]-1, ex[1]-1)):
            print("--valid")
        if self.__location_valid((ex[0]-1, ex[1])):
            print("-0valid")
        if self.__location_valid((ex[0]-1, ex[1]+1)):
            print("-+valid")
        if self.__location_valid((ex[0], ex[1]-1)):
            print("0-valid")
        if self.__location_valid((ex[0], ex[1])):
            print("00valid")
        if self.__location_valid((ex[0], ex[1]+1)):
            print("0+valid")
        if self.__location_valid((ex[0]+1, ex[1]-1)):
            print("+-valid")
        if self.__location_valid((ex[0]+1, ex[1])):
            print("+0valid")
        if self.__location_valid((ex[0]+1, ex[1]+1)):
            print("++valid")
        
                

if __name__ == '__main__':
    for loop in range(0, 4):
        # genrate student table
        student_table, exclusion_table = generate_student_table()


        '''# sorted
        st2 = sorted(student_table, key = attrgetter('height'))
        for s in st2:
            print(s.height) # debug
        '''


        ss = SeatSheet(ROW_MAX, COLUMN_MAX, students=student_table)
        ss.info()
        #print(ss.height_score())
        #print(ss.responsibility_score())
        ss.exclusion_score(exclusion_table)



    # gui
    root = Tk()
    frame = Frame(root)
    frame.pack()

    Label(frame, text="teacher").grid(row=0, column = round(COLUMN_MAX/2)-1)

    for r in range(0, ROW_MAX):
        for c in range(0, COLUMN_MAX):
            st = ss.table[(r, c)].info() if ss.table[(r, c)] else "xx" 
            seatInfo = "["+str(r)+str(c)+"]\n" + st + "\n\n"
            Label(frame, text=seatInfo).grid(row=(r+1), column=c)

    root.mainloop()
