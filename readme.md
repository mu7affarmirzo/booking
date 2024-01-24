# FastAPI Project

This is a FastAPI project with Uvicorn, Alembic, and SQLAlchemy.

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/your-fastapi-project.git
cd your-fastapi-project
```

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/your-fastapi-project.git
cd your-fastapi-project
```

### 2. Create a Virtual Environment
```bash
# On Unix or MacOS
python3 -m venv venv

# On Windows
python -m venv venv
```


### 3. Activate the Virtual Environment
```bash
# On Unix or MacOS
source venv/bin/activate

# On Windows
venv\Scripts\activate
```


### 4. Install Dependencies
```bash
pip install -r requirements.txt
```


### 5. Create and Configure .env File
```bash
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
```


### 6. Run Alembic Migrations
```bash
alembic upgrade head
```


### 7. Run the FastAPI Application
```bash
uvicorn main:app --reload
```


### 8. Alembic Migrations for future use
```bash
alembic revision --autogenerate -m "Your Migration Message"
alembic upgrade head
```


### 9. Documentation
```bash
http://127.0.0.1:8000/docs
```