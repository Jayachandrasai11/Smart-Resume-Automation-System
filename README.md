# Smart-Resume-Automation-System
# 📘 Resume RAG Automation System

## 🚀 Overview

A production-ready automation platform for **resume parsing, structured
data processing, and recruiter-friendly candidate search**.

This system automates resume ingestion, parsing, semantic search, and
reporting --- significantly reducing manual recruiter effort and
enabling data-driven hiring decisions.

------------------------------------------------------------------------

## 🏗️ System Architecture

The platform follows a structured ETL + Semantic Search architecture:

Gmail → ETL Pipeline → LLM Parsing → PostgreSQL + pgvector → Django
Dashboard → Power BI Analytics

------------------------------------------------------------------------

## 🔄 ETL Workflow

### 1️⃣ Extract

-   Automatically fetch resumes from Gmail (PDF / DOCX).
-   No manual uploads required.
-   Triggered via one-click dashboard button.

### 2️⃣ Transform

-   Parse resume text into structured JSON using:
    -   Gemini API
    -   Perplexity API
-   Regex fallback for robust extraction.
-   Cleaned and validated structured output.

### 3️⃣ Load

-   Store structured candidate data in PostgreSQL.
-   Use **pgvector** for semantic similarity search.
-   Maintain job-wise candidate pools.

------------------------------------------------------------------------

## 🔹 Core Features

### ✅ Python-based ETL Pipeline

-   Automated resume ingestion
-   Structured data extraction
-   Error handling & logging
-   Scalable processing design

### ✅ Semantic Search Engine

-   SentenceTransformers embeddings
-   pgvector similarity search
-   Match score calculation
-   Skill-based ranking

### ✅ Job Lifecycle Management

-   Separate candidate pool per job description
-   Archive/delete resumes after hiring rounds close
-   Prevents database clutter

### ✅ Django Web Application

-   One-click **"Start Resume Processing"** button
-   Job description input interface
-   Candidate search results table
-   Filters:
    -   Skills
    -   Education
    -   Match threshold %
-   Export to CSV / Excel

### ✅ Reporting & Analytics

Integrated **Power BI Dashboard** including: - Candidate match %
distribution - Skill frequency across resumes - Job lifecycle
analytics - Interactive recruiter dashboards

### ✅ Production Deployment

-   Docker containerized
-   Portable and scalable
-   Deployable on:
    -   Render
    -   Railway
-   CI/CD ready via GitHub

------------------------------------------------------------------------

## 🧠 Technology Stack

  Layer              Technology
  ------------------ ----------------------
  Backend            Python
  Web Framework      Django
  Database           PostgreSQL
  Vector DB          pgvector
  Embeddings         SentenceTransformers
  LLM APIs           Gemini, Perplexity
  Containerization   Docker
  Analytics          Power BI
  Deployment         Render / Railway

------------------------------------------------------------------------

## 📊 SDLC Coverage

-   Requirement Analysis
-   System Design & Architecture
-   Development (Backend + Frontend)
-   Testing & Validation
-   Deployment
-   Monitoring & Reporting

------------------------------------------------------------------------

## 📂 Project Structure (High-Level)

    resume-rag-system/
    │
    ├── etl_pipeline/
    ├── embeddings/
    ├── django_app/
    ├── docker/
    ├── analytics/
    ├── docs/
    └── README.md

------------------------------------------------------------------------

## ⚙️ Setup Guide (High-Level)

1.  Clone the repository
2.  Configure environment variables (DB, API Keys)
3.  Run Docker containers
4.  Migrate PostgreSQL database
5.  Start Django server
6.  Access dashboard
7.  Click "Start Resume Processing"

------------------------------------------------------------------------

## 🎯 Key Benefits

-   Eliminates manual resume screening
-   Improves hiring efficiency
-   Enables semantic candidate matching
-   Provides recruiter-friendly dashboards
-   Fully production-ready architecture

------------------------------------------------------------------------

## 📈 Future Enhancements

-   Automated interview scheduling integration
-   Multi-language resume support
-   AI-based candidate ranking explanation
-   Real-time recruiter notification system

------------------------------------------------------------------------

## 📌 Author

Designed and developed as a production-grade Resume RAG Automation
Platform for intelligent hiring workflows.
