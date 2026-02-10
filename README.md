
# Coderr Backend

This project provides a backend for a quiz generating application. It creates quizzes from YouTube links. It is vuild with **Django** and the **Django REST Framework**.
It provides a RESTful API for managing registration, login, logout, creating quizzes, retrieving quizzes, updating quizzes and deleting quizzes.


## Documentation

To view all possible endpoints go to this link after the server runs: api/schema/swagger-ui/


## Tech Stack

**Server:** Python, Django, Django REST Framework


## Features

- User authentication with JWT Token and HTTP only cookies
- Fetching audio from a YouTube video
- Transcribes the audio into text format
- Creates quizzes based on the transcript with the Gemini API 


## Prerequisites

-A global version of ffmpeg has to be installed. It also needs to be inserted into the system environment variables (User) PATH.

-An API key for the usage of the Gemini AI. Insert the API key in a .env file with the key named: GEMINI_API_KEY 


## Installation



Clone the repository:
```bash
git clone https://github.com/Marcel-Goehn/quizly_backend
```
Create and activate a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

Create migration plan:
```bash
python manage.py makemigrations
```

Migrate the database:
```bash
python manage.py migrate
```

Start development server:
```bash
python manage.py runserver
```

    
## Related

Here is the related frontend

[Quizly Frontend](https://github.com/Developer-Akademie-Backendkurs/project.Quizly)


## Authors

- [@Marcel-Goehn](https://github.com/Marcel-Goehn)


## License


This project is licensed under the MIT License.


## Feedback

If you have any feedback, feel free to reach out: 
marcelgoehn@googlemail.com