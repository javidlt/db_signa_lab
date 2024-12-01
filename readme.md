
# Librerías a instalar
- fastapi
- uvicorn
- pymongo
- pydgraph
- cassandra-driver
- pandas
- torch
- sentence_transformers
```
pip install fastapi uvicorn pymongo pydgraph cassandra-driver pandas numpy==1.23.5 torch==2.1.0 sentence-transformers datetime
```

# Correr para insertar datos
- Correr contenedor dgraph, mongo y cassandra de docker
```
cd data
py populate.py
```

### Correr
- Se debe de tener acceso a internet para cargar el modelo dado que viene desde hugging face
```
uvicorn app:app --reload
```

## Correr cli
```
py cli.py
```
