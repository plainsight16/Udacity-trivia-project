import os
from unicodedata import category
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
            "categories": [category.format() for category in categories]
        })

    """
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/categories/<int:id>/questions')
    def get_questions(id):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        try:
            current_category = Category.query.filter(
                Category.id == id).one_or_none().format()
            if current_category == None:
                abort(404)
            questions = [question.format()
                         for question in Question.query.order_by(Question.id).filter(Question.category == id).all()]
            categories = [category.format()
                          for category in Category.query.order_by(Category.id).all()]
            return jsonify({
                "success": True,
                "questions": questions[start:end],
                "total_questions": len(questions),
                "current_category": current_category,
                "categories": categories
            })
        except:
            abort(500)

    """
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>')
    def delete_question(id):
        question = Question.query.filter(Question.id == id).one_or_none()
        if question == None:
            abort(404)
        question.delete()
        total_question = [question.format()
                          for question in Question.query.all()]
        return jsonify({
            "success": True,
            "deleted": id,
            "total_questions": len(total_question)
        })
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        data = request.get_json()
        if data == None:
            abort(404)
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

    return app
