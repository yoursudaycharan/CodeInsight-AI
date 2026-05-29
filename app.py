"""
CodeInsight AI — Flask Backend
Powered by Groq API (llama-3.3-70b-versatile)
"""

import os
import json
import re
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # loads GROQ_API_KEY from .env file

app = Flask(__name__)
CORS(app)

# ─── Groq client ───────────────────────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


# ─── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are CodeInsight AI, an expert programming tutor and code analyst.
You MUST respond with ONLY valid JSON — no markdown, no backticks, no extra text.

Your JSON must EXACTLY follow this schema:
{
  "complexity": {
    "time": "O(n) — linear time because...",
    "space": "O(1) — constant space because..."
  },
  "concepts": ["array", "recursion", "loop"],
  "explanation": {
    "1": "Line 1 does X...",
    "2": "Line 2 does Y..."
  },
  "errors": [
    {
      "type": "SyntaxError|RuntimeError|LogicError",
      "line": 5,
      "message": "Detailed error description",
      "fix": "How to fix it"
    }
  ],
  "corrected_code": "full corrected code here",
  "optimization": "Detailed optimization suggestions with code examples",
  "dry_run": "Step-by-step trace of code execution with variable states",
  "expected_output": "What the code prints or returns",
  "quiz": [
    {
      "question": "What does this function return when n=5?",
      "options": ["A) 5", "B) 10", "C) 15", "D) 25"],
      "answer": "B) 10"
    }
  ]
}

Rules:
- explanation keys must be string integers matching actual line numbers
- errors array is empty [] if no errors found
- corrected_code is the fixed version (same as original if no fixes needed)
- quiz has exactly 4 MCQ questions, each with 4 options (A/B/C/D prefix)
- dry_run traces variable values step by step
- optimization includes concrete suggestions with before/after code snippets
- Be beginner-friendly or advanced based on mode parameter
- ONLY output the JSON object, nothing else"""


def build_user_prompt(code: str, language: str, mode: str) -> str:
    return f"""Analyze this {language} code in {mode} mode.

CODE:
```{language}
{code}
```

Provide complete analysis in the exact JSON schema. Include all 4 quiz questions."""


def extract_json(text: str) -> dict:
    """Robustly extract JSON from model response."""
    text = text.strip()
    # Remove markdown code fences if present
    text = re.sub(r'^```(?:json)?\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to find JSON object within response
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            return json.loads(match.group())
        raise


# ─── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    if not client:
        return jsonify({"error": "GROQ_API_KEY not configured. Set it as an environment variable."}), 500

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    code = data.get("code", "").strip()
    language = data.get("language", "python").strip()
    mode = data.get("mode", "beginner").strip()

    if not code:
        return jsonify({"error": "No code provided"}), 400

    if len(code) > 8000:
        return jsonify({"error": "Code too long (max 8000 characters)"}), 400

    valid_languages = {"python", "javascript", "java", "c", "cpp"}
    if language not in valid_languages:
        return jsonify({"error": f"Unsupported language: {language}"}), 400

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": build_user_prompt(code, language, mode)},
            ],
            temperature=0.3,
            max_tokens=4096,
            response_format={"type": "json_object"},
        )

        raw = response.choices[0].message.content
        result = extract_json(raw)

        # Ensure required keys exist with defaults
        result.setdefault("complexity", {"time": "N/A", "space": "N/A"})
        result.setdefault("concepts", [])
        result.setdefault("explanation", {})
        result.setdefault("errors", [])
        result.setdefault("corrected_code", code)
        result.setdefault("optimization", "No optimization suggestions.")
        result.setdefault("dry_run", "No dry run available.")
        result.setdefault("expected_output", "N/A")
        result.setdefault("quiz", [])

        return jsonify(result)

    except json.JSONDecodeError as e:
        return jsonify({"error": f"Failed to parse AI response: {str(e)}"}), 500
    except Exception as e:
        err_msg = str(e)
        if "api_key" in err_msg.lower() or "authentication" in err_msg.lower():
            return jsonify({"error": "Invalid Groq API key. Check your GROQ_API_KEY environment variable."}), 401
        if "rate_limit" in err_msg.lower():
            return jsonify({"error": "Groq rate limit reached. Please wait a moment and try again."}), 429
        return jsonify({"error": f"Analysis failed: {err_msg}"}), 500


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "groq_configured": bool(GROQ_API_KEY),
        "model": "llama-3.3-70b-versatile"
    })


if __name__ == "__main__":
    if not GROQ_API_KEY:
        print("⚠️  WARNING: GROQ_API_KEY not set!")
        print("   Set it with: export GROQ_API_KEY=your_key_here")
        print("   Get a free key at: https://console.groq.com\n")
    else:
        print("✅ Groq API key loaded")
    print("🚀 CodeInsight AI starting at http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)