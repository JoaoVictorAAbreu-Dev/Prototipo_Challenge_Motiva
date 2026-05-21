<h1 align="center">Nexus Sentinel</h1>

<p align="center">
  <strong>Enterprise Geospatial Monitoring Platform</strong>
</p>

<p align="center">
  Plataforma corporativa de monitoramento geoespacial, desenvolvida com foco em escalabilidade, modularidade e separação clara de responsabilidades.
</p>

<p align="center">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a>
  <a href="#"><img src="https://img.shields.io/badge/backend-FastAPI-009688" alt="Backend"></a>
  <a href="#"><img src="https://img.shields.io/badge/frontend-React%20%2B%20TypeScript-61DAFB" alt="Frontend"></a>
  <a href="#"><img src="https://img.shields.io/badge/database-PostgreSQL%20%2B%20PostGIS-336791" alt="Database"></a>
</p>

<hr>

<h2>Visão geral</h2>

<p>
  O Nexus Sentinel foi criado para cenários que exigem monitoramento geoespacial confiável, auditável e fácil de evoluir.
  O projeto separa domínio, aplicação, infraestrutura e interface para reduzir acoplamento e aumentar a manutenibilidade.
</p>

<p>
  A arquitetura foi desenhada para suportar crescimento por capacidade de negócio, com backend moderno, frontend responsivo e persistência espacial.
</p>

<h2>Sumário</h2>

<ul>
  <li><a href="#visao-geral">Visão geral</a></li>
  <li><a href="#arquitetura">Arquitetura</a></li>
  <li><a href="#principais-funcionalidades">Principais funcionalidades</a></li>
  <li><a href="#estrutura-do-projeto">Estrutura do projeto</a></li>
  <li><a href="#como-executar">Como executar</a></li>
  <li><a href="#desenvolvimento-local">Desenvolvimento local</a></li>
  <li><a href="#banco-de-dados">Banco de dados</a></li>
  <li><a href="#seguranca">Segurança</a></li>
  <li><a href="#api">API</a></li>
  <li><a href="#testes">Testes</a></li>
  <li><a href="#qualidade-de-codigo">Qualidade de código</a></li>
  <li><a href="#deploy">Deploy</a></li>
  <li><a href="#licenca">Licença</a></li>
</ul>

<h2>Arquitetura</h2>

<pre><code>┌──────────────────────────────────────────────────────────────┐
│                      Frontend Layer                          │
│               React + TypeScript + Vite + Tailwind           │
│            Domain | Application | Infrastructure | UI        │
└──────────────────────────────────────────────────────────────┘
                           ↕ HTTP / REST
┌──────────────────────────────────────────────────────────────┐
│                       Backend Layer                          │
│                FastAPI + SQLAlchemy + SQLModel               │
│            Domain | Application | Infrastructure | API       │
└──────────────────────────────────────────────────────────────┘
                           ↕ SQL
┌──────────────────────────────────────────────────────────────┐
│                        Data Layer                             │
│              PostgreSQL + PostGIS + Redis                    │
└──────────────────────────────────────────────────────────────┘
</code></pre>

<h3>Princípios de projeto</h3>

<ul>
  <li>Domain-Driven Design para centralizar regras de negócio.</li>
  <li>Clean Architecture para separar responsabilidades.</li>
  <li>Modular Monolith para organizar o sistema por contexto.</li>
  <li>Repository Pattern para desacoplar persistência.</li>
  <li>Use Case Pattern para explicitar fluxos de aplicação.</li>
</ul>

<h2>Principais funcionalidades</h2>

<table>
  <tr>
    <th>Backend</th>
    <th>Frontend</th>
  </tr>
  <tr>
    <td>
      <ul>
        <li>API REST com FastAPI.</li>
        <li>Suporte a operações assíncronas.</li>
        <li>Consultas geoespaciais com PostgreSQL + PostGIS.</li>
        <li>Cache e mensageria com Redis.</li>
        <li>Autenticação pronta para JWT.</li>
        <li>Migrações com Alembic.</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>React 18 com TypeScript.</li>
        <li>Vite para build e desenvolvimento rápidos.</li>
        <li>Tailwind CSS para interface responsiva.</li>
        <li>Leaflet para mapas interativos.</li>
        <li>Zustand para gerenciamento de estado.</li>
        <li>Axios para integração com a API.</li>
      </ul>
    </td>
  </tr>
</table>

<h2>Estrutura do projeto</h2>

<h3>Backend</h3>

<pre><code>backend/
├── app/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   ├── presentation/
│   ├── main.py
│   └── config.py
├── tests/
├── requirements.txt
├── Dockerfile
└── .env.example
</code></pre>

<h3>Frontend</h3>

<pre><code>frontend/
├── src/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   ├── presentation/
│   ├── App.tsx
│   └── main.tsx
├── index.html
├── package.json
├── vite.config.ts
├── tailwind.config.js
├── tsconfig.json
├── Dockerfile
└── .env.example
</code></pre>

<h2>Como executar</h2>

<h3>Pré-requisitos</h3>

<ul>
  <li>Docker e Docker Compose.</li>
  <li>Node.js 18+.</li>
  <li>Python 3.12+.</li>
</ul>

<h3>Execução com Docker</h3>

<pre><code>git clone &lt;repository&gt;
cd nexus-sentinel
cp .env.example .env
docker-compose up -d
</code></pre>

<h3>Acessos principais</h3>

<ul>
  <li>Frontend: <code>http://localhost:3000</code></li>
  <li>Backend API: <code>http://localhost:8000</code></li>
  <li>Documentação da API: <code>http://localhost:8000/api/docs</code></li>
  <li>Banco de dados: <code>localhost:5432</code></li>
</ul>

<h2>Desenvolvimento local</h2>

<h3>Backend</h3>

<pre><code>cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
</code></pre>

<h3>Frontend</h3>

<pre><code>cd frontend
npm install
npm run dev
</code></pre>

<h2>Banco de dados</h2>

<ul>
  <li><code>monitors</code>: zonas de monitoramento geoespacial.</li>
  <li><code>alerts</code>: eventos e notificações.</li>
  <li><code>users</code>: gerenciamento de usuários.</li>
  <li><code>audit_logs</code>: trilha de auditoria.</li>
</ul>

<h2>Segurança</h2>

<ul>
  <li>CORS configurado.</li>
  <li>Autenticação baseada em JWT.</li>
  <li>Hash de senhas com bcrypt.</li>
  <li>Proteção contra SQL injection com SQLAlchemy.</li>
  <li>Validação de entrada com Pydantic.</li>
  <li>Segredos definidos por ambiente.</li>
</ul>

<h2>API</h2>

<h3>Criar monitor</h3>

<pre><code>POST /api/v1/monitors
Content-Type: application/json

{
  "name": "Perimeter Zone A",
  "description": "Main facility perimeter",
  "monitor_type": "perimeter",
  "latitude": -15.793889,
  "longitude": -47.879444,
  "radius_meters": 500
}
</code></pre>

<h3>Outros endpoints</h3>

<pre><code>GET /api/v1/monitors/{monitor_id}
GET /api/v1/monitors?skip=0&amp;limit=20
</code></pre>

<h2>Testes</h2>

<h3>Backend</h3>

<pre><code>cd backend
pytest
pytest -v
pytest --cov
pytest -k "monitor"
</code></pre>

<h3>Frontend</h3>

<pre><code>cd frontend
npm run test
npm run test:watch
</code></pre>

<h2>Qualidade de código</h2>

<h3>Backend</h3>

<pre><code>cd backend
black .
flake8 .
mypy .
isort .
</code></pre>

<h3>Frontend</h3>

<pre><code>cd frontend
npm run lint
npm run format
npm run type-check
</code></pre>

<h2>Deploy</h2>

<pre><code>docker-compose build
docker-compose up -d
docker-compose logs -f backend
docker-compose logs -f frontend
</code></pre>

<h2>Licença</h2>

<p>Distribuído sob a licença MIT. Consulte o arquivo <code>LICENSE</code> para mais detalhes.</p>
