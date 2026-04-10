class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name

    def __str__(self):
        return f"Student Name: {self.name}"

    def __repr__(self):
        return f"Student({self.student_id}, '{self.name}')"


s = Student(1, "Pushpak")

print("print(s):", s)        # __str__
print("repr(s):", repr(s))  # __repr__ 