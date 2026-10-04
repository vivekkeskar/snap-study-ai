# 📚 Snap & Study AI

> **Upload it. Understand it. Master it.**

Snap & Study AI is an intelligent, interactive study assistant built using Python, Streamlit, and Google's modern Gemini SDK (`google-genai`). It allows students to ask complex study questions, upload photos of textbook pages, handwritten notes, diagrams, and programming error logs, receive step-by-step solutions, and automatically email structured revision notes to themselves.

---

## 🌟 Key Features

- 💬 **Interactive Gemini Chat**: Session-persisted multi-turn chat powered by `gemini-2.5-flash`.
- 📸 **Multimodal Image Support**: Upload handwritten notes, textbook pages, diagrams, or code screenshots (`.png`, `.jpg`, `.jpeg`, `.webp`).
- 🎯 **Tailored Study Modes**:
  - Direct Explanation
  - Step-by-Step Problem Solving
  - Code Explanation & Bug Fixing
  - Simplify (Explain Like I'm 5)
  - Short Notes Generation
  - Interview Questions
  - Example Generator
  - Alternative Explanations
- 🌐 **Multilingual Learning**: Native comprehension and response capability for English, Hindi, and Marathi.
- 📧 **Automated Email Notes**: Summarize key concepts from the chat and dispatch high-quality revision notes directly to the student's email via Gmail SMTP.
- 🧹 **Instant Session Reset**: Clear session history while maintaining student onboarding info.

---

## 🛠️ Technology Stack

- **Framework**: Python 3.9+ & Streamlit
- **LLM Engine**: Google Gemini (`google-genai` SDK, model: `gemini-2.5-flash`)
- **Email Service**: Python `smtplib` + Gmail SSL SMTP
- **Session Management**: Streamlit Session State
- **Config Management**: Streamlit Secrets (`secrets.toml`)

---

## 📂 Project Structure

```text
snap-study-ai/
│
├── app.py                      # Main Streamlit application UI & control flow
├── prompts.py                  # Tutor system prompt & email summary instructions
├── requirements.txt            # Project dependencies (streamlit, google-genai)
├── .gitignore                  # Git ignore rules for secrets and environment files
├── README.md                   # Project documentation
│
└── .streamlit/
    └── secrets.toml.example    # Configuration template for API keys & credentials
```

---

## 🚀 Quickstart & Local Setup

### 1. Prerequisites
Ensure you have Python 3.9 or higher installed.

### 2. Clone Repository & Navigate
```bash
git clone https://github.com/your-username/snap-study-ai.git
cd snap-study-ai
```

### 3. Set Up Virtual Environment & Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Configure Secrets

Create your `.streamlit/secrets.toml` file from the provided template:

```bash
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Open `.streamlit/secrets.toml` and fill in your credentials:

```toml
GEMINI_API_KEY = "AIzaSy..."

# Gmail configuration for emailing study notes
GMAIL_ADDRESS = "your-email@gmail.com"
GMAIL_APP_PASSWORD = "xxxx-xxxx-xxxx-xxxx"
```

#### How to get a Gemini API Key:
1. Visit [Google AI Studio](https://aistudio.google.com/).
2. Create a new API key.
3. Paste the key into `GEMINI_API_KEY`.

#### How to generate a Gmail App Password:
1. Enable 2-Step Verification on your Google Account.
2. Go to **Google Account Settings > Security > App Passwords**.
3. Create a new app password named "Snap Study AI".
4. Copy the 16-character code into `GMAIL_APP_PASSWORD`.

---

## 🏃 Running the Application

Launch the Streamlit app locally:

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## ☁️ Deploying to Streamlit Cloud

1. Push your repository to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of Snap & Study AI"
   git branch -M main
   git remote add origin https://github.com/your-username/snap-study-ai.git
   git push -u origin main
   ```
2. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **New app**, select your repository, branch (`main`), and set `app.py` as the main file path.
4. Under **Advanced Settings > Secrets**, paste the contents of your `.streamlit/secrets.toml`.
5. Click **Deploy**!

---

## ❓ Troubleshooting

- **Invalid API Key Error**: Ensure `GEMINI_API_KEY` is accurately set in `.streamlit/secrets.toml` without quotes or whitespace issues.
- **Gmail Auth Failure**: Verify that 2-Factor Authentication is active on your Google account and that you are using a 16-character App Password, not your standard account password.
- **Image Upload Issues**: Supported formats are JPG, JPEG, PNG, and WEBP. For optimal performance, ensure images are clear and well-lit.

---

## 📄 License

Distributed under the MIT License. Feel free to use and modify for personal study or portfolio projects.
