# AGENTIS

**AGENTIS** is a modular AI pipeline system that helps match patients to relevant clinical trials. It takes a natural-language patient description, searches ClinicalTrials.gov, evaluates eligibility against each trial's real inclusion/exclusion criteria, and returns a ranked, explained shortlist - turning a process that normally takes clinical trial coordinators days into a single request.

**Live app on GCP:** https://agentis-469658382656.us-west1.run.app

## The Problem

Hospitals often can't offer in-house treatment for certain conditions, so coordinators search ClinicalTrials.gov for a suitable trial instead. The site's search UI is difficult to use well, and manually reading through dense eligibility criteria for dozens of candidate trials - while managing a full patient caseload - is slow. AGENTIS automates that search-and-match process.

## How It Works

AGENTIS is a four-agent pipeline. Each agent has one job, and only the agents that actually need language understanding call an LLM - the rest is plain data processing.

```
Patient description (natural language)
        │
        ▼
1. Profile Parser        — extracts structured patient data (condition, treatments, history, etc.)
        │
        ▼
2. Query Builder          — queries the ClinicalTrials.gov API and parses candidate trials
        │
        ▼
3. Eligibility Checker    — compares the patient against each trial's criteria, in parallel
        │
        ▼
4. Ranker & Explainer     — ranks eligible/uncertain trials and summarizes each one
        │
        ▼
Ranked, explained shortlist of trials
```

### 1. Profile Parser
Takes a free-text patient description and extracts a structured profile (condition, stage, current/prior treatments, allergies, performance status, etc.) using a frontier LLM with structured output. Distinguishes explicitly-stated-absent information ("no known allergies") from information that was simply never mentioned, so downstream agents don't confuse silence for a negative.

### 2. Query Builder
Builds a query against the [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api) from the parsed condition/location, fetches candidate trials, and extracts the relevant fields (title, eligibility criteria, locations, status, etc.) from the deeply nested API response into a clean, structured object per trial. No LLM call - this stage is pure data retrieval and parsing.

### 3. Eligibility Checker
For every candidate trial, compares the patient profile against that trial's actual inclusion/exclusion criteria and returns an eligibility verdict (`ELIGIBLE`, `NOT ELIGIBLE`, or `UNCERTAIN`) with reasoning. Runs concurrently across all candidate trials using `asyncio`, since each comparison is an independent LLM call.

### 4. Ranker & Explainer
Takes the eligible/uncertain trials, ranks them (favoring active recruitment status and higher eligibility confidence), and generates a short human-readable summary and ranking rationale for each - without letting the model regenerate factual data (like exact trial locations) that's already been reliably extracted upstream.

## Tech Stack

- **Backend:** FastAPI
- **Models:** OpenAI (`o4-mini`) for the two reasoning-heavy stages (Profile Parser, Eligibility Checker); an open-source model (GPT-OSS-120B)via Groq for the lighter stage (Query Builder has no LLM call; Ranker uses the open source model since its job is summarizing/ordering already-correct data)
- **Data source:** [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api)
- **Frontend:** Jinja2 templates (Note: Frontend code for this project was generated using Codex)
- **Package management:** uv
- **Deployment:** Docker, deployed on Google Cloud Run

## Project Structure

```
agentis/
├── agents/           # The four pipeline agents (profile parser, query builder, eligibility checker, ranker)
├── models.py         # Shared Pydantic schemas - the contract between each pipeline stage
├── clients.py        # LLM client setup (OpenAI + Groq)
├── pipeline.py        # Orchestrator - calls the four agents in sequence
├── api.py             # FastAPI route definitions
├── web.py             # Jinja2 template rendering / web-facing routes, mounts api.py
├── main.py            # For local console testing
├── templates/          # Jinja2 HTML templates
├── static/             # Static assets (CSS/JS)
├── Dockerfile
└── pyproject.toml / uv.lock
```

## Running Locally

1. Clone the repo and install dependencies with [uv](https://docs.astral.sh/uv/):
   ```bash
   uv sync
   ```
2. Set your API keys as environment variables (or in a `.env` file):
   ```
   OPENAI_API_KEY=your_key_here
   GROQ_API_KEY=your_key_here
   ```
3. Run the app locally:
   ```bash
   uv run uvicorn api:app --reload
   ```
   or
   ```bash
   uv run uvicorn web:app --reload
   ```

## Running with Docker

```bash
docker build -t agentis .
docker run -p 8080:8080 --env-file .env agentis
```

## Web Deployment (Google Cloud Run)

AGENTIS is deployed as a containerized service on Google Cloud Run.

Live deployment: https://agentis-469658382656.us-west1.run.app


## API

**POST** `/agentis`

```json
{
  "message": "61 year old male with stage 2 pancreatic cancer, currently taking gemcitabine, no prior radiation, no prior immunotherapy, otherwise healthy with good organ function."
}
```

Returns a ranked list of matching trials, each with a title, summary, location/contact info, and reasoning for both its eligibility and its rank.

## Notes & Limitations

- AGENTIS is a matching/research tool, not a substitute for clinical judgment - eligibility determinations should always be confirmed by a qualified clinician against the trial's official protocol.
- Query Builder currently issues a single query per patient profile; trial recall could be improved by querying multiple condition synonyms and deduplicating results.
- Built as a from-scratch rebuild of an earlier version of AGENTIS that was originally prototyped in IBM watsonx Agent Lab.

## Developed by

Krish Makwana