# SHL Conversational Assessment Recommender

An AI-powered conversational recommendation system that helps recruiters identify the most suitable SHL assessments through natural language conversations.

The system understands hiring requirements, maintains conversation context in a stateless API, retrieves the most relevant SHL assessments using semantic search with FAISS, and generates structured recommendations using Gemini.

---

## Features

- Conversational assessment recommendation
- Multi-turn conversation support
- Stateless conversation handling
- Semantic search using Sentence Transformers
- FAISS vector similarity search
- Hybrid retrieval with rule-based reranking
- Conversation intent detection
- Intelligent query building from conversation history
- Assessment refinement
- Assessment comparison
- Safe handling of off-topic requests
- REST API built with FastAPI
- Interactive API documentation with Swagger

---

## Tech Stack

## Requirements

- Python 3.12+

### Backend

- Python 3.12
- FastAPI

### AI & NLP

- Google Gemini 2.5 Flash
- Sentence Transformers
- all-MiniLM-L6-v2

### Retrieval

- FAISS
- Hybrid Semantic + Keyword Reranking

### Data Collection

- BeautifulSoup4
- Requests

### Prompt Engineering

- Custom Prompt Templates

---

## Architecture

```
                    User
                      │
                      ▼
              FastAPI (/chat)
                      │
                      ▼
         Conversation Analyzer
                      │
            Conversation State
                      │
                      ▼
              Query Builder
                      │
                      ▼
             FAISS Retriever
                      │
            Top SHL Assessments
                      │
                      ▼
              Gemini 2.5 Flash
                      │
                      ▼
              Structured JSON
```

---

## Project Structure

```text
app/
├── api/
├── catalog/
├── core/
├── llm/
├── models/
├── prompts/
├── retrieval/
├── services/
├── utils/
└── main.py

data/
├── raw/
├── processed/
└── index/

sample_conversations/

scripts/

tests/
```

---

## How It Works

1. User sends the complete conversation history.
2. Conversation Analyzer determines the user's intent.
3. Conversation State extracts hiring information such as:
   - Role
   - Domain
   - Seniority
   - Hiring intent
4. Query Builder constructs an optimized retrieval query.
5. FAISS retrieves the most relevant SHL assessments.
6. Hybrid reranking improves retrieval quality.
7. Gemini generates recommendations strictly from the retrieved assessments.
8. FastAPI returns structured JSON.

---

## Supported Capabilities

- Recommend SHL assessments
- Refine previous recommendations
- Compare SHL assessments
- Clarify missing hiring information
- Reject off-topic requests

---

## API

### Health Check

GET

```
/health
```

---

### Chat

POST

```
/chat
```

Example Request

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hiring Java developers with leadership skills"
    }
  ]
}
```

Example Response

```json
{
  "reply": "Based on your requirements, I recommend the following assessments.",
  "recommendations": [
    {
      "name": "Core Java (Advanced Level) (New)",
      "url": "...",
      "test_type": "K"
    }
  ],
  "end_of_conversation": false
}
```

---

## Dataset Preparation

The SHL catalog was prepared through a custom pipeline:

- Discover assessment URLs
- Download assessment pages
- Parse assessment information
- Clean extracted text
- Enrich metadata
- Generate embedding text
- Build FAISS vector index

---

## Testing

The project includes tests for:

- Retriever
- Conversation Analyzer
- Query Builder
- Prompt Generation
- Chat Service
- Recommendation
- Refinement
- Comparison
- Replay of provided sample conversations

---

## Design Decisions

- Stateless API architecture
- Semantic retrieval using embeddings
- Hybrid reranking to improve retrieval precision
- Separation of conversation analysis from retrieval
- Dedicated query builder for multi-turn conversations
- JSON-only responses from the LLM
- Graceful handling of LLM failures

---

## Future Improvements

- Larger assessment catalog
- Cross-encoder reranking
- Conversation memory persistence
- Streaming responses
- Authentication
- Deployment with Docker
- Automated evaluation metrics

---

## Author

Pruthviraj B. Khot