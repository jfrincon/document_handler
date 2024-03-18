from qdrant_client.http.models import PointStruct
from qdrant_client.http.models import Distance, VectorParams
from django.conf import settings

def check_collections():
    """Ensures a Qdrant collection exists, creating it if necessary."""
    client = settings.QDRANT_CLIENT
    #check if collection exists
    try:
        # Try to get information about the collection
        client.get_collection(settings.COLLECTION_NAME)
        print(f"Collection exists.")
    except Exception as e:
        if e.status_code == 404:
            #if it doesn't exist creates one
            client.recreate_collection(
                collection_name="embed_collection",
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )
            print(f"Collection '{settings.COLLECTION_NAME}' did not exist.")
        else:
            print(f"Error getting collection information: {e}")

def save_document(embeddings, file_name: str, hashed_id: str):
    """Saves document embedding to Qdrant.

    Args:
        embeddings: Document embedding.
        file_name: Document filename (str).
        hashed_id: Unique document identifier (str).

    Returns:
        Qdrant operation information.
    """
    document_point = PointStruct(
        id=hashed_id,
        vector=embeddings, 
        payload={'name':file_name}
    )
    client = settings.QDRANT_CLIENT
    operation_info = client.upsert(
        collection_name=settings.COLLECTION_NAME,
        wait=True,
        points=[
            document_point
        ],
    )
    return operation_info

def search_document(embedding) -> str:
    """Searches for top 3 similar documents to embedding in Qdrant.

    Args:
    embedding: Document embedding.

    Returns:
    Formatted string with top 3 similar documents and scores.
    """
    client = settings.QDRANT_CLIENT
    search_result = client.search(
        collection_name=settings.COLLECTION_NAME,
        query_vector=embedding,
        limit=3,
    )
    answer = "The most similar files that we found are:\n"
    idx = 1
    for result in search_result:
        file_name = result.payload['name']
        score = result.score
        sentence = "{}th {} with a score of {}\n".format(idx, file_name, score)
        idx+=1
        answer += sentence
    print(answer)
    return answer


