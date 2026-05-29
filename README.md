# 🧠 CodeInsight AI

> **AI-powered code analysis tool** that explains, debugs, optimizes, and quizzes you on your code — powered by Groq's blazing-fast LLaMA 3.3 70B.

---

## ✨ Features

- **Line-by-line Explanation** — Understand exactly what every line of your code does, in beginner or advanced mode
- **Bug Detection & Auto-Fix** — Identifies Syntax, Runtime, and Logic errors with specific fixes
- **Time & Space Complexity** — Instant Big-O analysis with reasoning
- **Code Optimization** — Concrete before/after suggestions to make your code faster and cleaner
- **Dry Run Tracer** — Step-by-step execution trace showing variable states at each stage
- **Expected Output** — Know what your code will print or return before running it
- **Key Concepts Tagger** — Highlights the programming concepts your code uses (recursion, sorting, etc.)
- **MCQ Quiz Generator** — Auto-generates 4 multiple-choice questions to test your understanding
- **Beginner & Advanced Modes** — Toggle depth of explanations based on your experience level

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| AI Engine | [Groq API](https://console.groq.com) — `llama-3.3-70b-versatile` |
| CORS | Flask-CORS |
| Config | python-dotenv |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- A free [Groq API key](https://console.groq.com)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yoursudaycharan/CodeInsight-AI.git
cd CodeInsight-AI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up your API key
cp .env.example .env
# Edit .env and add your Groq API key:
# GROQ_API_KEY=your_key_here

# 4. Run the server
python app.py
```

The app will be live at **http://localhost:5000**

---

## 🔑 Environment Variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free API key at [console.groq.com](https://console.groq.com).

---

## 📡 API Reference

### `POST /analyze`

Analyze a code snippet and get a full AI-powered breakdown.

**Request Body:**

```json
{
  "code": "def factorial(n):\n    return 1 if n == 0 else n * factorial(n-1)",
  "language": "python",
  "mode": "beginner"
}
```

| Field | Type | Values | Description |
|---|---|---|---|
| `code` | string | — | The source code to analyze (max 8000 chars) |
| `language` | string | `python`, `javascript`, `java`, `c`, `cpp` | Programming language |
| `mode` | string | `beginner`, `advanced` | Explanation depth |

**Response:**

```json
{
  "complexity": {
    "time": "O(n) — linear due to n recursive calls",
    "space": "O(n) — call stack grows with each recursion"
  },
  "concepts": ["recursion", "base case", "factorial"],
  "explanation": {
    "1": "Defines a function named factorial that takes one argument n",
    "2": "Returns 1 if n is 0 (base case), otherwise returns n multiplied by factorial(n-1)"
  },
  "errors": [],
  "corrected_code": "...",
  "optimization": "...",
  "dry_run": "...",
  "expected_output": "factorial(5) → 120",
  "quiz": [...]
}
```

### `GET /health`

Check API status and configuration.

```json
{
  "status": "ok",
  "groq_configured": true,
  "model": "llama-3.3-70b-versatile"
}
```

---

## 📁 Project Structure

```
codeinsight-ai/
├── app.py              # Flask backend & API routes
├── requirements.txt    # Python dependencies
├── .env                # Environment variables (not committed)
├── .env.example        # Example env file
└── templates/
    └── index.html      # Frontend UI
```

---

## 🌐 Supported Languages

- Python
- JavaScript
- Java
- C
- C++

---

## ⚙️ Configuration

| Setting | Default | Description |
|---|---|---|
| Max code length | 8000 chars | Prevents oversized requests |
| AI Temperature | 0.3 | Low for consistent, factual output |
| Max tokens | 4096 | Response length limit |
| Model | `llama-3.3-70b-versatile` | Groq's most capable model |

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Groq](https://groq.com) for their ultra-fast LLM inference API
- [Meta AI](https://ai.meta.com) for the LLaMA 3.3 model
- [Flask](https://flask.palletsprojects.com) for the lightweight web framework

---

<p align="center">Built with ❤️ and a lot of <code>print("debug")</code></p>
