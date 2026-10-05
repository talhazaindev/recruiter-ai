import type { ButtonHTMLAttributes, InputHTMLAttributes, ReactNode, TextareaHTMLAttributes } from 'react'

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  size?: 'sm' | 'md'
}

export function Button({
  variant = 'primary',
  size = 'md',
  className = '',
  children,
  ...props
}: ButtonProps) {
  const base =
    'inline-flex items-center justify-center gap-2 rounded-[10px] font-medium transition disabled:opacity-50 disabled:cursor-not-allowed'
  const sizes = size === 'sm' ? 'px-3 py-1.5 text-sm' : 'px-4 py-2.5 text-sm'
  const variants = {
    primary: 'bg-[var(--signal)] text-white hover:bg-[var(--signal-strong)]',
    secondary: 'bg-white/80 text-[var(--ink)] border border-[var(--line)] hover:bg-white',
    ghost: 'bg-transparent text-[var(--ink-muted)] hover:bg-white/50 hover:text-[var(--ink)]',
    danger: 'bg-[var(--danger)] text-white hover:opacity-90',
  }
  return (
    <button className={`${base} ${sizes} ${variants[variant]} ${className}`} {...props}>
      {children}
    </button>
  )
}

export function Input(props: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <input
      {...props}
      className={`w-full rounded-[10px] border border-[var(--line)] bg-white/90 px-3 py-2.5 text-[var(--ink)] placeholder:text-[var(--ink-muted)] ${props.className || ''}`}
    />
  )
}

export function TextArea(props: TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <textarea
      {...props}
      className={`w-full rounded-[10px] border border-[var(--line)] bg-white/90 px-3 py-2.5 text-[var(--ink)] placeholder:text-[var(--ink-muted)] min-h-[110px] ${props.className || ''}`}
    />
  )
}

export function Tag({
  children,
  tone = 'neutral',
}: {
  children: ReactNode
  tone?: 'neutral' | 'signal' | 'ok' | 'warn' | 'danger'
}) {
  const tones = {
    neutral: 'bg-slate-100 text-slate-700',
    signal: 'bg-[var(--signal-soft)] text-[var(--signal-strong)]',
    ok: 'bg-emerald-50 text-emerald-800',
    warn: 'bg-amber-50 text-amber-800',
    danger: 'bg-red-50 text-red-700',
  }
  return (
    <span className={`inline-flex items-center rounded-md px-2 py-0.5 text-xs font-medium ${tones[tone]}`}>
      {children}
    </span>
  )
}

export function ScoreMeter({ score }: { score: number }) {
  const clamped = Math.max(0, Math.min(100, score))
  return (
    <div className="flex items-center gap-2 min-w-[110px]" aria-label={`Match score ${clamped}`}>
      <div className="h-2 flex-1 rounded-full bg-slate-200 overflow-hidden">
        <div
          className="h-full rounded-full bg-[var(--signal)] transition-[width] duration-500"
          style={{ width: `${clamped}%` }}
        />
      </div>
      <span className="text-sm font-semibold tabular-nums w-8 text-right">{Math.round(clamped)}</span>
    </div>
  )
}

export function EmptyState({
  title,
  description,
  action,
}: {
  title: string
  description: string
  action?: ReactNode
}) {
  return (
    <div className="rounded-[var(--radius)] border border-dashed border-[var(--line)] bg-white/50 px-8 py-14 text-center">
      <h3 className="font-[family-name:var(--font-display)] text-xl font-semibold">{title}</h3>
      <p className="mt-2 text-[var(--ink-muted)] max-w-md mx-auto">{description}</p>
      {action ? <div className="mt-6 flex justify-center">{action}</div> : null}
    </div>
  )
}

export function LiveRegion({ children }: { children: ReactNode }) {
  return (
    <div role="status" aria-live="polite" aria-atomic="true" className="sr-only">
      {children}
    </div>
  )
}

export function Panel({ children, className = '' }: { children: ReactNode; className?: string }) {
  return (
    <div
      className={`rounded-[var(--radius)] border border-[var(--line)] bg-[var(--surface)] backdrop-blur-md shadow-[var(--shadow)] ${className}`}
    >
      {children}
    </div>
  )
}

export function Drawer({
  open,
  onClose,
  title,
  children,
}: {
  open: boolean
  onClose: () => void
  title: string
  children: ReactNode
}) {
  if (!open) return null
  return (
    <div className="fixed inset-0 z-50 flex justify-end" role="dialog" aria-modal="true" aria-label={title}>
      <button className="absolute inset-0 bg-slate-900/30" aria-label="Close drawer" onClick={onClose} />
      <div className="relative h-full w-full max-w-lg overflow-y-auto bg-white shadow-2xl border-l border-[var(--line)] p-6">
        <div className="flex items-start justify-between gap-4 mb-4">
          <h2 className="font-[family-name:var(--font-display)] text-xl font-semibold">{title}</h2>
          <Button variant="ghost" size="sm" onClick={onClose}>
            Close
          </Button>
        </div>
        {children}
      </div>
    </div>
  )
}

export function StepRail({
  steps,
  current,
}: {
  steps: { key: string; label: string }[]
  current: string
}) {
  const idx = steps.findIndex((s) => s.key === current)
  return (
    <nav aria-label="Job pipeline" className="flex items-center gap-1 overflow-x-auto">
      {steps.map((step, i) => {
        const active = step.key === current
        const done = i < idx
        return (
          <div key={step.key} className="flex items-center gap-1">
            <span
              className={`rounded-full px-3 py-1 text-xs font-medium whitespace-nowrap ${
                active
                  ? 'bg-[var(--signal)] text-white'
                  : done
                    ? 'bg-[var(--signal-soft)] text-[var(--signal-strong)]'
                    : 'bg-white/70 text-[var(--ink-muted)] border border-[var(--line)]'
              }`}
            >
              {step.label}
            </span>
            {i < steps.length - 1 ? <span className="text-[var(--ink-muted)] text-xs px-1">→</span> : null}
          </div>
        )
      })}
    </nav>
  )
}

export function ProgressRing({ value, total }: { value: number; total: number }) {
  const pct = total > 0 ? Math.min(100, Math.round((value / total) * 100)) : 0
  const r = 28
  const c = 2 * Math.PI * r
  const offset = c - (pct / 100) * c
  return (
    <div className="relative inline-flex items-center justify-center" aria-label={`Progress ${pct}%`}>
      <svg width="72" height="72" viewBox="0 0 72 72" className="-rotate-90">
        <circle cx="36" cy="36" r={r} fill="none" stroke="#e2e8f0" strokeWidth="6" />
        <circle
          cx="36"
          cy="36"
          r={r}
          fill="none"
          stroke="var(--signal)"
          strokeWidth="6"
          strokeDasharray={c}
          strokeDashoffset={offset}
          strokeLinecap="round"
          className="transition-[stroke-dashoffset] duration-500"
        />
      </svg>
      <span className="absolute text-sm font-semibold tabular-nums">{pct}%</span>
    </div>
  )
}
