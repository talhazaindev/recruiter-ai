import { useQuery } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { api } from '../api/client'
import { Button, Panel, Tag } from '../components/ui'

export function JobOverviewPage() {
  const { jobId } = useParams()
  const job = useQuery({ queryKey: ['job', jobId], queryFn: () => api.getJob(jobId!), enabled: Boolean(jobId) })

  if (job.isLoading) return <p className="text-[var(--ink-muted)]">Loading…</p>
  if (!job.data) return <p className="text-[var(--danger)]">Job not found</p>

  const j = job.data
  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <div className="flex items-center gap-2 mb-2">
          <Tag tone="signal">{j.status}</Tag>
        </div>
        <h1 className="font-[family-name:var(--font-display)] text-3xl font-semibold">
          {j.jd.job_title || 'Untitled role'}
        </h1>
        <p className="mt-2 text-[var(--ink-muted)]">{j.jd.job_summary || 'Add a job summary in the JD editor.'}</p>
      </div>

      <div className="grid sm:grid-cols-3 gap-3">
        <Panel className="p-4">
          <p className="text-xs text-[var(--ink-muted)]">Candidates</p>
          <p className="text-2xl font-semibold tabular-nums">{j.candidate_count}</p>
        </Panel>
        <Panel className="p-4">
          <p className="text-xs text-[var(--ink-muted)]">Shortlisted</p>
          <p className="text-2xl font-semibold tabular-nums">{j.shortlisted_count}</p>
        </Panel>
        <Panel className="p-4">
          <p className="text-xs text-[var(--ink-muted)]">Needs review</p>
          <p className="text-2xl font-semibold tabular-nums">{j.needs_review_count}</p>
        </Panel>
      </div>

      <Panel className="p-5 space-y-3">
        <h2 className="font-semibold">Continue pipeline</h2>
        <div className="flex flex-wrap gap-2">
          <Link to={`/jobs/${jobId}/jd`}>
            <Button variant="secondary">Edit JD</Button>
          </Link>
          <Link to={`/jobs/${jobId}/ingest`}>
            <Button>Ingest CVs</Button>
          </Link>
          <Link to={`/jobs/${jobId}/results`}>
            <Button variant="ghost">Results</Button>
          </Link>
        </div>
      </Panel>

      {j.jd.requirements_must_have.skills.length > 0 ? (
        <Panel className="p-5">
          <h2 className="font-semibold mb-2">Must-have skills</h2>
          <div className="flex flex-wrap gap-2">
            {j.jd.requirements_must_have.skills.map((s) => (
              <Tag key={s} tone="signal">
                {s}
              </Tag>
            ))}
          </div>
        </Panel>
      ) : null}
    </div>
  )
}
