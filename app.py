import streamlit as st
from groq import Groq

# 1. Cấu hình trang Streamlit
st.set_page_config(page_title="Death Battle AI Master", page_icon="⚔️", layout="wide")

st.title("⚔️ Death Battle AI Master (Endless Fictional & DBVN 2.5 Standard)")
st.caption("AI tra cứu Feat, Hax, Meta Debate từ Endless Fictional, DBVN 2.5 và TikTok Death Battle VN.")

# 2. Tự động lấy API Key từ Streamlit Secrets
api_key = st.secrets.get("GROQ_API_KEY", "")

with st.sidebar:
    st.header("⚙️ Tùy chọn")
    if st.button("🔄 Tạo kèo đấu mới", use_container_width=True):
        st.session_state.chat_messages = []
        st.session_state.battle_submitted = False
        st.rerun()

# 3. System Prompt chuẩn VS Debating VN
SYSTEM_PROMPT = """
Bạn là "Death Battle Master AI" - Một Master Debater kỳ cựu mang tư duy và chuẩn mực từ các cộng đồng Versus Debating lớn nhất Việt Nam:
1. Group Facebook "Death Battle VN 2.5" (DBVN 2.5)
2. Group Facebook "Endless Fictional" (EF)
3. Cộng đồng TikTok Death Battle VN

NHIỆM VỤ & PHONG CÁCH PHÂN TÍCH:
1. Áp dụng quy chuẩn Scaling và meta debate tại các group VS Debating Việt Nam (EF, DBVN 2.5, TikTok DBVN) kết hợp VSBattles Wiki.
2. Tra cứu Feat, Anti-feat, Statement, Hax, Resistance và các trận debate kinh điển tại Việt Nam.
3. Sẵn sàng phản biện lại NLF, Wank/Highball hoặc Downplay. Khách quan ghi nhận scan/proof chuẩn.

CẤU TRÚC PHÂN TÍCH CHUẨN:
1. STATS OVERVIEW (AP/Durability/Speed Tier)
2. HAX & RESISTANCE ANALYSIS
3. VN COMMUNITY META & DEBATE FEATS
4. BATTLE SCENARIO
5. FINAL VERDICT (% Victory + Winner)
"""

# Khởi tạo Session State
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []
if "battle_submitted" not in st.session_state:
    st.session_state.battle_submitted = False

# Kiểm tra nếu chưa cấu hình Secrets
if not api_key:
    st.error("⚠️ Hệ thống chưa cài đặt GROQ_API_KEY trong Streamlit Secrets! Vui lòng cấu hình Secrets trên Streamlit Cloud.")
    st.stop()

# ----------------------------------------------------
# BƯỚC 1: FORM NHẬP KÈO ĐẤU
# ----------------------------------------------------
if not st.session_state.battle_submitted:
    st.subheader("📋 Bước 1: Thiết lập kèo đấu")
    
    with st.form("battle_form"):
        col1, col2 = st.columns(2)
        with col1:
            char1 = st.text_input("Nhân vật 1:", placeholder="Ví dụ: Gojo Satoru")
        with col2:
            char2 = st.text_input("Nhân vật 2:", placeholder="Ví dụ: Saitama")
            
        condition = st.text_area("Điều kiện đấu (Form, vị trí, bloodlust...):", placeholder="Ví dụ: Equal speed, bloodlust, địa điểm ở Trái Đất")
        
        submit_btn = st.form_submit_button("🚀 Gửi & Phân tích")
        
    if submit_btn:
        if not char1.strip() or not char2.strip():
            st.warning("Vui lòng nhập tên cả 2 nhân vật!")
        else:
            initial_prompt = f"BATTLE: {char1.strip()} VS {char2.strip()}\nĐIỀU KIỆN: {condition.strip() if condition.strip() else 'Tiêu chuẩn (Standard / No Prep)'}"
            st.session_state.chat_messages.append({"role": "user", "content": initial_prompt})
            st.session_state.battle_submitted = True
            st.rerun()

# ----------------------------------------------------
# BƯỚC 2: HIỂN THỊ PHÂN TÍCH & PHẢN BIỆN LẦN LƯỢT
# ----------------------------------------------------
else:
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if st.session_state.chat_messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("AI đang tra cứu Feat & Meta Debate từ cộng đồng VN..."):
                try:
                    client = Groq(api_key=api_key)
                    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                    
                    for m in st.session_state.chat_messages[-6:]:
                        messages.append({"role": m["role"], "content": m["content"]})

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=messages,
                        temperature=0.7
                    )

                    bot_reply = response.choices[0].message.content
                    st.markdown(bot_reply)
                    st.session_state.chat_messages.append({"role": "assistant", "content": bot_reply})
                    st.rerun()

                except Exception as e:
                    st.error(f"Lỗi API: {e}")

    if prompt := st.chat_input("Gửi thêm phản biện, bằng chứng hoặc câu hỏi tiếp theo..."):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        st.rerun()
