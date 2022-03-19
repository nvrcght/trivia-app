# API Development and Documentation Final Project

## Trivia App

Trivia app based on Udacity repository: https://github.com/udacity/cd0037-API-Development-and-Documentation-project


### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. 

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. 

## API Documentation

### Getting Started

* Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.

* Authentication: This version of the application does not require authentication or API keys.


### Endpoints

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Parameters  
    No parameters.
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

`GET '/api/v1.0/questions'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Parameters  
    `page`
        Specifies which page of questions to return. Each page has maximum of 10 questions.  
- Returns: Questions per page if the page exists. Raises an error otherwise.

```json
{
 "total_questions": "19",
 "questions": [
     {
        "id": "1",
        "question": "What is the capital of the UK?",
        "answer": "London",
        "category": "Geography",
        "difficulty": "1"
    },
    {
        "id": "2",
        "question": "What is the capital of Thailand?",
        "answer": "Bangkok",
        "category": "Geography",
        "difficulty": "2"
    },    
       
 ],
 "categories": {
     "1": "Science",
     "2": "Art",
     "3": "Geography",
},
 "current_category": "Geography"
}
```

`DELETE '/api/v1.0/questions/:id'`

- Deletes a question by ID.
- Parameters  
    No parameters.
- Returns: Successful response if delete was successful, otherwise raises.

`POST '/api/v1.0/search'`

- Searches questions based on search term.
- Parameters  
    `searchTerm`  
        Specifies search term. Case insensitive.  
- Returns: List of questions that match the search term. Otherwise raises.

```json
{
 "total_questions": "19",
 "questions": [
     {
        "id": "1",
        "question": "What is the capital of the UK?",
        "answer": "London",
        "category": "Geography",
        "difficulty": "1"
    },
    {
        "id": "2",
        "question": "What is the capital of Thailand?",
        "answer": "Bangkok",
        "category": "Geography",
        "difficulty": "2"
    },    
       
 ],
 "current_category": "Geography"
}
```

`POST '/api/v1.0/questions'`

- Creates a new question.
- Parameters  
    `question`  
        Question to add.  
    `answer`  
        Answer to the question.  
    `category`  
        Category to which the question belongs.  
    `difficulty`  
        Difficulty of the question.  
- Returns: Successful response if delete was successful, otherwise raises.


`GET '/api/v1.0/categories/:id/questions'`

- Fetches a list of questions given a category id.
- Parameters  
    No parameters.
- Returns: Questions per category if there are any. Raises an error otherwise.

```json
{
 "total_questions": "19",
 "questions": [
     {
        "id": "1",
        "question": "What is the capital of the UK?",
        "answer": "London",
        "category": "Geography",
        "difficulty": "1"
    },
    {
        "id": "2",
        "question": "What is the capital of Thailand?",
        "answer": "Bangkok",
        "category": "Geography",
        "difficulty": "2"
    },    
       
 ],
 "current_category": "Geography"
}
```

`GET '/api/v1.0/quizzes'`

- Fetches a list of questions given a category id.
- Parameters  
    `previous_questions`  
        List of previously generated questions played in current quiz.  
    `quiz_category`  
        Category to which the question belongs.  
- Returns: Questions for quiz category. Raises an error otherwise.

```json
{
 "question": 
     {
        "id": "1",
        "question": "What is the capital of the UK?",
        "answer": "London",
        "category": "Geography",
        "difficulty": "1"
    },
}
```

### Error Handling

Errors are returned as JSON objects in the following format:
```json
{
    "success": False, 
    "error": 404,
    "message": "Resource not found"
}
```
The API will return three error types when requests fail:

404: Resource not found
422: Malformed Data Request
500: Internal Server Error
