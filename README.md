# Codebase Orientation

### Agentic Developer Onboarding & Feature Scaffolder — built with IBM Bob 2.0

![Next.js](https://img.shields.io/badge/Next.js-black?logo=next.js) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white) ![IBM Granite](https://img.shields.io/badge/IBM%20Granite-052FAD) ![watsonx](https://img.shields.io/badge/watsonx-052FAD) ![React Flow](https://img.shields.io/badge/React%20Flow-ff0072) ![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

`Category: Developer Onboarding` · `Hackathon: IBM Bob 2.0`

## Overview

Developers spend 50-60% of their time reading and reverse-engineering existing code rather than writing features, and it takes an average of 2-4 weeks to reach a first meaningful PR on a new codebase. Codebase Orientation points at any repo and hands a new developer two things a senior teammate would otherwise spend a day producing by hand: an **Architecture & Impact Map** of how the modules fit together, and a set of **Starter Tasks** grounded in real files in that repo.

## Problem Statement

- Bugs and outages frequently trace back to developers missing subtle side effects across tightly coupled modules they didn't know existed.
- Standard coding copilots suggest snippets line-by-line; they don't hold repository-wide context, so new developers end up manually copy-pasting files into a chat window and hitting token limits.
- IBM Bob 2.0's full-repository context, Agent Mode, subagents, and parallel execution are built for exactly this class of problem.

## Solution

```
Repo URL / local path
        │
        ▼
  Ingestion & module
   detection
        │
   ┌────┴────┐
   ▼         ▼
Architecture   Starter Task
& Impact Map   Scaffolder
(per-module    (TODO/FIXME
subagents,     signals →
run in         Granite-drafted
parallel)      onboarding tasks)
   │         │
   └────┬────┘
        ▼
  Interactive frontend
  (map view + task list)
```

## Key Features

1. **Architecture & Impact Map** — detects candidate modules/services from repo manifests, summarizes each one concurrently via IBM Granite (one call per module, run in parallel — mirroring Bob 2.0's subagent model), and renders an interactive dependency graph. Click a node to see its AI-generated summary and key files.
2. **Starter Task Scaffolder** — scans the repo for TODO/FIXME/HACK signals and turns them into concrete onboarding tasks, each pointing at a real file and explaining why it teaches the system.
3. **Demo-safe by design** — AI calls fall back to deterministic mock responses when no Watsonx credentials are configured, so the whole pipeline runs end-to-end without a live IBM Cloud account.

## Built with Bob 2.0

- **Agent Mode / subagents** — the Architecture Map pipeline (`backend/app/services/architecture_agent.py`) dispatches one summarization subagent per detected module.
- **Parallel execution** — those subagent calls run concurrently via `asyncio.gather`, not sequentially.
- *(Fill in during the build: specific Bob IDE sessions used, screenshots referenced below.)*

## Tech Stack

| Layer | Tech |
|---|---|
| Frontend | Next.js, React, TypeScript, Tailwind CSS, React Flow |
| Backend | FastAPI, Python, Pydantic |
| AI Layer | IBM Watsonx, IBM Granite |
| Infrastructure | Docker, Docker Compose |

## Getting Started

### Prerequisites

- Docker & Docker Compose
- `git` (used to shallow-clone the repo you point this at)
- (Optional) IBM Cloud account with Watsonx access for live Granite calls — without credentials the AI service falls back to deterministic mock responses.

### Run everything

```bash
cp .env.example .env
# fill in IBM Watsonx credentials in .env if you have them
docker compose up --build
```

- Frontend: http://localhost:3000
- Backend API docs: http://localhost:8000/docs

Paste a public GitHub repo URL (or a local path already on the machine running the backend) into the landing page and hit **Analyze**.

## Project Structure

```
backend/    FastAPI application (ingestion, architecture map, starter tasks)
frontend/   Next.js application (repo input, map view, task list)
bob_sessions/   Bob IDE session screenshots/exports (required for submission)
docker-compose.yml
```

## Demo

*(Fill in before submission: demo video link, sample repo walkthrough, impact metric — e.g. "time-to-first-commit: 14 days → under 2 hours".)*

## `bob_sessions/`

Contains real Bob IDE task session screenshots and exported task history from building this project — see `bob_sessions/README.md`.

## Team

*(Add team members and roles here.)*
