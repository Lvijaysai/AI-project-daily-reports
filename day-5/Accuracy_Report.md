# AI Knowledge Assistant: Performance Evaluation Report

**Project Name:** AI Knowledge Assistant

**Evaluation Sample:** 100 Questions

**Environment:** Google Colab (Local Ollama Qwen 2.5 7B + MySQL)

**Date:** March 12, 2026

## 1. Executive Summary

This report analyzes the performance of the AI Knowledge Assistant across a representative sample of 100 analytical and conversational queries. While the infrastructure is stable and the database connection is secure, the evaluation revealed a significant bottleneck in **Intent Classification**, which directly impacted the accuracy and efficiency of data-driven responses.

## 2. System Architecture Overview

The system utilizes a multi-layered RAG (Retrieval-Augmented Generation) pipeline:

* **Backend:** FastAPI with `nest_asyncio` for Colab compatibility.
* **AI Engine:** Ollama running `qwen2.5:7b` (Local).
* **Database:** MySQL (Temporary sandbox) with a pooled connection.
* **Logic:** Context Aggregator, RAG Filler (Schema/Examples), and an Intent Classifier.

## 3. Key Metrics

| Metric | Result | Status |
| --- | --- | --- |
| **Total Questions Processed** | 100 | Completed |
| **Avg. Execution Time (Optimal)** | 2.0s - 4.5s | Good |
| **Avg. Execution Time (Inefficient)** | 8.0s - 16.9s | Warning |
| **Intent Accuracy** | ~15% | Critical |
| **LLM Confidence Average** | 0.92 | High (Potential Hallucination) |

## 4. Performance Analysis

### 4.1. Intent Classification Accuracy

The evaluation identified that approximately **85% of analytical questions** were misclassified as `general` instead of `sql`.

* **Root Cause:** The classifier required specific keywords (e.g., "how many") or a combination of "DB entities" and "actions." Standard analytical phrasing like *"Which month..."* or *"Average price..."* failed to trigger the SQL engine.
* **Impact:** The system bypassed the database, resulting in the AI answering from its training data rather than the uploaded CSV, leading to factual inaccuracies.

### 4.2. Latency and Efficiency

A clear correlation was observed between **Intent** and **Execution Time**:

* **SQL Intent:** Generally processed within **2–5 seconds**. The LLM generates short, efficient code blocks.
* **General Intent:** Often exceeded **8 seconds**, with some reaching **16.9 seconds**.
* **Reasoning:** In `general` mode, the LLM generates long-form conversational text and processes the entire RAG context without the instruction to be brief (unlike the SQL prompt instructions).

### 4.3. Confidence Score Reliability

The system reported high confidence (1.0) for almost all `general` responses.

* **Finding:** The AI is "confident" in its conversational ability, even when it lacks the database facts to answer correctly. This creates a risk of "Confident Hallucination" where the user trusts a wrong answer.

## 5. Technical Feedback & Findings

### Critical Issues

1. **Keyword Weakness:** The system failed to recognize that "Which," "What is the total," and "Monthly trend" are data requests.
2. **RAG Filler Underutilization:** In the logs, `schema_included` was frequently `False` because the intent was not recognized as `sql`, preventing the system from attaching the necessary metadata.
3. **Backpressure & Retries:** High execution times (>14s) suggest the LLM is hitting local compute limits or the retry logic in `query_service.py` is being triggered unnecessarily.

### Strengths

1. **Stable MySQL Integration:** Zero database connection failures were reported during the 100-question stress test.
2. **Clean SQL Generation:** When the intent *was* correctly identified, the SQL generated was valid and followed the `hotel_reservations` schema perfectly.
3. **Memory Persistence:** The `memory_pipeline_updated` event successfully logged user interactions for session history.

## 6. Remediation Plan

### Phase 1: Intent Classifier Patch (Immediate)

* Update `intent_classifier.py` to include a broader dictionary of analytical triggers (`highest`, `lowest`, `trend`, `monthly`, `bill`, `price`).
* Lower the threshold for SQL detection to ensure data-driven questions always hit the database.

### Phase 2: Latency Optimization

* Implement a `max_tokens` constraint for `general` responses to prevent the LLM from generating excessive text.
* Streamline the `rag_filler` to only pull schema info if analytical keywords are detected, regardless of the final intent.

### Phase 3: Confidence Calibration

* Adjust `confidence_checker.py` to penalize the score if a question appears analytical but the SQL engine was bypassed.

## 7. Conclusion

The AI Knowledge Assistant is a robust framework, but its "brain" is currently disconnected from its "memory" due to the intent classifier. By implementing the suggested keyword expansion, the project will transition from a conversational bot to a highly accurate analytical agent.

---
