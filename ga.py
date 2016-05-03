#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

import random
import seat
import copy
import math
import student
import sys
import getopt
#from operator import itemgetter, attrgetter
from operator import attrgetter

    
class GA(object):
    
    def __init__(self, st_table, population=10):
        self.__st_table = st_table
        self.POOLSIZE = population
        self.__pool = []
        for _ in range(0, self.POOLSIZE):
            sttable = copy.deepcopy(self.__st_table) # st_table is expendable should copy another one to use
            ss = seat.SeatSheet(seat.ROW_MAX, seat.COLUMN_MAX, students=sttable)
            ss.calc_score()
            self.__pool.append( copy.deepcopy(ss))
        self.__generation = 0
        self.__best = []
        
    @property
    def best(self):
        return self.__best
        
    @property
    def pool(self):
        return self.__pool
        
    def __eliminating(self):
        min_score = 99999
        idxmin = 0
        for i in self.__pool:
            #print("i:", self.__pool.index(i)) # debug
            if i.score < min_score:
                min_score = i.score
                idxmin = self.__pool.index(i)
        #print("[eliminating...] pool[{0}] is min".format(idxmin)) # debug
        
        del self.__pool[idxmin]
        #print(self.info(), "(after del)") # debug
        
    def __crossover(self):
        # pick 2 random elements in pool
        rnd1 = 0
        rnd2 = 0
        while rnd1 == rnd2:
            rnd1 = random.randint(0, len(self.__pool)-1)
            rnd2 = random.randint(0, len(self.__pool)-1)
        student_table = copy.deepcopy(self.__st_table)
        #ss = seat.SeatSheet(seat.ROW_MAX, seat.COLUMN_MAX, students=None, xtable=self.__xtable)
        #ss = seat.SeatSheet(seat.ROW_MAX, seat.COLUMN_MAX, students=None)
        ss = seat.SeatSheet(seat.ROW_MAX, seat.COLUMN_MAX, students=student_table)
        for x in ss.table:
            x = None
        #print(ss.info()) #debug        
        
        # copy the same student in sheetA and sheetB to new sheet
        ss1 = self.__pool[rnd1]
        ss2 = self.__pool[rnd2]
        for r in range(0, ss.row):
            for c in range(0, ss.column):
                st1 = ss1.table[r, c]
                st2 = ss2.table[r, c]
                
                try:
                    if type(st1) == 'Student' and type(st2) == 'Student':
                        if st1.number == st2.number:
                            #string = "the same in {0} {1}, {2} {3}".format(r, c, st1.info(), st2.info()) # debug
                            #print(string) # debug
                            
                            # find index of the same student in student_table
                            for x in student_table:
                                if x.number == st1.number:
                                    idx = student_table.index(x)
                            ss.table[(r, c)] = copy.deepcopy(student_table[idx])
                            del student_table[idx]
                except AttributeError as err:
                    print(err)
        #print("after copy the same student in sheetA and sheetB to new sheet") # debug
        #print(ss.info()) # debug

        # fill students to the other empty seats by ranodm, new sheet complete
        for r in range(0, seat.ROW_MAX):
            for c in range(0, seat.COLUMN_MAX):
                if ss.table[(r, c)] == None:
                    if student_table:
                        rnd = random.randint(0, len(student_table)-1) 
                        ss.table[(r, c)] = student_table[rnd]
                        del student_table[rnd]
        #print("after fill students to the other empty seats by ranodm, new sheet complete") # debug
        #print(ss.info()) # debug
        return ss
    
    def __mutation(self, ss=None):
        """" pick 2 random student and swap both """
        r1, c1 = (0, 0)
        r2, c2 = (0, 0)
        while (r1, c1) == (r2, c2):
            r1 = random.randint(0, ss.row-1)
            c1 = random.randint(0, ss.column-1)
            r2 = random.randint(0, ss.row-1)
            c2 = random.randint(0, ss.column-1)
        #print("[mutation...] pick 2 random student in seat sheet ({0}, {1}) , ({2}, {3})".format(r1, c1, r2, c2)) # debug
        #print("beofre mutation") # debug
        #print(ss.info())  # debug
        
        # swap two students
        (ss.table[(r2, c2)], ss.table[(r1, c1)]) = (ss.table[(r1, c1)], ss.table[(r2, c2)]) 
        #print("after mutation") # debug
        #print(ss.info()) # debug
        return ss
        
    def next_generation(self):
        """ crossover, mutation  """
        self.__generation += 1
        
        # 1) crossover
        #print("before eliminate, pool size:", len(self.__pool)) # debug
        ELIMINATE_RETE = 0.2
        eliminateCount = round(len(self.__pool) * ELIMINATE_RETE) 
        for _ in range(0, eliminateCount):
            self.__eliminating()
        #print("after eliminate, pool size:", len(self.__pool)) # debug
        
        # 2) mating and mutation
        while len(self.__pool) < self.POOLSIZE:
            #print("before mutaton, pool size:", len(self.__pool)) # debug
            ss = self.__crossover()
            # mutation
            ss = self.__mutation(ss)
            ss.calc_score()
            self.__pool.append(ss)
            #print("new ss score:", ss.score) # debug
            #print("after mutaton, pool size:", len(self.__pool)) # debug
            
        
            self.__best.append(ss)
            self.__best = sorted(self.__best, key=attrgetter('score'), reverse=True)
                
            while len(self.__best) > 10:
                del self.__best[-1]

       
    @property
    def generation(self):
        return self.__generation
    
    def info(self):
        scoreStr = ""
        for i in self.__pool:
            scoreStr += str(i.score) + " "
        string = "[GA {0}] {1}".format(self.generation, scoreStr)
        return string
        
    def average(self):
        sum_score = 0
        for i in self.__pool:
            sum_score += i.score
        return sum_score/len(self.__pool)

    def sd(self):
        """ standard difference """
        self.__mean = self.average()
        sum_score = 0
        for i in self.__pool:
            sum_score += (i.score - self.__mean) ** 2
        sd = math.sqrt( sum_score / len(self.__pool) )
        return sd
        
    def max(self):
        max_score = 0
        for i in self.__pool:
            max_score = i.score if i.score > max_score else max_score
        return max_score


def report(gaSimu, filename="ga-result.txt"):
    # write file
    gnt = gaSimu.generation
    avg = round(gaSimu.average(), 2)
    sd = round(gaSimu.sd(), 2)
    max_score = gaSimu.max()
    #filename = "ga-result-{0}.txt".format(gnt)
    fout = open(filename, "w", encoding="utf-8")
    fout.write("GA RESULT WITH {0} GERERATION\navg:{1}, sd:{2}, max:{3}\n\n".format(gnt, avg, sd, max_score))
    
    # best
    for ss in gaSimu.best:
        fout.write("seat sheet best {0} score: {1}\n".format(gaSimu.best.index(ss), ss.score))
        fout.write("------------------------------------\n")
        
        FIELD_WIDTH = 23
        for r in range(0, ss.row):
            for c in range(0, ss.column):
                string = "({0}, {1}) ".format(r, c)
                fout.write( string.ljust(FIELD_WIDTH, " ") )
            fout.write("\n")
            for c in range(0, ss.column):
                string = ss.table[(r, c)].info() if ss.table[(r, c)] else ""
                fout.write( string.ljust(FIELD_WIDTH, " ") )
            fout.write("\n")
                
        fout.write("\n\n")
    
    # pool
    for ss in gaSimu.pool:
        fout.write("seat sheet score: {0}\n".format(ss.score))
        fout.write("------------------------\n")
        
        for r in range(0, ss.row):
            for c in range(0, ss.column):
                string = "({0}, {1}) ".format(r, c)
                fout.write( string.ljust(FIELD_WIDTH, " ") )
            fout.write("\n")
            for c in range(0, ss.column):
                string = ss.table[(r, c)].info() if ss.table[(r, c)] else ""
                fout.write( string.ljust(FIELD_WIDTH, " ") )
            fout.write("\n")
                
        fout.write("\n\n")
    fout.close()        

usage = (
    "USAGE: ga.py [option] [file]\n"
    "   -h, --help: help\n"
    "   -i, --input: input <filename>\n"
    "   -o, --output: output <filename>\n"
    "   -p, --population: population size\n"
    "   -g, --generation: GA generations\n"
)
    
def main(argv):
    
    try:
        opts, args = getopt.getopt(argv, "hi:o:p:g:", ["help", "input=", "output=", "population=", "generation="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
        
    DEFAULT_INPUT_FILENAME = "student.txt"
    DEFAULT_OUTPUT_FILENAME = "ga-report.txt"
    ifile = DEFAULT_INPUT_FILENAME
    ofile = DEFAULT_OUTPUT_FILENAME
    population = 10
    generation = 20
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-i", "--input"):
            ifile = arg
        elif opt in ("-o", "--output"):
            ofile = arg
        elif opt in ("-p", "--population"):
            population = int(arg)
        elif opt in ("-g", "--generation"):
            generation = int(arg)
        
    student_table = student.import_student_file(ifile)
    gaSimu = GA(student_table, population)
    
    avg = round(gaSimu.average(), 2)
    sd = round(gaSimu.sd(), 2)
    print(gaSimu.info(), "(average:", str(avg), "sd:", str(sd), ")")
    
    # GA generation loop
    for _ in range(0, generation):
        gaSimu.next_generation()
        avg = str(round(gaSimu.average(), 2))
        avg = avg.ljust(8, " ")
        sd = str(round(gaSimu.sd(), 2))
        sd = sd.ljust(7, " ")
        print(gaSimu.info(), "(average:", avg, "sd:", sd, ")")
        
    report(gaSimu, ofile)
    
if __name__ == '__main__':    
    main(sys.argv[1:])
