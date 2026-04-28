from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
from sentence_transformers import SentenceTransformer

#  connexion à Milvus (localhost car script hors Docker)
connections.connect(host="milvus", port="19530")

model = SentenceTransformer("all-MiniLM-L6-v2")

#  schema
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
    FieldSchema(name="name", dtype=DataType.VARCHAR, max_length=200)
]

schema = CollectionSchema(fields)

#  créer collection 
collection = Collection("chess_openings", schema)

#  données
openings = [
    "King's Pawn Opening e4",
    "Queen's Gambit d4 c4",
    "Sicilian Defense c5",
    "French Defense e6",
    "Caro-Kann Defense c6"
]

vectors = model.encode(openings).tolist()

collection.insert([vectors, openings])
collection.flush()

print(" Data inserted")