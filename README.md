
# GitHub Summary: SENTINEL

## Project Description
SENTINEL is an AI-powered, community-driven investigative and alert system designed to assist in locating missing persons and responding to emergencies. It integrates voice interaction, real-time data monitoring, and OSINT tools into a unified web-based platform to support first responders and empower community volunteers.

## Key Features
- **AI Brain (CodeLlama)**: Intelligent Q&A and investigative reasoning
- **Voice Interaction (Piper)**: Natural speech synthesis and voice alerts
- **Voice Input & Transcription**: Hands-free operation with natural language commands
- **Live Monitoring**: Real-time emergency radio traffic via trunking server or Broadcastify API
- **Case File Management**: Automated creation and updates with timelines and visual pattern recognition
- **OSINT Tools**: Scrapes public data sources for clues and patterns
- **Dashboard Interface**: Web-based UI with alerts, case tracking, and data visualization
- **Telegram & Discord Integration**: Alerts and Q&A via popular platforms
- **Modular & Reproducible**: Low-cost, open-source, and easy to deploy

## Target Users
- Search and rescue teams
- Community volunteers and citizen investigators
- Nonprofits and public safety organizations
- Emergency responders
- Future public-facing version for citizen engagement

## Technologies Used
- **Frontend**: React
- **AI Engine**: CodeLlama via `llama.cpp`
- **Voice Synthesis**: Piper (Norman medium voice)
- **Backend** *(planned)*: Flask, Django, or Node.js
- **Database** *(planned)*: SQLite, PostgreSQL, or MongoDB
- **Monitoring**: Python (`listener.py`) with trunking server or Broadcastify API
- **OSINT Tools**: Python (`requests`, `BeautifulSoup`, `Selenium`)
- **Bots**: Telegram Bot API, Discord.py or Discord.js

## System Architecture Overview
- **Frontend** communicates with the **AI brain** and **voice system** for interactive responses.
- **Live monitoring** triggers alerts sent to the frontend and messaging platforms.
- **Backend** manages case files and stores data in the **database**.
- **OSINT scraper** feeds public data into the system for analysis and visualization.

