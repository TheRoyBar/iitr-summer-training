#1. **Personal Introduction Program**  
#Take name, college, branch, year, and goal as input. Print a clean introduction.

name = input("Enter your name: ")
col = input("Enter your college name: ")
branch = input("Enter department name: ")
year = int(input("Enter the current year: "))
goal = input("Enter your life's goal: ")

print(f"Hello, I am {name}. I am from the {branch} department in {col}. \
      I am currently in my {year} year. My life's goal is to {goal}.")
