import streamlit as st
import time
from google import genai
from google.genai import types

st.set_page_config(page_title="Death Battle AI Master", page_icon="⚔️", layout="wide")

st.title("⚔️ Death Battle AI Master (Endless Fictional & DBVN 2.5 Standard)")
st.caption("AI tra cứu Feat, Hax, Meta Debate từ Endless Fictional, DBVN 2.5 và TikTok Death Battle VN.")

default_api_key = st.secrets.get("GEMINI_API_KEY", "")

with st.sidebar:
    st.header("⚙️ Cấu hình")
    user_api_key = st.text_input(
        "Dùng API Key riêng (Tùy chọn):", 
        value="", 
        type="password",
        help="Hệ thống đã có sẵn API Key mặc định. Bạn chỉ cần nhập nếu muốn dùng Key của riêng mình."
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
        st.error("Chưa cấu hình GEMINI_API_KEY trong Streamlit Secrets! Vui lòng cài đặt trước.")
    else:
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("AI đang tra cứu Feat & Meta Debate từ cộng đồng VN..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    recent_messages = st.session_state.chat_messages[-2:]
                    contents = [
                        types.Content(
                            role="user" if m["role"] == "user" else "model", 
                            parts=[types.Part.from_text(text=m["content"])]
                        ) for m in recent_messages
                    ]

                    # Sử dụng mô hình mới gemini-3.6-flash theo đúng thông báo từ Google API
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=contents,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT,
                            temperature=0.7
                        )
                    )
                    
                    if response and hasattr(response, 'text') and response.text:
                        bot_reply = response.text
                        st.markdown(bot_reply)
                        st.session_state.chat_messages.append({"role": "assistant", "content": bot_reply})
                    else:
                        st.error("Không nhận được dữ liệu từ mô hình. Vui lòng thử lại!")

                except Exception as e:
                    st.error(f"Lỗi truy vấn API: {e}")
