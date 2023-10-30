import langchain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import ReadTheDocsLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()
langchain.debug = True
embeddings = OpenAIEmbeddings()


def ingest_html_docs(path):
    loader = ReadTheDocsLoader(
        path=path,
        custom_html_tag=('div', {'id': 'main'}),
        features='lxml'
    )
    documents = loader.load()
    print(f'loaded {len(documents)} documents')

    for doc in documents:
        current_path = doc.metadata['source']
        real_url = current_path.replace('../aws_kendra_docs/', 'https://')
        doc.metadata.update({'source': real_url})

    return documents


def split_docs(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400,
                                                   chunk_overlap=50,
                                                   separators=['\n\n', '\n', ' ', ''])
    doc_chunks = text_splitter.split_documents(documents=documents)

    print(f'documents chunk length: {len(doc_chunks)} chunks')
    return doc_chunks


def create_faiss_local_index(documents):
    db = FAISS.from_documents(documents=documents, embedding=embeddings)
    db.save_local(folder_path='./', index_name='aws_kendra_index')


if __name__ == '__main__':
    docs = ingest_html_docs('../aws_kendra_docs/docs.aws.amazon.com/kendra/latest')
    chunks = split_docs(documents=docs)
    create_faiss_local_index(documents=chunks)