# Feed-O-Meter
Feed-O-Meter is a research prototype that lets design students practice delivering feedback to AI-generated mentee personas. The system pairs a React front end with a Flask/OpenAI backend that analyzes mentor feedback, tracks interaction metrics, and rewrites design ideas based on accumulated action plans. This document focuses on running the system locally and reproducing study sessions.

## Repository Layout
```
Feed-O-Meter/
├── client/             # React SPA (login, start, feedback, manage pages)
├── server/             # Flask app, SQLAlchemy models, OpenAI prompts
├── requirements.txt    # Backend dependencies
├── package.json        # CRA defaults for the client
└── macenv/             # Optional local virtual environment
```

## Prerequisites
- Python 3.10+
- Node.js 18+ (with npm)
- OpenAI API key with access to GPT-4o / GPT-4-turbo
- macOS/Linux shell instructions below; adapt paths for Windows as needed.

## Backend Setup
1. **Create a virtual environment and install dependencies**
   ```bash
   cd server
   python -m venv .venv
   source .venv/bin/activate         # Windows: .venv\Scripts\activate
   pip install -r ../requirements.txt
   ```
2. **Configure OpenAI credentials**  
   Create `server/.env` (or project-level `.env`) with:
   ```
   My_OpenAI_key=sk-your-key
   ```
3. **Initialize the database and run the Flask server**
   ```bash
   python main.py
   ```
   The first launch creates `database.db` with all tables and seeds new users as they register.

## Frontend Setup
1. **Install packages**
   ```bash
   cd client
   npm install
   ```
2. **Start the development server**
   ```bash
   npm start
   ```
   CRA listens on `http://localhost:3000` and proxies API requests to `http://127.0.0.1:5000`.

## Account Creation and Experimental Modes
1. Navigate to `http://localhost:3000`.
2. Use the sign-up form on the login page to create a mentor account with email, password, display name, and participant number.
3. Participant numbers (1–24) determine:
   - The sequence of design ideas per round (see `ideaOrder` and `Ideas` arrays in `server/main.py`).
   - Whether rounds 2 and 3 run with the full Feed-O-Meter experience or a baseline chat-only condition (`InitialSetting.mode`).

## Running a Study Session
1. **Start Page (`/`)**  
   - Fetches the current round with `/getSetting`.  
   - Configure mentor persona (character card), three goal statements, and session time limit; `/saveSetting` copies values to all remaining rounds.  
   - Press **Start** to enter `/feedback`.
2. **Feedback Page (`/feedback`)**  
   - `IdeaContainer` shows the student’s topic, problem, and idea.  
   - `Chat` lets mentors submit feedback; the backend (`/response`) classifies each sentence, evaluates six quality metrics, extracts knowledge/action plans, and generates the mentee’s reply.  
   - When the system detects missing perspectives, it sets `questionChecker` so the student auto-asks a follow-up via `/askQuestion`.  
   - `Student` panel (mode 1 only) visualizes question vs. statement ratio (QNS), divergent vs. convergent ratio (CND), six evaluation scores, experience gauge, and the mentee’s current “thinking” text.
3. **Idea Update**  
   - When enough action plans accumulate, the **Update Idea** button calls `/updateIdea`, which rewrites title/problem/idea using GPT-4-turbo and the stored chat log.
4. **Advance Rounds**  
   - Invoke `/nextRound` (triggered inside the UI workflow) to record a `finish` log entry and load the next preset idea.

## Research Data and Management Tools
- Every key event (`start`, `student_question`, `update_idea`, `finish`) is appended to `UserLog` with timestamps and serialized metadata.
- Visit `/manage` to download a participant’s full log: enter the participant number, press **Download**, and the client saves `P{num}.csv` generated from `/getLogData`.
- Persistent artifacts: `server/database.db` contains `User`, `Idea`, `InitialSetting`, `KnowledgeState`, `ChatLog`, and `UserLog`. For clean runs, delete the file and restart the backend to recreate an empty database.

## Citation
```
@article{LIM2026103687,
title = {Feed-O-Meter: Investigating AI-generated mentee personas as interactive agents for scaffolding design feedback practice},
journal = {International Journal of Human-Computer Studies},
volume = {208},
pages = {103687},
year = {2026},
issn = {1071-5819},
doi = {https://doi.org/10.1016/j.ijhcs.2025.103687},
url = {https://www.sciencedirect.com/science/article/pii/S1071581925002447},
author = {Hyunseung Lim and Dasom Choi and DaEun Choi and Sooyohn Nam and Hwajung Hong},
keywords = {Design education, Design feedback, Human-computer interaction, Large language model, AI-generated agent},
abstract = {Effective feedback, including critique and evaluation, helps designers develop design concepts and refine their ideas, supporting informed decision-making throughout the iterative design process. However, in studio-based design courses, students often struggle to provide feedback due to a lack of confidence and fear of being judged, which limits their ability to develop essential feedback-giving skills. Recent advances in large language models (LLMs) suggest that role-playing with AI agents can allow learners to engage in multi-turn feedback without the anxiety of external judgment or the time constraints of real-world settings. Yet prior studies have raised concerns that LLMs struggle to behave like real people in role-play scenarios, diminishing the educational benefits of these interactions. Therefore, designing AI-based agents that effectively support learners in practicing and developing intellectual reasoning skills requires more than merely assigning the target persona's personality and role to the agent. By addressing these issues, we present Feed-O-Meter, a novel system that employs carefully designed LLM-based agents to create an environment in which students can practice giving design feedback. The system enables users to role-play as mentors, providing feedback to an AI mentee and allowing them to reflect on how that feedback impacts the AI mentee's idea development process. A user study (N=24) indicated that Feed-O-Meter increased participants' engagement and motivation through role-switching and helped them adjust feedback to be more comprehensible for an AI mentee. Based on these findings, we discuss future directions for designing systems to foster feedback skills in design education.}
}
```
