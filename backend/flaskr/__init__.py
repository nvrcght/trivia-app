import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    # CORS(app, resources={r"*/api/*": {"origins": '*'}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    # @app.after_request
    # def after_request(response):
    #     response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    #     response.headers.add('Access-Control-Allow-Mothods', 'GET, POST, DELETE')
    #     return response
        


    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        res = {'categories':
            {cat.id: cat.type for cat in categories}
        }
        return jsonify(res)

    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, int)
        starting_question = (page-1) * QUESTIONS_PER_PAGE
        questions = Question.query.order_by(Question.id).all()[starting_question: starting_question + QUESTIONS_PER_PAGE]
        questions_data = [question.format() for question in questions]
        
        res = {
            "total_questions": Question.query.count(),
            "questions": questions_data,
            "categories": {cat.id: cat.type for cat in Category.query.all()},
            "current_category": "foo" #TODO
            }
        
        
        return jsonify(res)

    @app.route('/questions/<id>', methods=["DELETE"])
    def delete_question(id):
        question = Question.query.get(id)
        if question:
            try:
                question.delete()
                return jsonify({"status": "success"})
            except:
                return jsonify({"status": "failure"})
        else:
            return jsonify({"status": "failure"})

    @app.route('/questions', methods=["POST"])
    def add_question():
        data = json.loads(request.data)
        if "searchTerm" in data:
            term = data["searchTerm"]
            questions = Question.query.filter(Question.question.ilike(f'%{term}%')).all()
            res = {
                "questions": [q.format() for q in questions],
                "total_questions": len(questions),
                "current_category": 'FOO' #TODO
            }
            return jsonify(res)
        else:
            question = Question(**data)
            try:
                question.insert()
                return jsonify({"status": "success", "question_id": f"{question.id}"})
            except:
                question.rollback()
                return jsonify({"status": "failure"})
        
    @app.route('/categories/<id>/questions')
    def question_per_category(id):
        query = Question.query.filter(Question.category==id).all()
        if query:
            questions = [q.format() for q in query]
            res = {
                "questions": questions,
                "total_questions": len(query),
                "current_category": "History" #TODO

            }
            return jsonify(res)
        else:
            # TODO add error handling
            res = {
                "error": "True"
            }
            return jsonify(res)

    @app.route('/quizzes', methods=["POST"])
    def play_quiz():
        # TODO add tests
        data = json.loads(request.data)
        print(data)
        
        previous_questions = data["previous_questions"]
        quiz_category = data["quiz_category"]
        category = quiz_category["id"]

        query = Question.query.filter(Question.category==category)
        num_rows = query.count()
        rand_id = random.randint(0, num_rows-1)

        
        q = query.offset(rand_id).first()
        while q.id in previous_questions:
            if len(previous_questions) == num_rows:
                res = {
                    "status": "error"
                }
                break
            rand_id = random.randint(0, num_rows-1)
            q = query.offset(rand_id).first()
        else:
            res = {
                "question": q.format()
            }
        return jsonify(res)
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app
