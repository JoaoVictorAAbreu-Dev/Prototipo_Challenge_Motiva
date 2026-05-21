# 🛰️ Nexus SENTINEL

**Enterprise Geospatial Monitoring Platform**

A scalable, enterprise-grade geospatial monitoring platform built with modern technologies and following Domain-Driven Design (DDD) and Clean Architecture principles.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                       │
│         React + TypeScript + Vite + Tailwind            │
│           (Domain | Application | Infrastructure | Presentation)
└─────────────────────────────────────────────────────────┘
                         ↕ HTTP/REST
┌─────────────────────────────────────────────────────────┐
│                    BACKEND LAYER                        │
│            FastAPI + SQLAlchemy + SQLModel              │
│  (Domain | Application | Infrastructure | Presentation) │
└─────────────────────────────────────────────────────────┘
                         ↕ SQL
┌─────────────────────────────────────────────────────────┐
│                   DATA LAYER                            │
│      PostgreSQL + PostGIS (Geospatial Extension)        │
│           Redis (Caching & Message Queue)               │
└─────────────────────────────────────────────────────────┘
```

### Design Patterns

- **Domain-Driven Design (DDD)**: Business logic separated into domain entities and value objects
- **Clean Architecture**: Clear separation of concerns (Domain → Application → Infrastructure → Presentation)
- **Modular Monolith**: Organized by business capabilities with clear boundaries
- **Repository Pattern**: Abstracted data persistence
- **Use Case Pattern**: Explicit application business rules

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.12+ (for local backend development)

### Setup with Docker

1. **Clone and setup**
   ```bash
   git clone <repository>
   cd nexus-sentinel
   cp .env.example .env
   ```

2. **Start services**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000
   - **API Documentation**: http://localhost:8000/api/docs
   - **Database**: localhost:5432

### Local Development

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

---

## 📁 Project Structure

### Backend (`/backend`)

```
backend/
├── app/
│   ├── domain/                 # Business logic & entities
│   │   ├── entities/           # Domain entities
│   │   ├── value_objects.py    # Value objects
│   │   ├── repositories.py     # Repository interfaces
│   │   └── exceptions.py       # Domain exceptions
│   ├── application/            # Use cases & DTOs
│   │   ├── use_cases/          # Application services
│   │   ├── dto/                # Data transfer objects
│   │   ├── mappers/            # Entity mappers
│   │   └── events/             # Domain events
│   ├── infrastructure/         # External integrations
│   │   ├── database/           # DB models & session
│   │   ├── repositories/       # Repository implementations
│   │   ├── external/           # External APIs
│   │   └── security/           # Auth & security
│   ├── presentation/           # API layer
│   │   ├── api/                # API routes
│   │   ├── schemas.py          # Pydantic schemas
│   │   ├── dependencies.py     # FastAPI dependencies
│   │   └── error_handlers.py   # Exception handlers
│   ├── main.py                 # FastAPI app
│   └── config.py               # Configuration
├── tests/                      # Test suite
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container image
└── .env.example               # Environment variables
```

### Frontend (`/frontend`)

```
frontend/
├── src/
│   ├── domain/                 # Types & interfaces
│   │   └── types.ts            # Domain models
│   ├── application/            # State & business logic
│   │   └── stores/             # Zustand stores
│   ├── infrastructure/         # External integrations
│   │   └── api/                # API client
│   ├── presentation/           # UI layer
│   │   ├── components/         # React components
│   │   ├── pages/              # Page components
│   │   ├── hooks/              # Custom hooks
│   │   └── styles/             # Global styles
│   ├── App.tsx                 # Root component
│   └── main.tsx                # Entry point
├── index.html                  # HTML template
├── package.json                # Dependencies
├── vite.config.ts              # Vite configuration
├── tailwind.config.js          # Tailwind configuration
├── tsconfig.json               # TypeScript configuration
├── Dockerfile                  # Container image
└── .env.example               # Environment variables
```

---

## 🔧 Core Features

### Backend

- ✅ **RESTful API** with FastAPI
- ✅ **Async/await** support throughout
- ✅ **PostgreSQL + PostGIS** for geospatial queries
- ✅ **Redis** for caching and session management
- ✅ **JWT Authentication** ready
- ✅ **CORS** properly configured
- ✅ **Database migrations** with Alembic
- ✅ **Structured logging**
- ✅ **Error handling** and validation

### Frontend

- ✅ **React 18** with TypeScript
- ✅ **Vite** for fast builds
- ✅ **Tailwind CSS** for styling
- ✅ **Leaflet** for interactive maps
- ✅ **Zustand** for state management
- ✅ **Axios** for HTTP requests
- ✅ **Responsive design** with mobile support
- ✅ **Type-safe** across the stack

---

## 📊 Database Schema

### Key Tables

- **monitors**: Geospatial monitoring zones
- **alerts**: Alert events and notifications
- **users**: User management
- **audit_logs**: Audit trail

### PostGIS Extensions

- Point geometry for coordinates
- Polygon geometry for boundaries
- Spatial indexing for performance

---

## 🔐 Security

- ✅ CORS configured
- ✅ JWT token-based auth
- ✅ Password hashing with bcrypt
- ✅ SQL injection prevention (SQLAlchemy)
- ✅ Input validation with Pydantic
- ✅ Environment-based secrets
- ✅ HTTPS ready

---

## 📝 API Documentation

Swagger UI: `http://localhost:8000/api/docs`

### Example Endpoints

**Create Monitor**
```http
POST /api/v1/monitors
Content-Type: application/json

{
  "name": "Perimeter Zone A",
  "description": "Main facility perimeter",
  "monitor_type": "perimeter",
  "latitude": -15.793889,
  "longitude": -47.879444,
  "radius_meters": 500
}
```

**Get Monitor**
```http
GET /api/v1/monitors/{monitor_id}
```

**List Monitors**
```http
GET /api/v1/monitors?skip=0&limit=20
```

---

## 🧪 Testing

### Backend

```bash
cd backend
pytest                    # Run all tests
pytest -v               # Verbose output
pytest --cov            # Coverage report
pytest -k "monitor"     # Run specific tests
```

### Frontend

```bash
cd frontend
npm run test            # Run tests
npm run test:watch     # Watch mode
```

---

## 📦 Deployment

### Docker Build

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Environment Variables

Copy `.env.example` to `.env` and update:

```bash
cp .env.example .env
# Edit .env with your values
```

---

## 🛠️ Development

### Code Quality

```bash
# Backend
cd backend
black .              # Format code
flake8 .             # Lint code
mypy .               # Type checking
isort .              # Sort imports

# Frontend
cd frontend
npm run lint         # ESLint
npm run format       # Prettier
npm run type-check   # TypeScript
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/monitor-analytics

# Commit changes
git commit -m "feat: add monitor analytics"

# Push and create PR
git push origin feature/monitor-analytics
```

---

## 📞 Support

- Documentation: [Wiki](./wiki)
- Issues: [GitHub Issues](./issues)
- Email: support@nexus-sentinel.com

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙋 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](./CONTRIBUTING.md)

---

**Built with ❤️ for enterprise-grade geospatial monitoring**

