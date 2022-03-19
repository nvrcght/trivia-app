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


    CORS(app)


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Mothods', 'GET, POST, DELETE')
        return response

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
        if not questions:
            abort(404)
        questions_data = [question.format() for question in questions]
        
        res = {
            "total_questions": Question.query.count(),
            "questions": questions_data,
            "categories": {cat.id: cat.type for cat in Category.query.all()},
            "current_category": "" #Where is this used?
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
                abort(500)
        else:
            abort(404)

    @app.route('/search', methods=["POST"])
    def search_question():
        data = json.loads(request.data)
        if "searchTerm" in data:
            term = data["searchTerm"]
            questions = Question.query.filter(Question.question.ilike(f'%{term}%')).all()
            res = {
                "questions": [q.format() for q in questions],
                "total_questions": len(questions),
                "current_category": "" #Where is this used?
            }
            return jsonify(res)
        else:
            abort(422)

    @app.route('/questions', methods=["POST"])
    def add_question():
        data = json.loads(request.data)
        try:
            question = Question(**data)
        except:
            abort(422)
        try:
            question.insert()
            return jsonify({"status": "success", "question_id": f"{question.id}"})
        except:
            question.rollback()
            return abort(500)
        
    @app.route('/categories/<id>/questions')
    def question_per_category(id):
        query = Question.query.filter(Question.category==id).all()
        if query:
            questions = [q.format() for q in query]
            res = {
                "questions": questions,
                "total_questions": len(query),
                "current_category": "" #Where is this used?
            }
            return jsonify(res)
        else:
            abort(404)

    @app.route('/quizzes', methods=["POST"])
    def play_quiz():
        data = json.loads(request.data)
        if "previous_questions" not in data or \
        "quiz_category" not in data or "id" not in data["quiz_category"]:
            abort(422)

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

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Malformed Data Request'
        }), 422  


    return app
