import streamlit as st
import os
from pathlib import Path
import time
from datetime import datetime, timedelta
import uuid
import glob

from config import Config
from utils.document_processor import DocumentProcessor
from utils.ai_summarizer import AISummarizer


# Page configuration
st.set_page_config(
    page_title=Config.APP_NAME,
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium design
st.markdown("""
    <style>
        /* Import modern fonts including Khmer support */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Noto+Sans+Khmer:wght@300;400;600;700&display=swap');
        
        * {
            font-family: 'Inter', 'Noto Sans Khmer', sans-serif;
        }
        
        /* Main container styling */
        .main {
            background: linear-gradient(135deg, #1A1A1A 0%, #1A1A1A 100%);
            padding: 2rem;
        }
        
        /* Card styling */
        .stApp {
            background: linear-gradient(135deg, #1A1A1A 0%, #1A1A1A 100%);
        }
        
        /* Custom card */
        .custom-card {
            background: linear-gradient(135deg, #1A1A1A 0%, #1A1A1A 100%);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            margin: 1rem 0;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        /* Header styling */
        h1 {
            color: #FFFFFF;
            font-weight: 700;
            font-size: 3rem !important;
            margin-bottom: 0.5rem;
        }
        
        h2 {
            color: #FFFFFF;
            font-weight: 600;
        }
        
        h3 {
            color: #764ba2;
            font-weight: 600;
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        /* File uploader */
        .uploadedFile {
            background: rgba(102, 126, 234, 0.1);
            border-radius: 12px;
            padding: 1rem;
            border: 2px dashed #667eea;
        }
        
        /* Success/Error messages */
        .stSuccess {
            background: rgba(0, 200, 83, 0.1);
            border-left: 4px solid #00c853;
            border-radius: 8px;
        }
        
        .stError {
            background: rgba(255, 23, 68, 0.1);
            border-left: 4px solid #ff1744;
            border-radius: 8px;
        }
        
        /* Sidebar */
        .css-1d391kg {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
        }
        
        /* Metrics */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            color: #667eea;
            font-weight: 700;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background: rgba(102, 126, 234, 0.1);
            border-radius: 8px;
            font-weight: 600;
        }
        
        /* Progress bar */
        .stProgress > div > div {
            background: linear-gradient(90deg, #1A1A1A 0%, #1A1A1A 100%);
        }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'uploaded_file_path' not in st.session_state:
        st.session_state.uploaded_file_path = None
    if 'extracted_text' not in st.session_state:
        st.session_state.extracted_text = None
    if 'summary' not in st.session_state:
        st.session_state.summary = None
    if 'document_info' not in st.session_state:
        st.session_state.document_info = None
    # Add unique session ID for file isolation
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())[:8]
    # Track uploaded files for cleanup
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []


def cleanup_old_files(max_age_hours: int = 24):
    """
    Clean up temporary files older than specified hours.
    This prevents disk space from filling up with old uploads.
    """
    try:
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        # Clean upload folder
        for folder in [Config.UPLOAD_FOLDER, Config.OUTPUT_FOLDER]:
            if os.path.exists(folder):
                for file_path in glob.glob(os.path.join(folder, '*')):
                    if os.path.isfile(file_path):
                        file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                        if file_modified < cutoff_time:
                            try:
                                os.remove(file_path)
                            except Exception:
                                pass  # Ignore errors for files in use
    except Exception:
        pass  # Don't crash app if cleanup fails


def save_uploaded_file(uploaded_file):
    """
    Save uploaded file to disk with unique naming to support multiple users.
    Uses session ID and UUID to prevent file collisions.
    """
    try:
        # Generate unique filename using session ID and UUID
        session_id = st.session_state.get('session_id', str(uuid.uuid4())[:8])
        unique_id = str(uuid.uuid4())[:8]
        
        # Parse original filename
        original_name = uploaded_file.name
        name_parts = os.path.splitext(original_name)
        
        # Create unique filename: originalname_sessionid_uniqueid.extension
        unique_filename = f"{name_parts[0]}_{session_id}_{unique_id}{name_parts[1]}"
        
        file_path = os.path.join(Config.UPLOAD_FOLDER, unique_filename)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Track file for potential cleanup
        st.session_state.uploaded_files.append(file_path)
        
        return file_path
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        return None


def main():
    initialize_session_state()
    
    # Clean up old temporary files (runs once per session)
    cleanup_old_files(max_age_hours=24)
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📄 Document AI Assistant")
        st.markdown("**Upload • Analyze • Summarize • Convert**")
    
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # API Key input
        api_key = Config.OPENAI_API_KEY or ""

        st.markdown("---")
        
        # Summary type selection
        summary_type = st.selectbox(
            "Summary Type",
            ["comprehensive", "brief", "bullet_points", "executive"],
            help="Choose the type of summary you want"
        )
        
        # Language selection
        language = st.selectbox(
            "Output Language / ភាសាលទ្ធផល",
            ["en", "km", "both"],
            format_func=lambda x: {
                "en": "English",
                "km": "ខ្មែរ (Khmer)",
                "both": "🌐 Both / ទាំងពីរ"
            }[x],
            help="Choose the language for AI-generated summaries and answers"
        )
        
        # Token limit
        max_tokens = st.slider(
            "Max Summary Tokens",
            min_value=200,
            max_value=2000,
            value=1000,
            step=100,
            help="Maximum length of the summary"
        )
        
        st.markdown("---")
        
    # Main content
    tab1, tab2 = st.tabs(["📤 Upload & Analyze", "🔄 Convert PDF to DOCX"])
    
    with tab1:
        st.markdown("### 📝 Analyze Your Document or Text")
        st.markdown("Choose how you want to provide content for analysis:")
        
        # Create two sub-tabs for different input methods
        input_tab1, input_tab2 = st.tabs(["📤 Upload File", "✍️ Paste Text"])
        
        with input_tab1:
            st.markdown("**Upload a document to analyze**")
            uploaded_file = st.file_uploader(
                "Choose a file",
                type=['pdf', 'docx', 'txt'],
                help="Upload a PDF, DOCX, or TXT file to analyze",
                key="file_uploader_main"
            )
            
            if uploaded_file:
                # Save file
                file_path = save_uploaded_file(uploaded_file)
                
                if file_path:
                    st.session_state.uploaded_file_path = file_path
                    file_extension = Path(uploaded_file.name).suffix
                    
                    # Display file info
                    col1, col2, col3 = st.columns(3)
                    
                    # Get document info
                    doc_info = DocumentProcessor.get_document_info(file_path, file_extension)
                    st.session_state.document_info = doc_info
                    
                    with col1:
                        st.metric("File Name", doc_info['file_name'])
                    with col2:
                        st.metric("File Size", f"{doc_info['file_size_mb']} MB")
                    with col3:
                        if 'page_count' in doc_info:
                            st.metric("Pages", doc_info['page_count'])
                        else:
                            st.metric("Type", doc_info['file_type'])
                    
                    st.markdown("---")
                    
                    # Extract text
                    with st.spinner("🔍 Extracting text from document..."):
                        try:
                            extracted_text = DocumentProcessor.extract_text(file_path, file_extension)
                            st.session_state.extracted_text = extracted_text
                            
                            # Display text preview
                            with st.expander("📖 Document Preview", expanded=False):
                                st.text_area(
                                    "Extracted Text",
                                    extracted_text[:2000] + ("..." if len(extracted_text) > 2000 else ""),
                                    height=300,
                                    disabled=True,
                                    key="preview_uploaded"
                                )
                                st.caption(f"Total characters: {len(extracted_text):,}")
                            
                            st.success("✅ Text extracted successfully!")
                            
                        except Exception as e:
                            st.error(f"❌ Error extracting text: {str(e)}")
        
        with input_tab2:
            st.markdown("**Enter or paste your text directly**")
            st.info("💡 Perfect for quick analysis without creating a file!")
            
            # Text input area
            pasted_text = st.text_area(
                "Your Text",
                height=300,
                placeholder="Paste or type your text here...\n\nSupports:\n- English text\n- Khmer text (ភាសាខ្មែរ)\n- Any other language\n\nThe AI will analyze and summarize your text in your selected language.",
                key="pasted_text_input",
                help="Enter the text you want to analyze"
            )
            
            if pasted_text and len(pasted_text.strip()) > 0:
                # Store the pasted text
                st.session_state.extracted_text = pasted_text.strip()
                
                # Display text statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Characters", f"{len(pasted_text):,}")
                with col2:
                    word_count = len(pasted_text.split())
                    st.metric("Words", f"{word_count:,}")
                with col3:
                    line_count = len(pasted_text.split('\n'))
                    st.metric("Lines", line_count)
                
                st.success("✅ Text ready for analysis!")
            elif pasted_text is not None and len(pasted_text.strip()) == 0:
                st.warning("⚠️ Please enter some text to analyze")
        
        st.markdown("---")
        
        # Summarize button (works for both upload and pasted text)
        if st.session_state.extracted_text:
            if st.button("🤖 Generate AI Summary", type="primary", use_container_width=True):
                if not api_key:
                    st.error("⚠️ Please provide an OpenAI API key in the sidebar")
                else:
                    with st.spinner("🧠 AI is analyzing your document..."):
                        try:
                            summarizer = AISummarizer(api_key=api_key)
                            
                            # Progress bar for effect
                            progress_bar = st.progress(0)
                            for i in range(100):
                                time.sleep(0.01)
                                progress_bar.progress(i + 1)
                            
                            result = summarizer.summarize(
                                st.session_state.extracted_text,
                                summary_type=summary_type,
                                max_tokens=max_tokens,
                                language=language
                            )
                            
                            if result['success']:
                                st.session_state.summary = result
                                
                                # Display summary
                                st.markdown("### 📋 Summary")
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    st.markdown(f"**Type:** {result['summary_type'].replace('_', ' ').title()}")
                                with col_b:
                                    lang_display = {
                                        'en': '🇬🇧 English',
                                        'km': '🇰🇭 ខ្មែរ (Khmer)',
                                        'both': '🌐 Both Languages'
                                    }.get(result.get('language', 'en'), 'English')
                                    st.markdown(f"**Language:** {lang_display}")
                                
                                summary_container = st.container()
                                with summary_container:
                                    st.markdown(f"""
                                    <div class="custom-card">
                                        {result['summary']}
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                # Metadata
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("Tokens Used", result['tokens_used'])
                                # with col2:
                                #     st.metric("Model", result['model'])
                                
                                # Download summary
                                st.download_button(
                                    "📥 Download Summary",
                                    data=result['summary'],
                                    file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                    mime="text/plain"
                                )
                                
                            else:
                                st.error(f"❌ {result['error']}")
                            
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
        else:
            st.info("👆 Please either **upload a file** or **paste text** above to get started!")
    
    with tab2:
        st.markdown("### Convert PDF to DOCX")
        
        pdf_file = st.file_uploader(
            "Choose a PDF file to convert",
            type=['pdf'],
            key="pdf_converter",
            help="Upload a PDF file to convert to DOCX format"
        )
        
        if pdf_file:
            pdf_path = save_uploaded_file(pdf_file)
            
            if st.button("🔄 Convert to DOCX", type="primary", use_container_width=True):
                with st.spinner("Converting PDF to DOCX..."):
                    # Use unique filename for output to prevent collisions
                    session_id = st.session_state.get('session_id', str(uuid.uuid4())[:8])
                    unique_id = str(uuid.uuid4())[:8]
                    output_filename = f"converted_{Path(pdf_file.name).stem}_{session_id}_{unique_id}.docx"
                    output_path = os.path.join(Config.OUTPUT_FOLDER, output_filename)
                    
                    # Track output file for cleanup
                    st.session_state.uploaded_files.append(output_path)
                    
                    result = DocumentProcessor.convert_pdf_to_docx(pdf_path, output_path)
                    
                    if result['success']:
                        st.success(f"✅ {result['message']}")
                        
                        # Provide download button
                        with open(output_path, 'rb') as f:
                            st.download_button(
                                "📥 Download DOCX",
                                data=f,
                                file_name=output_filename,
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                    else:
                        st.error(f"❌ {result['message']}")
    
    
     


if __name__ == "__main__":
    main()
