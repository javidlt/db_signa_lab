from fastapi import FastAPI
from routes import router
from db import DgraphClient

app = FastAPI(title="FastAPI Dgraph App")

@app.on_event("startup")
async def startup_event():
    # Initialize schema
    client = DgraphClient()
    client.set_schema()
    client.close()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)