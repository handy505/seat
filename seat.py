#!/usr/bin/python
#-*- coding: UTF-8 -*-
from tkinter import *
import random
import math
import collections
from operator import itemgetter, attrgetter 


ROW_MAX = 3
COLUMN_MAX = 3	

def generate_student_table():
	# genrate student table
	s1 = Student(1, 'Ada', 160, True)
	s2 = Student(2, 'Bess', 170)
	s3 = Student(3, 'Carol', 155, True)
	s4 = Student(4, 'Dale', 175)
	s5 = Student(5, 'Eileen ', 154)
	s6 = Student(6, 'Florence ', 158)
	s7 = Student(7, 'Gill', 153)
	s8 = Student(8, 'Hannah', 163, True)
	s9 = Student(9, 'Irma', 168)
	student_table = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
	#for s in student_table:
	#	print(s.info()) # debug 
	return student_table


def distance(a, b):
	return math.hypot(abs(a[0] - b[0]), abs(a[1] - b[1]))
	
	
def height_score(seattable):
	score = []
	for i in range(0, ROW_MAX):
		for j in range(0, COLUMN_MAX):
			st = seattable[(i,j)]
			#score.append(st.height * i)
			score.append(st.height * distance((i,j), (0, COLUMN_MAX/2)))
	#print(score) # debug
	return sum(score)


def responsibility_score(seattable):
	col_score = []
	for c in range(0, COLUMN_MAX):
		rcount = 0
		for r in range(0, ROW_MAX):
			st = seattable[(r,c)]
			rcount = rcount + (1 if st.responsibility == True else 0)
		print("rcount", c, ":", rcount) # debug
		col_score.append(1000) if rcount >=1 else col_score.append(0)
	return sum(col_score)
	

def print_seat_table():
	for i in range(0, ROW_MAX):
		for j in range(0, COLUMN_MAX):	
			s = seat_table[(i,j)]
			print(i, j, s.info())
			
class SeatTableObj:
	def __init__(self, row=ROW_MAX, column=COLUMN_MAX, students=[]):
		self.__score = 0
		self.__students = students
		self.__row = row
		self.__column = column
		self.dct = collections.OrderedDict()
	
	'''	
	@property
	def dct(self):
		return self.__dct'''

	
	@property
	def score(self):
		return self.__score
	@score.setter
	def score(self, arg):
		self.__score = arg
		
	'''	
	def info(self):
		for i in range(0, __row):
			for j in range(0, __column):	
				s = self.__content[(i,j)]
				print(i, j, s.info())'''
	
class Student:
	def __init__(self, number=0, name="empty", height=150, responsibility=False):
		self.__number = number
		self.__name = name
		self.__responsibility = responsibility
		self.__height = height
	
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
	def responsibility(self):
		return self.__responsibility	
	@responsibility.setter
	def responsibility(self, name):
		self.__responsibility = responsibility
		 
	def info(self):
		return "#" + str(self.__number) + "," + self.__name + "," + str(self.__responsibility) + "," + str(self.__height)
	
		
if __name__ == '__main__':
		
	'''	
	seat_table_empty = list()		
	for i in range(0,ROW_MAX):
		for j in range(0,COLUMN_MAX):
			seat_table_empty.append((i,j))
	print(seat_table_empty)
	print("distance:", distance((0,3),(3,6)))'''
	
	for i in range(0,3):
		# genrate student table
		student_table = generate_student_table()
		
		'''
		# sorted
		st2 = sorted(student_table, key = attrgetter('height'))
		for s in st2:
			print(s.height) # debug''' 
		
		# generate seat table
		'''seat_table = collections.OrderedDict()
		for i in range(0, ROW_MAX):
			for j in range(0, COLUMN_MAX):
				rnd = random.randint(0, len(student_table)-1)
				seat_table[(i,j)] = student_table[rnd]
				student_table.pop(rnd)
		print_seat_table()'''
		
		pos = SeatTableObj()
		pos.dct[(0,0)] = "abc"
		pos.dct[(0,1)] = "def"
		str = pos.dct.get((0,0))
		print(str)
		
		
		'''
		hscore = height_score(seat_table)
		print("hscore:", hscore)
		
		rscore = responsibility_score(seat_table)
		print("responsibility:", rscore)
		
		score = hscore + rscore
		
		print("-------------------------")
		'''
			
	'''		
	root = Tk()
	frame = Frame(root)
	frame.pack()

	Label(frame, text="teacher").grid(row=0, column = round(COLUMN_MAX/2))

	for r in range(0,ROW_MAX):
		for c in range(0,COLUMN_MAX):
			st = seat_table[r,c]
			seatInfo = "["+str(r+1)+str(c+1)+"]\n" + st.info() + "\n\n"
			Label(frame, text=seatInfo).grid(row=(r+1), column=c)
	
	root.mainloop()'''

