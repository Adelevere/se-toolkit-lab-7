## Deploy

### Prerequisites
- Docker and Docker Compose installed
- Environment file `.env.docker.secret` with required variables

### Environment Variables
Create `.env.docker.secret` with:

```bash
# Backend
LMS_API_KEY=your-secret-key
AUTOCHECKER_EMAIL=your-email@innopolis.university
AUTOCHECKER_API_PASSWORD=your-github-usernametelegram-alias
AUTOCHECKER_API_URL=https://auche.namaz.live
AUTOCHECKER_API_LOGIN=https://auche.namaz.live/api/login
AUTOCHECKER_API_BASE=https://auche.namaz.live/api

# Bot
BOT_TOKEN=your-telegram-bot-token
LLM_API_KEY=your-qwen-api-key
LLM_API_MODEL=coder-model

# Database
POSTGRES_DB=db-lab-7
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Ports
BACKEND_HOST_PORT=42001
POSTGRES_HOST_PORT=42004
PGADMIN_HOST_PORT=42003
LMS_API_HOST_PORT=42002
