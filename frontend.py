# frontend.py
import streamlit as st
from timer_logic import run_pomodoro
from mood import get_tips, get_adjusted_times

st.title("📘 기분 기반 포모도로 타이머")

# 세션 상태 초기화
if "stage" not in st.session_state:
    st.session_state.stage = "input"

if "mood" not in st.session_state:
    st.session_state.mood = None

# 1단계: 시간 설정 입력
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
    mood_choice = st.selectbox("오늘의 기분을 선택하세요:", ["좋음", "무난함", "우울", "짜증/지침"])
    if st.button("포모도로 시작"):
        st.session_state.mood = mood_choice
        st.session_state.stage = "run"
        st.rerun()

# 3단계: 타이머 실행
elif st.session_state.stage == "run":
    # 기분 기반 시간 계산
    focus_time, break_time, rounds = get_adjusted_times(
        st.session_state.base_focus,
        st.session_state.base_break,
        st.session_state.base_rounds,
        st.session_state.mood
    )

    # 포모도로 실행
    total_focus = run_pomodoro(focus_time, break_time, rounds)

    # 결과 출력
    st.success("🎉 포모도로 세션 완료!")
    st.write(f"🕓 총 집중 시간: **{total_focus}분**")
    st.info(f"📖 명언: _{get_tips(st.session_state.mood)}_")

    st.session_state.stage = "done"

# 4단계: 다시 시작
elif st.session_state.stage == "done":
    if st.button("다시 시작하기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()