# API DOCUMENTATION

## API ENDPOINTS

**Base Url** - `http://127.0.0.1:5000`

### Available Endpoints
- Categories
    - [GET '/categories'](#get-categories)
    - [GET '/categories/<int:id>/questions'](#get-categories-questions)

- Questions
    - [GET '/questions?page=2'](#get-questions)
    - [POST '/questions'](#post-questions)
    - [DELETE '/questions/<int:id>'](#delete-questions)

- Quizzes
    - [POST '/quizzes'](#post-quizzes)


#### 1. GET '/categories'<a name="get-categories"></a>

``` $ curl http://127.0.0.1:5000/categories ```
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of id: `category_string` key: value pairs.

Example response
```
{
    "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "success": true
}
```

#### 2. GET '/categories/<int:id>/questions'<a name="get-categories-questions"></a>
``` curl http://127.0.0.1:5000/categories/<int:id>/questions```
- Fetches a dictionary of questions which are of the same type of category specified using `id` in the request arguments
- Request Arguments - `id`
- Returns an object with keys;
    i. **boolean** `success`,
    ii. **list** of dict `questions`,
    iii. **integer** `current_category`,
    iv. **integer** `total_questions`
- Example Response
    ```
        {
            "current_category": 1,
            "questions": [
                {
                "answer": "The Liver",
                "category": 1,
                "difficulty": 4,
                "id": 20,
                "question": "What is the heaviest organ in the human body?"
                },
                {
                "answer": "Alexander Fleming",
                "category": 1,
                "difficulty": 3,
                "id": 21,
                "question": "Who discovered penicillin?"
                },
                {
                "answer": "Blood",
                "category": 1,
                "difficulty": 4,
                "id": 22,
                "question": "Hematology is a branch of medicine involving the study of what?"
                },
                {
                "answer": "Bakare",
                "category": 1,
                "difficulty": 5,
                "id": 24,
                "question": "What is my name"
                },
                {
                "answer": "Aot",
                "category": 1,
                "difficulty": 5,
                "id": 25,
                "question": "What is my best anime"
                }
            ],
            "success": true,
            "total_questions": 5
        }
    ```
- Errors
    - Passing in an unknown id `curl http://127.0.0.1:5000/categories/20000/questions`
    - Returns
        ```
        {
            "success": False,
            "message": "Resource not found"
        }
        ```

### 3. GET '/questions?page=1' <a name="get-questions"></a>
``` curl http://127.0.0.1:5000/questions?page=1 ```
- Fetches a dictionary of questions
- Request Arguments: integer `page` (optional, 10 questions per page, defaults to 1 when not specified)
- Returns an object with keys;
    i. **boolean** `success`,
    ii. **list** of dict `questions` with keys;
        - **string** `answer`,
        - **integer** `category`,
        - **integer** `difficulty`,
        - **integer** `id`,
        - **string** `question`,
    iii. **list** `current_category`,
    iv. **list** `category`
    iv. **integer** `total_questions`
- Example Response
```
    "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
    ],
    "current_category": [
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports"
    ],
    "questions": [
        {
        "answer": "Edward Scissorhands",
        "category": 5,
        "difficulty": 3,
        "id": 6,
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
        "answer": "Muhammad Ali",
        "category": 4,
        "difficulty": 1,
        "id": 9,
        "question": "What boxer's original name is Cassius Clay?"
        },
        {
        "answer": "Brazil",
        "category": 6,
        "difficulty": 3,
        "id": 10,
        "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
       [...]
    ],
    "success": true,
    "total_questions": 10
    }
```
- Errors 
    - Requesting for a page that does not exist `$ curl http://127.0.0.1:5000/questions?page=2000`
    - Returns 
        ```
        {
            "success": False,
            "message": 'Resource not found'
        }
        ```

### 4. POST '/questions'<a name="post-questions"></a>
- Create a new question
``` $ curl -X POST -H 'Content-type:application/json' -d '{"answer":"Asia", "question":"Where is China?" "category":"1", "difficulty":"2"}' http://127.0.0.1:5000/questions ```
    - creates a new question and inserts into the database
    - Request Headers: ```application/json```
        - **string** `answer`,
        - **integer** `category`,
        - **integer** `difficulty`,
        - **string** `question`
    - Example Response
    ```
        {    
            "questions": [
                {
                "answer": "Edward Scissorhands",
                "category": 5,
                "difficulty": 3,
                "id": 6,
                "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
                },
                {
                "answer": "Muhammad Ali",
                "category": 4,
                "difficulty": 1,
                "id": 9,
                "question": "What boxer's original name is Cassius Clay?"
                },
                {
                "answer": "Brazil",
                "category": 6,
                "difficulty": 3,
                "id": 10,
                "question": "Which is the only team to play in every soccer World Cup tournament?"
                },
            [...] 
        "success": true,
            "total_questions": 10 
        }
    ```
    - Errors 
        - When a parameter is missing ``` $ curl -X POST -H 'Content-type:application/json' -d '{"answer":"Asia", "question":"Where is China?" "category":"1"}' http://127.0.0.1:5000/questions ```
        - Returns 
        ```
            {
                "success": False,
                "message": "Bad request"
            }
        ```

- Search for a question
``` $ curl -X POST -H 'Content-type:application/json' -d '{"searchTerm":"What"}' http://127.0.0.1:5000/questions ```
    - Probes thorough the database using a serch_term for a particullar question
    - Request Headers: `application/json`
        - **string** `searchTerm`
    - Example Response
    ```
         {
            "answer": "Aot",
            "category": 1,
            "difficulty": 5,
            "id": 25,
            "question": "What is my best anime"
        }
    ```
    - Errors
        - When SearchTerm cannot be found ``` $ curl -X POST -H 'Content-type:application/json' -d '{"searchTerm":"flippity"}' http://127.0.0.1:5000/questions ```
        - Returns
            ```
                {
                    "success": False,
                    "message": "Resource not found"
                }
            ```

### 5. DELETE '/questions/<int:id>' <a name="delete-questions"></a>
``` $ curl -X DELETE http://127.0.0.1:5000/questions/3 ```
- Deletes a question with id:`id` from the database
- Request Argument: int:id
- Example Response
```
    {
        "success": True,
        "deleted": 3,
        "total_questions": 9
    }

```
- Errors
    - When deleting a id that does not exist in the database ` $ curl -X DELETE http://127.0.0.1:5000/questions/3000`
    - Returns
        ```
            {
                "success": False,
                "message": "Resource not found"
            }
        ```
### 6. POST '/quizzes' <a name="post-quizzes"></a>
Get a random question 
``` $ curl -X POST -H 'Content-type:application/json' -d '{"previous_question":"3", "quiz_category":{"type" : "Science", "id" : "1"}}' ```
- Retrieves a random question that has not been previously retrived from the database
- Request Header: `application/json`
- Example Response
```
    {
        "success": True
        "question": {
            {
                "answer": "Edward Scissorhands",
                "category": 5,
                "difficulty": 3,
                "id": 6,
                "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
            }
        }
    }
```
- Errors
    - posting without content `curl -X POST http://127.0.0.1:5000/quizzes`
    - Returns
        ```
            {
            "success": False,
            "message": "Bad request" 
            }
        ```