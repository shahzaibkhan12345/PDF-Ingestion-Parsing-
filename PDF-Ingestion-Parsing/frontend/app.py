# import streamlit as st
# import requests
# import json

# # Define the FastAPI backend URL
# BACKEND_URL = "http://127.0.0.1:8000/api/docs/upload"

# # Page config
# st.set_page_config(
#     page_title="PDF to JSONL Converter",
#     page_icon="📄",
#     layout="centered"
# )

# # 🌈 Custom CSS for modern look
# st.markdown("""
# <style>
# /* Background gradient */
# .stApp {
#     background: linear-gradient(135deg, #e3f2fd, #fce4ec);
#     color: #333;
#     font-family: 'Segoe UI', sans-serif;
# }

# /* Titles */
# h1 {
#     color: #1e3d59;
#     text-align: center;
#     font-weight: 700;
# }
# h2, h3 {
#     color: #3c4858;
# }

# /* Upload box */
# .css-1cpxqw2, .stFileUploader {
#     border: 2px dashed #6c63ff !important;
#     padding: 20px;
#     border-radius: 12px;
#     background-color: #ffffffaa;
# }

# /* Buttons */
# .stButton>button {
#     background-color: #6c63ff;
#     color: white;
#     font-weight: bold;
#     border-radius: 8px;
#     padding: 10px 28px;
#     transition: 0.3s;
# }
# .stButton>button:hover {
#     background-color: #5146d9;
#     transform: scale(1.03);
# }

# /* Download button */
# .stDownloadButton>button {
#     background-color: #00bfa6;
#     color: white;
#     font-weight: bold;
#     border-radius: 8px;
#     padding: 10px 28px;
#     transition: 0.3s;
# }
# .stDownloadButton>button:hover {
#     background-color: #009e8c;
#     transform: scale(1.03);
# }
# </style>
# """, unsafe_allow_html=True)

# # Title and subtitle
# st.title("📄 PDF → JSONL Converter")
# st.subheader("Upload a PDF and convert it into a structured, training-ready JSONL format.")

# # File uploader widget
# uploaded_file = st.file_uploader(
#     "📤 Upload your PDF file below", 
#     type="pdf", 
#     help="Supported: scholarly papers, articles, reports."
# )

# if uploaded_file is not None:
#     st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")

#     # Process button
#     if st.button("🚀 Process PDF"):
#         with st.spinner("⏳ Processing document... Please wait."):
#             try:
#                 files = {
#                     'file': (uploaded_file.name, uploaded_file.getvalue(), 'application/pdf')
#                 }

#                 response = requests.post(BACKEND_URL, files=files)

#                 if response.status_code == 200:
#                     parsed_data = response.json()

#                     st.balloons()
#                     st.success("🎉 PDF processed successfully!")

#                     # Build JSONL string
#                     jsonl_output = "\n".join(json.dumps(record) for record in parsed_data)

#                     with st.expander("🔍 View Raw JSONL Data"):
#                         st.json(parsed_data)

#                     st.download_button(
#                         label="⬇️ Download JSONL File",
#                         data=jsonl_output,
#                         file_name=f"{uploaded_file.name.replace('.pdf', '_parsed.jsonl')}",
#                         mime="application/jsonl"
#                     )
#                 else:
#                     st.error(f"❌ Error: {response.status_code} - {response.text}")

#             except requests.exceptions.RequestException as e:
#                 st.error(f"⚠️ Could not connect to backend. Make sure FastAPI server is running. Error: {e}")
#             except Exception as e:
#                 st.error(f"🔥 Unexpected error: {e}")
import streamlit as st
import requests
import json

# -------------------- CONFIG --------------------
BACKEND_URL = "http://127.0.0.1:8000/api/docs/upload"

st.set_page_config(
    page_title="DeepScan AI",
    page_icon="🤖",
    layout="wide",
)

# -------------------- CUSTOM CSS --------------------
st.markdown("""
<style>
/* Global background */
.stApp {
    background: linear-gradient(135deg, #eef2f3, #e7eff9, #fdf2f8);
    font-family: 'Segoe UI', sans-serif;
    color: #2c2c2c;
}

/* Headers */
h1, h2, h3 {
    font-weight: 700;
    color: #1a202c;
}

/* Card-like containers */
.block-container {
    padding: 2rem 3rem;
    background: rgba(255, 255, 255, 0.85);
    border-radius: 16px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.05);
}

/* Upload box */
.stFileUploader {
    border: 2px dashed #6b46c1 !important;
    background: rgba(255,255,255,0.9);
    border-radius: 14px;
    padding: 25px;
}

/* Buttons */
.stButton>button, .stDownloadButton>button {
    border-radius: 10px;
    padding: 12px 32px;
    font-weight: 600;
    border: none;
    transition: all 0.3s ease;
}

.stButton>button {
    background: linear-gradient(90deg, #6b46c1, #805ad5);
    color: #fff;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #553c9a, #6b46c1);
    transform: translateY(-2px);
}

.stDownloadButton>button {
    background: linear-gradient(90deg, #0fbf9f, #06a77d);
    color: #fff;
}
.stDownloadButton>button:hover {
    background: linear-gradient(90deg, #0a9c83, #0fbf9f);
    transform: translateY(-2px);
}

/* Expander */
.streamlit-expanderHeader {
    font-weight: bold;
    font-size: 16px;
    color: #2d3748;
}

/* Footer */
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
st.sidebar.title("⚙️ DeepScan Settings")
st.sidebar.markdown("Configure options below:")

backend_url = st.sidebar.text_input("Backend URL", BACKEND_URL)
st.sidebar.info("Default: `http://127.0.0.1:8000/api/docs/upload`")

st.sidebar.markdown("---")
st.sidebar.success("📌 Tip: Use scholarly PDFs for best structured results.")

st.sidebar.markdown("Made with ❤️ for FYP by **Revotic-AI**")

# -------------------- HEADER --------------------
st.markdown("<h1 style='text-align:center;'>🤖 DeepScan AI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#4a5568;'>Transform PDFs into Structured JSONL for AI/ML Training</h3>", unsafe_allow_html=True)
st.markdown("---")

# -------------------- MAIN TABS --------------------
tab1, tab2, tab3 = st.tabs(["📤 Upload & Process", "📊 Results", "ℹ️ About Project"])

# ---- TAB 1: Upload ----
with tab1:
    st.subheader("📂 Upload your PDF")
    uploaded_file = st.file_uploader("Drag & Drop or Select a PDF", type="pdf")

    if uploaded_file is not None:
        st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")

        if st.button("🚀 Process PDF"):
            with st.spinner("⏳ Analyzing your document..."):
                try:
                    files = {
                        'file': (uploaded_file.name, uploaded_file.getvalue(), 'application/pdf')
                    }
                    response = requests.post(backend_url, files=files)

                    if response.status_code == 200:
                        st.session_state["parsed_data"] = response.json()
                        st.balloons()
                        st.success("🎉 Processing complete! Switch to the Results tab.")
                    else:
                        st.error(f"❌ Backend error {response.status_code}: {response.text}")

                except requests.exceptions.RequestException as e:
                    st.error(f"⚠️ Could not reach backend. Error: {e}")
                except Exception as e:
                    st.error(f"🔥 Unexpected error: {e}")

# ---- TAB 2: Results ----
with tab2:
    st.subheader("📊 Parsed Results")
    if "parsed_data" in st.session_state:
        parsed_data = st.session_state["parsed_data"]
        jsonl_output = "\n".join(json.dumps(record) for record in parsed_data)

        with st.expander("🔍 View Structured JSONL Data"):
            st.json(parsed_data)

        st.download_button(
            label="⬇️ Download JSONL File",
            data=jsonl_output,
            file_name=f"{uploaded_file.name.replace('.pdf', '_parsed.jsonl') if uploaded_file else 'parsed.jsonl'}",
            mime="application/jsonl"
        )
    else:
        st.info("📥 No results yet. Please upload and process a PDF in the first tab.")


# -------------------- FOOTER --------------------
st.markdown(
    "<p style='text-align:center; color:gray;'>DeepScan AI © 2025 | Powered by Streamlit & FastAPI</p>",
    unsafe_allow_html=True
)