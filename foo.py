# foo.py

def factorial(n):
	s = 1
	for i in range(1, n+1):
		s *= i
	return s
	
print(factorial(50))