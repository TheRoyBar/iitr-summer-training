#4. **Marks Grade Calculator**  
#Take marks out of 100 and assign grade using if-elif-else.

marks = int(input("Enter your marks out of 100: "))
if (marks == 100):
    print("A")
elif (marks >= 90):
    print("B")
elif (marks >= 80):
    print("C")
elif (marks >= 70):
    print("D")
elif (marks >= 60):
    print("E")
else:
    print("F")