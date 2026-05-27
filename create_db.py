import os
import glob
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import MarkdownTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

print("⏳ กำลังโหลดโมเดลภาษา (ฟรี)...")
# ใช้โมเดลฟรีที่รองรับภาษาไทยได้ดีเยี่ยม
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

print("⏳ กำลังอ่านไฟล์ .md ทั้งหมด...")
docs = []
# สแกนหาไฟล์ .md ทั้งหมดในโฟลเดอร์โดยอัตโนมัติ
md_files = glob.glob("*.md")

for file in md_files:
    try:
        loader = TextLoader(file, encoding="utf-8")
        docs.extend(loader.load())
        print(f"✅ อ่านไฟล์ {file} สำเร็จ")
    except Exception as e:
        print(f"⚠️ อ่านไฟล์ {file} ไม่ได้: {e}")

print(f"\nรวมไฟล์ที่อ่านได้ทั้งหมด: {len(md_files)} ไฟล์")

print("\n⏳ กำลังหั่นข้อความและสร้างสมองกล (Vector Database)...")
text_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=100)
splits = text_splitter.split_documents(docs)

vectorstore = Chroma.from_documents(
    documents=splits, 
    embedding=embeddings, 
    persist_directory="./jhd_vectordb" # สร้างเป็นโฟลเดอร์ฐานข้อมูล
)

print("\n🎉 สร้างฐานข้อมูลเสร็จสมบูรณ์! โฟลเดอร์ 'jhd_vectordb' ถูกสร้างขึ้นแล้วครับ")