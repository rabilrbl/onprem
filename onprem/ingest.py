# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_ingest.ipynb.

# %% auto 0
__all__ = ['chunk_size', 'chunk_overlap', 'LOADER_MAPPING', 'DEFAULT_DB', 'MyElmLoader', 'load_single_document', 'load_documents',
           'process_documents', 'does_vectorstore_exist', 'Ingester']

# %% ../nbs/01_ingest.ipynb 3
import os
import os.path
import glob
from typing import List
from dotenv import load_dotenv
from multiprocessing import Pool
from tqdm import tqdm

from langchain.document_loaders import (
    CSVLoader,
    EverNoteLoader,
    PyMuPDFLoader,
    TextLoader,
    UnstructuredEmailLoader,
    UnstructuredEPubLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
)

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
import chromadb
from chromadb.config import Settings
chunk_size = 500
chunk_overlap = 50

# %% ../nbs/01_ingest.ipynb 4
class MyElmLoader(UnstructuredEmailLoader):
    """Wrapper to fallback to text/plain when default does not work"""

    def load(self) -> List[Document]:
        """Wrapper adding fallback for elm without html"""
        try:
            try:
                doc = UnstructuredEmailLoader.load(self)
            except ValueError as e:
                if 'text/html content not found in email' in str(e):
                    # Try plain text
                    self.unstructured_kwargs["content_source"]="text/plain"
                    doc = UnstructuredEmailLoader.load(self)
                else:
                    raise
        except Exception as e:
            # Add file_path to exception message
            raise type(e)(f"{self.file_path}: {e}") from e

        return doc

# %% ../nbs/01_ingest.ipynb 5
# Map file extensions to document loaders and their arguments
LOADER_MAPPING = {
    ".csv": (CSVLoader, {}),
    # ".docx": (Docx2txtLoader, {}),
    ".doc": (UnstructuredWordDocumentLoader, {}),
    ".docx": (UnstructuredWordDocumentLoader, {}),
    ".enex": (EverNoteLoader, {}),
    ".eml": (MyElmLoader, {}),
    ".epub": (UnstructuredEPubLoader, {}),
    ".html": (UnstructuredHTMLLoader, {}),
    ".md": (UnstructuredMarkdownLoader, {}),
    ".odt": (UnstructuredODTLoader, {}),
    ".pdf": (PyMuPDFLoader, {}),
    ".ppt": (UnstructuredPowerPointLoader, {}),
    ".pptx": (UnstructuredPowerPointLoader, {}),
    ".txt": (TextLoader, {"encoding": "utf8"}),
    # Add more mappings for other file extensions and loaders as needed
}


def load_single_document(file_path: str) -> List[Document]:
    ext = "." + file_path.rsplit(".", 1)[-1].lower()
    if ext in LOADER_MAPPING:
        loader_class, loader_args = LOADER_MAPPING[ext]
        loader = loader_class(file_path, **loader_args)
        return loader.load()

    raise ValueError(f"Unsupported file extension '{ext}'")

def load_documents(source_dir: str, ignored_files: List[str] = []) -> List[Document]:
    """
    Loads all documents from the source documents directory, ignoring specified files
    """
    all_files = []
    for ext in LOADER_MAPPING:
        all_files.extend(
            glob.glob(os.path.join(source_dir, f"**/*{ext.lower()}"), recursive=True)
        )
        all_files.extend(
            glob.glob(os.path.join(source_dir, f"**/*{ext.upper()}"), recursive=True)
        )
    filtered_files = [file_path for file_path in all_files if file_path not in ignored_files]

    with Pool(processes=os.cpu_count()) as pool:
        results = []
        with tqdm(total=len(filtered_files), desc='Loading new documents', ncols=80) as pbar:
            for i, docs in enumerate(pool.imap_unordered(load_single_document, filtered_files)):
                results.extend(docs)
                pbar.update()

    return results

def process_documents(source_directory:str, ignored_files: List[str] = [], ) -> List[Document]:
    """
    Load documents and split in chunks
    """
    print(f"Loading documents from {source_directory}")
    documents = load_documents(source_directory, ignored_files)
    if not documents:
        print("No new documents to load")
        return
    print(f"Loaded {len(documents)} new documents from {source_directory}")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} chunks of text (max. {chunk_size} tokens each)")
    return texts

def does_vectorstore_exist(persist_directory: str, embeddings: HuggingFaceEmbeddings) -> bool:
    """
    Checks if vectorstore exists
    """
    db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    if not db.get()['documents']:
        return False
    return True

# %% ../nbs/01_ingest.ipynb 6
from typing import Any, Dict, Generator, List, Optional, Tuple, Union
from .utils import get_datadir
os.environ['TOKENIZERS_PARALLELISM'] = '0'
DEFAULT_DB = 'vectordb'

class Ingester:
    def __init__(self,
                 embedding_model_name:str ='sentence-transformers/all-MiniLM-L6-v2',
                 embedding_model_kwargs:dict ={'device': 'cpu'}
                ):
        """
        Ingests all documents in `source_folder` (previously-ingested documents are ignored)

        **Args**:
          - *embedding_model*: name of sentence-transformers model
          - *embedding_model_kwargs*: arguments to embedding model (e.g., `{device':'cpu'}`)

        **Returns**: `None`
        """
        self.persist_directory = os.path.join(get_datadir(), DEFAULT_DB)
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
        self.chroma_settings = Settings(persist_directory=self.persist_directory,anonymized_telemetry=False)
        self.chroma_client = chromadb.PersistentClient(settings=self.chroma_settings , path=self.persist_directory)
        return
     
    
    def get_db(self):
        db = None
        if does_vectorstore_exist(self.persist_directory, self.embeddings):
            db = Chroma(persist_directory=self.persist_directory, 
                        embedding_function=self.embeddings, 
                        client_settings=self.chroma_settings, client=self.chroma_client)
        return db
            
    
    def ingest(self,
               source_directory:str, 
              ):
        """
        Ingests all documents in `source_folder` (previously-ingested documents are ignored)

        **Args**:

          - *source_directory*: path to folder containing document store

        **Returns**: `None`
        """

        if not os.path.exists(source_directory):
            raise ValueError('The source_directory does not exist.')
        texts = None
        db = self.get_db()
        if db:
            # Update and store locally vectorstore
            print(f"Appending to existing vectorstore at {self.persist_directory}")
            collection = db.get()
            texts = process_documents(source_directory, 
                                      ignored_files=[metadata['source'] for metadata in collection['metadatas']])
            if texts:
                print(f"Creating embeddings. May take some minutes...")
                db.add_documents(texts)
        else:
            # Create and store locally vectorstore
            print("Creating new vectorstore")
            texts = process_documents(source_directory)
            if texts:
                print(f"Creating embeddings. May take some minutes...")
                db = Chroma.from_documents(texts, 
                                           self.embeddings, persist_directory=self.persist_directory, 
                                           client_settings=self.chroma_settings, client=self.chroma_client)
        if texts:
            db.persist()
            print(f"Ingestion complete! You can now query your documents using the prompt method")
        db = None
        return
