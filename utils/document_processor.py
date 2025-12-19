import pdfplumber
from docx import Document
from pdf2docx import Converter
import os
from typing import Optional, Dict


class DocumentProcessor:
    """Handles document extraction and conversion"""
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
        return text.strip()
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            raise Exception(f"Error extracting text from DOCX: {str(e)}")
        return text.strip()
    
    @staticmethod
    def extract_text_from_txt(file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except UnicodeDecodeError:
            # Try with different encoding if UTF-8 fails
            with open(file_path, 'r', encoding='latin-1') as file:
                text = file.read()
        except Exception as e:
            raise Exception(f"Error reading TXT file: {str(e)}")
        return text.strip()
    
    @staticmethod
    def extract_text(file_path: str, file_extension: str) -> str:
        """Extract text based on file type"""
        extension = file_extension.lower().replace('.', '')
        
        if extension == 'pdf':
            return DocumentProcessor.extract_text_from_pdf(file_path)
        elif extension == 'docx':
            return DocumentProcessor.extract_text_from_docx(file_path)
        elif extension == 'txt':
            return DocumentProcessor.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {extension}")
    
    @staticmethod
    def convert_pdf_to_docx(pdf_path: str, output_path: str) -> Dict[str, str]:
        """Convert PDF to DOCX format"""
        try:
            cv = Converter(pdf_path)
            cv.convert(output_path)
            cv.close()
            
            return {
                'success': True,
                'output_path': output_path,
                'message': 'PDF successfully converted to DOCX'
            }
        except Exception as e:
            return {
                'success': False,
                'output_path': None,
                'message': f'Conversion failed: {str(e)}'
            }
    
    @staticmethod
    def get_document_info(file_path: str, file_extension: str) -> Dict:
        """Get basic information about the document"""
        file_size = os.path.getsize(file_path)
        
        info = {
            'file_name': os.path.basename(file_path),
            'file_size': file_size,
            'file_size_mb': round(file_size / (1024 * 1024), 2),
            'file_type': file_extension.upper()
        }
        
        # Add page count for PDF
        if file_extension.lower() == '.pdf':
            try:
                with pdfplumber.open(file_path) as pdf:
                    info['page_count'] = len(pdf.pages)
            except:
                info['page_count'] = 'Unknown'
        
        return info
