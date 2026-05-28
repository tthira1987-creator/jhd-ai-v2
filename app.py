__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import os
from openai import OpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="JHD Intelligence V2", page_icon="🌟")
st.title("🌟 น้อง SUN (JHD Secretary V2)")
st.caption("Status: Custom AI (RAG System)")

# 2. โหลดสมองกล (ใช้ @st.cache_resource เพื่อให้โหลดแค่ครั้งเดียว เว็บจะได้ไม่ช้า)
@st.cache_resource
def load_brain():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    db = Chroma(persist_directory="./jhd_vectordb", embedding_function=embeddings)
    return db

db = load_brain()

# 3. ดึง API Key จากระบบหลังบ้าน (Secrets)
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except:
    st.error("⚠️ ยังไม่ได้ตั้งค่า API Key ในระบบ Secrets ของ Streamlit ครับ")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")

# 4. ระบบความจำแชท
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 5. รับข้อความและประมวลผล
if prompt := st.chat_input("พิมพ์คุยกับน้อง SUN..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 🧠 ให้สมองกลค้นหาข้อมูล (ดึงมา 4 ส่วนที่ตรงกับคำถามที่สุด)
    docs = db.similarity_search(prompt, k=4)
    context = "\n".join([doc.page_content for doc in docs])

    # 🤖 สั่งการ Gemini (พร้อมส่งข้อมูลจากสมองกลไปให้)
    system_prompt = f"""คุณคือ "น้อง SUN" แอดมินบริการลูกค้าของแบรนด์ JHD
    กฎเหล็ก:
    1. ใช้ข้อมูล [Knowledge Base] ด้านล่างนี้หาคำตอบ ห้ามแต่งราคาหรือแพ็กเกจขึ้นมาเองเด็ดขาด
    2. ตอบสั้น กระชับ เป็นกันเอง กล้าประเมินราคาและเสนอแพ็กเกจทันที
    3. เมื่อลูกค้าถามหาสินค้าแบบกว้างๆ ให้สรุปรายชื่อซีรีส์จาก [Knowledge Base] มาเป็นข้อๆ (Bullet points) พร้อมราคาเริ่มต้น **แต่หากหาข้อมูลที่เกี่ยวข้องไม่พบ ห้ามแต่งชื่อสินค้าหรือเดาราคาขึ้นมาเองเด็ดขาด** ให้ถามกลับว่าลูกค้าสนใจงานหมวดไหน (เช่น แผ่นพลาสวูด หรือ แผ่นคอมโพสิต)
    4. เมื่อลูกค้าถามหาสินค้าหรือขอรายละเอียดแบบกว้างๆ ให้สรุปรายชื่อซีรีส์สินค้าหลักทั้งหมดมาเป็นข้อๆ (Bullet points) พร้อมราคาเริ่มต้นสั้นๆ ให้ลูกค้าเห็นภาพรวมก่อนเสมอ แล้วค่อยถามถามเพื่อเจาะจงความต้องการ
    5. ห้ามหลุดบอกลูกค้าว่าคุณอ่านข้อมูลจาก Knowledge Base

    [Knowledge Base]:
    {context}
    """

    # เตรียมส่งประวัติแชทล่าสุดให้ AI
    messages_to_send = [{"role": "system", "content": system_prompt}]
    messages_to_send.extend([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]])

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="google/gemini-2.5-flash",
                messages=messages_to_send,
                temperature=0.0
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"เกิดข้อผิดพลาด: {e}")
