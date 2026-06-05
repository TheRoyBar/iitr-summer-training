#6. **Attendance Eligibility Checker**  
#Take total classes and attended classes. Calculate attendance 
# percentage and print eligibility.

total = int(input("Enter total number of classes:"))
att = int(input("Enter number of attended classes:"))

a = (att/total)*100

if (a>=75):
    print("You are clear.")
else:
    print("Sorry, you don't have enough.")