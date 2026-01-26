#from langchain.document_loaders import DirectoryLoader
#from  langchain_community.document_loaders import DirectoryLoader
import os
from typing import Optional, List, Any

import gradio as gr
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.document_loaders import DirectoryLoader
from langchain.prompts import PromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms.base import LLM

from modelscope import AutoTokenizer, AutoModel
from langchain.prompts import PromptTemplate

import sqlite3,os
from langchain.schema import Document


def load_embedding_model(model_name="ernie-tiny"):
    """
    加载embedding模型
    :param model_name:
    :return:
    """
    encode_kwargs = {"normalize_embeddings": False}
    model_kwargs = {"device": "cuda:0"}
    return HuggingFaceEmbeddings(
        model_name="/root/bak/model/model",
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

conn = sqlite3.connect('auth.db')
# 创建一个Cursor:
cursor = conn.cursor()
cursor.execute('''SELECT id,
       module_name,
       file_name,
       file_content
  FROM android_example;''') 

rows = cursor.fetchall()
ids = [str(i) for i in range(len(rows))]
texts = []
metadata = []
for row in rows:
    texts.append(Document(page_content=row[3], metadata={"module_name": row[1],"file_name": row[2]}))
    #metadata.append()
    

embeddings = load_embedding_model('')



db = Chroma.from_documents(
    documents=texts,  # 直接传入字符串列表
    embedding=embeddings,
    ids=ids,
    persist_directory="./chroma_db2"
)

db.persist()


# 关闭连接
cursor.close()
conn.close()

