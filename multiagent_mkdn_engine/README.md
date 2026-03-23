# Autonomous Decision Intelligence (ADI): Multi-Agent Markdown Engine

[![AI Agentic Workflow](https://img.shields.io/badge/GenAI-Agentic%20Workflow-blue.svg)](#)
[![Stack](https://img.shields.io/badge/Stack-Python%20%7C%20Gemini%20%7C%20GoogleADK%20%7C%20VertexAI-blue.svg)](#)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-green.svg)](#)

A proof-of-concept framework demonstrating an **Autonomous Decision Intelligence (ADI)** system, designed to bypass traditional enterprise diagnostic dashboards in favor of closed-loop fiscal execution.

## Executive Summary: Bridging the "Latency-to-Action" Gap

Traditional enterprise retail analytics suffers from excessive time-to-insight. Critical capital management decisions are often stalled by the requirement to manually reconcile quantitative inventory data with qualitative consumer sentiment, leading to missed margin opportunities and stagnant stock.

I built this framework to showcase the orchestration of a multi-agent GenAI system capable of resolving this gap. By using LLMs to synthesize unstructured data—such as NLP-driven recursive analysis of customer reviews—with structured financial constraints, this system moves AI from a passive advisor into an active capital management tool. All actions are governed by strict, programmable fiscal guardrails and automated budget depletion tracking.

---

### Conceptual Architecture and Tech Stack

The entire "Insight-to-Action" loop is orchestrated through a specialized multi-agent workflow. The diagram below details how specialized agents decompose the problem and coordinate the financial solution.

<img width="1408" height="768" alt="Gemini_Generated_Image_pk9hatpk9hatpk9h (1)" src="https://github.com/user-attachments/assets/17547fcb-766f-423a-89c5-f3f091ba10a4" />

***Note: Refer to `agent.py` for specific agent configurations and `tools.py` for executable logical constraints.***

---

## Strategic Pillars and Core Capabilities

This project is built around three fundamental capabilities that differentiate it from passive reporting systems:

### 🚀 1. Reduced Time-to-Insight (Diagnostic Velocity)
Bypasses manual reporting latency by enabling an autonomous **Analyst Agent**. This agent performs real-time, SKU-level diagnostics (based on `inventory.csv`) to identify liquidity bottlenecks instantly, rather than waiting for fiscal week close reports.

### 🧠 2. Unstructured Data Synthesis (Qualitative Decisioning)
Moves beyond quantitative sales velocity. A specialized **Strategist Agent** performs NLP-driven sentiment analysis on unstructured customer reviews. It differentiates between:
* **Pricing Misalignment:** Standard slow sales trigger a standard (e.g., 20%) markdown.
* **Product Quality/Defect:** Poor sentiment triggers an aggressive (e.g., 40%) clearance markdown to protect brand integrity.

### ✅ 3. Closed-Loop Execution with Responsible Guardrails (Active Capital Management)
Transition from insight to verified action. The final stage is not a report, but a verified **tool execution**. It moves Beyond "Chat" into active fiscal change, governed by programmable rules defined in `tools.py`:
* **Cost-Floor Protection:** Decisions are rejected if the proposed markdown dips below the product cost.
* **Budget Depletion Tracking:** The system autonomously checks the `remaining_markdown_budget` before execution, ensuring AI decisions remain within strict corporate financial boundaries.

---

## Technical Overview and Repository Structure

The architecture is implemented using the **Google Agent Development Kit (ADK)** and **Gemini 1.5 Flash**.

| File | Description | Core Responsibility | Key Technologies |
| :--- | :--- | :--- | :--- |
| `agent.py` | Agent & Role Setup | Defines the properties, instructions, and recursive reasoning paths of the specialized Analyst and Strategist agents. | Vertex AI, LLM Prompts |
| `tools.py` | Tool Layer & Logic Gates | Contains the custom Python tools executed by the agents. Crucially defines the logical guardrails (`cost` checks, `budget` depletion). | Python, Financial Logic |
| `inventory.csv`| Mock Data Store | Contains SKU-level data, including sales velocity, cost, current price, and (qualitative) recent reviews. | Flat File Database |
| `main.py` | Flow Orchestration | Defines the sequential state machine, state transfer between agents, and the loop starting point. | Google ADK (SequentialAgent) |

### Proof-of-Concept Workflow Details:
* **State Management:** The `SequentialAgent` structure manages context transfer between nodes. When the Analyst completes its diagnostic, its findings are statefully transferred to the Strategist as conversational history, ensuring context preservation.
* **Recursive Reason Logging:** The system maintains auditable reasoning logs, detailing *why* a specific markdown percentage was selected based on keywords found during review parsing.

---

## Quick Start (Running the Simulation)

### Prerequisites
1.  **Google Cloud Project:** Access to Gemini 1.5 Flash (via Vertex AI) and standard permissions.
2.  **Authentication:** Set up your environment credentials (e.g., `gcloud auth application-default login` and set your `GOOGLE_CLOUD_PROJECT` env variable).
3.  **Python 3.9+**

### Installation
Clone the repository and install the dependencies:
```bash
git clone [Your_GitHub_Repo_URL]
cd adi-multiagent-markdown
pip install pandas google-cloud-aiplatform
# Install Google ADK (ensure this path is valid for your specific installation method)
pip install google-adk
