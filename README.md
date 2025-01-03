# Running the Backend

## Virtual environment
Make sure python3-venv is in your machine
```bash
sudo apt install python3-venv
```
Make a python virtual environment with the following command:
```bash
python3 -m venv .venv
```
activate the environment
```bash
source .venv/bin/activate
```

## Install dependencies
Install the required packages with the following command:
```bash
pip install -r requirements.txt
```
## Running the backend
To run the backend server, use the following command:

```bash
uvicorn app.main:app --reload
```

The app will start:

```bash
http://127.0.0.1:8000/
```

Once the application is running, you can access the API documentation provided by Swagger at:

```bash
http://127.0.0.1:8000/docs
```

Here, you can explore and interact with the various API endpoints.

# ORM
SQLAlchemy

# Make changes in the database
execute the following command
```bash
./push.sh
```

## Authentication
using supabase authentication

- SMTP
  Using Gmail custom smtp (smtp.gmail.com) and therefore can handle 1100 user mail authentication in 1 hour
  

