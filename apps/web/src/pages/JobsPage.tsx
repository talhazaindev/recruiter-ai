import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { api, emptyJd } from '../api/client'
import { Button, EmptyState, Panel, Tag } from '../components/ui'

export function JobsPage() {
  const navigate = useNavigate()
  const qc = useQueryClient()
  const jobs = useQuery({ queryKey: ['jobs'], queryFn: api.listJobs })
  const create = useMutation({
    mutationFn: () => api.createJob({ ...emptyJd(), job_title: 'Untitled role' }, 'draft'),
    onSuccess: (job) => {
      qc.invalidateQueries({ queryKey: ['jobs'] })
      navigate(`/jobs/${job.id}/jd`)
    },
  })
  const remove = useMutation({
    mutationFn: (jobId: string) => api.deleteJob(jobId),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['jobs'] })
    },
  })

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="font-[family-name:var(--font-display)] text-3xl font-semibold tracking-tight">
            Jobs command center
          </h1>
          <p className="mt-1 text-[var(--ink-muted)]">
            Create a JD, ingest CVs, rank fits, shortlist, and review low-confidence parses.
          </p>
        </div>
        <Button onClick={() => create.mutate()} disabled={create.isPending}>
          {create.isPending ? 'Creating…' : 'New job'}
        </Button>
      </div>

      {jobs.isLoading ? <p className="text-[var(--ink-muted)]">Loading jobs…</p> : null}
      {jobs.isError ? (
        <p className="text-[var(--danger)]" role="alert">
          {(jobs.error as Error).message}. Is the API running on port 8000?
        </p>
      ) : null}
      {remove.isError ? (
        <p className="text-[var(--danger)]" role="alert">
          {remove.error instanceof Error ? remove.error.message : 'Unable to delete the job description.'}
        </p>
      ) : null}

      {!jobs.isLoading && (jobs.data?.length ?? 0) === 0 ? (
        <EmptyState
          title="Create your first JD"
          description="Start with a structured job description, then upload CVs or connect a Drive folder."
          action={<Button onClick={() => create.mutate()}>New job</Button>}
        />
      ) : (
        <div className="space-y-3">
          {jobs.data?.map((job, i) => (
            <motion.div
              key={job.id}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: Math.min(i * 0.04, 0.3) }}
            >
              <Panel className="p-4 hover:bg-white/90 transition">
                <div className="flex flex-wrap items-center justify-between gap-3">
                  <Link to={`/jobs/${job.id}`} className="min-w-0 flex-1">
                    <div>
                      <h2 className="font-[family-name:var(--font-display)] text-lg font-semibold">
                        {job.jd.job_title || 'Untitled role'}
                      </h2>
                      <p className="text-sm text-[var(--ink-muted)] mt-0.5 line-clamp-1">
                        {job.jd.job_summary || 'No summary yet'}
                      </p>
                    </div>
                  </Link>
                  <div className="flex items-center gap-2">
                    <div className="flex items-center gap-2">
                      <Tag tone="signal">{job.status}</Tag>
                      <span className="text-xs text-[var(--ink-muted)]">
                        {job.candidate_count} cand · {job.shortlisted_count} short · {job.needs_review_count}{' '}
                        review
                      </span>
                    </div>
                    <Button
                      size="sm"
                      variant="danger"
                      disabled={remove.isPending}
                      onClick={() => {
                        const title = job.jd.job_title || 'Untitled role'
                        if (window.confirm(`Delete "${title}" and all of its CVs and candidates? This cannot be undone.`)) {
                          remove.mutate(job.id)
                        }
                      }}
                    >
                      Delete JD
                    </Button>
                  </div>
                </div>
              </Panel>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  )
}
