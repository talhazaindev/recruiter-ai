import { Link, NavLink, Outlet, useNavigate, useParams, useLocation } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { api } from '../api/client'
import { StepRail, Tag } from './ui'

const PIPELINE = [
  { key: 'overview', label: 'Overview' },
  { key: 'jd', label: 'JD' },
  { key: 'ingest', label: 'Ingest' },
  { key: 'results', label: 'Results' },
  { key: 'shortlist', label: 'Shortlist' },
  { key: 'review', label: 'Review' },
]

export function AppShell() {
  const navigate = useNavigate()
  const location = useLocation()
  const { jobId } = useParams()
  const me = useQuery({ queryKey: ['me'], queryFn: api.me })
  const job = useQuery({
    queryKey: ['job', jobId],
    queryFn: () => api.getJob(jobId!),
    enabled: Boolean(jobId),
  })

  function logout() {
    localStorage.removeItem('access_token')
    navigate('/login')
  }

  const pathSegment = location.pathname.split('/').pop() || 'overview'
  const currentStep = PIPELINE.some((p) => p.key === pathSegment) ? pathSegment : 'overview'

  return (
    <div className="min-h-screen flex flex-col">
      <a href="#main" className="skip-link">
        Skip to content
      </a>
      <header className="border-b border-[var(--line)] bg-white/70 backdrop-blur-md sticky top-0 z-40">
        <div className="mx-auto max-w-[1440px] px-4 py-3 flex items-center gap-4 justify-between">
          <div className="flex items-center gap-6 min-w-0">
            <Link to="/" className="font-[family-name:var(--font-display)] text-lg font-semibold tracking-tight">
              Recruiter<span className="text-[var(--signal)]">AI</span>
            </Link>
            <Link to="/" className="text-sm text-[var(--ink-muted)] hover:text-[var(--ink)]">
              Jobs
            </Link>
            {jobId && job.data ? (
              <div className="hidden md:block min-w-0">
                <StepRail steps={PIPELINE} current={currentStep} />
              </div>
            ) : null}
          </div>
          <div className="flex items-center gap-3 text-sm">
            <span className="hidden sm:inline text-[var(--ink-muted)]">{me.data?.email}</span>
            <button
              type="button"
              onClick={logout}
              className="text-[var(--ink-muted)] hover:text-[var(--ink)]"
            >
              Sign out
            </button>
          </div>
        </div>
      </header>

      <div className="mx-auto max-w-[1440px] w-full flex-1 flex gap-0 md:gap-6 px-4 py-6">
        {jobId ? (
          <aside className="hidden md:block w-52 shrink-0">
            <div className="sticky top-20 space-y-1">
              <p className="text-xs uppercase tracking-wide text-[var(--ink-muted)] mb-3 px-2">
                {job.data?.jd.job_title || 'Job'}
              </p>
              {PIPELINE.map((item) => {
                const to = item.key === 'overview' ? `/jobs/${jobId}` : `/jobs/${jobId}/${item.key}`
                return (
                  <NavLink
                    key={item.key}
                    to={to}
                    end={item.key === 'overview'}
                    className={({ isActive }) =>
                      `block rounded-lg px-3 py-2 text-sm ${
                        isActive
                          ? 'bg-[var(--signal-soft)] text-[var(--signal-strong)] font-medium'
                          : 'text-[var(--ink-muted)] hover:bg-white/60 hover:text-[var(--ink)]'
                      }`
                    }
                  >
                    {item.label}
                  </NavLink>
                )
              })}
              {job.data ? (
                <div className="pt-4 px-2 space-y-2">
                  <Tag tone="signal">{job.data.status}</Tag>
                  <p className="text-xs text-[var(--ink-muted)]">
                    {job.data.candidate_count} candidates · {job.data.shortlisted_count} shortlisted ·{' '}
                    {job.data.needs_review_count} review
                  </p>
                </div>
              ) : null}
            </div>
          </aside>
        ) : null}

        <main id="main" className="flex-1 min-w-0">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
