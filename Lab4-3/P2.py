
"""
Vorraluck Taladon
683040740-0
P2
"""

from datetime import date, timedelta

# Base Class

class Person:
    _counter = 1

    def __init__(self, name, age, birthdate, bloodgroup, is_married):
        self.name = name
        self.age = age
        self._birthdate = birthdate
        self._id = self.__generate_id()
        self.__bloodgroup = bloodgroup
        self.__is_married = is_married

    def __generate_id(self):
        year = date.today().year
        pid = f"{year}{Person._counter:03d}"
        Person._counter += 1
        return pid

    def display_public_info(self):
        print(f"Name: {self.name}, Age: {self.age}, ID: {self._id}")


# Level 2 Classes

class Staff(Person):
    def __init__(self, name, age, birthdate, bloodgroup, is_married,
                 department, start_year):
        super().__init__(name, age, birthdate, bloodgroup, is_married)
        self.department = department
        self.start_year = start_year
        self.tenure_year = self.__calculate_tenure()
        self.__salary = 0

    def __calculate_tenure(self):
        return date.today().year - self.start_year

    def get_salary(self):
        return self.__salary

    def set_salary(self, amount):
        self.__salary = amount

    def display_public_info(self):
        super().display_public_info()
        print(f"Department: {self.department}, Tenure: {self.tenure_year}")


class Student(Person):
    def __init__(self, name, age, birthdate, bloodgroup, is_married,
                 start_year, major, level, grade_list=None):
        super().__init__(name, age, birthdate, bloodgroup, is_married)
        self.start_year = start_year
        self.major = major
        self.level = level
        self.grade_list = grade_list or []
        self.gpa = self.calculate_instance_gpa()
        self.__graduation_date = self.__calculate_graduation_date()

    @staticmethod
    def calculate_gpa(grades):
        grade_map = {'A':4, 'B':3, 'C':2, 'D':1, 'F':0}
        total = sum(c * grade_map[g] for c, g in grades)
        credits = sum(c for c, _ in grades)
        return total / credits if credits else 0

    def calculate_instance_gpa(self):
        return Student.calculate_gpa(self.grade_list)

    def __calculate_graduation_date(self):
        if self.level.lower() == "undergraduate":
            return self.start_year + 4
        return self.start_year + 2

    def display_public_info(self):
        super().display_public_info()
        print(f"Major: {self.major}, Level: {self.level}, GPA: {self.gpa}")

# Level 3 - Staff

class Professor(Staff):
    def __init__(self, name, age, birthdate, bloodgroup, is_married,
                 department, start_year, professorship, admin_position=0):
        super().__init__(name, age, birthdate, bloodgroup, is_married,
                         department, start_year)
        self.professorship = professorship
        self.admin_position = admin_position
        self.set_salary()

    def set_salary(self):
        salary = (30000 +
                  self.tenure_year * 1000 +
                  self.professorship * 10000 +
                  self.admin_position * 10000)
        super().set_salary(salary)

    def display_public_info(self):
        super().display_public_info()
        print(f"Professor Level: {self.professorship}, Salary: {self.get_salary()}")


class Administrator(Staff):
    def __init__(self, name, age, birthdate, bloodgroup, is_married,
                 department, start_year, admin_position):
        super().__init__(name, age, birthdate, bloodgroup, is_married,
                         department, start_year)
        self.admin_position = admin_position
        self.set_salary()

    def set_salary(self):
        salary = 15000 + self.tenure_year * 800 + self.admin_position * 5000
        super().set_salary(salary)

    def display_public_info(self):
        super().display_public_info()
        print(f"Admin Level: {self.admin_position}, Salary: {self.get_salary()}")


# Level 3 - Student

class UndergraduateStudent(Student):
    def __init__(self, name, age, birthdate, bloodgroup, is_married,
                 start_year, major, level, club=None, grade_list=None):
        super().__init__(name, age, birthdate, bloodgroup, is_married,
                         start_year, major, level, grade_list)
        self.club = club
        self.course_list = []

    def register_course(self, course):
        self.course_list.append(course)

    def display_public_info(self):
        super().display_public_info()
        print(f"Club: {self.club}, Courses: {self.course_list}")


class GraduateStudent(Student):
    def __init__(self, name, age, birthdate, bloodgroup, is_married,
                 start_year, major, level, advisor_name, grade_list=None):
        super().__init__(name, age, birthdate, bloodgroup, is_married,
                         start_year, major, level, grade_list)
        self.advisor_name = advisor_name
        self.thesis_name = None
        self.__proposal_date = None

    def set_thesis(self, thesis):
        self.thesis_name = thesis

    def set_proposal_date(self, proposal_date):
        self.__proposal_date = proposal_date

    def get_proposal_date(self):
        return self.__proposal_date

    def display_public_info(self):
        super().display_public_info()
        print(f"Advisor: {self.advisor_name}, Thesis: {self.thesis_name}")




print("===== STAFF TEST =====")
prof = Professor(
    name="Dr. Smith",
    age=45,
    birthdate="1979-05-10",
    bloodgroup="O",
    is_married=True,
    department="Computer Science",
    start_year=2015,
    professorship=3,
    admin_position=1
)
prof.display_public_info()

print("\n===== ADMIN TEST =====")
admin = Administrator(
    name="Ms. Johnson",
    age=40,
    birthdate="1984-03-12",
    bloodgroup="A",
    is_married=False,
    department="HR",
    start_year=2018,
    admin_position=2
)
admin.display_public_info()

print("\n===== UNDERGRADUATE STUDENT TEST =====")
ug = UndergraduateStudent(
    name="Alice",
    age=20,
    birthdate="2004-01-01",
    bloodgroup="B",
    is_married=False,
    start_year=2023,
    major="IT",
    level="undergraduate",
    club="Robotics",
    grade_list=[(3, 'A'), (3, 'B'), (3, 'A')]
)
ug.register_course("CS101")
ug.register_course("CS102")
ug.display_public_info()

print("\n===== GRADUATE STUDENT TEST =====")
grad = GraduateStudent(
    name="Bob",
    age=25,
    birthdate="1999-02-02",
    bloodgroup="AB",
    is_married=False,
    start_year=2024,
    major="Data Science",
    level="graduate",
    advisor_name="Dr. Lee",
    grade_list=[(3, 'A'), (3, 'A')]
)
grad.set_thesis("AI in Healthcare")
grad.display_public_info()
