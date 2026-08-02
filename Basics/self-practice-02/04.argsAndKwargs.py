# *args: Allows a function to accept any number of positional arguments, which are stored as a tuple.
# **kwargs: Allows a function to accept any number of keyword arguments, which are stored as a dictionary.


# args and kwargs are just naming conventions. You could write:
def func(*numbers, **details):
    print('number->', numbers)
    print('detasls->', details)
    
func(1,2,3, name='ram', brother='sham' )

# arguments pass by value or by reference 
# but in python arguments gets passed through pass-by-assignment or pass-by-object. 

# mutable objects - changes made to obj inside function will be reflected to outside the function as well. 
# immutable objects