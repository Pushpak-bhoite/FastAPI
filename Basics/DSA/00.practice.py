print("========== check if number is positive or negative =========")

def check_even_or_odd(num):
    print("-->", num % 2 )
    if(num % 2 == 0 ):
        return "Even"
    else:
        return "Odd"

# =======================


print(check_even_or_odd(1))