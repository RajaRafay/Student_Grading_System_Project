import json
from abc import ABC, abstractmethod

# Abstract Student Class
class Student(ABC):
    def __init__(self, name, rollNo, marks):
        self.name = name
        self.rollNo = rollNo
        self.marks = marks
        self.grade = None

    @abstractmethod
    def calculate_grade(self):
        pass

    @abstractmethod
    def generate_report(self):
        pass
    
    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "name": self.name,
            "rollNo": self.rollNo,
            "marks": self.marks,
            "grade": self.grade
        }

    @staticmethod
    def from_dict(data):
        if(data["type"]=="ScienceStudent"):
            student = ScienceStudent(data["name"], data["rollNo"], data["marks"])
        elif(data["type"]=="ArtsStudent"):
            student = ArtsStudent(data["name"], data["rollNo"], data["marks"])
        else:
            raise ValueError("Unknown student type")
        student.grade = data.get("grade")
        return student


# ScienceStudent Class inherited from Student Abstract Class
class ScienceStudent(Student):
    def calculate_grade(self):
        weight = {
                    "Physics": 0.3,
                    "Chemistry": 0.3,
                    "Math": 0.4
                 }
        avg = 0.0
        for key, value in weight.items():
            avg = avg + (self.marks[key] * value) 
        self.grade = self.get_grade(avg)
    
    def get_grade(self, avg):
        if(avg>=90):
            return 'A'
        elif(avg>=80):
            return 'B'
        elif(avg>=70):
            return 'C'
        elif(avg>=60):
            return 'D'
        else:
            return 'F'
    
    def generate_report(self):
        report = f"Science Student Report:\nName: {self.name}, Roll No: {self.rollNo}\n"
        for key, value in self.marks.items():
            report = report + (f"{key}: {value}\n")
        self.calculate_grade()
        report = report + (f"Grade: {self.grade}\n")
        return report


# ArtsStudent Class inherited from Student Abstract Class
class ArtsStudent(Student):
    def calculate_grade(self):
        avg = sum(self.marks.values()) / len(self.marks)
        self.grade = self.get_grade(avg)
    
    def get_grade(self, avg):
        if(avg>=90):
            return 'A'
        elif(avg>=80):
            return 'B'
        elif(avg>=70):
            return 'C'
        elif(avg>=60):
            return 'D'
        else:
            return 'F'
    
    def generate_report(self):
        report = f"Arts Student Report:\nName: {self.name}, Roll No: {self.rollNo}\n"
        for key, value in self.marks.items():
            report = report + (f"{key}: {value}\n")
        self.calculate_grade()
        report = report + (f"Grade: {self.grade}\n")
        return report


# StudentManager Class (Utility Class)
class StudentManager:
    def __init__(self):
        self.students = []

    # Add Student
    def add_student(self, student):
        self.students.append(student)

    # Delete Student
    def delete_student(self, rollNo):
        for student in self.students:
            if(student.rollNo == rollNo):
                self.students.remove(student)
                print(f"Student {student.name} with rollNo {student.rollNo} is deleted successfully")
                return
        print(f"The student with rollNo {rollNo} doesn't exist!")

    # Search Student
    def search_student(self, rollNo):
        for student in self.students:
            if(student.rollNo == rollNo):
                print(student.generate_report())
                return
        print(f"The student with rollNo {rollNo} doesn't exist!")

    # Update Student
    def update_student(self, rollNo):
        for i, student in enumerate(self.students):
            if(student.rollNo == rollNo):
                name = input("Enter student name: ")
                rollNo = int(input("Enter student rollNo: "))
                std_type = input("Enter student type ('s' for science/'a' for arts): ").lower()

                if(std_type=="science" or std_type=='s'):
                    subjects = ["Physics", "Chemistry", "Math"]
                elif(std_type=="arts" or std_type=='a'):
                    subjects = ["History", "Literature", "Sociology"]
                else:
                    print("Invalid type.")
                    continue

                marks = {}
                for subject in subjects:
                    marks[subject] = float(input(f"Enter marks of {subject}: "))
                
                if(std_type=="science" or std_type=='s'):
                    new_student = ScienceStudent(name, rollNo, marks)
                else:
                    new_student = ArtsStudent(name, rollNo, marks)

                new_student.calculate_grade()
                self.students[i] = new_student
                print("Student updated successfully!")
                return
        print(f"The student with rollNo {rollNo} doesn't exist!")

    # List All Students
    def list_student(self):
        if not self.students:
            print("No student is present!!")
        else:
            for student in self.students:
                print(student.generate_report())
    
    # Save Student Data to File
    def save_to_file(self, filename):
        if not self.students:
            print("No student is present to save student data in file!!")
            print("Exiting the program...")
        else:
            with open(filename, 'w') as f:
                json.dump([student.to_dict() for student in self.students], f, indent=4)
            print("Saving student data in file and Exiting the program...")
        

    # Load Student Data from File
    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.students = [Student.from_dict(item) for item in data]
        except FileNotFoundError:
            print("No file exist!!")



# Main Function
def main():
    manager = StudentManager()
    filename = "students.json"
    manager.load_from_file(filename)

    while(True):
        print("-----Welcome to Student Grading System-----")
        print("1. Add new student")
        print("2. Delete student")
        print("3. Search student")
        print("4. Update student")
        print("5. List all student")
        print("6. Save to file")
        print("7. Load from file")
        print("0. Exit")
        try:
            choice = int(input("Enter a choice(0-7): "))
        except ValueError:
            print("Invalid input! Please enter integer value!")
            continue

        if(choice==1):
            name = input("Enter student name: ")
            try:
                rollNo = int(input("Enter student rollNo: "))
            except ValueError:
                print("Invalid input! Please enter integer value!")
                continue
                
            std_type = input("Enter student type ('s' for science/'a' for arts): ").lower()

            if(std_type=="science" or std_type=='s'):
                subjects = ["Physics", "Chemistry", "Math"]
            elif(std_type=="arts" or std_type=='a'):
                subjects = ["History", "Literature", "Sociology"]
            else:
                print("Invalid type.")
                continue

            marks = {}
            try:
                for subject in subjects:
                    marks[subject] = float(input(f"Enter marks of {subject}: "))
            except:
                print("Invalid input! Please enter float value")
                continue

            if(std_type=="science" or std_type=='s'):
                student = ScienceStudent(name, rollNo, marks)
            else:
                student = ArtsStudent(name, rollNo, marks)

            student.calculate_grade()
            manager.add_student(student)
            print("Student added successfully.")
        
        elif(choice==2):
            try:
                rollNo = int(input("Enter student rollNo which you want to delete: "))
                manager.delete_student(rollNo)
            except ValueError:
                print("Invalid Input! Please enter integer value in rollNo")

        elif(choice==3):
            try:
                rollNo = int(input("Enter student rollNo which you want to search: "))
                manager.search_student(rollNo)
            except ValueError:
                print("Invalid Input! Please enter integer value in rollNo")
        
        elif(choice==4):
            try:
                rollNo = int(input("Enter student rollNo which you want to update: "))
                manager.update_student(rollNo)
            except ValueError:
                print("Invalid Input! Please enter integer value in rollNo")

        elif(choice==5):
            manager.list_student()

        elif(choice==6):
            manager.save_to_file(filename)
            print("Student Data is saved to file.")

        elif(choice==7):
            manager.load_from_file(filename)
            print("Student Data is loaded from file.")

        elif(choice==0):
            manager.save_to_file(filename)
            break

        else:
            print("Invalid choice. Try again.")



if __name__ == "__main__":
    main()
