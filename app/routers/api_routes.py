from pgvector.psycopg import register_vector
import psycopg
from fastapi import APIRouter, File, UploadFile, status
import pandas as pd
from .functions import extract_features
import numpy as np

router = APIRouter()
df = pd.read_csv("./app/static/headless data preprocessed.csv")
conn = psycopg.connect(dbname='vector_embeddings', user = "postgres", password = "password",host = "172.17.0.2", port = 8000, autocommit=True, )
register_vector(conn)

bucket_url = "https://d3otl31mwgzea2.cloudfront.net/recommendation_system/"

@router.post("/", tags=["visual_search_recommendations"])
async def get_visual_recommendations(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        if contents:
            
            temp_path = "./app/static/temp.jpg"
            with open(temp_path, "wb") as f:
                f.write(contents)
        
            query = extract_features(temp_path)
            confidence_score = 0.67
            result = conn.execute('SELECT 1 - (embedding <=> %s) AS cosine_similarity, id, base_path FROM recommendation_system WHERE 1 - (embedding <=> %s) > %s ORDER BY cosine_similarity DESC', (query, query, confidence_score)).fetchall()
            bucket_path = []
            for element in result:
                bucket_path.append(bucket_url + str(element[2]).replace("\\", "/"))
                      
            filtered_df = df[df['image'].isin(bucket_path)]
            filtered_df = filtered_df.replace(['Unknown', np.nan], None)
        
            return {"message": "Success", "result": filtered_df.drop(['text_features', 'text_embeddings'], axis=1).to_dict(orient='records'), "status": str(status.HTTP_200_OK)}
    
    except Exception as e:
            return {"message": f"No product found for the given image", "result": [], "status": str(status.HTTP_400_BAD_REQUEST)} 