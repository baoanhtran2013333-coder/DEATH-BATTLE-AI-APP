import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Death Battle AI Master", page_icon="⚔️", layout="wide")

st.title("⚔️ Death Battle AI Master (Endless Fictional & DBVN 2.5 Standard)")
st.caption("AI tra cứu Feat, Hax, Meta Debate từ Endless Fictional, DBVN 2.5 và TikTok Death Battle VN.")

default_api_key = st.secrets.get("OPENROUTER_API_KEY", "")

with st.sidebar:
    st.header("⚙️ Cấu hình")
    user_api_key = st.text_input(
        "Dùng API Key OpenRouter (Tùy chọn):", 
        value="", 
        type="password",
        help="Dán API Key sk-or-v1-... từ OpenRouter vào đây."
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

# Danh sách các model Free ổn định nhất trên OpenRouter hiện tại
FREE_MODELS = [
    "google/gemini-2.0-flash-lite-001:free",
    "meta-llama/llama-3.1-8b-instruct:free",
    "qwen/qwen-2.5-72b-instruct:free",
    "mistralai/mistral-7b-instruct:free"
]

if prompt := st.chat_input("Nhập kèo đấu hoặc gửi phản biện/scan/bằng chứng cho AI..."):
    if not api_key:
        st.error("Vui lòng dán OpenRouter API Key vào ô cấu hình bên trái!")
    else:
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("AI đang tra cứu Feat & Meta Debate từ cộng đồng VN..."):
                client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=api_key,
                )

                messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                for m in st.session_state.chat_messages[-4:]:
                    messages.append({"role": m["role"], "content": m["content"]})

                success = False
                last_error = ""

                # Thử lần lượt từng model free trong danh sách
                for model_name in FREE_MODELS:
                    try:
                        response = client.chat.completions.create(
                            model=model_name,
                            messages=messages,
                            temperature=0.7
                        )
                        if response and response.choices and response.choices[0].message.content:
                            bot_reply = response.choices[0].message.content
                            st.markdown(bot_reply)
                            st.session_state.chat_messages.append({"role": "assistant", "content": bot_reply})
                            success = True
                            break
                    except Exception as e:
                        last_error = str(e)
                        continue

                if not success:
                    st.error(f"Tất cả các mô hình miễn phí hiện đang bận hoặc gián đoạn. Vui lòng bấm 'Tạo kèo đấu mới' và thử lại sau ít phút! Chi tiết: {last_error}")
