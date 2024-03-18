from django.conf import settings
import docx


def extract_text_from_docx(docx_file):
    """Extracts text content from a DOCX file.

    Raises ValueError if the file is not a valid DOCX or there's a processing error.

    Args:
        docx_file: File object to extract text from (Any, likely io.BytesIO).

    Returns:
        Extracted text content as a string.
    """
    if not docx_file.content_type.startswith('application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
        raise ValueError('Uploaded file is not a valid DOCX document.')

    try:
        doc = docx.Document(docx_file)
        full_text = []
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text.strip())
        return '\n'.join(full_text)
    except Exception as e:
        raise ValueError(f'Error processing DOCX file: {e}')


def hash_text_to_int(text: str) -> int:
    """Hashes text to a 32-bit integer using hash and bitmasking.

    Args:
        text: Text to hash (str).

    Returns:
        32-bit integer representation of the hash value.
    """

    hashed_value = hash(text)
    return hashed_value & (2**32 - 1)