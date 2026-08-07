# arrays are different than List
# it's built in module provides type specific array structure
# Adv - memory efficient than list, becoz store memory elements of same type 
#   - operations in arrays are faster than list 

import array


# Syntax: array.array(typecode, [initializer])
arr = array.array('i', [1, 2, 3, 4, 5])  # 'i' = signed integers
print(arr)           # array('i', [1, 2, 3, 4, 5])
print(arr[0])        # 1
arr.append(6)        # Add element
print("type code ->",arr.typecode)  # 'i'

# Float array
float_arr = array.array('f', [1.5, 2.5, 3.5])
print(float_arr)     # array('f', [1.5, 2.5, 3.5])