# Scaffold for Celery Beat and Event-Driven SSE (FastAPI + React)

This scaffold demonstrates an **event-driven microservice setup** using:

- **FastAPI** — backend API with Server-Sent Events (SSE)
- **Celery + Celery Beat** — distributed task processing and scheduling
- **Redis** — message broker
- **MongoDB** — database for persistent storage
- **React (Vite)** — frontend for live updates

---

## Architecture Overview

![alt text](architecture.png)

## Getting Started with Podman (or Docker)

### Build and Start All Services

```bash
podman compose up --build
```

| Service           | Description                       |     Port |
| ----------------- | --------------------------------- | -------: |
| **backend**       | FastAPI backend (SSE endpoint)    |   `8000` |
| **frontend**      | React frontend (served via Nginx) |   `3000` |
| **celery_worker** | Celery worker for background jobs | internal |
| **celery_beat**   | Celery scheduler (periodic jobs)  | internal |
| **redis**         | Message broker for Celery         |   `6379` |
| **mongo**         | MongoDB database                  |  `27017` |

### Access the Application

- Frontend: http://localhost:3000
- Backend (API): http://localhost:8000
- Live Events: http://localhost:8000/events

### Running Frontend in Development Mode

```bash
cd frontend
npm install
npm run dev
```
