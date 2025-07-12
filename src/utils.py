"""
Utility functions
"""

import logging
import os
from typing import Optional

def setup_logging(verbose: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def validate_openai_key(api_key: Optional[str]) -> bool:
    """Validate OpenAI API key."""
    if not api_key:
        return False
    
    # Basic validation - should start with 'sk-'
    if not api_key.startswith('sk-'):
        return False
    
    return True

def count_tokens(text: str, model: str = 'gpt-4') -> int:
    """Count tokens in text."""
    try:
        import tiktoken
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except:
        # Rough estimation: 1 token ≈ 4 characters
        return len(text) // 4

def truncate_content(content: str, max_tokens: int = 1000, model: str = 'gpt-4') -> str:
    """Truncate content to fit within token limit."""
    current_tokens = count_tokens(content, model)
    
    if current_tokens <= max_tokens:
        return content
    
    # Rough truncation based on character count
    ratio = max_tokens / current_tokens
    truncated_length = int(len(content) * ratio * 0.9)  # 90% to be safe
    
    return content[:truncated_length] + "\n... (truncated)"