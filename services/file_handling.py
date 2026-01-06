from langchain_community.document_loaders import (
    PyPDFLoader, 
    TextLoader, 
    UnstructuredWordDocumentLoader
)

def get_loader(file_path):
    ext = file_path.split('.')[-1].lower()
    if ext == 'pdf':
        return PyPDFLoader(file_path)
    elif ext == 'docx':
        return UnstructuredWordDocumentLoader(file_path)
    else:
        return TextLoader(file_path)