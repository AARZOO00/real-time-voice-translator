"""
Translator using Claude API for more accurate translations
"""

import anthropic
import os

class ClaudeTranslator:
    def __init__(self, api_key=None):
        # Note: API key should be in environment variable
        self.client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
    
    def translate(self, text, source_lang, target_lang):
        """Translate using Claude"""
        lang_map = {
            'hi': 'Hindi',
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German'
        }
        
        source = lang_map.get(source_lang, source_lang)
        target = lang_map.get(target_lang, target_lang)
        
        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": f"Translate this {source} text to {target}. Return ONLY the translation:\n\n{text}"
            }]
        )
        
        return message.content[0].text.strip()