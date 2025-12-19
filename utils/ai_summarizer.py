from openai import OpenAI
from typing import Optional, Dict
from config import Config


class AISummarizer:
    """Handles AI-powered document summarization using OpenAI"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenAI client"""
        self.api_key = api_key or Config.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        self.client = OpenAI(api_key=self.api_key)
    
    def summarize(
        self, 
        text: str, 
        summary_type: str = "comprehensive",
        max_tokens: int = None,
        language: str = "en"
    ) -> Dict[str, str]:
        """
        Summarize text using OpenAI API with language support
        
        Args:
            text: The text to summarize
            summary_type: Type of summary ('brief', 'comprehensive', 'bullet_points')
            max_tokens: Maximum tokens for the response
            language: Output language ('en' for English, 'km' for Khmer, etc.)
            
        Returns:
            Dictionary with summary and metadata
        """
        if not text or len(text.strip()) == 0:
            return {
                'success': False,
                'summary': '',
                'error': 'No text provided for summarization'
            }
        
        # Language-specific instructions
        language_instructions = {
            'en': "",
            'km': "Please provide the summary in Khmer language (ភាសាខ្មែរ). ",
            'both': "Please provide the summary in both English and Khmer language (ភាសាខ្មែរ), clearly separating each language section. "
        }
        
        lang_instruction = language_instructions.get(language, "")
        
        # Prepare prompt based on summary type
        prompts = {
            'brief': f"{lang_instruction}Provide a brief 2-3 sentence summary of the following document:",
            'comprehensive': f"{lang_instruction}Provide a comprehensive summary of the following document, covering all main points and key details:",
            'bullet_points': f"{lang_instruction}Summarize the following document in clear bullet points, highlighting the main ideas:",
            'executive': f"{lang_instruction}Create an executive summary of the following document, suitable for business stakeholders:"
        }
        
        prompt = prompts.get(summary_type, prompts['comprehensive'])
        
        try:
            response = self.client.chat.completions.create(
                model=Config.AI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert multilingual document analyst. Provide clear, accurate, and well-structured summaries in the requested language. You are proficient in English, Khmer (ភាសាខ្មែរ), and other languages."
                    },
                    {
                        "role": "user",
                        "content": f"{prompt}\n\n{text}"
                    }
                ],
                max_tokens=max_tokens or Config.MAX_TOKENS,
                temperature=Config.TEMPERATURE
            )
            
            summary = response.choices[0].message.content.strip()
            
            return {
                'success': True,
                'summary': summary,
                'model': Config.AI_MODEL,
                'tokens_used': response.usage.total_tokens,
                'summary_type': summary_type,
                'language': language
            }
            
        except Exception as e:
            return {
                'success': False,
                'summary': '',
                'error': f'Summarization failed: {str(e)}'
            }
    
    def extract_key_points(self, text: str) -> Dict[str, any]:
        """Extract key points from the document"""
        try:
            response = self.client.chat.completions.create(
                model=Config.AI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at identifying key information in documents."
                    },
                    {
                        "role": "user",
                        "content": f"Extract the key points, main topics, and important details from this document:\n\n{text}"
                    }
                ],
                max_tokens=800,
                temperature=0.5
            )
            
            key_points = response.choices[0].message.content.strip()
            
            return {
                'success': True,
                'key_points': key_points,
                'tokens_used': response.usage.total_tokens
            }
            
        except Exception as e:
            return {
                'success': False,
                'key_points': '',
                'error': f'Key point extraction failed: {str(e)}'
            }
    
    