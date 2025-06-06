# Mood-based Pomodoro Timer (Streamlit Version)

import streamlit as st
import time
import math

# 시간 배율 (기분에 따른 가중치)
mood_multipliers = {
    "좋음": {"focus": 1.2, "break": 0.8, "rounds": 1.2},
    "무난함": {"focus": 1.0, "break": 1.0, "rounds": 1.0},
    "우울": {"focus": 0.6, "break": 1.2, "rounds": 0.8},
    "짜증/지침": {"focus": 0.4, "break": 1.5, "rounds": 0.5},
}

# 기분에 따른 명언
tips = {
    "좋음": "오늘의 노력은 내일의 기적을 만든다.",
    "무난함": "지금 이 순간도 충분히 의미 있다.",
    "우울": "작은 한 걸음이 큰 변화를 만든다.",
    "짜증/지침": "지친 날엔, 멈추지 않는 것만으로도 충분하다."
}

st.title("📘 기분 기반 포모도로 타이머")

# 세션 상태 변수 초기화
if "stage" not in st.session_state:
    st.session_state.stage = "input"
if "mood" not in st.session_state:
    st.session_state.mood = None

# 1단계: 사용자 기본 시간 입력
if st.session_state.stage == "input":
    with st.form("base_time_form"):
        base_focus = st.number_input("기본 집중 시간 (분)", min_value=1, value=25)
        base_break = st.number_input("기본 휴식 시간 (분)", min_value=1, value=5)
        base_rounds = st.number_input("반복 횟수", min_value=1, value=4)
        submitted = st.form_submit_button("다음")

    if submitted:
        st.session_state.base_focus = base_focus
        st.session_state.base_break = base_break
        st.session_state.base_rounds = base_rounds
        st.session_state.stage = "mood"
        st.rerun()

# 2단계: 기분 선택
elif st.session_state.stage == "mood":
    mood_choice = st.selectbox("오늘의 기분을 선택하세요:", list(mood_multipliers.keys()))
    if st.button("포모도로 시작"):
        st.session_state.mood = mood_choice
        st.session_state.stage = "run"
        st.rerun()


    
# 3단계: 타이머 실행
elif st.session_state.stage == "run":
    mood = st.session_state.mood
    base_focus = st.session_state.base_focus
    base_break = st.session_state.base_break
    base_rounds = st.session_state.base_rounds

    multiplier = mood_multipliers[mood]
    focus_time = math.ceil(base_focus * multiplier["focus"])
    break_time = math.ceil(base_break * multiplier["break"])
    rounds = max(1, round(base_rounds * multiplier["rounds"]))
    total_focus = 0

    for i in range(1, rounds + 1):
        st.write(f"## 🔵 라운드 {i}: 집중 {focus_time}분")
        with st.empty():
            for sec in range(focus_time * 60, 0, -1):
                mins, secs = divmod(sec, 60)
                st.markdown(f"**⏳ 집중 남은 시간: {mins:02d}:{secs:02d}**")
                time.sleep(1)
        total_focus += focus_time

        if i < rounds:
            st.write(f"### ⏸ 휴식 {break_time}분")
            with st.empty():
                for sec in range(break_time * 60, 0, -1):
                    mins, secs = divmod(sec, 60)
                    st.markdown(f"**🌿 휴식 남은 시간: {mins:02d}:{secs:02d}**")
                    time.sleep(1)

    # 완료 메시지
    st.success("🎉 포모도로 세션 완료!")
    st.write(f"🕓 총 집중 시간: **{total_focus}분**")
    st.info(f"📖 명언: _{tips[mood]}_")
    st.session_state.stage = "done"

# 완료 후 다시 시작 버튼 표시
elif st.session_state.stage == "done":
    if st.button("다시 시작하기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()
