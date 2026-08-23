

def armstrong_no(no):
    temp = no
    total = 0
    digits = 0
    while no != 0 :
        no = int(no/10)
        digits += 1
    no = temp
    while no != 0  :    
        lastNo = int(no%10)        
        pow = lastNo
        for i in range(digits-1):
            lastNo = pow * lastNo
        total = total + lastNo
        no = int(no/10)
        
    return temp == total
    

print(armstrong_no(1534))
        
# print(pow(5,3))  # or use this function
# print(5 ** 3)