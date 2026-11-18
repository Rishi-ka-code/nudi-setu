# -*- coding: utf-8 -*-
"""
Backend Configuration for Kannada Dialect Converter.
Loads API keys from environment variables or local .env file.
The UI never exposes or requires entering API keys.
"""

import os
from pathlib import Path

# Look for .env file in project root if available locally
env_path = Path(__file__).resolve().parent.parent / ".env"
if env_path.exists():
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key not in os.environ:
                        os.environ[key] = val
    except Exception:
        pass

# Loaded API Key (silently available to backend)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
