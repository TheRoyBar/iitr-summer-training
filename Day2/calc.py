#2. **Simple Calculator**  #
# Take two numbers and an operator from the user. Perform addition, subtraction, multiplication, or division.

n1 = int(input("Enter number 1: "))
n2 = int(input("Enter number 2: "))
choice = input("Enter symbol +,_,*: ")

if choice == '+':
    print(n1+n2)
elif choice == '-':
    print(n1-n2)
elif choice == '*':
    print(n1*n2)

else:
    print("Wrong choice!")