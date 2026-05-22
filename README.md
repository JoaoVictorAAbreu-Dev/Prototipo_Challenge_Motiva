<h1 align="center">Nexus-SENTINEL</h1>

<p align="center">
  Plataforma enterprise para gestão rodoviária com Digital Twin operacional,
  inteligência de criticidade, clustering logístico e geração de evidência regulatória.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/backend-FastAPI-0f172a?style=for-the-badge&logo=fastapi&logoColor=22c55e" alt="FastAPI" />
  <img src="https://img.shields.io/badge/frontend-React%20%2B%20TypeScript-0f172a?style=for-the-badge&logo=react&logoColor=61dafb" alt="React TypeScript" />
  <img src="https://img.shields.io/badge/database-PostgreSQL%20%2B%20PostGIS-0f172a?style=for-the-badge&logo=postgresql&logoColor=60a5fa" alt="PostgreSQL PostGIS" />
  <img src="https://img.shields.io/badge/architecture-DDD%20%7C%20Clean%20Architecture-0f172a?style=for-the-badge&logo=codefactor&logoColor=f8fafc" alt="DDD Clean Architecture" />
</p>

<p align="center">
  <a href="#visao-geral">Visão Geral</a> •
  <a href="#capacidades">Capacidades</a> •
  <a href="#arquitetura">Arquitetura</a> •
  <a href="#api">API</a> •
  <a href="#execucao">Execução</a> •
  <a href="#validacao">Validação</a>
</p>

<hr />

<h2 id="visao-geral">Visão Geral</h2>

<p>
  O Nexus-SENTINEL é um monólito modular orientado a domínio para priorização de manutenção rodoviária.
  O sistema utiliza <strong>microtrechos</strong> como malha operacional principal e mantém
  <strong>monitors</strong> como camada de gestão, observação e suporte contratual.
</p>

<p>
  A plataforma entrega uma superfície operacional com projeção temporal, agrupamento inteligente de ordens,
  buffer logístico para retenção estratégica e geração de dossiê digital em PDF para trilha de conformidade.
</p>

<table>
  <tr>
    <td><strong>Problema resolvido</strong></td>
    <td>Priorização operacional, redução de deslocamento improdutivo e suporte à conformidade ANTT.</td>
  </tr>
  <tr>
    <td><strong>Modelo principal</strong></td>
    <td><code>microsegments</code> + simulação temporal + clusters DBSCAN + Compliance Mirror.</td>
  </tr>
  <tr>
    <td><strong>Experiência</strong></td>
    <td>Dashboard dark mode enterprise com mapa operacional central, briefing técnico e KPIs executivos.</td>
  </tr>
</table>

<h2 id="capacidades">Capacidades</h2>

<ul>
  <li><strong>Operational Priority Engine:</strong> cálculo de IPO com EVI, chuva, dias sem manutenção, risco operacional e peso contratual.</li>
  <li><strong>Digital Twin Operacional:</strong> simulação das próximas semanas com recalculo de criticidade e evolução do risco.</li>
  <li><strong>Clustering logístico:</strong> agrupamento DBSCAN de microtrechos críticos próximos para formação de frentes de intervenção.</li>
  <li><strong>Logistics-Compliance Buffer:</strong> retenção estratégica de ordens por até 48h para maximizar eficiência operacional.</li>
  <li><strong>Compliance Mirror:</strong> exportação de PDF com evidência operacional, histórico e conformidade contratual.</li>
  <li><strong>Dashboard executivo:</strong> KPIs de redução operacional, economia logística, combustível economizado e criticidade média da malha.</li>
</ul>

<h2 id="arquitetura">Arquitetura</h2>

<p>
  O backend foi estruturado com <strong>DDD</strong>, <strong>Clean Architecture</strong> e
  <strong>Modular Monolith</strong>, com separação explícita entre domínio, aplicação,
  infraestrutura e apresentação.
</p>

<table>
  <thead>
    <tr>
      <th align="left">Camada</th>
      <th align="left">Responsabilidade</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>domain</code></td>
      <td>Entidades, value objects, contratos de repositório e regras centrais de negócio.</td>
    </tr>
    <tr>
      <td><code>application</code></td>
      <td>Use cases por módulo e orquestração de fluxos.</td>
    </tr>
    <tr>
      <td><code>infrastructure</code></td>
      <td>SQLAlchemy, bootstrap de seed, persistência e exportação PDF.</td>
    </tr>
    <tr>
      <td><code>presentation</code></td>
      <td>Routers FastAPI, DTOs Pydantic e composição da API pública.</td>
    </tr>
  </tbody>
</table>

<h3>Domínios do backend</h3>

<table>
  <thead>
    <tr>
      <th align="left">Módulo</th>
      <th align="left">Função</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>operational_intelligence</code></td>
      <td>Monitors, microsegments e cálculo de IPO.</td>
    </tr>
    <tr>
      <td><code>simulation</code></td>
      <td>Projeção temporal da malha e recalculo operacional.</td>
    </tr>
    <tr>
      <td><code>logistics</code></td>
      <td>DBSCAN, compensação logística e buffer de agrupamento estratégico.</td>
    </tr>
    <tr>
      <td><code>compliance</code></td>
      <td>Geração de dossiê digital de evidência em PDF.</td>
    </tr>
  </tbody>
</table>

<h3>Estrutura ativa</h3>

<pre><code>backend/app/
├── core/
├── domain/
├── infrastructure/
├── modules/
│   ├── compliance/
│   ├── logistics/
│   ├── operational_intelligence/
│   └── simulation/
└── presentation/

frontend/src/
├── domain/
├── infrastructure/
└── presentation/
    ├── components/
    ├── hooks/
    ├── pages/
    ├── styles/
    └── utils/</code></pre>

<h2>Fluxo Operacional</h2>

<ol>
  <li>O seed inicial carrega a malha de <code>highway_data.json</code> para <code>microsegments</code>.</li>
  <li>A API entrega o estado atual da malha com IPO projetado em tempo real.</li>
  <li>O slider temporal aciona projeção futura via backend.</li>
  <li>Os clusters são recalculados com DBSCAN a partir dos microtrechos projetados.</li>
  <li>O buffer logístico decide retenção ou despacho imediato da ordem.</li>
  <li>O Compliance Mirror exporta o PDF do trecho selecionado.</li>
</ol>

<h2 id="api">API</h2>

<p>
  Base local padrão: <code>http://localhost:8000/api/v1</code><br />
  Documentação interativa: <code>http://localhost:8000/api/docs</code>
</p>

<table>
  <thead>
    <tr>
      <th align="left">Método</th>
      <th align="left">Rota</th>
      <th align="left">Descrição</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>GET</code></td>
      <td><code>/microsegments</code></td>
      <td>Lista a malha operacional atual com IPO, criticidade, recomendação e metadados.</td>
    </tr>
    <tr>
      <td><code>GET</code></td>
      <td><code>/microsegments/{microsegment_id}</code></td>
      <td>Retorna o detalhe operacional de um microtrecho.</td>
    </tr>
    <tr>
      <td><code>POST</code></td>
      <td><code>/simulation/project</code></td>
      <td>Projeta a malha nas próximas semanas e recalcula o comportamento operacional.</td>
    </tr>
    <tr>
      <td><code>POST</code></td>
      <td><code>/calculate-ipo</code></td>
      <td>Executa o cálculo isolado do Operational Priority Engine.</td>
    </tr>
    <tr>
      <td><code>POST</code></td>
      <td><code>/generate-clusters</code></td>
      <td>Gera clusters de intervenção com métricas logísticas e buffer estratégico.</td>
    </tr>
    <tr>
      <td><code>GET</code></td>
      <td><code>/export-compliance-report/{segment_id}</code></td>
      <td>Exporta o dossiê digital de evidência operacional em PDF.</td>
    </tr>
    <tr>
      <td><code>GET</code></td>
      <td><code>/monitors</code></td>
      <td>Lista a camada de gestão de monitors.</td>
    </tr>
    <tr>
      <td><code>GET</code></td>
      <td><code>/monitors/{monitor_id}</code></td>
      <td>Consulta um monitor específico.</td>
    </tr>
    <tr>
      <td><code>POST</code></td>
      <td><code>/monitors</code></td>
      <td>Cria um novo monitor operacional.</td>
    </tr>
    <tr>
      <td><code>GET</code></td>
      <td><code>/health</code></td>
      <td>Health check da aplicação.</td>
    </tr>
  </tbody>
</table>

<h2>Stack Técnica</h2>

<table>
  <thead>
    <tr>
      <th align="left">Camada</th>
      <th align="left">Tecnologias</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Backend</td>
      <td>FastAPI, Pydantic, SQLAlchemy, asyncpg, GeoAlchemy2</td>
    </tr>
    <tr>
      <td>Geoespacial</td>
      <td>PostgreSQL, PostGIS</td>
    </tr>
    <tr>
      <td>Analytics</td>
      <td>NumPy, scikit-learn</td>
    </tr>
    <tr>
      <td>Compliance</td>
      <td>ReportLab</td>
    </tr>
    <tr>
      <td>Frontend</td>
      <td>React 18, TypeScript, Vite, Leaflet, Axios</td>
    </tr>
    <tr>
      <td>Qualidade</td>
      <td>Pytest, ESLint, TypeScript compiler</td>
    </tr>
    <tr>
      <td>Infra</td>
      <td>Docker, Docker Compose</td>
    </tr>
  </tbody>
</table>

<h2 id="execucao">Execução</h2>

<h3>Docker</h3>

<pre><code class="language-powershell">docker-compose up --build</code></pre>

<table>
  <thead>
    <tr>
      <th align="left">Serviço</th>
      <th align="left">URL padrão</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Frontend</td>
      <td><code>http://localhost:3000</code></td>
    </tr>
    <tr>
      <td>Backend</td>
      <td><code>http://localhost:8000</code></td>
    </tr>
    <tr>
      <td>Swagger</td>
      <td><code>http://localhost:8000/api/docs</code></td>
    </tr>
  </tbody>
</table>

<h3>Execução local</h3>

<details open>
  <summary><strong>Backend</strong></summary>
  <pre><code class="language-powershell">cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload</code></pre>
</details>

<details open>
  <summary><strong>Frontend</strong></summary>
  <pre><code class="language-powershell">cd frontend
npm install
npm run dev</code></pre>
</details>

<h3>Configuração de ambiente</h3>

<p>
  O backend expõe um arquivo base em <code>backend/.env.example</code>.
  A principal configuração é a conexão <code>DATABASE_URL</code> para PostgreSQL/PostGIS.
</p>

<h2>Seed Operacional</h2>

<ul>
  <li>O seed inicial é carregado de <code>highway_data.json</code>.</li>
  <li>O bootstrap ocorre no startup da API quando a tabela <code>microsegments</code> está vazia.</li>
  <li>A malha usa <code>microsegments</code> como agregados principais do Digital Twin.</li>
  <li><code>monitors</code> permanecem como camada de gestão e observação operacional.</li>
</ul>

<h2 id="validacao">Validação</h2>

<p>Comandos recomendados para verificação local:</p>

<pre><code class="language-powershell">cd backend
pytest

cd ..\frontend
npm run lint
npm run type-check
npm run build</code></pre>

<p>
  Estado validado da base atual:
</p>

<ul>
  <li><code>pytest</code> passando no backend.</li>
  <li><code>npm run lint</code> passando no frontend.</li>
  <li><code>npm run type-check</code> passando no frontend.</li>
  <li><code>npm run build</code> passando no frontend.</li>
</ul>

<h2>Roteiro de Demonstração</h2>

<ol>
  <li>Abrir o dashboard e observar a malha carregada.</li>
  <li>Mover o slider de semanas para agravar EVI, IPO e criticidade.</li>
  <li>Observar a reorganização dos clusters e o efeito do buffer logístico.</li>
  <li>Selecionar um microtrecho crítico no mapa ou na lista lateral.</li>
  <li>Exportar o PDF de compliance diretamente do briefing operacional.</li>
</ol>

<h2>Diretrizes de Engenharia</h2>

<ul>
  <li>Separação explícita de responsabilidades entre backend e frontend.</li>
  <li>Domínios isolados por módulo para facilitar evolução futura.</li>
  <li>Tipagem forte em Pydantic e TypeScript.</li>
  <li>Base preparada para crescimento sem perder legibilidade operacional.</li>
</ul>

<hr />

<p align="center">
  Documentação estruturada para apresentação técnica, leitura executiva e evolução contínua do produto.
</p>
