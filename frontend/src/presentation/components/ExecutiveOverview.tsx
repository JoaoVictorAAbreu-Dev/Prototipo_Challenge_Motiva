import { memo } from 'react'

export interface ExecutiveMetric {
  title: string
  value: string
  note: string
  tone:
    | 'cyan'
    | 'blue'
    | 'emerald'
    | 'violet'
    | 'amber'
    | 'rose'
    | 'sky'
    | 'slate'
}

interface ExecutiveOverviewProps {
  metrics: ExecutiveMetric[]
}

export const ExecutiveOverview = memo<ExecutiveOverviewProps>(({ metrics }) => (
  <section className="executive-shell rounded-[28px] border border-white/10 p-5 sm:p-6">
    <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
      <div className="min-w-0">
        <p className="text-[10px] uppercase tracking-[0.38em] text-cyan-300/70">
          Executive command layer
        </p>
        <h2 className="mt-2 text-2xl font-semibold tracking-tight text-white sm:text-[30px]">
          Plataforma operacional de infraestrutura crítica
        </h2>
        <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-400">
          Superfície executiva para leitura de risco, agrupamento logístico,
          intervenção temporal e conformidade operacional.
        </p>
      </div>
      <div className="rounded-full border border-cyan-400/15 bg-cyan-400/10 px-4 py-2 text-[11px] uppercase tracking-[0.22em] text-cyan-100">
        implantável • corporativo • industrial
      </div>
    </div>

    <div className="mt-5 grid grid-cols-1 gap-3 sm:grid-cols-2 2xl:grid-cols-4">
      {metrics.map((metric) => (
        <div
          key={metric.title}
          className={`executive-kpi executive-kpi--${metric.tone}`}
        >
          <span>{metric.title}</span>
          <strong>{metric.value}</strong>
          <small>{metric.note}</small>
        </div>
      ))}
    </div>

    <div className="mt-4 grid grid-cols-1 gap-3 xl:grid-cols-3">
      <div className="executive-note">
        <strong>Heatmap operacional</strong>
        <span>camadas térmicas reativas por criticidade e pressão de malha</span>
      </div>
      <div className="executive-note">
        <strong>Clusters de intervenção</strong>
        <span>DBSCAN consolidando ordens para elevar ROI logístico</span>
      </div>
      <div className="executive-note">
        <strong>Compliance Mirror</strong>
        <span>dossiês digitais exportáveis para trilha regulatória</span>
      </div>
    </div>
  </section>
))

ExecutiveOverview.displayName = 'ExecutiveOverview'
