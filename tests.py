from unittest import TestCase
from unittest.mock import patch

from classes import BaseClass, Person, ClassRoom, Student, Quiz, Teacher, Question


class TestBaseClass(TestCase):

    def setUp(self):
        self.base = BaseClass()

    def test_has_id(self):
        self.assertEqual(36, len(self.base.id))


class TestPerson(TestCase):
    def setUp(self):
        self.person = Person(name='ramadan')
        self.classRoom1 = ClassRoom('1')
        self.classRoom2 = ClassRoom('2')

    def test_created(self):
        self.assertEqual('ramadan', self.person.name)
        self.assertEqual([], self.person.assigned_classes)

    def test_assign_to_class(self):
        self.assertEqual([], self.person.assigned_classes)
        self.person.assign_to_class(self.classRoom1)
        self.assertEqual([self.classRoom1], self.person.assigned_classes)
        self.person.assign_to_class(self.classRoom2)
        self.assertEqual([self.classRoom1, self.classRoom2], self.person.assigned_classes)


class TestStudent(TestCase):

    def setUp(self):
        self.student = Student(name='ramadan')
        self.quiz = Quiz()

    def test_created(self):
        self.assertEqual('ramadan', self.student.name)
        self.assertEqual([], self.student.assigned_classes)
        self.assertEqual([], self.student.quizzes)

    @patch('classes.Quiz.solve_question', autospec=True)
    def test_solve_question(self, solve):
        # no quizzes
        self.assertFalse(self.student.solve_question('', '', ''))

        self.student.quizzes.append(self.quiz)

        # wrong quiz id
        self.assertFalse(self.student.solve_question('', '', ''))
        self.assertFalse(solve.called)

        # correct quiz id
        self.assertTrue(self.student.solve_question(self.quiz.id, 'question_id', 'solution'))
        solve.assert_called_with(self.quiz, 'question_id', 'solution')

    @patch('classes.Quiz.get_grade', autospec=True)
    def test_get_total_grade(self, get_grade):
        # no quizzes
        get_grade.return_value = 10
        self.assertEqual(0, self.student.get_total_grade())
        self.student.quizzes.append(self.quiz)
        self.assertEqual(10, self.student.get_total_grade())


class TestTeacher(TestCase):

    def setUp(self):
        self.teacher = Teacher(name='ramadan')
        self.question = Question('', '', '')

    def test_created(self):
        self.assertEqual('ramadan', self.teacher.name)
        self.assertEqual([], self.teacher.assigned_classes)

    @patch('classes.Quiz.add_question')
    def test_create_quiz_empty(self, add_question):
        self.assertIsInstance(Teacher.create_quiz([]), Quiz)
        self.assertFalse(add_question.called)

    @patch('classes.Quiz.add_question')
    def test_create_quiz(self, add_question):
        quiz = Teacher.create_quiz([self.question])
        self.assertIsInstance(quiz, Quiz)
        self.assertTrue(add_question.called)

    def test_assign_quiz_to_student(self):
        self.student = Student(name='ramadan')
        self.quiz1 = Quiz()
        self.quiz2 = Quiz()

        self.assertEqual([], self.student.quizzes)

        Teacher.assign_quiz_to_student(self.student, self.quiz1)
        self.assertEqual([self.quiz1], self.student.quizzes)

        Teacher.assign_quiz_to_student(self.student, self.quiz2)
        self.assertEqual([self.quiz1, self.quiz2], self.student.quizzes)


class TestClassRoom(TestCase):

    def setUp(self):
        self.room = ClassRoom(name='math')

    def test_created(self):
        self.assertEqual('math', self.room.name)


class TestQuestion(TestCase):

    def setUp(self):
        self.question = Question('question_text', ['ch1', 'ch2'], 'sol')

    def test_created(self):
        self.assertEqual('question_text', self.question.question_text)
        self.assertEqual(['ch1', 'ch2'], self.question.choices)
        self.assertEqual('sol', self.question.solution)
        self.assertEqual('', self.question.student_solution)
        self.assertEqual(1, self.question.weight)

    def test_solve(self):
        self.question.solve('sol')
        self.assertEqual('sol', self.question.student_solution)

    def test_is_correct(self):
        self.question.student_solution = 'sol'
        self.assertTrue(self.question.is_correct())

        self.question.student_solution = 'ch1'
        self.assertFalse(self.question.is_correct())

    def test_get_grade(self):
        self.question.student_solution = 'sol'
        self.assertEqual(1, self.question.get_grade())

        self.question.student_solution = 'ch1'
        self.assertEqual(0, self.question.get_grade())


class TestQuiz(TestCase):

    def setUp(self):
        self.quiz = Quiz()
        self.question1 = Question('question_text', ['ch1', 'ch2'], 'sol')
        self.question2 = Question('question_text', ['ch1', 'ch2'], 'sol')
        self.question3 = Question('question_text', ['ch1', 'ch2'], 'sol')

    def test_created(self):
        self.assertEqual([], self.quiz.questions)

    def test_add_question(self):
        self.assertEqual([], self.quiz.questions)

        self.quiz.add_question(self.question1)
        self.assertEqual([self.question1], self.quiz.questions)

        self.quiz.add_question(self.question2)
        self.assertEqual([self.question1, self.question2], self.quiz.questions)

        self.quiz.add_question(self.question3)
        self.assertEqual([self.question1, self.question2, self.question3], self.quiz.questions)

    def test_get_grade(self):
        # no questions
        self.assertEqual(0, self.quiz.get_grade())

        self.question1.student_solution = 'sol'
        self.question2.student_solution = 'sol'
        self.question3.student_solution = 'sol'
        self.quiz.questions.append(self.question1)
        self.quiz.questions.append(self.question2)
        self.quiz.questions.append(self.question3)
        self.assertEqual(3, self.quiz.get_grade())

        self.question1.student_solution = 'ch1'
        self.assertEqual(2, self.quiz.get_grade())

        self.question2.student_solution = 'ch1'
        self.assertEqual(1, self.quiz.get_grade())

        self.question3.student_solution = 'ch1'
        self.assertEqual(0, self.quiz.get_grade())

    @patch('classes.Question.solve', autospec=True)
    def test_solve_question(self, solve):
        # no quizzes
        self.assertFalse(self.quiz.solve_question('', ''))

        self.quiz.questions.append(self.question1)

        # wrong quiz id
        self.assertFalse(self.quiz.solve_question('', ''))
        self.assertFalse(solve.called)

        # correct quiz id
        self.assertTrue(self.quiz.solve_question(self.question1.id, 'solution'))
        solve.assert_called_with(self.question1, 'solution')

