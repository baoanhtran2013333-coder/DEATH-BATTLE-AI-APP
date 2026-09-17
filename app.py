import streamlit as st
from groq import Groq

st.set_page_config(page_title="Death Battle AI Master", page_icon="⚔️", layout="wide")

st.title("⚔️ Death Battle AI Master (Endless Fictional & DBVN 2.5 Standard)")
st.caption("AI tra cứu Feat, Hax, Meta Debate từ Endless Fictional, DBVN 2.5 và TikTok Death Battle VN.")

default_api_key = st.secrets.get("GROQ_API_KEY", "")

with st.sidebar:
    st.header("⚙️ Cấu hình")
    user_api_key = st.text_input(
        "Dùng API Key Groq (Tùy chọn):", 
        value="", 
        type="password",
        help="Dán API Key gsk_... lấy miễn phí từ console.groq.com vào đây."
    )
    if st.button("🔄 Tạo kèo đấu mới"):
        st.session_state.chat_messages = []
        st.rerun()

api_key = user_api_key.strip() or default_api_key

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

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Nhập kèo đấu hoặc gửi phản biện/scan/bằng chứng cho AI..."):
    if not api_key:
        st.error("Vui lòng dán Groq API Key (bắt đầu bằng gsk_...) vào ô cấu hình bên trái!")
    else:
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("AI đang tra cứu Feat & Meta Debate từ cộng đồng VN..."):
                try:
                    client = Groq(api_key=api_key)

                    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                    for m in st.session_state.chat_messages[-4:]:
                        messages.append({"role": m["role"], "content": m["content"]})

                    # Dùng model llama3-8b-8192 cố định của Groq
                    response = client.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=messages,
                        temperature=0.7
                    )

                    bot_reply = response.choices[0].message.content
                    st.markdown(bot_reply)
                    st.session_state.chat_messages.append({"role": "assistant", "content": bot_reply})

                except Exception as e:
                    st.error(f"Lỗi API Groq: {e}")
