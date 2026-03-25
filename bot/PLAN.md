# Bot Development Plan

## Project Overview
This Telegram bot provides an interface to the Learning Management System (LMS) backend. Users can retrieve information about labs, check scores, and interact with the system using natural language commands. The bot is designed with a testable architecture where command handlers are pure functions that return text responses, independent of the Telegram transport layer.

## Architecture
The bot follows a modular structure with clear separation of concerns:

- **bot/handlers/** — Pure functions that process commands and return text responses. Each handler receives input parameters and returns a string, with no knowledge of Telegram.
- **bot/services/** — API clients for external services (LMS backend, LLM). Handles HTTP requests and error handling.
- **bot/config.py** — Centralized configuration loading from environment variables.
- **bot/bot.py** — Entry point with two modes: Telegram mode (connects to Telegram API) and test mode (prints responses to stdout for offline verification).

## Implementation Phases

### Phase 1: Project Scaffold (Current Task)
- Create directory structure: handlers/, services/
- Implement --test mode for offline command testing
- Add basic commands: /start, /help, /health, /labs
- Configure dependencies with pyproject.toml

### Phase 2: Backend Integration
- LMS API client to fetch labs and submission data
- Implement /scores command with lab filtering
- Add error handling and retry logic

### Phase 3: LLM Intent Routing
- Qwen API client for natural language understanding
- Route user queries to appropriate commands
- Handle free-form questions about labs and scores

### Phase 4: Production Deployment
- Background execution with nohup
- Logging and monitoring
- Health checks and auto-restart

## Testing Strategy
- `--test` mode for all commands without Telegram connection
- Handlers are pure functions → unit testable
- Integration tests with mock LMS API responses
