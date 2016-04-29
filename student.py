#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

import sys
import random

class Student(object):
    """ student """
    def __init__(self, number=0, name="empty", height=150, duty=False, exc=False):
        self.__number = number
        self.__name = name
        self.__duty = duty
        self.__height = height
        self.__exclusive = exc
        
    @property
    def exclusive(self):
        return self.__exclusive
        
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
        dutyStr = "du" if self.__duty else "nd"
        excStr = "xc" if self.__exclusive else "nx"
        return ("#{num},{name},{height},{duty},{exc}".format(
            num=self.__number, name=self.__name, height=self.__height, duty=dutyStr, exc=excStr)
        )


def generate_student_table_9():
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

def generate_student_table_16():
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
    s9 = Student(9, 'Irma', 167)
    s10 = Student(10, 'Hugo', 166)
    s11 = Student(11, 'Ian', 165)
    s12 = Student(12, 'Jacob', 172)
    s13 = Student(13, 'Kerr', 171)
    s14 = Student(14, 'Lambert', 169)
    s15 = Student(15, 'Marcus', 178)
    s16 = Student(16, 'Nat', 177)
    
    
    st_table = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16]
    exclusion_table = [s1, s9]
    #for s in st_table:
    #	print(s.info()) # debug
    return st_table, exclusion_table



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
    s9 = Student(9, 'Irma', 167)
    
    s10 = Student(10, 'Hugo', 166)
    s11 = Student(11, 'Ian', 165)
    s12 = Student(12, 'Jacob', 172)
    s13 = Student(13, 'Kerr', 171, True)
    s14 = Student(14, 'Lambert', 169)
    s15 = Student(15, 'Marcus', 178)
    s16 = Student(16, 'Nat', 177)
    s17 = Student(17, 'Olivia', 162)
    s18 = Student(18, 'Pandora', 168)
    s19 = Student(19, 'Rebeca', 165)
    
    s20 = Student(20, 'Sandra', 160)
    s21 = Student(21, 'Tiffay', 168)
    s22 = Student(22, 'Upton', 172)
    s23 = Student(23, 'Vic', 173)
    s24 = Student(24, 'Wayne', 178)
    s25 = Student(25, 'Yale', 177)
    s26 = Student(26, 'Zachary', 175)
    s27 = Student(27, 'Victor', 166)
    s28 = Student(28, 'Wade', 165)
    s29 = Student(29, 'Uriah', 160)
    
    s30 = Student(30, 'Scott', 163)
    s31 = Student(31, 'Sean', 166)
    s32 = Student(32, 'Samuel', 169, True)
    s33 = Student(33, 'Simon', 160)
    s34 = Student(34, 'Ted', 159)
    s35 = Student(35, 'Vicky', 162)
    s36 = Student(36, 'Virginia', 164)
    s37 = Student(37, 'Vivian', 166, True)
    s38 = Student(38, 'Wallis', 161)
    s39 = Student(39, 'Veromca', 169)
    
    s40 = Student(40, 'Sheila', 163)
    s41 = Student(41, 'Sherry', 164)
    s42 = Student(42, 'Sibyl', 165)
    s43 = Student(43, 'Sophia', 173)
    s44 = Student(44, 'Spring', 175)
    s45 = Student(45, 'Truda', 163)
    s46 = Student(46, 'Ula', 165)
    s47 = Student(47, 'Claire', 169, True)
    s48 = Student(48, 'Chloe', 158)
    s49 = Student(49, 'Cora', 159)
    
    
    st_table = ([s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, 
                s11, s12, s13, s14, s15, s16, s17, s18, s19, s20,
                s21, s22, s23, s24, s25, s26, s27, s28, s29, s30,
                s31, s32, s33, s34, s35, s36, s37, s38, s39, s40,
                s41, s42, s43, s44, s45, s46, s47, s48, s49])
    exclusion_table = [s1, s9]
    #for s in st_table:
    #	print(s.info()) # debug
    return st_table, exclusion_table
    
def generate_empty_student_file(filename="student.txt"):
    fout = open(filename, "w", encoding="utf-8")
    fout.write("# STUDENT LIST\n\n")
    for i in range(0, 49):
        h = random.randint(150, 180)
        string = "{num}, {name}, {height}, {duty}, {x}\n".format(num=i+1, name="unknow", height=h, duty="nduty", x="nexc")
        fout.write(string)
        
    '''fout.write("\n# EXCLUSION LIST\n")
    fout.write("{}\n")'''
    fout.close()    

'''def import_student_file(filename="student.txt"):
    fin = open(filename, "r", encoding="utf-8")
    st_table = []
    xtable = []
    for line in fin.readlines():
    
        if line[0] in {"#", "", "\n"}: 
            continue
        elif line[0] == "{":
            line = line.strip("\n")
            lst = line.split(",")
            for s in lst: 
                s = s.strip(" {}")
                if(s.isdecimal()): 
                    for st in st_table:
                        if s == st.number:
                            xtable.append(st)
        else:
            line = line.strip("\n")
            #print(line)
            
            tp = line.split(",")
            num = tp[0].strip(" ")
            name = tp[1].strip(" ")
            height = tp[2].strip(" ")
            duty = True if tp[3].strip(" ") == "True" else False
            st = Student(int(num), name, int(height), duty)
            st_table.append(st)
    fin.close()
    
    #for st in st_table: print(st.info())
    #print(xtable)
    return st_table, xtable
'''

def import_student_file(filename="student.txt"):
    fin = open(filename, "r", encoding="utf-8")
    st_table = []
    xtable = []
    for line in fin.readlines():
    
        if line[0] in {"#", "", "\n"}: 
            continue
        else:
            line = line.strip("\n")
            #print(line)
            
            tp = line.split(",")
            num = tp[0].strip(" ")
            name = tp[1].strip(" ")
            height = tp[2].strip(" ")
            duty = True if tp[3].strip(" ") == "duty" else False
            exc = True if tp[4].strip(" ") == "exc" else False
            st = Student(int(num), name, int(height), duty, exc)
            st_table.append(st)
    fin.close()
    
    #for st in st_table: print(st.info())
    #print(xtable)
    return st_table




if __name__ == '__main__':
    
    pass
    