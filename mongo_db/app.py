from fastapi import FastAPI
from db import get_mongo_db
from routes import router

app = FastAPI()
db = get_mongo_db()

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)