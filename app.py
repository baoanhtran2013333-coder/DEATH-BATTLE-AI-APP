import streamlit as st
import time
from google import genai
from google.genai import types

st.set_page_config(page_title="Death Battle AI Master", page_icon="⚔️", layout="wide")

st.title("⚔️ Death Battle AI Master (Endless Fictional & DBVN 2.5 Standard)")
st.caption("AI tra cứu Feat, Hax, Meta Debate từ Endless Fictional, DBVN 2.5 và TikTok Death Battle VN.")

default_api_key = st.secrets.get("GEMINI_API_KEY", "")

user_api_key = st.sidebar.text_input(
    "Nhập Google Gemini API Key:", 
    value=default_api_key, 
    type="password",
    help="Nếu đã cài API Key trong Secrets thì không cần nhập thêm."
)
st.sidebar.markdown("[Lấy API Key miễn phí tại đây](https://aistudio.google.com/)")

api_key = user_api_key or default_api_key

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

if st.sidebar.button("🔄 Tạo kèo đấu mới"):
    st.session_state.chat_messages = []
    st.rerun()

for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Nhập kèo đấu hoặc gửi phản biện/scan/bằng chứng cho AI..."):
    if not api_key:
        st.error("Vui lòng nhập Gemini API Key ở thanh bên trái!")
    else:
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("AI đang tra cứu Feat & Meta Debate từ cộng đồng VN..."):
                client = genai.Client(api_key=api_key)
                contents = [
                    types.Content(
                        role="user" if m["role"] == "user" else "model", 
                        parts=[types.Part.from_text(text=m["content"])]
                    ) for m in st.session_state.chat_messages
                ]

                # Danh sách mô hình ưu tiên -> dự phòng
                models_to_try = ['gemini-3.6-flash', 'gemini-2.5-flash']
                success = False

                for model_name in models_to_try:
                    try:
                        response = client.models.generate_content(
                            model=model_name,
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
                            success = True
                            break
                    except Exception as e:
                        # Nếu lỗi 503 hoặc lỗi model, tự động chuyển sang model tiếp theo trong danh sách
                        continue

                if not success:
                    st.error("Hệ thống máy chủ Gemini hiện đang quá tải ở tất cả mô hình. Vui lòng thử lại sau vài giây!")
