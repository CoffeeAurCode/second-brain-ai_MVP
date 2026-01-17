from embeddings import embed
vector = embed("Gradient descent is an optimization algorithm")
print(type(vector))
print(len(vector))
print(vector[:5])