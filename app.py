import streamlit as st
from groq import Groq

# Cấu hình trang Streamlit
st.set_page_config(page_title="Death Battle AI Master", page_icon="⚔️", layout="wide")

st.title("⚔️ Death Battle AI Master (Endless Fictional & DBVN 2.5 Standard)")
st.caption("AI tra cứu Feat, Hax, Meta Debate từ Endless Fictional, DBVN 2.5 và TikTok Death Battle VN.")

# Tự động lấy API Key từ Streamlit Secrets
api_key = st.secrets.get("GROQ_API_KEY", "")

with st.sidebar:
    st.header("⚙️ Tùy chọn")
    if st.button("🔄 Tạo kèo đấu mới", use_container_width=True):
        st.session_state.chat_messages = []
        st.rerun()

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

# Hiển thị lịch sử chat
for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Danh sách model chuẩn đang hoạt động trên Groq
GROQ_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile"
]

if prompt := st.chat_input("Nhập kèo đấu hoặc gửi phản biện/scan/bằng chứng cho AI..."):
    if not api_key:
        st.error("⚠️ Chưa cài đặt GROQ_API_KEY trong Streamlit Secrets!")
    else:
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("AI đang tra cứu Feat & Meta Debate từ cộng đồng VN..."):
                client = Groq(api_key=api_key)
                messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                for m in st.session_state.chat_messages[-4:]:
                    messages.append({"role": m["role"], "content": m["content"]})

                success = False
                last_error = ""

                # Thử lần lượt các model Groq chuẩn
                for model_name in GROQ_MODELS:
                    try:
                        response = client.chat.completions.create(
                            model=model_name,
                            messages=messages,
                            temperature=0.7
                        )
                        if response and response.choices:
                            bot_reply = response.choices[0].message.content
                            st.markdown(bot_reply)
                            st.session_state.chat_messages.append({"role": "assistant", "content": bot_reply})
                            success = True
                            break
                    except Exception as e:
                        last_error = str(e)
                        continue

                if not success:
                    st.error(f"Lỗi API Groq: {last_error}")
