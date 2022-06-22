import json
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginated_selection(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_selection = [item.format() for item in selection]
    return formatted_selection[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route('/categories')
    def index():
        categories = Category.query.all()
        return jsonify({
            "success": True,
            "categories": paginated_selection(request, categories)
        })

    """
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        questions = paginated_selection(request, questions)
        if len(questions) == 0:
            abort(404)
        categories = [category.format()['type']
                      for category in Category.query.all()]
        return jsonify({
            "success": True,
            "questions": questions,
            "current_category": categories,
            "categories": categories
        })

    """
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        question = Question.query.filter(Question.id == id).one_or_none()
        if question == None:
            abort(404)
        question.delete()
        total_question = Question.query.all()
        total_question = paginated_selection(request, total_question)
        return jsonify({
            "success": True,
            "deleted": id,
            "total_questions": len(total_question)
        })

    """
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.get_json()
        if data == None:
            abort(404)
        question = data.get("question")
        answer = data.get("answer")
        category = data.get("category")
        difficulty = data.get("difficulty")
        searchTerm = data.get("searchTerm")

        if searchTerm:
            searched_questions = Question.query.order_by(Question.id).filter(
                Question.question.ilike('%{}%'.format(searchTerm))).all()
            searched_questions = paginated_selection(
                request, searched_questions)
            return jsonify({
                "success": True,
                "questions": searched_questions,
                "total_questions": len(searched_questions)
            })
        else:
            try:
                new_question = Question(question=data.get("question"), answer=data.get(
                    'answer'), category=int(data.get("category")), difficulty=int(data.get('difficulty')))
                new_question.insert()
                questions = [question.format()
                             for question in Question.query.all()]
                return jsonify({
                    "success": True,
                    "questions": questions,
                    "total_questions": len(questions)
                })
            except:
                abort(422)

    """
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category(id):
        try:
            current_category = Category.query.filter(
                Category.id == id).one_or_none().format()
            if current_category == None:
                abort(404)
            questions = Question.query.order_by(
                Question.id).filter(Question.category == id).all()
            questions = paginated_selection(request, questions)
            return jsonify({
                "success": True,
                "questions": questions,
                "total_questions": len(questions),
                "current_category": current_category,
            })
        except:
            abort(500)
    """
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def get_quiz():
        data = request.get_json()
        if data == None:
            abort(404)
        category = data.get("quiz_category", None)
        previous_questions = data.get("previous_questions", None)
        try:
            if not previous_questions:
                if category:
                    questions = Question.query.filter(
                        Question.category == category['id']).all()
                else:
                    questions = Question.query.all()
            else:
                if category:
                    questions = Question.query.filter(Question.category == category['id']).filter(
                        Question.id.not_in(previous_questions)).all()
                else:
                    questions = Question.query.filter(
                        Question.id.not_in(previous_questions)).all()

            questions = [question.format() for question in questions]
            total_questions = len(questions)

            if total_questions == 1:
                random_question = questions[0]
            else:
                random_question = questions[random.randint(0, total_questions)]
            return jsonify({
                "success": True,
                "random_questions": random_question
            })
        except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "message": "Resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "message": "unprocessable request"
        }), 422

    return app
