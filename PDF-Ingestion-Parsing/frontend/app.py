import streamlit as st
import requests
import json

# Define the FastAPI backend URL
BACKEND_URL = "http://127.0.0.1:8000/api/docs/upload"

# Page config
st.set_page_config(
    page_title="PDF to JSONL Converter",
    page_icon="📄",
    layout="centered"
)

# 🌈 Custom CSS for modern look
st.markdown("""
<style>
/* Background gradient */
.stApp {
    background: linear-gradient(135deg, #e3f2fd, #fce4ec);
    color: #333;
    font-family: 'Segoe UI', sans-serif;
}

/* Titles */
h1 {
    color: #1e3d59;
    text-align: center;
    font-weight: 700;
}
h2, h3 {
    color: #3c4858;
}

/* Upload box */
.css-1cpxqw2, .stFileUploader {
    border: 2px dashed #6c63ff !important;
    padding: 20px;
    border-radius: 12px;
    background-color: #ffffffaa;
}

/* Buttons */
.stButton>button {
    background-color: #6c63ff;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    padding: 10px 28px;
    transition: 0.3s;
}
.stButton>button:hover {
    background-color: #5146d9;
    transform: scale(1.03);
}

/* Download button */
.stDownloadButton>button {
    background-color: #00bfa6;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    padding: 10px 28px;
    transition: 0.3s;
}
.stDownloadButton>button:hover {
    background-color: #009e8c;
    transform: scale(1.03);
}
</style>
""", unsafe_allow_html=True)

# Title and subtitle
st.title("📄 PDF → JSONL Converter")
st.subheader("Upload a PDF and convert it into a structured, training-ready JSONL format.")

# File uploader widget
uploaded_file = st.file_uploader(
    "📤 Upload your PDF file below", 
    type="pdf", 
    help="Supported: scholarly papers, articles, reports."
)

if uploaded_file is not None:
    st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")

    # Process button
    if st.button("🚀 Process PDF"):
        with st.spinner("⏳ Processing document... Please wait."):
            try:
                files = {
                    'file': (uploaded_file.name, uploaded_file.getvalue(), 'application/pdf')
                }

                response = requests.post(BACKEND_URL, files=files)

                if response.status_code == 200:
                    parsed_data = response.json()

                    st.balloons()
                    st.success("🎉 PDF processed successfully!")

                    # Build JSONL string
                    jsonl_output = "\n".join(json.dumps(record) for record in parsed_data)

                    with st.expander("🔍 View Raw JSONL Data"):
                        st.json(parsed_data)

                    st.download_button(
                        label="⬇️ Download JSONL File",
                        data=jsonl_output,
                        file_name=f"{uploaded_file.name.replace('.pdf', '_parsed.jsonl')}",
                        mime="application/jsonl"
                    )
                else:
                    st.error(f"❌ Error: {response.status_code} - {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ Could not connect to backend. Make sure FastAPI server is running. Error: {e}")
            except Exception as e:
                st.error(f"🔥 Unexpected error: {e}")
