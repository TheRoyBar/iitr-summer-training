#14. **Safe Division Program**  
#Take two numbers and divide them. Handle division by zero and invalid input.

n1 = int(input("Enter number 1:"))
n2 = int(input("Enter number 2:"))

try:
    num = n1/n2
    print(f"The division is: {num}")

except ZeroDivisionError: 
    print("The second number you entered is Zero. Try again!")