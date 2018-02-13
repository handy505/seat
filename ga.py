#!/usr/bin/env python3
#-*- coding: UTF-8 -*-
import random
import seat
import copy
import math
import student
import sys
import getopt
from operator import attrgetter

class GeneAlgorithm(object):
    def __init__(self):
        self.chromosomes = []





def wheel_select(elements):
    right = 0
    left = 0
    bound = []
    for x in elements:
        left = right
        right += x.score
        bound.append((left, right))
    #print(bound)
      
    max_value = bound[-1][1]
    #print("max value:", max_value)
    
    rnd = random.randint(0, max_value-1)
    for idx, ele in enumerate(bound):
        left = ele[0]
        right = ele[1]
        if left <= rnd < right:
            return idx 

def wheel_select_inverse(elements):
    right = 0
    left = 0
    bound = []
    for x in elements:
        left = right
        right += (1/x.score)
        bound.append((left, right))
    #print(bound)
      
    max_value = bound[-1][1]
    #print("max value:", max_value)
    
    rnd = random.uniform(0, max_value)
    for idx, ele in enumerate(bound):
        left = ele[0]
        right = ele[1]
        if left <= rnd < right:
            return idx 
            
            
class GA(object):
    
    def __init__(self, st_table, population=10):
        self.__st_table = st_table
        self.POOLSIZE = population
        self.__pool = []
        for _ in range(0, self.POOLSIZE):
            sttable = copy.deepcopy(self.__st_table) # st_table is expendable should copy another one to use
            ss = seat.SeatSheet(seat.ROW_MAX, seat.COLUMN_MAX, students=sttable)
            #ss.calc_score()
            self.__pool.append( copy.deepcopy(ss))
        self.__generation = 0
        self.__best = []
        
    @property
    def best(self):
        return self.__best
        
    @property
    def pool(self):
        return self.__pool
        
    def __mutation(self, ss=None):
        """" pick 2 random student and swap both """
        r1, c1 = (0, 0)
        r2, c2 = (0, 0)
        while (r1, c1) == (r2, c2):
            r1 = random.randint(0, ss.row-1)
            c1 = random.randint(0, ss.column-1)
            r2 = random.randint(0, ss.row-1)
            c2 = random.randint(0, ss.column-1)
            
        # swap two students
        (ss.table[(r2, c2)], ss.table[(r1, c1)]) = (ss.table[(r1, c1)], ss.table[(r2, c2)]) 
        return ss
    
    def crossover_wheel(self):
        
        # prepare new student_table and seat_sheet to fill newborn seat_sheet
        student_table = copy.deepcopy(self.__st_table)
        ss = seat.SeatSheet(seat.ROW_MAX, seat.COLUMN_MAX, students=student_table)
        for x in ss.table: x = None 
        
        # pick up 2 different by wheel select
        idx1 = 0
        idx2 = 0
        while idx1 == idx2: 
            idx1 = wheel_select(self.__pool)
            idx2 = wheel_select(self.__pool)
                    
        # copy the same student in sheetA and sheetB to newborn sheet
        ss1 = self.__pool[idx1]
        ss2 = self.__pool[idx2]
        for r in range(0, ss.row):
            for c in range(0, ss.column):
                st1 = ss1.table[r, c]
                st2 = ss2.table[r, c]
                
                try:
                    if type(st1) == 'Student' and type(st2) == 'Student':
                        if st1.number == st2.number:
                            
                            # find index of the same student in student_table
                            for x in student_table:
                                if x.number == st1.number:
                                    idx = student_table.index(x)
                            ss.table[(r, c)] = copy.deepcopy(student_table[idx])
                            del student_table[idx]
                except AttributeError as err:
                    print(err)
        
        
        # fill students to the other empty seats by random, new sheet complete
        for r in range(0, seat.ROW_MAX):
            for c in range(0, seat.COLUMN_MAX):
                if ss.table[(r, c)] == None:
                    if student_table:
                        rnd = random.randint(0, len(student_table)-1) 
                        ss.table[(r, c)] = student_table[rnd]
                        del student_table[rnd]
                        
        ss = self.__mutation(ss)
        return ss

    def worst(self, pool):
        min_idx = 0
        min_score = pool[min_idx].score
        for i, e in enumerate(pool):
            #print(i, "min_score:", min_score, "e.score", e.score)
            if e.score <= min_score: 
                min_score = e.score
                min_idx = i
        return min_idx
            
    def next_generation(self):
        """ crossover, mutation  """
        self.__generation += 1
        
        # 1) crossover
        CROSSOVER_RETE = 0.4
        newborn_count = round(len(self.__pool) * CROSSOVER_RETE) 
        for _ in range(0, newborn_count):
            ss = self.crossover_wheel()
            #ss.calc_score()
            self.__pool.append(ss)
            
            # best recorded
            if len(self.__best) < 3:
                self.__best.append(ss)
            else:
                idx = self.worst(self.__best)
                #print("worst idx:", idx)
                if ss.score > self.__best[idx].score:
                    del self.__best[idx]
                    self.__best.append(ss)
                    self.__best = sorted(self.__best, key=attrgetter('score'), reverse=True)
            
        
        # pick up to next generation
        new_generation = []            
        for _ in range(0, self.POOLSIZE):
            selected = wheel_select(self.__pool)
            new_generation.append(self.__pool[selected])
            del self.__pool[selected]
        self.__pool.clear()
        self.__pool.extend(new_generation)
       
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
    fout = open(filename, "w", encoding="utf-8")
    fout.write("GA RESULT WITH {0} GENERATION\n".format(gnt))
    fout.write("mean:{0}, sd:{1}\n\n".format(avg, sd))
    
    # best
    for ss in gaSimu.best:
        fout.write("best {0} score: {1}\n".format(gaSimu.best.index(ss), ss.score))
        fout.write("-------------------------\n")
        
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
