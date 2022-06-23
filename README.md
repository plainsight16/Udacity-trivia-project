# API DOCUMENTATION

## API ENDPOINTS

Base Url - http://127.0.0.1:5000

### Available Endpoints
- Categories
    - GET '/categories'
    - GET '/categories/<int:id>/questions'

- Questions
    - GET '/questions?page=2'
    - POST '/questions'
    - DELETE '/questions/<int:id>'

- Quizzes
    - POST '/quizzes'


#### 1. GET '/categories'

""" $ curl http://127.0.0.1:5000/categories """
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, """categories""", that contains an object of """id: category_string""" key: value pairs.

Example response
"""
{
    "success": True,
    "categories": {

    }
}
"""
