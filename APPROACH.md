# SHL Conversational Assessment Recommender
## Technical Approach

### Author
Pruthviraj B. Khot

---

# 1. Problem Statement

The objective of this project is to build an AI-powered conversational recommendation system that recommends appropriate SHL assessments based on a recruiter's hiring requirements.

Unlike a traditional keyword search, recruiters should be able to interact naturally with the system through multiple conversation turns. The system should understand conversation history, retrieve relevant SHL assessments, and generate recommendations while remaining completely stateless.

---

# 2. Solution Overview

The solution combines semantic retrieval with a Large Language Model (LLM).

The overall workflow is:

```

User Conversation
↓
Conversation Analyzer
↓
Conversation State
↓
Query Builder
↓
Semantic Retrieval (FAISS)
↓
Hybrid Reranking
↓
Gemini 2.5 Flash
↓
Structured JSON Response

```

Each component has a single responsibility, making the system modular and easy to maintain.

---

# 3. Data Collection

The SHL product catalog was collected using custom Python scripts.

The data collection pipeline consists of:

- Discovering assessment URLs
- Downloading assessment pages
- Parsing HTML
- Extracting structured information
- Cleaning extracted content
- Enriching metadata
- Building embeddings

The extracted information includes:

- Assessment name
- URL
- Description
- Category
- Test type
- Duration
- Languages
- Relevant textual content

---

# 4. Data Cleaning

Raw HTML pages contained a large amount of navigation and website boilerplate such as:

- Outdated browser messages
- Footer links
- Cookie notices
- Navigation menus

These sections were removed before generating embeddings.

Cleaning the text significantly improved semantic retrieval quality by ensuring that embeddings represent only meaningful assessment information.

---

# 5. Embedding Generation

Each assessment is converted into an embedding document containing:

- Assessment name
- Categories
- Test type
- Duration
- Languages
- Description
- Important content paragraphs

Sentence embeddings are generated using:

**Model**

```

sentence-transformers/all-MiniLM-L6-v2

```

This model provides a good balance between embedding quality, speed, and memory usage.

---

# 6. Vector Search

Embeddings are indexed using FAISS.

The implementation uses cosine similarity by:

- L2 normalizing embeddings
- Using an Inner Product index

This enables fast semantic retrieval across the assessment catalog.

---

# 7. Hybrid Retrieval

Pure semantic similarity sometimes returns assessments that are semantically similar but not the best practical match.

To improve ranking, a lightweight reranking stage was implemented.

The final score combines:

- Semantic similarity
- Exact assessment name matches
- Keyword overlap
- Category matching
- Test type matching

Additional ranking heuristics prioritize actual assessments over report products when appropriate.

This hybrid approach improves recommendation quality without introducing expensive cross-encoder models.

---

# 8. Conversation Understanding

A Conversation Analyzer processes the entire conversation history.

It extracts structured hiring information such as:

- Job role
- Seniority
- Domain
- Hiring intent
- User intent

The analyzer identifies whether the user wants to:

- Receive recommendations
- Refine recommendations
- Compare assessments
- Provide additional information
- Ask an unrelated question

This allows the system to behave differently depending on the conversation.

---

# 9. Conversation State

Since the API is stateless, every request includes the full conversation history.

The Conversation State stores extracted information including:

- Role
- Domain
- Seniority
- Job description availability
- Recommendation intent
- Refinement intent
- Comparison intent

This enables consistent behaviour without maintaining server-side sessions.

---

# 10. Query Builder

Instead of concatenating every user message, a Query Builder constructs an optimized retrieval query.

The query combines:

- Original hiring request
- Role
- Domain
- Seniority
- Job description
- Important hiring keywords

This produces more focused retrieval queries and improves semantic search quality during multi-turn conversations.

---

# 11. Prompt Engineering

Prompt templates were designed for three tasks:

- Recommendation
- Refinement
- Comparison

Each prompt instructs Gemini to:

- Use only retrieved SHL assessments
- Never invent assessment names
- Never invent URLs
- Return valid JSON
- Produce structured recommendations

Restricting the model to retrieved context minimizes hallucinations.

---

# 12. API Design

The application is implemented using FastAPI.

Endpoints:

### GET /health

Returns application health status.

### POST /chat

Accepts the complete conversation history.

Returns:

- Reply
- Recommended assessments
- End-of-conversation flag

The API is intentionally stateless to simplify deployment and scalability.

---

# 13. Error Handling

The application includes graceful handling for:

- Invalid JSON responses
- Gemini API failures
- Temporary service unavailability
- Quota exceeded errors

Fallback responses ensure the API always returns valid JSON.

---

# 14. Testing

The project includes dedicated tests for:

- Retriever
- Conversation Analyzer
- Query Builder
- Prompt generation
- Chat Service
- Recommendation
- Refinement
- Comparison
- Replay of sample conversations

This helped validate individual components before full system integration.

---

# 15. Design Decisions

Several important engineering decisions were made during development.

### Semantic Search

Semantic retrieval performs better than keyword search because recruiters naturally describe hiring needs in different ways.

### FAISS

FAISS provides efficient vector similarity search and scales well for larger assessment catalogs.

### Hybrid Ranking

Combining semantic similarity with lightweight rule-based scoring improves recommendation relevance while keeping inference fast.

### Stateless Architecture

Passing the entire conversation history in every request removes the need for server-side session management and aligns with the assignment requirements.

### Structured Conversation State

Separating conversation understanding from retrieval keeps the system modular and easier to extend.

---

# 16. Limitations

Current limitations include:

- Evaluation performed on the publicly available SHL catalog.
- Larger proprietary catalogs may improve recommendation diversity.
- Hybrid reranking uses handcrafted heuristics rather than a learned ranking model.
- Recommendation quality depends on the capabilities of the underlying LLM.

---

# 17. Future Improvements

Potential future enhancements include:

- Cross-encoder reranking
- Metadata filtering
- Larger embedding models
- Persistent conversation memory
- Docker deployment
- Continuous evaluation pipeline
- User authentication
- Analytics dashboard

---

# 18. Conclusion

This project demonstrates a complete conversational retrieval-augmented recommendation system for SHL assessments.

The solution combines semantic retrieval, conversation understanding, hybrid reranking, and LLM-based reasoning to provide structured assessment recommendations through a stateless FastAPI service.

The modular architecture allows the system to be extended to larger assessment catalogs and more advanced ranking models with minimal architectural changes.