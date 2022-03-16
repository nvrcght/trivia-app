import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app, QUESTIONS_PER_PAGE
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""

        pass

    @staticmethod
    def _mock_question_data():
        """Helper method to generate mock data"""
        return {
            "question": "Heres a new question string",
            "answer": "Heres a new answer string",
            "difficulty": 1,
            "category": 3
        } 

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data["categories"]), 6)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data["questions"]), 10)  
        self.assertEqual(set(data), {"currentCategory", "questions", "totalQuestions", "categories"})

    def test_get_questions_paginated(self):
        res = self.client().get('/questions?page=2')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(len(data["questions"]), 9)  

    def test_question_per_category(self):
        res = self.client().get('/categories/4/questions')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(set(data), 
        {"questions", "totalQuestions", "currentCategory"})

        self.assertEqual(len(data["questions"]), 4)

    def test_question_per_category_question_not_found(self):
        res = self.client().get('/categories/100/questions')  
        #TODO
    
    def test_delete_question(self):
        """Creates a new record and tests delete question endpoint"""
        data = TriviaTestCase._mock_question_data() 
        new_question = Question(**data)
        new_question.insert()

        q_id = new_question.id
        self.assertIsInstance(Question.query.get(q_id), Question)

        res = self.client().delete(f'/questions/{q_id}')
        self.assertEqual(res.status_code, 200)
        self.assertIsNone(Question.query.get(q_id))

    def test_add_question(self):
        data = json.dumps(TriviaTestCase._mock_question_data())
        res = self.client().post('/questions', data=data)
        new_question_id = json.loads(res.data)["question_id"]
        inserted_question = Question.query.get(new_question_id)
        self.assertIsInstance(inserted_question, Question)
        inserted_question.delete()

    def test_search_question(self):
        data = TriviaTestCase._mock_question_data()
        data.update({"searchTerm": "Who"})
        res = self.client().post('/questions', data=json.dumps(data))  
        self.assertEqual(res.status_code, 200)
        num_questions = json.loads(res.data)["numQuestions"]
        self.assertEqual(num_questions, 3)
       

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()