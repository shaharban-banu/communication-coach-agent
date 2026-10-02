# Communication Coach Agent

An Agentic AI-powered communication training platform that helps users analyze, improve, and generate professional communication through a modular coaching workflow.

**Live Application:** https://communication-coach-frontend.onrender.com  
**Backend API:** https://communication-coach-agent-mtr6.onrender.com  
**API Documentation:** https://communication-coach-agent-mtr6.onrender.com/docs

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Live Demo](#live-demo)
- [Local Installation](#local-installation)
- [Environment Variables](#environment-variables)
- [Run the Application](#run-the-application)
- [Docker Deployment](#docker-deployment)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Deployment](#deployment)
- [Limitations](#limitations)
- [Future Enhancements](#future-enhancements)
- [Security Notes](#security-notes)
- [Author](#author)

---

## Overview

Communication Coach Agent is an AI-based application designed to support users in communicating more clearly, confidently, and professionally.

It uses an agent-oriented workflow to identify a communication task, plan an appropriate response, select relevant capabilities, execute the task, and provide feedback or an improved response.

The application is intended for use cases such as professional email writing, grammar correction, tone improvement, interview preparation, workplace communication, and customer interactions.

## Key Features

- **Email Writing:** Generate structured, professional emails for workplace and everyday situations.
- **Grammar Correction:** Identify and correct grammar and wording issues while preserving intended meaning.
- **Tone Improvement:** Rewrite messages to sound more polite, professional, clear, or appropriate to the context.
- **Interview Coaching:** Support interview practice and improve the clarity of interview responses.
- **Conflict Resolution:** Help formulate respectful and constructive messages for difficult conversations.
- **Customer Communication:** Draft empathetic and professional responses to customer concerns.
- **Communication Analysis:** Analyze a message and provide feedback on communication quality.
- **Response Improvement:** Produce an improved version of a user's communication.
- **Scoring and Feedback:** Provide communication scores and improvement suggestions when supported by the selected workflow.
- **Conversation Sessions:** Organize conversations in the frontend and use session identifiers with the API.

## How It Works

The intended agent workflow is:

```text
User Query
    |
    v
Intent Detection
    |
    v
Communication Planner
    |
    v
Tool Selection
    |
    v
Task Execution
    |
    v
Scoring and Feedback
    |
    v
Improved Communication Response
```

The agent can route requests to specialized capabilities such as grammar correction, tone analysis, email generation, interview coaching, and conversation improvement.

## Architecture

```text
                 User
                  |
                  v
       Streamlit Frontend (Render)
                  |
             HTTPS Requests
                  |
                  v
       FastAPI Backend (Render)
          Dockerized Service
                  |
                  v
        Communication Agent
          /      |       \
         v       v        v
   Intent    Planner   Tool Selection
   Detection             |
                         v
                Specialized Tools
                         |
                         v
                Groq LLM Inference
                         |
                         v
               Feedback / Response
                         |
                         v
                  Streamlit UI
```

### Deployment Architecture

- **Frontend:** Streamlit application hosted as a Render Python web service.
- **Backend:** FastAPI application packaged in Docker and hosted as a Render web service.
- **LLM Provider:** Groq API, configured through backend environment variables.
- **Source Control:** GitHub.

## Technology Stack

| Area | Technologies |
|---|---|
| Language | Python 3.11 |
| Backend API | FastAPI, Uvicorn |
| Frontend | Streamlit |
| HTTP Client | Requests |
| Configuration | Pydantic Settings, python-dotenv |
| LLM Integration | Groq |
| Containerization | Docker, Docker Compose |
| Testing | pytest |
| Hosting | Render |
| Version Control | Git, GitHub |

## Project Structure

```text
communication-coach-agent/
│
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── analyze.py
│   │   │   ├── coach.py
│   │   │   ├── improve.py
│   │   │   ├── chat_history.py
│   │   │   ├── health.py
│   │   │   └── metrics.py
│   │   ├── middleware.py
│   │   └── exception_handlers.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   │
│   ├── tools/
│   │   └── ...
│   │
│   └── main.py
│
├── frontend/
│   ├── app.py
│   ├── api_client.py
│   ├── components.py
│   ├── styles.py
│   ├── test_api_client.py
│   └── __init__.py
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── frontend_requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

*The tree is representative. Update it if the repository's actual package or test layout differs.*

## Live Demo

| Resource | Link |
|---|---|
| Live Streamlit Application | https://communication-coach-frontend.onrender.com |
| Backend Health Check | https://communication-coach-agent-mtr6.onrender.com/health |
| Swagger API Documentation | https://communication-coach-agent-mtr6.onrender.com/docs |
| GitHub Repository | https://github.com/shaharban-banu/communication-coach-agent |

### Demo Prompts

Try these prompts in the live application:

**Professional Email**
> Write a professional email to my manager requesting one day of sick leave. Keep it polite, concise, and professional.

**Grammar Correction**
> I am interested to apply for this position because I have good knowledge in Python and I am looking forward to join your company.

**Tone Improvement**
> I already told you to send the report. Why haven't you completed it yet? Send it immediately.

**Interview Practice**
> Act as a technical interviewer for a Python developer position. Ask me one interview question at a time. After I answer, evaluate my response and suggest how I can communicate it more clearly.

**Customer Communication**
> A customer is angry because their order was delivered late. Draft a professional response that acknowledges their frustration, apologizes, and explains that we are working to resolve the issue.

## Local Installation

### Prerequisites

- Python 3.11
- Git
- Docker Desktop (only if running the backend with Docker)
- A Groq API key

### 1. Clone the repository

```bash
git clone https://github.com/shaharban-banu/communication-coach-agent.git
cd communication-coach-agent
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows Git Bash**

```bash
python -m venv venv
source venv/Scripts/activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

Install backend dependencies:

```bash
pip install -r requirements.txt
```

Install frontend dependencies:

```bash
pip install -r frontend_requirements.txt
```

## Environment Variables

Create a local `.env` file in the repository root. Use `.env.example` as a reference.

Example:

```env
APP_NAME=Communication Coach Agent
APP_ENV=development
DEBUG=false
API_V1_PREFIX=/api/v1

LLM_PROVIDER=groq
LLM_MODEL=openai/gpt-oss-20b
LLM_API_KEY=your_groq_api_key

LOG_LEVEL=INFO
```

Do not commit the real `.env` file or API credentials.

For the frontend, configure the backend base URL using `API_BASE_URL`.

Local default:

```env
API_BASE_URL=http://localhost:8000
```

For the deployed frontend, the value is:

```env
API_BASE_URL=https://communication-coach-agent-mtr6.onrender.com
```

The frontend's API client uses the local URL as a fallback when `API_BASE_URL` is not set.

## Run the Application

### Option A: Run backend and frontend separately

**Terminal 1: Start FastAPI**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend:

- Health: http://localhost:8000/health
- Swagger: http://localhost:8000/docs

**Terminal 2: Start Streamlit**

Set the frontend API URL to the local backend.

Windows PowerShell:

```powershell
$env:API_BASE_URL="http://localhost:8000"
streamlit run frontend/app.py
```

Windows Git Bash:

```bash
export API_BASE_URL="http://localhost:8000"
streamlit run frontend/app.py
```

Open the local Streamlit URL printed in the terminal, commonly:

```text
http://localhost:8501
```

### Option B: Run the backend using Docker Compose

Ensure Docker Desktop is running, then execute:

```bash
docker compose up --build
```

The backend will be available at:

```text
http://localhost:8000
```

To stop the containers:

```bash
docker compose down
```

For local Docker-based backend execution, run the Streamlit frontend separately and set `API_BASE_URL=http://localhost:8000`.

## API Endpoints

The API is versioned under `/api/v1`.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check backend health |
| POST | `/api/v1/analyze` | Analyze communication |
| POST | `/api/v1/coach` | Run the communication coaching workflow |
| POST | `/api/v1/improve` | Generate an improved communication response |
| GET | `/api/v1/chat-history/{session_id}` | Retrieve conversation history for a session |
| GET | `/api/v1/metrics` | Access application metrics, if enabled in the deployment |

Interactive API documentation:

https://communication-coach-agent-mtr6.onrender.com/docs

Refer to the Swagger schemas for the exact request and response fields.

## Testing

Run the test suite from the repository root:

```bash
pytest
```

Run a specific test module, for example:

```bash
pytest frontend/test_api_client.py -v
```

For the final review, verify the key workflows through the deployed UI and inspect the Render service logs if a request fails.

## Deployment

The project uses separate Render services.

### Backend

- Runtime: Docker
- Repository branch: `main`
- Dockerfile: `./Dockerfile`
- Health check: `/health`
- Required LLM configuration is stored in the backend service's Render environment.

### Frontend

- Runtime: Python 3
- Repository branch: `main`
- Build command:

```bash
pip install -r frontend_requirements.txt
```

- Start command:

```bash
streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0
```

- Environment variable:

```env
API_BASE_URL=https://communication-coach-agent-mtr6.onrender.com
```

After pushing changes to the connected branch, Render can automatically redeploy the services when auto-deploy is enabled.

## Limitations

- Render free services may spin down after periods of inactivity, so the first request can take longer while a service starts.
- Conversation state currently uses in-memory/session-based handling. It should not be treated as durable storage across service restarts or deployments.
- LLM output quality and response time depend on the configured provider, model, API availability, and request limits.
- The application provides AI-generated communication suggestions. Users should review generated content before using it in important professional situations.

## Future Enhancements

- Persistent conversation storage using a database.
- More comprehensive automated evaluation of agent outputs.
- Expanded interview practice with multi-turn session persistence.
- Improved observability, request tracing, and error reporting.
- Additional communication scenarios and configurable coaching styles.
- CI/CD automation for tests and deployment checks.

## Security Notes

- Keep API keys in environment variables or a secret manager.
- Never commit `.env`, credentials, or provider tokens.
- Rotate any credential that has been accidentally exposed.
- Avoid placing sensitive personal or business information into prompts unless appropriate for the intended environment.

## Author

**Shaharban Banu**

- GitHub: https://github.com/shaharban-banu
- LinkedIn: https://www.linkedin.com/in/shaharban-v-695a84145

---

If you find this project useful, feel free to explore the repository and try the live application.
