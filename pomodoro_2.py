import streamlit as st
import time
import math

# 기분별 가중치
mood_multipliers = {
    "좋음": {"focus": 1.2, "break": 0.8, "rounds": 1.0},
    "무난함": {"focus": 1.0, "break": 1.0, "rounds": 1.0},
    "우울": {"focus": 0.8, "break": 1.2, "rounds": 1.0},
    "짜증/지침": {"focus": 0.6, "break": 1.5, "rounds": 1.0},
}

tips = {
    "좋음": "오늘의 노력은 내일의 기적을 만든다.",
    "무난함": "지금 이 순간도 충분히 의미 있다.",
    "우울": "작은 한 걸음이 큰 변화를 만든다.",
    "짜증/지침": "지친 날엔, 멈추지 않는 것만으로도 충분하다."
}

st.title("📘 기분 기반 포모도로 타이머")

# 세션 초기화
default_state = {
    "stage": "input",
    "status": "stopped",
    "mode": "focus",      # focus or break
    "current_round": 1,
    "remaining_sec": 0,
    "total_focus": 0,
    "finished": False
}
for key, value in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = value

# 1단계: 시간 입력
if st.session_state.stage == "input":
    with st.form("base_time_form_unique"):
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
    mood_choice = st.selectbox("오늘의 기분을 선택하세요:", list(mood_multipliers.keys()), key="mood_select")
    if st.button("포모도로 시작"):
        st.session_state.mood = mood_choice
        st.session_state.stage = "run"
        st.session_state.status = "running"
        st.rerun()

# 3단계: 실행 중
elif st.session_state.stage == "run":
    mood = st.session_state.mood
    multiplier = mood_multipliers[mood]
    focus_time = math.ceil(st.session_state.base_focus * multiplier["focus"])
    break_time = math.ceil(st.session_state.base_break * multiplier["break"])
    rounds = max(1, round(st.session_state.base_rounds * multiplier["rounds"]))

    st.markdown(f"### 현재 라운드: {st.session_state.current_round} / {rounds}")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⏸️ 일시정지"):
            st.session_state.status = "paused"
            st.rerun()
    with col2:
        if st.button("▶️ 재시작"):
            st.session_state.status = "running"
            st.rerun()
    with col3:
        if st.button("⏹️ 중단"):
            # 💡 현재 focus 중이었다면 경과 시간 누적
            if st.session_state.mode == "focus":
                full_focus_sec = focus_time * 60
                elapsed_sec = full_focus_sec - st.session_state.remaining_sec
                st.session_state.total_focus += elapsed_sec // 60  # 분 단위 누적
            st.session_state.stage = "done"
            st.session_state.finished = False
            st.rerun()

    # 시간 계산 및 표시
    mode_label = "🔵 집중" if st.session_state.mode == "focus" else "🌿 휴식"
    duration = focus_time if st.session_state.mode == "focus" else break_time
    if st.session_state.remaining_sec == 0:
        st.session_state.remaining_sec = duration * 60

    timer_placeholder = st.empty()
    if st.session_state.status == "running":
        mins, secs = divmod(st.session_state.remaining_sec, 60)
        timer_placeholder.markdown(f"**{mode_label} 남은 시간: {mins:02d}:{secs:02d}**")
        time.sleep(1)
        st.session_state.remaining_sec -= 1

        # 한 타이머 종료 시점
        if st.session_state.remaining_sec == 0:
            if st.session_state.mode == "focus":
                st.session_state.total_focus += focus_time
                st.session_state.mode = "break"
            else:
                st.session_state.current_round += 1
                if st.session_state.current_round > rounds:
                    st.session_state.stage = "done"
                    st.session_state.finished = True
                    st.rerun()
                else:
                    st.session_state.mode = "focus"
        st.rerun()
    else:
        mins, secs = divmod(st.session_state.remaining_sec, 60)
        timer_placeholder.markdown(f"**⏸️ 일시정지됨: {mins:02d}:{secs:02d}**")

# 4단계: 완료
elif st.session_state.stage == "done":
    if st.session_state.finished:
        st.success("🎉 포모도로 세션 완료!")
    else:
        st.warning("⏹️ 세션이 중단되었습니다.")

    st.write(f"🕓 **총 집중 시간: {st.session_state.total_focus}분**")
    st.info(f"📖 명언: _{tips[st.session_state.mood]}_")

    if st.button("🔁 다시 시작하기"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# streamlit run "C:\Users\권소연\OneDrive\바탕 화면\file\python\swwwwwwwwwwwwwww.py"