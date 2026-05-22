import { memo } from 'react'

interface SimulationControlProps {
  currentWeeks: number
  targetWeeks: number
  onChange: (value: number) => void
}

export const SimulationControl = memo<SimulationControlProps>(
  ({ currentWeeks, targetWeeks, onChange }) => (
    <section className="digital-twin-panel rounded-[24px] border border-cyan-400/10 bg-slate-950/70 p-5">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <p className="text-[11px] uppercase tracking-[0.24em] text-cyan-300/60">
            Simulador temporal
          </p>
          <h3 className="mt-1 text-lg font-semibold text-white">
            Simular próximas semanas
          </h3>
          <p className="mt-1 text-sm text-slate-400">
            O Digital Twin projeta degradação de EVI, recalcula IPO e reorganiza
            os clusters em tempo real.
          </p>
        </div>
        <div className="digital-twin-panel__counter">
          {currentWeeks.toFixed(1)} sem
        </div>
      </div>

      <div className="mt-5 grid grid-cols-1 gap-3 xl:grid-cols-[minmax(0,1fr)_220px] xl:items-center">
        <input
          type="range"
          min={0}
          max={12}
          step={1}
          value={targetWeeks}
          onChange={(event) => onChange(Number(event.target.value))}
          className="digital-twin-slider"
        />
        <div className="flex justify-between text-[11px] uppercase tracking-[0.2em] text-slate-500">
          <span>Agora</span>
          <span>12 semanas</span>
        </div>
      </div>
    </section>
  ),
)

SimulationControl.displayName = 'SimulationControl'
