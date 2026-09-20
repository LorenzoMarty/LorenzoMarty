<p align="center"><img src="assets/banner.svg" alt="Lorenzo Marty — AI & LLMOps engineer. Manga-style cover with a night skyline and one window still lit." width="100%"></p>

<p align="center">
  Santa Maria, Brazil · Internet Systems student at UFSM · research fellow at a robotics company<br>
  <a href="https://www.linkedin.com/in/lorenzo-marty/"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-lorenzo--marty-111111?style=flat-square&logo=linkedin&logoColor=white"></a>
  <a href="mailto:lorenzodreis@gmail.com"><img alt="Email" src="https://img.shields.io/badge/Email-lorenzodreis@gmail.com-111111?style=flat-square&logo=gmail&logoColor=white"></a>
</p>

<img src="assets/ch1.svg" alt="Chapter 1: Origin" width="100%">

I'm a Python developer aiming at AI engineering, with one habit I can't shake: **I instrument everything.** An LLM feature that ships without a trace, a cost number and a way to check its answers isn't finished — it's a demo.

Since 2026 I've been a research fellow at a robotics company, building Python backend services for observability and telemetry plus a Next.js frontend on a design system. On my own time I ship products end to end, from schema to deploy. I do my best work at night; off the keyboard, it's anime and manga.

<img src="assets/ch2.svg" alt="Chapter 2: Night Log" width="100%">

<img src="assets/nightlog.svg" alt="Totals, a skyline of logged work sessions per month, and a star map with one star per day logged" width="100%">

*My commit graph only shows part of the story: much of my work lives in private and organization repositories, in design docs and in decisions. So I keep a dated log, one entry per work session. Each building is a month, each star a day I logged. \* month to date.*

<img src="assets/ch3.svg" alt="Chapter 3: Signature Technique" width="100%">

Every LLM feature gets a trace, a cost number and an audit step before it ships. The correction pipeline of [Donc](https://github.com/LorenzoMarty/Donc), my ENEM essay platform:

```mermaid
flowchart LR
    A([Student essay]) --> B[Celery queue]
    B --> C[Specialized agents<br/>theme · thesis · argumentation<br/>repertoire · grammar]
    C --> D[Score per competency]
    D --> E{Elimination gate}
    E --> F[Score audit]
    F --> G([Feedback + study plan])
    C -.-> T[(Langfuse traces<br/>+ cost in BRL)]
    D -.-> T
    F -.-> T
    classDef flow fill:#fbfbf8,stroke:#0d0d0d,stroke-width:2px,color:#0d0d0d;
    classDef obs fill:#d6d6d1,stroke:#0d0d0d,stroke-dasharray:4 3,color:#0d0d0d;
    class A,B,C,D,E,F,G flow;
    class T obs;
```

<img src="assets/ch4.svg" alt="Chapter 4: Story Arcs" width="100%">

| | Arc | What it does | Stack |
|:-:|---|---|---|
| ● | [**Donc**](https://github.com/LorenzoMarty/Donc) · [app](https://app-redacao-five.vercel.app) | ENEM essay platform: pipeline of specialized LLM agents, RAG, gamified cognitive trainer | Next.js 16 · FastAPI · Postgres + pgvector · Celery · agno · OpenAI · Langfuse |
| ◐ | [**Agenda-Juri**](https://github.com/LorenzoMarty/Agenda-Juri) | Law-firm CRM: cases, deadlines, Google Calendar/Drive sync, AI meeting summaries | Django 6 · React 19 · Celery · Redis · Docker · GCP |
| ○ | [**Oráculo Chatbot**](https://github.com/LorenzoMarty/Oraculo-Chatbot) | RAG chatbot over documents, websites and videos | Django · Agno · Qdrant |
| ○ | [**Transcripty**](https://github.com/LorenzoMarty/Transcripty) | Meeting recorder with transcription and automated summaries | Python · Streamlit · Whisper · LLM |
| ⊘ | **NexaFit** | Fitness PWA: workout logging and body-evolution charts | Next.js 16 · Drizzle · Neon · Tailwind 4 |
| ◌ | **RastroAI** | Investigative intelligence on Brazilian open public data | Python · Postgres · Neo4j |

*● live · ◐ client work · ○ public · ⊘ private · ◌ in design*

<img src="assets/ch5.svg" alt="Chapter 5: Loadout and Next Arc" width="100%">

![Python](https://img.shields.io/badge/-Python-111111?style=flat-square&logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/-FastAPI-111111?style=flat-square&logo=fastapi&logoColor=white) ![Django](https://img.shields.io/badge/-Django-111111?style=flat-square&logo=django&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-111111?style=flat-square&logo=postgresql&logoColor=white) ![Redis](https://img.shields.io/badge/-Redis-111111?style=flat-square&logo=redis&logoColor=white) ![Celery](https://img.shields.io/badge/-Celery-111111?style=flat-square&logo=celery&logoColor=white) ![OpenAI](https://img.shields.io/badge/-OpenAI-111111?style=flat-square&logo=openai&logoColor=white) ![Prometheus](https://img.shields.io/badge/-Prometheus-111111?style=flat-square&logo=prometheus&logoColor=white) ![Grafana](https://img.shields.io/badge/-Grafana-111111?style=flat-square&logo=grafana&logoColor=white) ![TypeScript](https://img.shields.io/badge/-TypeScript-111111?style=flat-square&logo=typescript&logoColor=white) ![Next.js](https://img.shields.io/badge/-Next.js-111111?style=flat-square&logo=nextdotjs&logoColor=white) ![React](https://img.shields.io/badge/-React-111111?style=flat-square&logo=react&logoColor=white) ![Docker](https://img.shields.io/badge/-Docker-111111?style=flat-square&logo=docker&logoColor=white)

**Focus:** LLM applications and agents · RAG · observability (OpenTelemetry, Prometheus, Grafana, Langfuse) · async pipelines · API design

| Now | Next arc | Endgame |
|---|---|---|
| Building Donc and the data foundation for RastroAI | Evaluation, tracing and cost control for LLM apps, in production | AI and data engineer at mid-level: reliable LLM systems, measured end to end |

<p align="center"><b><i>To be continued…</i></b></p>
