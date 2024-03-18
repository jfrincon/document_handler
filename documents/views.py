from django.shortcuts import render
from .forms import DocumentForm
from documents.utils.qdrant_utils import save_document, check_collections, search_document
from documents.utils.utils import hash_text_to_int, extract_text_from_docx
from documents.utils.langchain_utils import generate_embedding
from django.contrib import messages

def upload_document(request):
    """Handles document upload via POST request.

    Processes uploaded DOCX file, extracts text, generates embedding,
    saves to Qdrant, and redirects on success. Renders upload form on GET.

    Args:
        request: Incoming HTTP request object (HttpRequest).

    Returns:
        HttpResponseRedirect on success, rendered template on GET (HttpResponse).
    """
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save(commit=False) 
                document_text = extract_text_from_docx(request.FILES['file'])
                file_name = request.FILES['file'].name
                hashed_id = hash_text_to_int(document_text)
                embedding_data = generate_embedding(document_text)
                check_collections()
                save_document(embedding_data, file_name, hashed_id)
                # Success message on successful upload
                message = 'file:{} uploaded successfully'.format(file_name)
                messages.success(request, message)
            except Exception as e:  # Catch potential errors during upload processing
                messages.error(request, f'An error occurred: {str(e)}')
            
        else:
            messages.error(request, 'There were errors in the form.')
    else:
        form = DocumentForm()

    return render(request, 'documents/upload.html', {'form': form})


def search(request):
    """Handles document search via POST request.

    Processes search query, generates embedding, searches Qdrant,
    and renders search results. Renders search form on GET.

    Args:
        request: Incoming HTTP request object (HttpRequest).

    Returns:
        Rendered template with search results on POST, search form on GET (HttpResponse).
    """
    if request.method == 'POST':
        text = request.POST.get('text')
        embedded_text = generate_embedding(text)
        processed_text = search_document(embedded_text)
        return render(request, 'documents/search.html', {'processed_text': processed_text})  # Render the result template
    else:
        return render(request, 'documents/search.html')  # Render the form template
