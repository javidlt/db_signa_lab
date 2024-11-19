from fastapi import FastAPI
from db import init_db
from routes import router

app = FastAPI(title="FastAPI Cassandra App")

@app.on_event("startup")
async def startup_event():
    init_db()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)