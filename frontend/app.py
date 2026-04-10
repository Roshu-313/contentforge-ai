import streamlit as st
import requests
import os

st.set_page_config(
    page_title="ContentForge AI",
    page_icon="⚡",
    layout="wide"
)

# ─── Header ───────────────────────────────────────────────────────────────
st.title("⚡ ContentForge AI")
st.caption("Autonomous Multi-Agent Content Intelligence System")
st.markdown("---")

# ─── API URL — works locally and on cloud ─────────────────────────────────
API_URL = os.getenv("API_URL", "http://localhost:8000")
# ─── Tabs ─────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["🚀 Generate Content", "📚 Content History"])

with tab1:
    st.subheader("Generate New Content")
    st.markdown("Enter any topic and let the AI agents research, write, and review your content automatically.")

    subject = st.text_input(
        "Enter a topic",
        placeholder="e.g. AI tools for freelancers in 2026",
        help="Be specific for better results"
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        generate_btn = st.button("🚀 Generate Content", type="primary", use_container_width=True)

    if generate_btn:
        if not subject:
            st.warning("Please enter a topic first.")
        else:
            with st.spinner("🤖 Agents are working... This takes 2-4 minutes."):
                try:
                    response = requests.post(
                        f"{API_URL}/generate",
                        json={"subject": subject},
                        timeout=300
                    )
                    if response.status_code == 200:
                        data = response.json()

                        st.success(f"✅ Content generated! Word count: {data.get('word_count', 0)}")
                        st.markdown("---")

                        col_blog, col_social = st.columns([2, 1])

                        with col_blog:
                            st.subheader("📝 Blog Post")
                            st.markdown(data.get("article", ""))

                        with col_social:
                            st.subheader("📱 Social Media Posts")
                            for post in data.get("social_media_posts", []):
                                platform = post.get("platform", "")
                                content = post.get("content", "")
                                with st.expander(f"{platform}", expanded=True):
                                    st.write(content)
                                    st.download_button(
                                        label=f"Copy {platform} post",
                                        data=content,
                                        file_name=f"{platform.lower()}_post.txt",
                                        mime="text/plain",
                                        key=f"download_{platform}"
                                    )
                    else:
                        st.error(f"API Error: {response.text}")

                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend API. Make sure it is running on localhost:8000")
                except requests.exceptions.Timeout:
                    st.error("⏱️ Request timed out. The agents are taking longer than expected. Try again.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

with tab2:
    st.subheader("Previously Generated Content")
    if st.button("🔄 Load History"):
        try:
            response = requests.get(f"{API_URL}/history", timeout=10)
            if response.status_code == 200:
                records = response.json()
                if not records:
                    st.info("No content generated yet.")
                else:
                    for rec in records:
                        with st.expander(f"📄 {rec.get('subject', 'Unknown')} — {rec.get('created_at', '')} ({rec.get('word_count', 0)} words)"):
                            st.markdown(rec.get("article", ""))
            else:
                st.error("Could not load history.")
        except Exception as e:
            st.error(f"Error loading history: {str(e)}")