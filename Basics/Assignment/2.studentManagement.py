# class Student:
#     def __init__(self, id, name, age):
#         self.id = id 
#         self.name = name
#         self.age = age

# class StudentManagementSystem:
#     def __init__(self):
#         self.students = []
    
#     def add_student(self, student):
#         self.students.append(student)

#     def view_student(self):
#         if not self.students:
#             print("No students found")
#         for student in self.students:
#             print(student.name)



# def main():

#     system = StudentManagementSystem()
#     print("Welcome")
#     while True:
#         print(" 1 to add  ")
#         print(" 2 to view all ")
#         print(" 3 to delete ")
#         print(" 4 to update ")
#         print(" 5 to stop ")
#         choice = input("Enter the choice  ")
#         match choice:
#             case "1":
#                 id = input("Enter id ")
#                 name = input("Enter name ")
#                 age =  input("Enter age ")
#                 print('id-> ', id )
#                 print('Enter name -> ', name)
#                 print('Enter age -> ', age)
#                 student = Student(id, name, age)
#                 system.add_student(student)
#             case "2":
#                 print('show all students')
#                 system.view_student()
#             case "5":
#                 break

# if __name__ == "__main__":
#     main()


class Student:
    def __init__(self, student_id, name, age, course):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.course = course

    def __str__(self):
        return f"ID: {self.student_id}, Name: {self.name}, Age: {self.age}, Course: {self.course}"


class StudentManagementSystem:
    def __init__(self):
        self.students = []

    # Add student
    def add_student(self, student):
        self.students.append(student)
        print("Student added successfully!")

    # View all students
    def view_students(self):
        if not self.students:
            print("No students found.")
        for student in self.students:
            print(student)

    # Search student by ID
    def search_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    # Update student
    def update_student(self, student_id, name=None, age=None, course=None):
        student = self.search_student(student_id)
        if student:
            if name:
                student.name = name
            if age:
                student.age = age
            if course:
                student.course = course
            print("Student updated successfully!")
        else:
            print("Student not found!")

    # Delete student
    def delete_student(self, student_id):
        student = self.search_student(student_id)
        if student:
            self.students.remove(student)
            print("Student deleted successfully!")
        else:
            print("Student not found!")


# CLI Interface
def main():
    system = StudentManagementSystem()

    while True:
        print("\n--- Student Management System ---")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            sid = input("Enter ID: ")
            name = input("Enter Name: ")
            age = int(input("Enter Age: "))
            course = input("Enter Course: ")
            student = Student(sid, name, age, course)
            print("studo->", student)
            print("studo->", type(student))
            system.add_student(student)

        elif choice == "2":
            system.view_students()

        elif choice == "3":
            sid = input("Enter ID to search: ")
            student = system.search_student(sid)
            print(student if student else "Student not found")

        elif choice == "4":
            sid = input("Enter ID to update: ")
            name = input("Enter new name (leave blank to skip): ")
            age = input("Enter new age (leave blank to skip): ")
            course = input("Enter new course (leave blank to skip): ")

            system.update_student(
                sid,
                name if name else None,
                int(age) if age else None,
                course if course else None
            )

        elif choice == "5":
            sid = input("Enter ID to delete: ")
            system.delete_student(sid)

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()