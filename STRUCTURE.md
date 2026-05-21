# 🏗️ Project Structure Documentation

## Nexus SENTINEL - Enterprise Architecture

### Overview

```
nexus-sentinel/
├── backend/                    # FastAPI Backend Service
├── frontend/                   # React Frontend Application
├── docker-compose.yml          # Multi-container orchestration
├── .env                        # Environment variables (local)
├── .env.example                # Environment template
├── README.md                   # Main documentation
└── STRUCTURE.md                # This file
```

---

## 📚 Backend Architecture (`/backend`)

### Layer-based Organization

```
backend/
├── app/
│   ├── main.py                 # FastAPI application factory
│   ├── config.py               # Application settings & configuration
│   │
│   ├── domain/                 # 🎯 DOMAIN LAYER
│   │   ├── __init__.py
│   │   ├── entities/           # Domain entities (aggregate roots)
│   │   │   ├── __init__.py
│   │   │   ├── base.py         # Base Entity class
│   │   │   └── monitor.py      # Monitor aggregate root
│   │   ├── value_objects.py    # Immutable value objects
│   │   ├── repositories.py     # Repository interfaces (abstractions)
│   │   └── exceptions.py       # Domain-specific exceptions
│   │
│   ├── application/            # 🔧 APPLICATION LAYER
│   │   ├── __init__.py
│   │   ├── use_cases/          # Use case implementations
│   │   │   ├── __init__.py
│   │   │   ├── create_monitor.py
│   │   │   └── get_monitor.py
│   │   ├── dto/                # Data Transfer Objects
│   │   ├── mappers/            # Domain ↔ DTO conversion
│   │   └── events/             # Domain events
│   │
│   ├── infrastructure/         # 🔌 INFRASTRUCTURE LAYER
│   │   ├── __init__.py
│   │   ├── database/           # Database setup & models
│   │   │   ├── __init__.py
│   │   │   ├── models.py       # SQLAlchemy ORM models
│   │   │   ├── session.py      # Database session management
│   │   │   ├── mappers.py      # Entity ↔ Model mapping
│   │   │   └── migrations/     # Alembic migrations
│   │   ├── repositories/       # Repository implementations
│   │   │   ├── __init__.py
│   │   │   └── monitor_repository.py
│   │   ├── external/           # External API integrations
│   │   └── security/           # Auth & encryption utilities
│   │
│   └── presentation/           # 🎨 PRESENTATION LAYER
│       ├── __init__.py
│       ├── schemas.py          # Pydantic request/response schemas
│       ├── dependencies.py     # FastAPI dependency injection
│       ├── error_handlers.py   # Exception handling middleware
│       └── api/                # API route definitions
│           ├── __init__.py
│           └── v1/
│               ├── __init__.py
│               └── routes.py   # Monitor endpoints
│
├── tests/                      # Test suite
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── conftest.py             # Pytest fixtures
│
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container image
└── docker-compose.yml          # Docker Compose config
```

### Layer Responsibilities

| Layer | Purpose | Dependencies |
|-------|---------|--------------|
| **Domain** | Business rules & logic | None |
| **Application** | Use cases & orchestration | Domain |
| **Infrastructure** | Data access & external services | Domain, Application |
| **Presentation** | HTTP API endpoints | All layers |

### Data Flow

```
HTTP Request
    ↓
Presentation (Schemas, validation)
    ↓
Application (Use Cases)
    ↓
Domain (Business logic)
    ↓
Infrastructure (Repository)
    ↓
Database (PostgreSQL + PostGIS)
```

---

## 💻 Frontend Architecture (`/frontend`)

### Layer-based Organization

```
frontend/
├── src/
│   ├── main.tsx                # Entry point
│   ├── App.tsx                 # Root component
│   │
│   ├── domain/                 # 🎯 DOMAIN LAYER
│   │   ├── types.ts            # TypeScript interfaces & types
│   │   └── interfaces.ts       # Service interfaces
│   │
│   ├── application/            # 🔧 APPLICATION LAYER
│   │   ├── stores/             # Zustand state management
│   │   │   ├── monitorStore.ts # Monitor state store
│   │   │   └── userStore.ts    # User state store
│   │   ├── use-cases/          # Business logic
│   │   └── services/           # Application services
│   │
│   ├── infrastructure/         # 🔌 INFRASTRUCTURE LAYER
│   │   ├── api/                # API client
│   │   │   └── client.ts       # Axios instance & methods
│   │   ├── storage/            # Local storage adapters
│   │   └── adapters/           # Third-party integrations
│   │
│   └── presentation/           # 🎨 PRESENTATION LAYER
│       ├── components/         # Reusable components
│       │   ├── MapComponent.tsx
│       │   └── MonitorList.tsx
│       ├── pages/              # Page components
│       │   └── DashboardPage.tsx
│       ├── hooks/              # Custom React hooks
│       │   └── useMap.ts
│       └── styles/             # Global styles
│           └── globals.css
│
├── index.html                  # HTML template
├── package.json                # Dependencies
├── vite.config.ts              # Vite configuration
├── tsconfig.json               # TypeScript configuration
├── tailwind.config.js          # Tailwind CSS configuration
├── postcss.config.js           # PostCSS configuration
├── .eslintrc.cjs               # ESLint configuration
├── .prettierrc.json            # Prettier configuration
├── Dockerfile                  # Container image
└── .env.example               # Environment template
```

### Component Structure

```
Page (DashboardPage)
├── Layout Components
│   ├── Header
│   └── Sidebar
└── Feature Components
    ├── MapComponent
    └── MonitorList
        └── MonitorCard
```

### State Management Flow

```
User Interaction
    ↓
Component Event Handler
    ↓
Zustand Store Action
    ↓
API Client (Infrastructure)
    ↓
Backend API
    ↓
Update Store
    ↓
Component Re-render
```

---

## 🗄️ Database Schema

### Core Tables

```
monitors
├── id (UUID)
├── name (String)
├── description (Text)
├── monitor_type (Enum)
├── status (Enum)
├── center_point (PostGIS Point)
├── radius_meters (Float)
├── created_at (Timestamp)
└── updated_at (Timestamp)

alerts
├── id (UUID)
├── monitor_id (FK)
├── event_type (String)
├── severity (Enum)
├── message (Text)
├── created_at (Timestamp)
└── resolved_at (Timestamp)
```

### PostGIS Spatial Data

- **Point**: Coordinate locations (latitude, longitude)
- **Polygon**: Monitored areas
- **LineString**: Movement paths
- **MultiPoint**: Multiple zones

---

## 🔄 API Endpoint Structure

### Versioning

```
/api/v1/
├── /monitors
│   ├── GET /            # List monitors
│   ├── POST /           # Create monitor
│   ├── GET /{id}        # Get monitor
│   ├── PUT /{id}        # Update monitor
│   └── DELETE /{id}     # Delete monitor
├── /alerts
│   ├── GET /
│   ├── POST /
│   └── GET /{id}
└── /auth
    ├── POST /login
    ├── POST /logout
    └── POST /refresh
```

---

## 📦 Dependencies

### Backend

**Core**
- FastAPI: Web framework
- SQLAlchemy: ORM
- Alembic: Migrations

**Database**
- psycopg2: PostgreSQL driver
- GeoAlchemy2: PostGIS extension
- Shapely: Geometry handling

**Security**
- python-jose: JWT tokens
- passlib: Password hashing
- cryptography: Encryption

**Frontend**

**Core**
- React: UI library
- Vite: Build tool
- TypeScript: Type safety

**UI**
- Tailwind CSS: Styling
- Leaflet: Maps
- Radix UI: Components

**State**
- Zustand: State management
- Axios: HTTP client

---

## 🚀 Build & Deploy

### Docker Images

```
nexus_sentinel_backend
├── Base: python:3.12-slim
├── Dependencies: FastAPI, SQLAlchemy, etc.
└── Port: 8000

nexus_sentinel_frontend
├── Build: node:20-alpine
├── Dependencies: React, Vite, Tailwind, etc.
└── Port: 5173

nexus_sentinel_db
├── Base: postgis/postgis:16-3.4
└── Port: 5432

nexus_sentinel_cache
├── Base: redis:7.2-alpine
└── Port: 6379
```

### Docker Compose Services

```yaml
postgres      → Database (PostGIS)
redis         → Cache layer
backend       → FastAPI API
frontend      → React SPA
```

---

## 📝 Naming Conventions

### Backend

- **Packages**: `snake_case`
- **Classes**: `PascalCase` (entities, repositories, use cases)
- **Functions**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`

### Frontend

- **Components**: `PascalCase` (e.g., `MapComponent`)
- **Hooks**: `useCamelCase` (e.g., `useMap`)
- **Files**: `camelCase` or `PascalCase` (components)
- **Constants**: `UPPER_SNAKE_CASE`
- **Types**: `PascalCase`

---

## 🔍 Key Design Patterns

### Backend

1. **Repository Pattern**: Abstract data access
2. **Use Case Pattern**: Explicit business logic
3. **Mapper Pattern**: Entity ↔ Model conversion
4. **Value Object**: Immutable, self-validating data
5. **Aggregate Root**: Entity ownership boundaries

### Frontend

1. **Component Pattern**: Reusable UI elements
2. **Hook Pattern**: Composable logic
3. **Store Pattern**: Centralized state
4. **Container/Presentational**: Smart/dumb components

---

## 📚 Additional Resources

- **DDD Principles**: [Domain-Driven Design](https://en.wikipedia.org/wiki/Domain-driven_design)
- **Clean Architecture**: [Clean Code by Robert Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- **FastAPI**: [https://fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **React**: [https://react.dev](https://react.dev)
- **PostgreSQL**: [https://www.postgresql.org](https://www.postgresql.org)
- **PostGIS**: [https://postgis.net](https://postgis.net)

---

**Version**: 1.0.0  
**Last Updated**: 2024-Q1  
**Maintainer**: Nexus SENTINEL Team
