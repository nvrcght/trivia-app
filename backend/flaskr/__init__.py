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

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
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
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=["POST"])
    def add_question():
        data = json.loads(request.data)
        if "searchTerm" in data:
            term = data["searchTerm"]
            questions = Question.query.filter(Question.question.ilike(f'%{term}%')).all()
            return jsonify({"status": "success", "numQuestions": len(questions)})
        else:
            question = Question(**data)
            try:
                question.insert()
                return jsonify({"status": "success", "question_id": f"{question.id}"})
            except:
                question.rollback()
                return jsonify({"status": "failure"})

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

        
        

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<id>/questions')
    def question_per_category(id):
        query = Question.query.filter(Question.category==id).all()
        if query:
            questions = [q.format() for q in query]
            res = {
                "questions": questions,
                "total_questions": Question.query.count(),
                "current_category": "History"

            }
            return jsonify(res)
        else:
            # TODO add error handling
            res = {
                "error": "True"
            }
            return jsonify(res)

        
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app
