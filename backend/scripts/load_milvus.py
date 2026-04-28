from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
from sentence_transformers import SentenceTransformer
import json

print(" Script lancé")

# Connexion à Milvus
connections.connect("default", host="milvus", port="19530")

# Supprimer collection si existe
if utility.has_collection("openings"):
    utility.drop_collection("openings")

# Modèle embedding
model = SentenceTransformer("all-MiniLM-L6-v2")

# Charger données
with open("data/openings.json") as f:
    data = json.load(f)

texts = [item["content"] for item in data]
names = [item["name"] for item in data]

embeddings = model.encode(texts)

# Schéma
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="name", dtype=DataType.VARCHAR, max_length=100),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
]

schema = CollectionSchema(fields, "Chess openings")

collection = Collection("openings", schema)

# Insert
collection.insert([names, embeddings.tolist()])

# Index
collection.create_index(
    field_name="embedding",
    index_params={
        "metric_type": "L2",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 128}
    }
)

collection.load()

print(" Data loaded into Milvus")