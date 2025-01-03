# Running the Backend

## Virtual environment
Make a python virtual environment with the following command:
```bash
python3 -m venv .venv
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

## See the outputs.
- GET all ingredients available to a user
![ingredients](https://cyzajynbjmgjijpbdgvg.supabase.co/storage/v1/object/public/statics/user_ingredients.jpg)

- GET all recipes available to a user
![recipes](https://cyzajynbjmgjijpbdgvg.supabase.co/storage/v1/object/public/statics/user_recipes.jpg)

- AI response
![ai](https://cyzajynbjmgjijpbdgvg.supabase.co/storage/v1/object/public/statics/ai_chat.jpg)


## Env file
[Drive link for env](https://drive.google.com/file/d/1_K_W5638rK1AQlSNNzYv3ZknqWZn6VCb/view?usp=sharing)
  

