import chromadb
from pdf_extractor import extract_text_from_pdf

client = chromadb.PersistentClient(path='./db')
collection = client.create_collection('legal_docs')

pdf_text = extract_text_from_pdf("./json-to-pdf.pdf")

collection.add(
    documents=[pdf_text],
    # metadata={'title': 'Constitution of the India'},
    ids=["doc_2"]
)

print("Document added successfully!", collection.get("doc_1"))