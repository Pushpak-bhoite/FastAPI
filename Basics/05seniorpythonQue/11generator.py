# A generator in Python is a simple way to create an iterator that produces values one at a time, instead of creating all the values at once.
# and it's one or more yield statements 

def my_generator():
    yield 1
    yield 2
    yield 3
    
#  This defines generator function but doesnt execute it 
gen = my_generator() 
print(next(gen)) # next resumes the function from where it last yielded 
print(next(gen))
print(next(gen))

