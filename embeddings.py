from sentence_transformers import SentenceTransformer
from typing import List, Union

try:
    _model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"Error loading model: {e}")
    _model = None

def embed(text: Union[str, None]) -> List[float]:
    if _model is None:
        raise RuntimeError("Model failed to initialize")
    if not text:
        text = ""
    embedding = _model.encode(text)
    return embedding.tolist()

if __name__ == "__main__":
    #Test to see if the module works alone
    test_text = "Hello, world!"
    vector = embed(test_text)
    print (f"Test input: '{test_text}'")
    print(f"Vector dimension: {len(vector)}")
    print(f"Sample values: {vector[:3]}...")