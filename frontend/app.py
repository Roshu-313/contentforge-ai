import streamlit as st
import requests
import json

st.set_page_config(
    page_title="ContentForge AI",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ ContentForge AI")
st.caption("Autonomous Multi-Agent Content Intelligence System")

API_URL = "http://localhost:8000"

tab1, tab2 = st.tabs(["Generate Content", "Content History"])

with tab1:
    st.subheader("Generate New Content")
    subject = st.text_input(
        "Enter a topic",
        placeholder="e.g. AI tools for freelancers in 2026"
    )

    if st.button("🚀 Generate Content", type="primary"):
        if not subject:
            st.warning("Please enter a topic first.")
        else:
            with st.spinner("Agents are working... This takes 2-4 minutes."):
                try:
                    response = requests.post(
                        f"{API_URL}/generate",
                        json={"subject": subject},
                        timeout=300
                    )
                    data = response.json()

                    st.success(f"✅ Generated! Word count: {data['word_count']}")

                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.subheader("📝 Blog Post")
                        st.markdown(data["article"])

                    with col2:
                        st.subheader("📱 Social Media Posts")
                        for post in data["social_media_posts"]:
                            with st.expander(post["platform"]):
                                st.write(post["content"])
                                st.button(
                                    "Copy",
                                    key=post["platform"]
                                )
                except Exception as e:
                    st.error(f"Error: {e}")

with tab2:
    st.subheader("Content History")
    if st.button("🔄 Refresh"):
        try:
            response = requests.get(f"{API_URL}/history")
            records = response.json()
            for rec in records:
                st.write(f"**{rec['subject']}** — {rec['created_at']} ({rec['word_count']} words)")
        except:
            st.error("Could not load history. Is the API running?")