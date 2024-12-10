# Insurance Agent AI Assistant

## 🚀 Project Overview

An AI-powered insurance agent assistant designed to provide seamless customer support and information retrieval for insurance-related queries.

## 📊 Demo Resources

- [Slide Deck](https://www.canva.com/design/DAGY4C8tCBo/G-c9F_-4NaFxquzQGXPXnw/edit?utm_content=DAGY4C8tCBo&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)
- [Demo Video](https://drive.google.com/file/d/1DA7e7CbZsNSs-u0nZtbg2ZiIQmADWYoi/view?usp=sharing)

## 💬 Sample Interaction Scenarios

The assistant can handle queries like:
- "Can you give me the claim status? My claim ID is [ClaimID]."
- "Can you tell me about my insurance policy?"
- "Can you provide detailed information regarding my insurance policy?"

## 🔧 Technology Stack

- frontend: Nextjs
- Backend: FastAPI, NodeJs
- Database: PostgreSQL and PGVector
- Language Model: Open AI models with langchain

## 🛠 Installation

### 1. Database Setup

Run the PGVector PostgreSQL container:

```bash
docker run --name pgvector-container \
  -e POSTGRES_USER=langchain \
  -e POSTGRES_PASSWORD=langchain \
  -e POSTGRES_DB=langchain \
  -p 6024:5432 \
  -d pgvector/pgvector:pg16
```

## 🚀 Running the Application

```bash
# Start the FastAPI application
uvicorn main:app --reload
```

## 🔍 Response Handling

The application processes responses using:
```python
response.data.payload.output
```


docker run --name pgvector-container -e POSTGRES_USER=langchain -e POSTGRES_PASSWORD=langchain -e POSTGRES_DB=langchain -p 6024:5432 -d pgvector/pgvector:pg16

