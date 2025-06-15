import asyncio
import bs4
from langchain_community.document_loaders import WebBaseLoader
from openai import OpenAI
from dotenv import load_dotenv
from langchain_unstructured import UnstructuredLoader

from typing import List
from langchain_core.documents import Document
from collections import defaultdict

from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

client = OpenAI()

page_urls = [
    "https://docs.chaicode.com/youtube/getting-started/",
    "https://docs.chaicode.com/youtube/chai-aur-html/welcome/",
    "https://docs.chaicode.com/youtube/chai-aur-html/introduction/",
    "https://docs.chaicode.com/youtube/chai-aur-html/emmit-crash-course/",
    "https://docs.chaicode.com/youtube/chai-aur-html/html-tags/",
]

page_url = "https://docs.chaicode.com/youtube/getting-started/"

#loader = WebBaseLoader(web_paths=[page_url])
docs = []
async def load_and_process_docs():
    async for doc in loader.alazy_load():
        docs.append(doc)
    
    for doc in docs[:5]:
        print(doc.page_content)


async def _get_setup_docs_from_url(url: str) -> List[Document]:
    loader = UnstructuredLoader(web_url=url)

    setup_docs = []
    parent_id = -1
    async for doc in loader.alazy_load():
        if doc.metadata["category"] == "Title":
            parent_id = doc.metadata["element_id"]
        if doc.metadata.get("parent_id") == parent_id:
            setup_docs.append(doc)

    return setup_docs

async def load_and_process_docs():
    setup_docs = []
    for url in page_urls:
        page_setup_docs = await _get_setup_docs_from_url(url)
        setup_docs.extend(page_setup_docs)

    setup_text = defaultdict(str)

    for doc in setup_docs:
        url = doc.metadata["url"]
        setup_text[url] += f"{doc.page_content}\n"

    dict(setup_text)

    print(dict(setup_text))

    
if __name__ == "__main__":
    # Run the async function
    asyncio.run(load_and_process_docs())