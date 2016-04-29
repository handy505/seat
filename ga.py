#!/usr/bin/env python3
#-*- coding: UTF-8 -*-

import random
import seat
import copy
import math
import student
import sys
import getopt
from operator import itemgetter, attrgetter


    
class GA(object):
    
    def __init__(self, st_table, xtable, population=10):
        self.__st_table = st_table
        self.__xtable = xtable
        self.POOLSIZE = population
        self.__pool = []
        for i in range(0, self.POOLSIZE):
            sttable = copy.deepcopy(self.__st_table) # st_table is expendables should copy another one to use
            ss = seat.SeatSheet(seat.ROW_MAX, seat.COLUMN_MAX, students=sttable, xtable=self.__xtable)
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
        min = 99999
        idxmin = 0
        for i in self.__pool:
            #print("i:", self.__pool.index(i)) # debug
            if i.score < min:
                min = i.score
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
        ss = seat.SeatSheet(seat.ROW_MAX, seat.COLUMN_MAX, students=None, xtable=self.__xtable)
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
        
        # pick 2 random student in seat sheet
        r1, c1 = (0, 0)
        r2, c2 = (0, 0)
        while (r1, c1) == (r2, c2):
            r1 = random.randint(0, ss.row-1)
            c1 = random.randint(0, ss.column-1)
            r2 = random.randint(0, ss.row-1)
            c2 = random.randint(0, ss.column-1)
        #print("[mutation...] pick 2 random student in seat sheet ({0}, {1}) , ({2}, {3})".format(r1, c1, r2, c2)) # debug
        
        st1 = ss.table[(r1, c1)]
        st2 = ss.table[(r2, c2)]
        #print("beofre mutation") # debug
        #print(ss.info())  # debug
        
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
        for i in range(0, eliminateCount):
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
        score = []
        scoreStr = ""
        for i in self.__pool:
            scoreStr += str(i.score) + " "
        string = "[GA {0}] {1}".format(self.generation, scoreStr)
        return string
        
    def average(self):
        sum = 0
        for i in self.__pool:
            sum += i.score
        return sum/len(self.__pool)

    def sd(self):
        """ standard difference """
        self.__u = self.average()
        sum = 0
        for i in self.__pool:
            sum += (i.score - self.__u) ** 2
        sd = math.sqrt( sum / len(self.__pool) )
        return sd
        
    def max(self):
        max = 0
        for i in self.__pool:
            max = i.score if i.score > max else max
        return max


def report(gaSimu, filename="ga-result.txt"):
    # write file
    gnt = gaSimu.generation
    avg = round(gaSimu.average(), 2)
    sd = round(gaSimu.sd(), 2)
    max = gaSimu.max()
    #filename = "ga-result-{0}.txt".format(gnt)
    fout = open(filename, "w", encoding="utf-8")
    fout.write("GA RESULT WITH {0} GERERATION\navg:{1}, sd:{2}, max:{3}\n\n".format(gnt, avg, sd, max))
    
    # best
    for ss in gaSimu.best:
        fout.write("seat sheet best {0} score: {1}\n".format(gaSimu.best.index(ss), ss.score))
        fout.write("------------------------------------\n")
        
        #linestr = ss.info()
        #fout.write(linestr)
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
        
        #linestr = ss.info()
        #fout.write(linestr)
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
    fout.close()        

usage = (
    "USAGE: ga.py [option] [file]\n"
    "   -h, --help: help\n"
    "   -e, --empty: generate empty student file, for modify\n"
    "   -i, --input: input <filename>\n"
    "   -o, --output: output <filename>\n"
    "   -p, --population: population size\n"
    "   -g, --generation: GA generations\n"
)
    
def main(argv):
    
    try:
        opts, args = getopt.getopt(argv, "hei:o:p:g:", ["help",  "epmty", "input=", "output=", "population=", "gereration="])
    except getopt.GetoptError:
        print('usage: ga.py [option] [file]]')
        sys.exit(2)
        
    ifile = "student.txt"
    ofile = "ga-report.txt"
    population = 10
    generation = 20
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-e", "--epmty"):
            print("generate empty file")
            student.generate_empty_student_file()
            sys.exit()
        elif opt in ("-i", "--input"):
            ifile = arg
        elif opt in ("-o", "--output"):
            ofile = arg
        elif opt in ("-p", "--population"):
            population = int(arg)
        elif opt in ("-g", "--gereration"):
            generation = int(arg)
        
    #print(ifile, ofile, population, generation)
    student_table, exclusion_table = student.import_student_file(ifile)
    gaSimu = GA(student_table, exclusion_table, population)
    avg = round(gaSimu.average(), 2)
    sd = round(gaSimu.sd(), 2)
    print(gaSimu.info(), "(average:", str(avg), "sd:", str(sd), ")")
    
    # ga generation loop
    for i in range(0, generation):
        gaSimu.next_generation()
        avg = str(round(gaSimu.average(), 2))
        avg = avg.ljust(8, " ")
        sd = str(round(gaSimu.sd(), 2))
        sd = sd.ljust(7, " ")
        print(gaSimu.info(), "(average:", avg, "sd:", sd, ")")
        

    report(gaSimu, ofile)
    
if __name__ == '__main__':    
    main(sys.argv[1:])
