import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="Death Battle AI Master", page_icon="⚔️", layout="wide")

st.title("⚔️ Death Battle AI Master (VSBw & DBVN Standard)")
st.caption("AI tự động tra cứu, phân tích Feat, Hax và tranh luận phản biện theo chuẩn VSBattles Wiki.")

# Lấy API Key từ Secrets hoặc từ người dùng nhập
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
Bạn là "Death Battle Master AI" - Chuyên gia phân tích Power Scaling, Versus Debating theo chuẩn VS Battles Wiki và cộng đồng Death Battle VN 2.5.

NHIỆM VỤ:
1. Khi người dùng đưa ra một kèo đấu, bạn TỰ ĐỘNG tra cứu kiến thức về nhân vật và phân tích theo cấu trúc chuẩn (Stats, Hax, Speed Blitz, Scenario, Final Verdict).
2. Khi người dùng phản biện (đưa ra Feat mới, chỉ ra điểm sai sót hoặc đưa ra lập luận đối lập), bạn phải đáp lại bằng tinh thần tranh luận khách quan, logic, tôn trọng chuẩn VSBw. Nếu lập luận của người dùng hợp lý, bạn sẵn sàng cập nhật lại Verdict!

CẤU TRÚC PHÂN TÍCH BAN ĐẦU:
1. STATS OVERVIEW (AP/Durability/Speed Tier theo VSBw)
2. HAX & RESISTANCE ANALYSIS
3. WIN-CONS & SPEED BLITZ
4. BATTLE SCENARIO
5. FINAL VERDICT (% Victory + Winner)
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

# Ô nhập liệu chat (Dùng st.chat_input để tạo thanh chat cố định ở dưới)
if prompt := st.chat_input("Nhập kèo đấu mới hoặc gửi phản biện/bằng chứng cho AI..."):
    if not api_key:
        st.error("Vui lòng nhập Gemini API Key ở thanh bên trái!")
    else:
        # Lưu và hiển thị tin nhắn của người dùng
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Gửi yêu cầu tới Gemini API
        with st.chat_message("assistant"):
            with st.spinner("AI đang phân tích và soạn phản hồi..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    # Chuyển đổi lịch sử chat sang định dạng của Gemini SDK
                    contents = []
                    for m in st.session_state.chat_messages:
                        role = "user" if m["role"] == "user" else "model"
                        contents.append(types.Content(role=role, parts=[types.Part.from_text(text=m["content"])]))

                    response = client.models.generate_content(
                        model='gemini-3.6-flash',
                        contents=contents,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT,
                            temperature=0.7
                        )
                    )
                    
                    if response and hasattr(response, 'text'):
                        bot_reply = response.text
                        st.markdown(bot_reply)
                        st.session_state.chat_messages.append({"role": "assistant", "content": bot_reply})
                    else:
                        st.error("Không nhận được phản hồi từ AI.")
                except Exception as e:
                    st.error(f"Lỗi kết nối Gemini API: {e}")
