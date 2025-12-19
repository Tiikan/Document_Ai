# 📄 Document AI Assistant

A powerful AI-powered document processing application that helps you extract insights from your documents. Upload files or paste text directly, and get intelligent AI-generated summaries in multiple languages including English and Khmer (ភាសាខ្មែរ).

---

## 🌟 Features

### Core Capabilities

- **📤 Multi-Format File Upload**: Upload PDF, DOCX, or TXT files
- **✍️ Direct Text Input**: Paste or type text directly without creating a file
- **🤖 AI-Powered Summarization**: Generate intelligent summaries using OpenAI GPT-4o-mini
- **🌐 Multi-Language Support**: Full support for Khmer (ភាសាខ្មែរ) and English
- **🔄 PDF to DOCX Conversion**: Convert PDF files to editable DOCX format
- **📊 Document Analytics**: View document metadata and statistics
- **🎨 Modern Dark UI**: Professional dark-themed interface with smooth interactions

### Summary Types

Choose from four different summary styles:
1. **Comprehensive**: Detailed summary covering all main points and key details
2. **Brief**: Quick 2-3 sentence overview
3. **Bullet Points**: Key ideas in clear bullet point format
4. **Executive**: Business-focused summary suitable for stakeholders

### Language Options send
- **English**: Get summaries in English
- **Khmer (ភាសាខ្មែរ)**: Get summaries in Khmer language
- **Both Languages**: Get bilingual summaries with both English and Khmer

---

## 🏗️ Project Architecture

### Technology Stack

```
┌─────────────────────────────────────────────────┐
│           Frontend Layer (Streamlit)            │
│  - Dark themed UI with modern design            │
│  - Interactive file upload & text input         │
│  - Real-time document processing feedback       │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│         Application Layer (Python)              │
│  - Document processing orchestration            │
│  - User input handling & validation             │
│  - Session state management                     │
└─────────────────────────────────────────────────┘
                      ↓
┌──────────────────────┬──────────────────────────┐
│  Document Processor  │    AI Summarizer         │
│  - PDF extraction    │  - OpenAI GPT-4o-mini    │
│  - DOCX extraction   │  - Multi-language        │
│  - TXT extraction    │  - Multiple summary types│
│  - PDF→DOCX convert  │  - Token management      │
└──────────────────────┴──────────────────────────┘
```

### Core Components

#### 1. **app.py** - Main Application
The entry point and UI layer of the application.

**Key Responsibilities:**
- Streamlit configuration and page setup
- Custom CSS for dark theme styling
- Session state initialization
- Tab-based navigation (Upload & Analyze, Convert PDF)
- File upload and text input handling
- Summary generation workflow
- Results display and download functionality

**UI Structure:**
```
├── Sidebar
│   ├── Summary Type Selector
│   ├── Language Selector (English/Khmer/Both)
│   └── Max Tokens Slider
│
└── Main Content Area
    ├── Tab 1: Upload & Analyze
    │   ├── Sub-tab: Upload File
    │   │   ├── File uploader (PDF/DOCX/TXT)
    │   │   ├── Document metadata display
    │   │   └── Text preview
    │   └── Sub-tab: Paste Text
    │       ├── Text area input
    │       └── Text statistics (chars/words/lines)
    │
    └── Tab 2: Convert PDF to DOCX
        ├── PDF file uploader
        └── Download converted DOCX
```

#### 2. **utils/document_processor.py** - Document Processing Module

Handles all document extraction and conversion operations.

**Class: DocumentProcessor**

```python
DocumentProcessor
├── extract_text_from_pdf(file_path: str) -> str
│   Purpose: Extract text from PDF files using pdfplumber
│   Process: Opens PDF → Iterates pages → Extracts text → Returns combined text
│   Error Handling: Raises exception with detailed error message
│
├── extract_text_from_docx(file_path: str) -> str
│   Purpose: Extract text from Word documents
│   Process: Opens DOCX → Reads paragraphs → Joins text → Returns string
│   Error Handling: Raises exception for corrupted files
│
├── extract_text_from_txt(file_path: str) -> str
│   Purpose: Read plain text files with encoding detection
│   Process: Try UTF-8 first → Fallback to Latin-1 → Return content
│   Error Handling: Multiple encoding attempts before failing
│
├── extract_text(file_path: str, file_extension: str) -> str
│   Purpose: Universal text extraction dispatcher
│   Process: Detects file type → Routes to appropriate extractor
│   Supported: PDF, DOCX, TXT
│
├── convert_pdf_to_docx(pdf_path: str, output_path: str) -> Dict
│   Purpose: Convert PDF files to editable DOCX format
│   Process: Uses pdf2docx Converter → Saves to output path
│   Returns: {success: bool, output_path: str, message: str}
│
└── get_document_info(file_path: str, file_extension: str) -> Dict
    Purpose: Extract document metadata
    Returns: {file_name, file_size, file_size_mb, file_type, page_count}
```

**Supported File Formats:**
- **PDF**: Text-based PDFs (scanned PDFs require OCR, not included)
- **DOCX**: Microsoft Word documents (.docx format)
- **TXT**: Plain text files with UTF-8 or Latin-1 encoding

#### 3. **utils/ai_summarizer.py** - AI Processing Module

Manages all AI-powered text analysis using OpenAI's GPT-4o-mini model.

**Class: AISummarizer**

```python
AISummarizer
├── __init__(api_key: Optional[str])
│   Purpose: Initialize OpenAI client
│   Validation: Ensures API key is provided
│
├── summarize(text, summary_type, max_tokens, language) -> Dict
│   Purpose: Generate AI-powered summaries
│   
│   Parameters:
│   - text: Content to summarize
│   - summary_type: 'comprehensive'|'brief'|'bullet_points'|'executive'
│   - max_tokens: Response length limit (200-2000)
│   - language: 'en'|'km'|'both'
│   
│   Process:
│   1. Validate text input
│   2. Build language-specific prompt
│   3. Select summary type template
│   4. Send request to OpenAI API
│   5. Parse and return response
│   
│   Returns: {
│       success: bool,
│       summary: str,
│       model: str,
│       tokens_used: int,
│       summary_type: str,
│       language: str
│   }
│
└── extract_key_points(text: str) -> Dict
    Purpose: Extract key information from documents
    Temperature: 0.5 (more focused responses)
    Max Tokens: 800
    Returns: {success, key_points, tokens_used}
```

**AI Model Configuration:**
- **Model**: GPT-4o-mini (cost-effective, fast, high-quality)
- **Default Tokens**: 1000 (adjustable from 200-2000)
- **Temperature**: 0.7 (balanced creativity/consistency)

**Language Support Implementation:**
```python
language_instructions = {
    'en': "",  # Default English
    'km': "Please provide the summary in Khmer language (ភាសាខ្មែរ).",
    'both': "Provide in both English and Khmer, clearly separated."
}
```

#### 4. **config.py** - Configuration Management

Centralized configuration for the entire application.

```python
class Config:
    # API Configuration
    OPENAI_API_KEY          # Loaded from .env file
    
    # File Handling
    UPLOAD_FOLDER = 'uploads'         # Temporary file storage
    OUTPUT_FOLDER = 'outputs'         # Converted files
    MAX_FILE_SIZE = 16 MB             # Upload limit
    ALLOWED_EXTENSIONS = PDF, DOCX, TXT
    
    # AI Model Settings
    AI_MODEL = 'gpt-4o-mini'          # OpenAI model
    MAX_TOKENS = 1000                 # Default response length
    TEMPERATURE = 0.7                 # Creativity level
    
    # Application Info
    APP_NAME = \"Document AI Assistant\"
    APP_VERSION = \"1.0.0\"
```

**Directory Auto-Creation:**
The config automatically creates necessary directories:
- `uploads/` - Stores temporarily uploaded files
- `outputs/` - Stores converted PDF→DOCX files

---

## 📂 Project Structure

```
document-ai-assistant/
│
├── app.py                          # Main Streamlit application
├── config.py                       # Configuration management
├── requirements.txt                # Python dependencies
│
├── .env                           # Environment variables (create this)
├── .env.example                   # Environment template
├── .gitignore                     # Git ignore rules
│
├── utils/                         # Core utility modules
│   ├── __init__.py
│   ├── document_processor.py      # Document extraction & conversion
│   └── ai_summarizer.py           # AI-powered summarization
│
├── uploads/                       # Uploaded files (auto-created)
├── outputs/                       # Converted files (auto-created)
│
├── start.bat                      # Windows launcher
├── start.sh                       # Unix/Linux launcher
│
└── docs/                          # Additional documentation
    ├── README.md                  # This file
    ├── KHMER_SUPPORT.md           # Khmer language guide
    ├── TEXT_INPUT_FEATURE.md      # Text input documentation
    ├── KHMER_UPDATE.md            # Language feature changelog
    └── SETUP_COMPLETE.md          # Initial setup guide
```

---

## 🚀 Installation & Setup

### Prerequisites

- **Python 3.8+** (Recommended: Python 3.10 or 3.11)
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **Internet Connection** (for OpenAI API calls)

### Step-by-Step Installation

#### 1. Clone or Navigate to Project

```bash
cd d:/MyWorking/Dev+Program/OwnProject/Django
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required Packages:**
```
streamlit==1.29.0          # Web interface
pdfplumber==0.10.3         # PDF text extraction
python-docx==1.1.0         # DOCX processing
openai==1.6.1              # OpenAI API client
Flask==3.0.0               # Web framework
flask-cors==4.0.0          # CORS handling
python-magic-bin==0.4.14   # File type detection
Pillow==10.1.0             # Image processing
pypdf==3.17.4              # PDF utilities
pdf2docx==0.5.6            # PDF conversion
python-dotenv==1.0.0       # Environment variables
```

#### 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the template
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**⚠️ Important:**
- Never commit the `.env` file to version control
- Keep your API key secure and private
- The app will not work without a valid API key

#### 4. Run the Application

**Option A: Using Python Module**
```bash
python -m streamlit run app.py
```

**Option B: Using Direct Command** (if streamlit is in PATH)
```bash
streamlit run app.py
```

**Option C: Using Launcher Scripts**

Windows:
```bash
start.bat
```

Unix/Linux/Mac:
```bash
chmod +x start.sh
./start.sh
```

The application will automatically open in your default browser at:
```
http://localhost:8501
```

---

## 📖 Usage Guide

### Basic Workflow

```
┌─────────────────────────────────────────────┐
│ Step 1: Choose Input Method                │
│  ├─ Upload File (PDF/DOCX/TXT)             │
│  └─ Paste Text Directly                    │
└─────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│ Step 2: Configure Settings (Sidebar)       │
│  ├─ Select Summary Type                    │
│  ├─ Choose Language (En/Khmer/Both)        │
│  └─ Adjust Max Tokens (200-2000)           │
└─────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│ Step 3: Generate Summary                   │
│  └─ Click "Generate AI Summary" button     │
└─────────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────────┐
│ Step 4: Review & Download                  │
│  ├─ Read the AI-generated summary          │
│  ├─ View tokens used                       │
│  └─ Download summary as TXT file           │
└─────────────────────────────────────────────┘
```

### Feature 1: Upload & Analyze Documents

#### Method A: File Upload

1. Navigate to **"📤 Upload & Analyze"** tab
2. Stay on **"📤 Upload File"** sub-tab
3. Click **"Choose a file"**
4. Select your document (PDF, DOCX, or TXT)
5. Wait for text extraction
6. Review extracted text in the preview
7. Click **"🤖 Generate AI Summary"**
8. Download summary if needed

**Supported Files:**
- PDF files (text-based, not scanned)
- Microsoft Word documents (.docx)
- Plain text files (.txt)

**File Information Displayed:**
- File name
- File size (in MB)
- Page count (for PDFs)
- Total characters extracted

#### Method B: Direct Text Input

1. Navigate to **"📤 Upload & Analyze"** tab
2. Click **"✍️ Paste Text"** sub-tab
3. Paste or type your text in the text area
4. View real-time statistics:
   - Character count
   - Word count
   - Line count
5. Click **"🤖 Generate AI Summary"**
6. Download summary if needed

**Best For:**
- Quick analysis without creating files
- Copying text from websites or emails
- Testing the summarization feature
- Processing short snippets

### Feature 2: PDF to DOCX Conversion

1. Navigate to **"🔄 Convert PDF to DOCX"** tab
2. Upload a PDF file
3. Click **"🔄 Convert to DOCX"**
4. Wait for conversion (may take a few seconds)
5. Download the converted DOCX file

**Notes:**
- Works best with text-based PDFs
- Maintains basic formatting
- Complex layouts may require manual adjustment
- Scanned PDFs require OCR (not included)

### Feature 3: Multi-Language Summaries

#### English Summary
1. In sidebar, select language: **"English"**
2. Upload file or paste text
3. Generate summary
4. Receive summary in English

#### Khmer Summary
1. In sidebar, select language send: **"ខ្មែរ (Khmer)"**
2. Upload file or paste text (any language)
3. Generate summary
4. Receive summary in Khmer (ភាសាខ្មែរ)

#### Bilingual Summary
1. In sidebar, select: **"🌐 Both / ទាំងពីរ"**
2. Upload file or paste text
3. Generate summary
4. Receive summary in both languages

**Language Support Details:**
- Full Unicode support for Khmer characters
- Google Noto Sans Khmer font for proper rendering
- AI translation powered by GPT-4o-mini
- Context-aware translations (not word-for-word)

---

## ⚙️ Configuration Options

### Sidebar Settings

#### 1. Summary Type
Choose the style of summary you need:

```
Comprehensive (Default)
├─ Most detailed option
├─ Covers all main points and key details
├─ Best for: Thorough understanding
└─ Typical length: 3-5 paragraphs

Brief
├─ Quick 2-3 sentence overview
├─ Captures main idea only
├─ Best for: Quick scanning
└─ Typical length: 2-3 sentences

Bullet Points
├─ Key ideas in list format
├─ Easy to scan and reference
├─ Best for: Presentations, notes
└─ Typical length: 5-10 bullet points

Executive
├─ Business-focused summary
├─ Highlights key decisions and stakeholder impact
├─ Best for: Business reports, memos
└─ Typical length: 1-2 paragraphs
```

#### 2. Output Language
```
English        → Summary in English only
ខ្មែរ (Khmer)  → Summary in Khmer only
Both / ទាំងពីរ  → Summary in both languages
```

#### 3. Max Summary Tokens
```
200   → Very brief (1-2 paragraphs)
500   → Short summary
1000  → Standard (default)
1500  → Detailed summary
2000  → Maximum detail
```

**Token Guide:**
- 1 token ≈ 4 characters in English
- 1 token ≈ 2-3 characters in Khmer
- More tokens = longer, more detailed summary
- More tokens = higher API costs

### File Configuration (config.py)

To modify application settings, edit `config.py`:

```python
class Config:
    # Change AI model
    AI_MODEL = 'gpt-4o-mini'  # or 'gpt-4', 'gpt-3.5-turbo'
    
    # Adjust default summary length
    MAX_TOKENS = 1000  # Change default
    
    # Modify creativity level
    TEMPERATURE = 0.7  # 0.0 = consistent, 1.0 = creative
    
    # Change file size limit
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB default
    
    # Modify upload directory
    UPLOAD_FOLDER = 'uploads'  # Change folder name
```

---

## 🎨 User Interface

### Design Philosophy

The application features a modern **dark theme** design:

```css
Color Scheme:
├─ Background: #1A1A1A (Dark gray)
├─ Cards: Dark with white borders
├─ Text: White (#FFFFFF)
├─ Buttons: Purple gradient (#667eea → #764ba2)
└─ Accents: Success (green), Error (red)
```

### Key UI Elements

1. **File Uploader**
   - Drag-and-drop support
   - Visual file type indicators
   - Progress feedback

2. **Text Area**
   - Large, comfortable input field
   - Helpful placeholder text
   - Real-time character count send

3. **Summary Display**
   - Clean card layout
   - Formatted text rendering
   - Supports markdown in Khmer

4. **Metrics Dashboard**
   - Token usage tracking
   - File statistics
   - Processing time (implicit)

---

## 🔧 Troubleshooting

### Common Issues

#### Issue 1: "streamlit: command not found"

**Solution:**
```bash
# Use Python module syntax instead
python -m streamlit run app.py
```

#### Issue 2: OpenAI API Error

**Possible Causes:**
- Invalid API key
- Insufficient credits
- Network connectivity issues

**Solutions:**
1. Verify API key in `.env` file is correct
2. Check your OpenAI account has credits
3. Test API key at https://platform.openai.com

#### Issue 3: PDF Extraction produces gibberish

**Cause:** PDF is scanned (image-based), not text-based

**Solution:**
- Use text-based PDFs only
- Or use OCR software first to convert to text
- Current version does not include OCR

#### Issue 4: File Upload Fails

**Possible Causes:**
- File too large (>16MB)
- Unsupported format
- Corrupted file

**Solutions:**
1. Check file size: `file_size_mb` metric
2. Verify format: PDF, DOCX, or TXT only
3. Try opening file in another program to test

#### Issue 5: Khmer Text Not Displaying

**Cause:** Browser font support issues

**Solutions:**
1. Update browser to latest version
2. Clear browser cache
3. Try different browser (Chrome/Firefox recommended)
4. Check Noto Sans Khmer font loads (inspect network tab)

#### Issue 6: Summary Takes Too Long

**Possible Causes:**
- Very large document
- High token limit
- OpenAI API server delay

**Solutions:**
1. Reduce max tokens in sidebar
2. Split large documents into sections
3. Try again (API delays are usually temporary)

---

## 📊 Performance & Optimization

### Processing Speed

```
File Upload & Extraction:
├─ PDF (10 pages):    2-5 seconds
├─ DOCX (Medium):     1-2 seconds
└─ TXT (Any size):    <1 second

AI Summarization:
├─ Brief (200 tokens):         3-5 seconds
├─ Standard (1000 tokens):     5-10 seconds
└─ Detailed (2000 tokens):     10-15 seconds

PDF to DOCX Conversion:
└─ Varies by PDF complexity:   5-30 seconds
```

### Resource Usage

```
Memory:
├─ Base Application:    ~200MB
├─ Per PDF (loaded):    ~10-50MB
└─ AI Processing:       Minimal (API-based)

Disk Space:
├─ Application:         ~50MB
├─ Dependencies:        ~300MB
└─ User Files:          Varies (temporary)
```

### Optimization Tips

1. **For Large Documents:**
   - Process in smaller chunks
   - Use lower token limits
   - Choose "brief" summary type

2. **For Batch Processing:**
   - Upload one file at a time
   - Clear `uploads/` folder periodically
   - Monitor token usage costs

3. **For Cost Optimization:**
   - Use lower max token values
   - Choose appropriate summary type
   - Avoid generating multiple summaries of same content

---

## 🔒 Security & Privacy

### Data Handling

```
User Files:
├─ Stored locally in uploads/ folder
├─ Automatically named based on upload name
├─ NOT automatically deleted
└─ Recommendation: Clear periodically

API Communication:
├─ Sent to OpenAI servers via HTTPS
├─ Subject to OpenAI's data policy
├─ May be used for OpenAI API improvement
└─ Recommendation: Don't process sensitive data

API Key:
├─ Stored in .env file (git-ignored)
├─ Loaded at runtime only
├─ Never exposed to frontend
└─ Recommendation: Keep .env file secure
```

### Security Best Practices

1. **Never commit `.env` file** to version control
2. **Clear `uploads/` folder** regularly
3. **Don't process confidential documents** (sent to OpenAI)
4. **Use environment variables** for API keys
5. **Keep dependencies updated** (`pip install -U -r requirements.txt`)

### GDPR & Compliance

⚠️ **Important:** This application:
- Sends document content to OpenAI's servers
- Stores files temporarily on local disk
- Does not include user authentication
- Is intended for personal/internal use

**For production/public deployment:**
- Add user authentication
- Implement file cleanup routines
- Add usage logging
- Review OpenAI's data processing agreement
- Implement proper access controls

---

## 💡 Use Cases & Examples

### 1. Academic Research
```
Scenario: Student with multiple research papers

Workflow:
1. Upload PDF of research paper
2. Select "Comprehensive" summary
3. Choose "English" language
4. Generate summary
5. Download for notes

Benefit: Quick understanding of key findings
```

### 2. Business Documents
```
Scenario: Executive reviewing reports

Workflow:
1. Paste email content or upload PDF report
2. Select "Executive" summary
3. Choose "English"
4. Generate summary
5. Share with team

Benefit: Rapid decision-making support
```

### 3. Translation & Learning
```
Scenario: Khmer student learning English

Workflow:
1. Paste English article text
2. Select "Both" languages
3. Generate bilingual summary
4. Compare English and Khmer versions

Benefit: Language learning aid
```

###4. Content Creation
```
Scenario: Writer summarizing drafts

Workflow:
1. Paste draft article
2. Select "Bullet Points"
3. Review key points
4. Refine original content

Benefit: Ensure main ideas are clear
```

---

## 🚧 Limitations & Known Issues

### Current Limitations

1. **No OCR Support**
   - Scanned PDFs cannot be processed
   - Only text-based PDFs work
   - Consider pre-processing with OCR software

2. **No Batch Processing**
   - One file/text at a time
   - For multiple files, process sequentially

3. **No User Authentication**
   - Open access to anyone with URL
   - Not suitable for multi-user production deployment

4. **No File Cleanup**
   - Uploaded files remain in uploads/
   - Manual cleanup required

5. **API Dependency**
   - Requires internet connection
   - Subject to OpenAI service availability
   - Costs accrue per API call

### Known Issues

- Very large PDFs (>100 pages) may timeout
- Complex PDF layouts may extract garbled text
- Khmer text in older browsers may render incorrectly
- PDF to DOCX conversion may not preserve complex formatting

---

## 🔄 Future Enhancements

### Planned Features

- [ ] OCR support for scanned documents
- [ ] Batch file processing
- [ ] Custom summary templates
- [ ] User authentication system
- [ ] Automatic file cleanup
- [ ] Usage analytics dashboard
- [ ] Support for more file formats (RTF, ODT)
- [ ] Cloud storage integration (Google Drive, Dropbox)
- [ ] Export summaries to PDF
- [ ] Multi-document comparison
- [ ] Streaming responses for long documents
- [ ] Offline mode with local AI models

---

## 📞 Support & Contribution

### Getting Help

- **Documentation**: Check this README and other `.md` files
- **Issues**: Report bugs or request features
- **Community**: Share your use cases and feedback

### Contributing

Contributions are welcome! Areas for contribution:
- Bug fixes
- Feature enhancements
- Documentation improvements
- Translation (additional languages)
- UI/UX improvements

---

## 📄 License

MIT License - Feel free to use this project for personal or commercial purposes.

---

## 🙏 Acknowledgments

### Technologies Used

- **Streamlit** - Web framework
- **OpenAI** - GPT-4o-mini AI model
- **pdfplumber** - PDF text extraction
- **python-docx** - DOCX processing
- **pdf2docx** - PDF conversion
- **Google Fonts** - Noto Sans Khmer font

### Special Thanks

- OpenAI for providing powerful AI APIs
- Streamlit team for the amazing framework
- Open source community for the libraries

---

## 📝 Version History

### Version 1.0.0 (Current)
- ✅ Multi-format file upload (PDF, DOCX, TXT)
- ✅ Direct text input
- ✅ AI summarization with 4 types
- ✅ Multi-language support (English, Khmer)
- ✅ PDF to DOCX conversion
- ✅ Dark themed modern UI
- ✅ Real-time text statistics
- ✅ Download summaries

---

**Built with ❤️ using Python, OpenAI, and Streamlit**

*Document AI Assistant - Transform your documents into insights*
