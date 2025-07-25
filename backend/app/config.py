import os

# Paths for storing PDFs and vector indexes
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data", "documents")
EMBEDDING_INDEX_DIR = os.path.join(BASE_DIR, "..", "embeddings", "index")

# Model config
LOCAL_MODEL_NAME = "gpt2"  # or your local model folder/name

# Embedding dimension for your vector index (adjust if needed)
EMBEDDING_DIM = 1536

# Other config constants
MAX_TOKENS_PER_CHUNK = 500
TOP_K_RESULTS = 5
