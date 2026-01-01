from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

PERSIST_DIR = DATA_DIR / "chroma"
PERSIST_DIR.mkdir(exist_ok=True)


ENTRIES_FILE = DATA_DIR / "entries.json"


CHROMA_COLLECTION = "text_vector_collection"


EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"


DEFAULT_TOP_K = 5
DEFAULT_MIN_SIMILARITY = 0.4  

# Chunking (characters)
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
