#9. **Student Dictionary Program**  
#Store name, branch, year, marks, and goal in a dictionary. Print a formatted profile.

name = input("Enter your name: ")
col = input("Enter your college name: ")
branch = input("Enter department name: ")
year = int(input("Enter the current year: "))
goal = input("Enter your life's goal: ")

dict = {'name': name,
        'college' : col,
        'department': branch,
        'year': year,
        'goal': goal
        }

print(dict)