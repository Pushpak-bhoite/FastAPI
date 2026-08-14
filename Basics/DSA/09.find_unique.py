b = {"rahul":1, "ram": 1, "sham": 2, "bran":3 }
print(b)

print(len(b))
uniq = dict() # we cant solve this problem without taking another dict, we del items from existing dict
# RuntimeError: dictionary changed size during iteration (rn it throws this error)
# it doesn't happen with list, we can change list whle iterating it. and about tuples they are immutable
for key, value in b.items():
    if value in uniq.values():
        continue
        # del b[key] #we dont need this rn but still for remembering
        # b.pop(key, None)#Safely return none without crashing if key doesn't exist
    else:
        uniq[key] = value
        # b.pop(key, None)
        
print(uniq)
    