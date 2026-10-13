import requests
import os
import json
import numpy as np 
import pandas as pd
import time
from sklearn.metrics.pairwise import cosine_similarity
import joblib

def create_embedding(text_list):     
    r = requests.post("http://localhost:11434/api/embed", json={
        "model": "bge-m3",
        "input": text_list
    })
    
    data = r.json()
    
    if "error" in data:
        raise RuntimeError(f"ollama Error: {data['error']}")
    
    return data["embeddings"]
    
    # embedding = r.json()
    # ["embeddings"]
    # return embedding



jsons = os.listdir("jsons")  # List all the jsons
my_dicts = []
chunk_id = 0

for json_file in jsons:
    with open(f"jsons/{json_file}") as f:
        Content = json.load(f)
    print(f"Creating Embeddings for {json_file} ")
    #embeddings = create_embedding([c['text'] for c in Content['chunks']])
    all_texts = [c['text'] for c in Content['chunks']]
    all_embeddings = []
    
    batch_size = 5
    for i in range(0, len(all_texts), batch_size):
        batch = all_texts[i:i + batch_size]
        batch_embeddings = create_embedding(batch)
        all_embeddings.extend(batch_embeddings)
        time.sleep(0.2)
    
    for i, chunk in enumerate(Content['chunks']):
        chunk['chunk_id'] = chunk_id
        chunk['embedding'] = all_embeddings[i]
        chunk_id += 1
        my_dicts.append(chunk)       

df = pd.DataFrame.from_records(my_dicts)
# Save this dataframe
joblib.dump(df, 'embeddings.joblib')

