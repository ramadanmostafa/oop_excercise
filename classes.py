import uuid


class BaseClass(object):
    """
    the very parent class for all classes
    """
    def __init__(self):
        """construct a BaseClass object"""
        self.id = str(uuid.uuid4())


class Person(BaseClass):

    def __init__(self, name=''):
        super(Person, self).__init__()
        self.name = name
        self.assigned_classes = []

    def assign_to_class(self, class_room):
        self.assigned_classes.append(class_room)


class Student(Person):
    def __init__(self,  name=''):
        super(Student, self).__init__(name)
        self.quizzes = []

    def solve_question(self, quiz_id, question_id, solution):
        for quiz in self.quizzes:
            if quiz_id == quiz.id:
                quiz.solve_question(question_id, solution)
                return True
        return False

    def get_total_grade(self):
        grade = 0
        for quiz in self.quizzes:
            grade += quiz.get_grade()

        return grade


class Teacher(Person):

    @staticmethod
    def create_quiz(questions):
        quiz = Quiz()
        for question in questions:
            quiz.add_question(question)
        return quiz

    @staticmethod
    def assign_quiz_to_student(student, quiz):
        student.quizzes.append(quiz)


class ClassRoom(BaseClass):
    def __init__(self, name):
        super(ClassRoom, self).__init__()
        self.name = name


class Question(BaseClass):
    def __init__(self, question_text, choices, solution, weight=1):
        """
        construct a question object
        :param question_text: str
        :param choices: list of strings
        :param solution: str
        """
        super(Question, self).__init__()
        self.question_text = question_text
        self.choices = choices
        self.solution = solution
        self.student_solution = ''
        self.weight = weight

    def solve(self, solution):
        self.student_solution = solution

    def is_correct(self):
        return self.solution == self.student_solution

    def get_grade(self):
        return self.weight if self.is_correct() else 0


class Quiz(BaseClass):
    def __init__(self):
        """
        construct a quiz object
        :param id: unique identifier for this quiz
        :param questions: list of Questions
        """
        super(Quiz, self).__init__()
        self.questions = []

    def add_question(self, question):
        self.questions.append(question)

    def get_grade(self):
        grade = 0
        for question in self.questions:
            grade += question.get_grade()
        return grade

    def solve_question(self, question_id, solution):
        for question in self.questions:
            if question.id == question_id:
                question.solve(solution)
                return True
        return False
