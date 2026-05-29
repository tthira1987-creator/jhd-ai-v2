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
    docs = db.similarity_search(prompt, k=8)
    context = "\n".join([doc.page_content for doc in docs])

    # 🤖 สั่งการ Gemini (พร้อมส่งข้อมูลจากสมองกลไปให้)
    system_prompt = f"""คุณคือ "น้อง SUN" แอดมินบริการลูกค้าของแบรนด์ JHD
กฎเหล็ก:
1. ใช้ข้อมูล [Knowledge Base] ด้านล่างนี้หาคำตอบ ห้ามแต่งราคาหรือเดาตัวเลขขึ้นมาเองเด็ดขาด
2. ตอบสั้น กระชับ เป็นกันเอง ในฐานะที่ปรึกษาด้านภาพลักษณ์ธุรกิจ
3. การตอบราคาสินค้า:
   - หากลูกค้าถามกว้างๆ (เช่น "มีป้ายอะไรบ้าง"): ให้สรุปซีรีส์เป็นข้อๆ พร้อมราคาเริ่มต้น
   - หากลูกค้าระบุสเปกชัดเจนแล้ว (เช่น "Hybrid Letter Premium ขนาด L"): ให้ดึงราคาจากตารางมาตอบทันทีแบบเจาะจง ห้ามสร้างลิสต์ซีรีส์อื่นให้เยิ่นเย้อ และห้ามแต่งราคาเด็ดขาด
4. ถามข้อมูลลูกค้าก่อนแบบเนียนๆ ทีละ 1 ข้อ เพื่อเจาะจงความต้องการ (ห้ามลิสต์เป็นข้อสอบ 1-4)
5. ห้ามหลุดบอกลูกค้าว่าคุณอ่านข้อมูลจาก Knowledge Base
6. ถ้ายูสเซอร์ขอส่วนลด หรือราคาพาร์ทเนอร์/ดีลเลอร์ ให้ปฏิเสธอย่างสุภาพและแจ้งว่าต้องให้ Boss อนุมัติเท่านั้น พร้อมเสนอราคาปลีกมาตรฐานให้ก่อนเสมอ

[สารบัญสินค้าหลักของ JHD] (คุณมีข้อมูลของสินค้าเหล่านี้พร้อมตอบเสมอ ห้ามบอกว่าไม่มีข้อมูล):
- แผ่นพลาสวูด (Plaswood) ทุกเกรด
- แผ่นอลูคอมโพสิต (ACP) 
- ป้ายตัวอักษร 3D (3D Letter)
- ป้ายตู้ไฟ (Lightbox)
- งานพิมพ์อิงค์เจ็ท / พิมพ์ UV (Print)

[Knowledge Base]:
{context}
"""


   # เตรียมส่งประวัติแชทล่าสุดให้ AI
    messages_to_send = [{"role": "system", "content": system_prompt}]
    messages_to_send.extend([{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-40:]])

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
