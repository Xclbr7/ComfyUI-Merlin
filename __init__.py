import os
import sys
import subprocess

# Try to install the Google AI SDK if it's not already installed
try:
    import google.generativeai as genai
except ImportError:
    print("Google AI SDK not found. Attempting to install...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-generativeai"])
    import google.generativeai as genai

# Import the node classes from separate files
from .gemini_prompt_expander import GeminiPromptExpander, NODE_CLASS_MAPPINGS as GEMINI_NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS
from .magic_photo_prompt import NODE_CLASS_MAPPINGS as MAGIC_PHOTO_NODE_CLASS_MAPPINGS

WEB_DIRECTORY = "./web"

# Merge the NODE_CLASS_MAPPINGS dictionaries
NODE_CLASS_MAPPINGS = {**GEMINI_NODE_CLASS_MAPPINGS, **MAGIC_PHOTO_NODE_CLASS_MAPPINGS}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
