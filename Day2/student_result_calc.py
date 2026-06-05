#1. Student Result Calculator
#Build a program that:
# - takes student name
# - takes marks for multiple subjects
# - calculates total and percentage
# - assigns grade
# - gives remarks
# - saves result to a text file

name = input("Enter your name:")
m1 = int(input("Enter marks for Subject 1: "))
m2 = int(input("Enter marks for Subject 2: "))
m3 = int(input("Enter marks for Subject 3: "))
m4 = int(input("Enter marks for Subject 4: "))
sum = m1+m2+m3+m4
percentage = sum/4
if (percentage >90):
  grade = 'A'
  remarks = 'Excellent'
elif (percentage >80):
  grade = 'B'
  remarks = "Good"
elif (percentage > 70):
  grade = 'C'
  remarks = "Average"
elif (percentage > 60):
  grade = 'D'
  remarks = "Below Average"
else:
  grade = 'F'
  remarks = "Better luck next time"

with open("student_records.txt", 'w') as file:
  file.write(f"Student name is: {name}, with a {percentage}% and remarks {remarks}.")
