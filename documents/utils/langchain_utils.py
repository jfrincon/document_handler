from django.conf import settings

def generate_embedding(text):
    """Generates an embedding for given text using LangChain embedder.

    Args:
        text: Text to embed (str).

    Returns:
        Generated embedding.
    """
    result = settings.LANGCHAIN_EMBEDDER.embed_query(text)
    return result
