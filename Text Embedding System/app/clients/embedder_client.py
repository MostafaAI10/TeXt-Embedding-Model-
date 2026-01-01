from sentence_transformers import SentenceTransformer
import numpy as np
from app.config import EMBEDDING_MODEL

_model = None

def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model

def encode(texts):
    """
    Encode text(s) and return L2-normalized float32 vectors.
    Accepts str or List[str]; returns np.ndarray (n, d) or (d,) if single.
    """
    single = False
    if isinstance(texts, str):
        texts = [texts]
        single = True

    model = _get_model()
    emb = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)

    norms = np.linalg.norm(emb, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    emb = emb / norms
    emb = emb.astype("float32")

    return emb[0] if single else emb
