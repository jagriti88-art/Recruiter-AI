import streamlit as st


def candidate_card(candidate, rank):

    medals = {
        1: "🥇",
        2: "🥈",
        3: "🥉"
    }

    medal = medals.get(rank, "🏅")

    st.markdown("---")

    # =========================
    # Header
    # =========================

    st.subheader(f"{medal} Rank #{rank} • {candidate['name']}")

    c1, c2 = st.columns([3, 1])

    with c1:
        st.write(f"**{candidate['headline']}**")
        st.write(f"📍 {candidate['location']}")
        st.write(f"💼 {candidate['company']}")
        st.write(f"🕒 {candidate['experience']} Years Experience")

    with c2:
        st.metric(
            "Final Match",
            f"{candidate['final']*100:.1f}%"
        )

    st.progress(candidate["final"])

    # =========================
    # Scores
    # =========================

    s1, s2, s3 = st.columns(3)

    with s1:
        st.metric(
            "Semantic",
            f"{candidate['semantic']*100:.1f}%"
        )

    with s2:
        st.metric(
            "Rule",
            f"{candidate['rule']*100:.1f}%"
        )

    with s3:
        st.metric(
            "Behavior",
            f"{candidate['behavior']*100:.1f}%"
        )

    # =========================
    # Skills
    # =========================

    st.write("### Skills")

    cols = st.columns(5)

    for i, skill in enumerate(candidate["skills"][:10]):
        cols[i % 5].success(skill)

    # =========================
    # Reason
    # =========================

    st.write("### AI Explanation")

    st.info(candidate["reason"])

    # =========================
    # Full Profile
    # =========================

    with st.expander("📄 Candidate Details"):

        st.write("**Candidate ID:**", candidate["candidate_id"])
        st.write("**Current Role:**", candidate["current_title"])
        st.write("**Company:**", candidate["company"])
        st.write("**Experience:**", candidate["experience"])
        st.write("**Location:**", candidate["location"])

        st.write("**Skills:**")
        st.write(", ".join(candidate["skills"]))