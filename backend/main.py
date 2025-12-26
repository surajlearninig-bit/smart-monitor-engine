from fastapi import FastAPI
import redis
import psycopg2
import os

app = FastAPI()

# Database & Redis Connections (Problem Solving: Using Env variables)
DB_HOST = os.getenv("DB_HOST", "localhost")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

@app.get("/")
def read_root():
    return {"message": "Smart Monitor API is Running"}

@app.get("/test-db")
def test_db():
    try:
        conn = psycopg2.connect(host=DB_HOST, database="mydb", user="user", password="password")
        return {"status": "PostgreSQL Connected!"}
    except Exception as e:
        return {"status": "DB Connection Failed", "error": str(e)}

@app.get("/test-redis")
def test_redis():
    try:
        r = redis.Redis(host=REDIS_HOST, port=6379)
        r.set("hits", 1)
        return {"status": "Redis Connected!", "value": r.get("hits").decode()}
    except Exception as e:
        return {"status": "Redis Connection Failed", "error": str(e)}