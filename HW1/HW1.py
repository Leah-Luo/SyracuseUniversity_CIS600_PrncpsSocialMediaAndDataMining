"""
CIS 600 Assignment 1 
Student Name: Leah Luo
Date: 09/07/2020
"""

import turtle as T
import random

# Define at least 1 class
class Test:	
	# Define at least 1 function for each class 
	def drawTree(distance, tur, colors):
		tur.hideturtle()
		if distance > 3:
			# Color of Flower
			ran = random.randint(0, 1)
			if ran == 0:
				tur.color(colors[0])
			else:
				tur.color(colors[1])
			
			# Size of Flower
			if distance <= 12 and distance >= 8:
				tur.pensize(distance / 3)
			elif distance < 8:
				tur.pensize(distance / 2)
			else: 
				tur.pensize(distance / 10)
				tur.color('sienna')
			# Draw the tree
			tur.forward(distance)
			a = 1.5 * random.random()
			tur.right(20 * a)
			b = 1.5 * random.random()
			# Recursive
			Test.drawTree(distance - 10 * b, tur, colors)
			tur.left(40 * a)
			# Recursive 
			Test.drawTree(distance - 10 * b, tur, colors)
			tur.right(20 * a)
			tur.up()
			tur.backward(distance)
			tur.down()
			
	def winterTree(distance, tur):
		tur.hideturtle()
		if distance > 12:
			tur.color('sienna')  
			tur.pensize(distance / 10) 
			tur.forward(distance)
			a = 1.5 * random.random()
			tur.right(20 * a)
			b = 1.5 * random.random()
			Test.winterTree(distance - 10 * b, tur)
			tur.left(40 * a)
			Test.winterTree(distance - 10 * b, tur)
			tur.right(20 * a)
			tur.up()
			tur.backward(distance)
			tur.down()

def main():
	print("-------------------- Four-Season Tree -----------------")
	# Instantiate objects of the class Test 
	test = Test
	
	# Colors for the tree (Spring, Summer, Fall)
	colorSp = ["snow", 'lightcoral', "aliceblue"]
	colorSu = ["PaleGreen3", "ForestGreen", "wheat"]
	colorF = ["darkorange", "gold", "moccasin"]
	
	# Use dictionary comprehensions to create dictionaries.
	options = [1, 2, 3, 4, 5]
	seasons = ["Spring", "Summer", "Fall", "Winter", "Exit"]
	Dic = {k:v for (k,v) in zip(options, seasons)}
	
	# List Comprehension
	userIn = [x for x in range(1, 6)]
	
	while True:
		# Print options for input
		for x in userIn:
			print(Dic.get(x) + " -- " + str(x))
			
		# Use at least 1 try-except to catch some exceptions
		try:
			# Use the input() function, or command-line arguments, to get some user input
			i = int(input("\nWhich season do you like best (input the number): "))
		except ValueError:
			print('\nWrong input! Please re-enter your answer')
		else:			
			if 1 <= i <= 4:
				
				# Use at least 1 looping statement
				# Use the input() function, or command-line arguments, to get some user input
				sizeIn = str(input("\nHow large do you want the tree to be (small, medium, large): ")).lower()
				# Size of the tree
				while sizeIn != 'small' and sizeIn != 'large' and sizeIn != 'medium':
					sizeIn = str(input("\nWrong input! Please re-enter your answer: ")).lower()
				if sizeIn == "small":
					distance = 40
				elif sizeIn == "medium":
					distance = 50
				elif sizeIn == "large":
					distance = 60
					
				# Create turtle and the screen for drawing 
				tur = T.Turtle()
				tur.speed(10)
				tur.hideturtle() 
				w = T.Screen()
				w.resetscreen()
				tur.getscreen().tracer(5, 0)
				
				# Use at least 1 decision-making statement
				if i == 1:
					w.screensize(bg = colorSp[2])
					tur.left(90)
					tur.up()
					tur.backward(150)
					tur.down()
					# Invoke the method defined in Test class
					test.drawTree(distance, tur, colorSp)
				# Draw the tree in Summer
				if i == 2:
					w.screensize(bg = colorSu[2])
					tur.left(90)
					tur.up()
					tur.backward(150)
					tur.down()
					# Invoke the method defined in Test class
					test.drawTree(distance, tur, colorSu)
				# Draw the tree in Fall
				if i == 3:
					w.screensize(bg = colorF[2])
					tur.left(90)
					tur.up()
					tur.backward(150)
					tur.down()
					# Invoke the method defined in Test class
					test.drawTree(distance, tur, colorF)
				if i == 4:
					w.screensize(bg='darkgrey')
					tur.left(90)
					tur.up()
					tur.backward(150)
					tur.down()
					# Invoke the method defined in Test class
					test.winterTree(distance, tur)
					# Snow on the ground
					for i in range(200):
						a = 200 - 400 * random.random()
						b = 10 - 20 * random.random()
						tur.up()
						tur.forward(b)
						tur.left(90)
						tur.forward(a)
						tur.down()
						tur.color('snow')
						tur.circle(1)
						tur.up()
						tur.backward(a)
						tur.right(90)
						tur.backward(b)
			elif i == 5:
				print("Good bye!")
				break
			elif i < 1 or i > 5:
				print('\nWrong input. Please re-enter your answer\n')
					

if __name__ == "__main__":
	main()