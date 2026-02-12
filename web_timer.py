import streamlit as st
import time
import base64

# --- デザイン設定 ---
st.set_page_config(page_title="ポモドーロ・スマホ版", layout="centered")

# --- 音再生の魔法（しっかり鳴らす版） ---
def play_sound_web():
    try:
        # Windowsの標準アラーム音
        with open("C:/Windows/Media/Alarm01.wav", "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            # autoplayに加えて、ループなしでしっかり最後まで流す設定
            md = f"""
                <audio autoplay="true">
                    <source src="data:audio/wav;base64,{b64}" type="audio/wav">
                </audio>
                """
            st.markdown(md, unsafe_allow_html=True)
            # 音が鳴り終わるまで少し待つ（ここがポイント！）
            time.sleep(1.5) 
    except:
        pass

# --- 強力なCSS（デザイン固定） ---
st.markdown("""
    <style>
    .stApp { background-color: #1C1C1E; color: white; }
    .timer-card {
        background-color: #2C2C2E; padding: 30px; border-radius: 25px;
        text-align: center; border: 1px solid #3A3A3C; margin-bottom: 20px;
    }
    .stButton>button {
        width: 100% !important;
        border-radius: 12px !important;
        height: 50px !important;
        background-color: #3A3A3C !important;
        color: #FFFFFF !important;
        border: 1px solid #545458 !important;
    }
    .stButton>button:hover {
        background-color: #48484A !important;
        color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- セッション管理 ---
if 'reps' not in st.session_state: st.session_state.reps = 0
if 'seconds' not in st.session_state: st.session_state.seconds = 0
if 'is_running' not in st.session_state: st.session_state.is_running = False

# --- メイン表示 ---
st.title("集中タイマー")

if st.session_state.reps == 0:
    status, color = "準備完了", "#FFFFFF"
elif st.session_state.reps % 2 == 0:
    status, color = "休憩中", "#32D74B"
else:
    status, color = "作業中！", "#FF453A"

mins, secs = divmod(st.session_state.seconds, 60)
st.markdown(f"""
    <div class="timer-card">
        <h2 style='color: {color}; margin: 0;'>{status}</h2>
        <h1 style='font-size: 80px; margin: 10px 0;'>{mins:02d}:{secs:02d}</h1>
    </div>
""", unsafe_allow_html=True)

st.write(f"### 完了回数: {st.session_state.reps // 2} 回")

# --- 操作ボタン ---
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("開始"):
        if not st.session_state.is_running:
            if st.session_state.seconds <= 0:
                st.session_state.reps += 1
                st.session_state.seconds = 25*60 if st.session_state.reps % 2 != 0 else 5*60
            st.session_state.is_running = True
            st.rerun()
with c2:
    if st.button("停止"):
        st.session_state.is_running = False
        st.rerun()
with c3:
    if st.button("リセット"):
        st.session_state.reps = 0
        st.session_state.seconds = 0
        st.session_state.is_running = False
        st.rerun()

# --- カウントダウン実行 ---
if st.session_state.is_running:
    if st.session_state.seconds > 0:
        time.sleep(1)
        st.session_state.seconds -= 1
        st.rerun()
    else:
        # 【修正】音を鳴らしてから次のフェーズへ
        play_sound_web()
        
        # フェーズを切り替えて次の秒数をセット
        st.session_state.reps += 1
        st.session_state.seconds = 25*60 if st.session_state.reps % 2 != 0 else 5*60
        
        # 自動で次のカウントダウンを開始

        st.rerun()
