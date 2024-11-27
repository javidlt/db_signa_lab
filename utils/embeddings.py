def generateEmbedding(mod, text):
    embedding = mod.encode(str(text)).tolist()
    return embedding

def dotProduct(embedding1,embedding2):
  result = 0
  for e1, e2 in zip(embedding1, embedding2):
    result += e1*e2
  return result