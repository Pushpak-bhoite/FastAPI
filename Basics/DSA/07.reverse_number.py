
def number_of_digits(n):
    cnt = 0
    while n:
        n  =  int(n/10)
        cnt += 1
        print(n)
    return cnt
print("number_of_digits->", number_of_digits(8345))

def reverse_the_number(num):
    rev = 0
    while num:
        rem = num%10
        num = int(num/10)
        rev = rev * 10 + rem
        
    return rev
print("reverse_the_number->", reverse_the_number(4567))
        