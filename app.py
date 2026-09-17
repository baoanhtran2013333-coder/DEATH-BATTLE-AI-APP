import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Death Battle AI Master", page_icon="⚔️", layout="wide")

st.title("⚔️ Death Battle AI Master (Endless Fictional & DBVN 2.5 Standard)")
st.caption("AI tra cứu Feat, Hax, Meta Debate từ Endless Fictional, DBVN 2.5 và TikTok Death Battle VN.")

# Lấy API Key từ Secrets hoặc từ ô nhập liệu ở thanh bên
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
1. Khi phân tích bất kỳ kèo đấu nào, bạn phải áp dụng quy chuẩn Scaling và các góc nhìn/meta debate phổ biến tại các group VS Debating Việt Nam (Endless Fictional, DBVN 2.5, TikTok DBVN) kết hợp với tiêu chuẩn VSBattles Wiki.
2. Tự động tra cứu các Feat, Anti-feat, Statement, Hax, Resistance và các trận debate kinh điển từng diễn ra trong cộng đồng Việt Nam để đưa ra lập luận chặt chẽ.
3. Luôn sẵn sàng phản biện lại người dùng nếu họ đưa ra NLF (No Limits Fallacy), Wank/Highball quá đà hoặc Downplay sai sự thật. Nếu người dùng đưa ra scan/proof hợp lý theo chuẩn DBVN/EF, hãy khách quan ghi nhận và cập nhật lại Verdict.

CẤU TRÚC PHÂN TÍCH CHUẨN:
1. STATS OVERVIEW (AP/Durability/Speed Tier theo VSBw & Meta DBVN/EF)
2. HAX & RESISTANCE ANALYSIS (Phân tích kĩ năng đặc biệt)
3. VN COMMUNITY META & DEBATE FEATS (Meta Tranh Luận VN)
4. BATTLE SCENARIO (Mô tả diễn biến giao tranh)
5. FINAL VERDICT (% Victory + Winner kèm lý do cốt lõi)
"""

# Khởi tạo lịch sử chat trong Session State
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# Nút để bắt đầu kèo đấu mới
if st.sidebar.button("🔄 Tạo kèo đấu mới"):
    st.session_state.chat_messages = []
    st.rerun()

# Hiển thị lịch sử trò chuyện
for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Ô nhập liệu chat cố định ở bên dưới
if prompt := st.chat_input("Nhập kèo đấu hoặc gửi phản biện/scan/bằng chứng cho AI..."):
    if not api_key:
        st.error("Vui lòng nhập Gemini API Key ở thanh bên trái!")
    else:
        # Lưu và hiển thị tin nhắn của người dùng
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Gửi yêu cầu tới Gemini API
        with st.chat_message("assistant"):
            with st.spinner("AI đang tra cứu Feat & Meta Debate từ cộng đồng VN..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    # Chuyển đổi lịch sử chat sang định dạng của Gemini SDK
                    contents = []
                    for m in st.session_state.chat_messages:
                        role = "user" if m["role"] == "user" else "model"
                        contents.append(
                            types.Content(
                                role=role, 
                                parts=[types.Part.from_text(text=m["content"])]
                            )
                        )

                    response = client.models.generate_content(
                        model='gemini-3.6-flash',
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
                        st.error("Không nhận được phản hồi từ AI. Vui lòng thử lại!")
                except Exception as e:
                    st.error(f"Lỗi hệ thống: {e}")
