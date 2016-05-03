#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
import sys
import random
import getopt


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
        return self.__number
        
    @property
    def height(self):
        return self.__height
        
    @height.setter
    def height(self, height):
        self.__height = height

    @property
    def name(self):
        return self.__name
        
    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def duty(self):
        return self.__duty
        
    @duty.setter
    def duty(self, arg):
        self.__duty = arg

    def info(self):
        """ empty """
        dutyStr = "du" if self.__duty else "nd"
        excStr = "xc" if self.__exclusive else "nx"
        return ("#{num},{name},{height},{duty},{exc}".format(
            num=self.__number, name=self.__name, height=self.__height, duty=dutyStr, exc=excStr)
        )

def generate_empty_student_file(filename="student.txt"):
    fout = open(filename, "w", encoding="utf-8")
    fout.write("# STUDENT LIST\n\n")
    for i in range(0, 49):
        h = random.randint(150, 180)
        string = "{num}, {name}, {height}, {duty}, {x}\n".format(num=i+1, name="unknow", height=h, duty="nduty", x="nexc")
        fout.write(string)
    fout.close()    


def import_student_file(filename="student.txt"):
    fin = open(filename, "r", encoding="utf-8")
    st_table = []
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
    return st_table

usage = (
    "USAGE: student.py"
)

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "ho:", ["help", "output="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    
    DEFAULT_OUTPUT_FILENAME = "student.txt"
    ofile = DEFAULT_OUTPUT_FILENAME
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-o", "--output"):
            ofile = arg
        
    generate_empty_student_file(filename=ofile)
        
if __name__ == '__main__':
    main(sys.argv[1:])
    