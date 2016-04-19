#!/usr/bin/python
import time
import random

class Conestant:
	def __init__(self):
		self.__origin_strategy_win = 0
		self.__change_strategy_win = 0
		
	def say_my1st_guess(self):
		self.__myguess = random.randint(0,2)
		return self.__myguess
		
	def getLeftover(self, num):
		self.__leftover = num
		
	def say_my2nd_guess_origin(self):
		return self.__myguess
		
	def say_my2nd_guess_change(self):
		return self.__leftover
		
	def increase_original_strategy_win(self):
		self.__origin_strategy_win += 1
		
	def get_origin_win(self):
		return self.__origin_strategy_win
		
	def increase_change_strategy_win(self):
		self.__change_strategy_win += 1
	
	def get_change_win(self):
		return self.__change_strategy_win

class Host:
	def excludeSomething(self, doors, first_guess):
		for i in range(0,3):
			if i != first_guess:
				if doors[i] == False:
					opendoor = i
					
		for i in range(0,3):
			if i != first_guess and i != opendoor:
				self.__leftover = i
				
		return self.__leftover

		
if __name__ == '__main__':
	
	c = Conestant()
	h = Host()
	
	for round in range(0,1000):
	
		doors = [False, False, False]
		car_number = random.randint(0,2)
		doors[car_number] = True
		print(doors)
		
		first_guess = c.say_my1st_guess()
		leftover = h.excludeSomething(doors, first_guess)
		c.getLeftover(leftover)
		
		second_guess1 = c.say_my2nd_guess_origin()
		second_guess2 = c.say_my2nd_guess_change()
		
		if c.say_my2nd_guess_origin() == car_number:
			c.increase_original_strategy_win()
		
		if c.say_my2nd_guess_change() == car_number:
			c.increase_change_strategy_win();
		#print(car_number, c.get_origin_win(), c.get_change_win()) #debug
		
	print("round:", round+1, "ori_win:", c.get_origin_win(), "chg_win:", c.get_change_win());

	