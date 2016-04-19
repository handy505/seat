#!/usr/bin/python
#-*- coding: UTF-8 -*-
from tkinter import *
import random
import math

	
def distance(a, b):
	return math.hypot(abs(a[0] - b[0]), abs(a[1] - b[1]))

class Student:
	def __init__(self, number=0, name="empty", responsibility=False, height=150):
		self.__number = number
		self.__name = name
		self.__responsibility = responsibility
		self.__height = height
		
	def info(self):
		return self.__name + "-" + str(self.__number)
		
if __name__ == '__main__':
	root = Tk()
	frame = Frame(root)
	frame.pack()

	Label(frame, text="teacher").grid(row=0, column=3)



	for r in range(0,7):
		for c in range(0,7):
			seatInfo = "["+str(r+1)+str(c+1)+"]\n"+"name\n\n"
			Label(frame, text=seatInfo).grid(row=(r+3), column=c)
			
			
	seat = list()		
	for i in range(0,7):
		for j in range(0,7):
			seat.append((i,j))

	print(seat)
	print("distance: ", distance((0,3),(3,6)))

	s1 = Student(1, 'aaa')
	s2 = Student(2, 'bbb')
	s3 = Student(3, 'ccc')
	s4 = Student(4, 'ddd')
	
	students = [s1, s2, s3, s4]
	for s in students:
		print(s.info())
		
	
	
	
	root.mainloop()

