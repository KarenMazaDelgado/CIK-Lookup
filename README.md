### Financial Document Contextualizer 
An automated pipeline deployed on AWS Lambda that leverages Claude 3 (Anthropic) via AWS Bedrock to perform RAG (Retrieval-Augmented Generation) on real-time SEC filings.

### Overview
This project automates the ingestion of financial data directly from the SEC EDGAR database. By translating company names into Central Index Keys (CIK), the system retrieves specific 10-K (Annual) or 10-Q (Quarterly) filings and utilizes Large Language Models (LLMs) to extract financial insights based on user queries.

### 🛠️ Tech Stack

Language: Python 


Cloud: AWS Lambda, AWS Bedrock 


Model: Anthropic Claude 3 Sonnet 

Data Source: SEC EDGAR API

# Financial Document Contextualizer 📊🤖

An automated pipeline deployed on **AWS Lambda** that leverages **Claude 3 (Anthropic)** via **AWS Bedrock** to perform RAG (Retrieval-Augmented Generation) on real-time SEC filings.

## ✨ Key Features
* **Real-Time Summarization:** Extracts and summarizes key financial insights from massive SEC filings in seconds.
* **Automated Ingestion Pipeline:** Programmatically fetches and preprocesses raw text/HTML filings for LLM consumption.
* **Prompt Enrichment:** Implements context-aware prompting by injecting relevant filing segments into the LLM context window.
* **Modular Architecture:** Separates CIK lookup logic from AI inference for better scalability and debugging.

## 📁 Project Structure
```text
├── CIK_Lookup.py      # Helper module for SEC CIK mapping and document retrieval
├── Claude_lambda.py   # Main AWS Lambda handler for Bedrock model invocation
├── SEC_LambdaOne.py   # Data ingestion script for S3 ticker updates
├── .gitignore         # Prevents tracking of local dependency packages
└── README.md          # Project documentation
```

### ⚙️ How It Works
Request: The Lambda receives a JSON payload with a company, year, and question.

Lookup: The CIKLookup class maps the company name to its unique SEC CIK and finds the filing URL.

Ingestion: The system fetches the raw text from the SEC server in real-time.

Enrichment: The text is truncated (preprocessing) and injected into a prompt for Claude 3.

Insight: The model returns a specialized financial analysis based only on the provided filing.
