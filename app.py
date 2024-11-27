from fastapi import FastAPI, Request
from routes import users, tweets, hashtags
from sentence_transformers import SentenceTransformer
from db import DB
from utils.embeddings import generateEmbedding

app = FastAPI()
app.include_router(users.router)
app.include_router(tweets.router)
app.include_router(hashtags.router)

db_instance = DB()

@app.on_event("startup")
async def startup_event():
    db_instance.connect_cassandra()
    db_instance.connect_mongo()
    db_instance.connect_dgraph()
    app.state.db = db_instance
    print("Conexión a bases de datos lista")
    print("Cargando modelo...")
    modelo = "intfloat/multilingual-e5-large-instruct"
    embedder = SentenceTransformer(modelo)
    embedding = generateEmbedding(embedder, "Hola, cómo estás?")
    app.state.embedder = embedder
    print(f"Modelo listo: {modelo}, {embedding}")

@app.middleware("http")
async def lifespan_middleware(request: Request, call_next):
    response = await call_next(request)
    return response