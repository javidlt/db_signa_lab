# Librerías a instalar
- fastapi
- uvicorn
- pymongo
- pydgraph
- cassandra-driver
- pandas
```
pip install fastapi uvicorn pymongo pydgraph cassandra-driver pandar
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