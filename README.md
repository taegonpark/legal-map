A web application that connects clients to personal injury attorneys based on their case.

# Scripts
Navigate to /legal_map to run everything

## To Run Scripts (Scrape Testing)
py -m app.scripts.<script_name>

## To Run Backend (App)
uvicorn app.main:app
Defaults to http://127.0.0.1:8000 in browser
For Swagger API testing, http://127.0.0.1:8000/docs
Endpoints in app.api.attorney.py


