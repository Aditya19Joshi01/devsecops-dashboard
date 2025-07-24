# 🔐 DevSecOps Security Scanner

A Dockerized security scanning dashboard that analyzes public GitHub repositories using [Bandit](https://bandit.readthedocs.io/) for Python vulnerabilities and generates AI-based summaries of the findings using Hugging Face.

Built with:
- 🐍 Python (Flask + Streamlit)
- 🐳 Docker + Docker Compose
- 🛡️ Bandit (static security analyzer)
- 📊 MongoDB Atlas (for scan history)
- 🤖 Hugging Face API (for LLM summaries)

---

## 🚀 Features

- 📥 Input any public GitHub repo URL
- 🔎 Run Bandit to identify Python security vulnerabilities
- 📈 View risk score + detailed vulnerability report
- 🤖 AI-generated summary of the report
- 🧠 MongoDB-backed scan history and trends
- 🐳 Fully Dockerized frontend + backend

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Aditya19Joshi01/devsecops-dashboard.git
cd devsecops-dashboard
```

---

### 2. Add your environment variables

Create a `.env` file:

```env
MONGO_URI=mongodb+srv://<username>:<password>@<cluster-url>/...
HUGGINGFACE_API_KEY=your_huggingface_api_key
```

✅ **Important:** Your `.env` is already in `.gitignore`

---

### 3. Build & Run with Docker Compose

```bash
docker-compose build
docker-compose up
```

- Frontend runs at: `http://localhost:8501`
- Backend API at: `http://localhost:5000`

---

## 🧪 Testing It Out

Try scanning some vulnerable repos:

- [`gwen001/pentest-tools`](https://github.com/gwen001/pentest-tools)
- [`milo2012/py-exp`](https://github.com/milo2012/py-exp)
- [`s0md3v/Breacher`](https://github.com/s0md3v/Breacher)

---

## 📂 Project Structure

```
devsecops-dashboard/
├── app.py               # Flask backend API
├── dashboard.py         # Streamlit frontend UI
├── scanner.py           # Clone + scan logic using Bandit
├── summarizer.py        # AI summarizer using HuggingFace
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
├── requirements.txt
├── .env                 # Not pushed
└── README.md
```

---

## 📦 Tech Stack

| Layer     | Tech Used             |
|-----------|------------------------|
| Frontend  | Streamlit              |
| Backend   | Flask                  |
| Security  | Bandit (CLI)           |
| AI        | Hugging Face LLM API   |
| DB        | MongoDB Atlas          |
| DevOps    | Docker, Docker Compose |

---

## 🧠 Future Improvements

- [ ] Use Trivy or Snyk for multi-language scanning
- [ ] Add authentication (GitHub OAuth)
- [ ] Visualize more security metrics
- [ ] Switch to self-hosted MongoDB via Docker

---

## 📜 License

MIT License © 2025 [Aditya Joshi](https://github.com/Aditya19Joshi01)

---

## 🙌 Acknowledgements

- [Bandit](https://bandit.readthedocs.io/)
- [Streamlit](https://streamlit.io/)
- [Flask](https://flask.palletsprojects.com/)
- [Hugging Face](https://huggingface.co/)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
