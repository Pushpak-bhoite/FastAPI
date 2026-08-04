try:
    print(10/0)
except ZeroDivisionError:
    print("cant divide by zero ")

print("========== catching multiple exceptions ==========")
try: 
    x = int(input())
    print(10/x)
except ValueError:
    print("Invalid number")
except ZeroDivisionError:
    print("cant divide by 0 ")
finally:
    print("This prints in any way")
    
    # x = list(range(3))
    # print(x)