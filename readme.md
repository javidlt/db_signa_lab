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
pip install fastapi uvicorn pymongo pydgraph cassandra-driver pandas numpy==1.23.5 torch==2.1.0 sentence-transformers
```

# Correr para insertar datos
- Correr contenedor dgraph, mongo y cassandra de docker
```
cd data
py populate.py
```

### Correr
```
uvicorn app:app --reload
```