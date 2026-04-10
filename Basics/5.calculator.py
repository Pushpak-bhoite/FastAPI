

def calculator():
    print("Welcome!")

    num1 = float(input("Enter no 1:"))
    operator = input("Operator:")
    num2 = float(input("Enter no 2:"))
    print("num 1 -",num1, "num 2 -", num2, "operator :", operator )

    match(operator):
        case '+':
            print("the answer is ->", num1 + num2)

        case  '-':
            print("the answer is ->", num1 - num2)
    
calculator()