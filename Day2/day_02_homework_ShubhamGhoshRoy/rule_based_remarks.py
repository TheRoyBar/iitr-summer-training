#Rule-Based Career Advisor**  
#Ask for Python level, math level, and project count. 
# Suggest a learning path using if-elif-else.

python_rate = int(input("Rate your python profiency out of 10:"))
math_rate = int(input("Rate your math level out of 10:"))
project_count = int(input("Enter the number of projects you have built."))

if (python_rate> 6 and math_rate> 7 and project_count>2):
    print("You can try becoming a Data Scientist or a ML Engineer.")
elif (python_rate > 7 and math_rate>4 and project_count > 2):
    print("You can try becoming a Python based backend enginner.")
else:
    print("Try learning more about Python if you interested in AI/ML/DS.")