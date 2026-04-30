from pymilvus import (
    connections,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
    utility,
)
from sentence_transformers import SentenceTransformer

print("Script lancé")

connections.connect(host="milvus", port="19530")

model = SentenceTransformer("all-MiniLM-L6-v2")

COLLECTION_NAME = "chess_openings"

# CLEAN
if utility.has_collection(COLLECTION_NAME):
    utility.drop_collection(COLLECTION_NAME)
    print("Old collection deleted")

# SCHEMA
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
    FieldSchema(name="name", dtype=DataType.VARCHAR, max_length=100),
]

schema = CollectionSchema(fields)

collection = Collection(COLLECTION_NAME, schema)

# DATA SIMPLE
openings = [
    "e4 e5",
    "e4 c5",
    "e4 e6",
    "e4 c6",
    "d4 d5",
    "d4 Nf6 c4"
]

vectors = model.encode(openings).tolist()

collection.insert([vectors, openings])
collection.flush()

print("Data inserted")

#  INDEX
collection.create_index(
    field_name="embedding",
    index_params={
        "metric_type": "COSINE",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 128}
    }
)

print("Index created")

#  LOAD
collection.load()

print("Collection loaded")

print("Total entities:", collection.num_entities)