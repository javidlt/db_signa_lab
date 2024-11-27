from fastapi import FastAPI, Request
from routes import users, tweets, hashtags
from db import DB

app = FastAPI()
app.include_router(users.router)
app.include_router(tweets.router)
app.include_router(hashtags.router)

db_instance = DB()

@app.on_event("startup")
async def startup_event():
    # db_instance.connect_cassandra()
    db_instance.connect_mongo()
    db_instance.connect_dgraph()
    app.state.db = db_instance

@app.middleware("http")
async def lifespan_middleware(request: Request, call_next):
    response = await call_next(request)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)