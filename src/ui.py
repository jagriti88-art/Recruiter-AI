import streamlit as st


def candidate_card(candidate, rank):

    medals = {
        1: "🥇",
        2: "🥈",
        3: "🥉"
    }

    medal = medals.get(rank, "🏅")

    with st.container():

        st.markdown(
            f"""
<div style="

background:white;

padding:25px;

border-radius:20px;

box-shadow:0px 8px 25px rgba(0,0,0,.08);

margin-bottom:25px;

border-left:8px solid #0f172a;

">

<h2>{medal} {candidate['name']}</h2>

<b>{candidate['headline']}</b>

<br>

📍 {candidate['location']}

<br>

💼 {candidate['company']}

<br>

🕒 {candidate['experience']} Years Experience

</div>

""",
            unsafe_allow_html=True
        )

        st.write("### ⭐ Final Match")
        st.progress(candidate["final"])

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Semantic",
                f"{candidate['semantic']*100:.1f}%"
            )

        with c2:
            st.metric(
                "Rule",
                f"{candidate['rule']*100:.1f}%"
            )

        with c3:
            st.metric(
                "Behavior",
                f"{candidate['behavior']*100:.1f}%"
            )

        st.write("#### Skills")

        cols = st.columns(5)

        for i, skill in enumerate(candidate["skills"][:10]):
            cols[i % 5].success(skill)

        with st.expander("View Full Profile"):

            st.write("Candidate ID:", candidate["candidate_id"])
            st.write("Current Role:", candidate["current_title"])
            st.write("Company:", candidate["company"])
            st.write("Experience:", candidate["experience"])
            st.write("Location:", candidate["location"])
            st.markdown("### 🤖 Why this Candidate?")
            st.info(candidate["reason"])