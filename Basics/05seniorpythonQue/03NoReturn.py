# we don't need to return list from my_func, 
from no_Return_other import my_func

items = []

items = my_func(items, 5) # I don't need to collect this returned value in items either, since list object aready modified  
print('items->', items) 
