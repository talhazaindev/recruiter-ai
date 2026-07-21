import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { api } from '../api/client'
import { JdStaleBanner } from '../components/JdStaleBanner'
import { Button, EmptyState, Panel, Tag } from '../components/ui'
import { numeric, pageRange, resultStatus } from '../utils/resultSafety'

const VIEWS = [
  { key: 'best_fit', label: 'Best fit' },
  { key: 'all', label: 'All' },
  { key: 'shortlisted', label: 'Shortlisted' },
  { key: 'needs_review', label: 'Needs review' },
  { key: 'failed_filters', label: 'Failed filters' },
] as const
const PAGE_SIZE = 50

export function ResultsPage() {
  const { jobId } = useParams()
  const qc = useQueryClient()
  const [view, setView] = useState<(typeof VIEWS)[number]['key']>('best_fit')
  const [offset, setOffset] = useState(0)

  const results = useQuery({
    queryKey: ['results', jobId, view, offset],
    queryFn: () => api.listResults(jobId!, view, PAGE_SIZE, offset),
    enabled: Boolean(jobId),
    refetchInterval: 3000,
  })

  const job = useQuery({
    queryKey: ['job', jobId],
    queryFn: () => api.getJob(jobId!),
    enabled: Boolean(jobId),
    refetchInterval: 3000,
  })

  const counts = useQuery({
    queryKey: ['result-counts', jobId],
    queryFn: async () => {
      const [all, best_fit, shortlisted, needs_review, failed_filters] = await Promise.all([
        api.listResults(jobId!, 'all'),
        api.listResults(jobId!, 'best_fit'),
        api.listResults(jobId!, 'shortlisted'),
        api.listResults(jobId!, 'needs_review'),
        api.listResults(jobId!, 'failed_filters'),
      ])
      return {
        all: all.total,
        best_fit: best_fit.total,
        shortlisted: shortlisted.total,
        needs_review: needs_review.total,
        failed_filters: failed_filters.total,
      }
    },
    enabled: Boolean(jobId),
  })

  const shortlist = useMutation({
    mutationFn: ({ id, value }: { id: string; value: boolean }) => api.shortlist(id, value),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['results', jobId] })
      qc.invalidateQueries({ queryKey: ['result-counts', jobId] })
      qc.invalidateQueries({ queryKey: ['shortlist', jobId] })
      qc.invalidateQueries({ queryKey: ['job', jobId] })
    },
  })
  const invalidateCandidateLists = () => {
    qc.invalidateQueries({ queryKey: ['results', jobId] })
    qc.invalidateQueries({ queryKey: ['result-counts', jobId] })
    qc.invalidateQueries({ queryKey: ['shortlist', jobId] })
    qc.invalidateQueries({ queryKey: ['review', jobId] })
    qc.invalidateQueries({ queryKey: ['job', jobId] })
  }
  const removeCv = useMutation({
    mutationFn: (resumeId: string) => api.deleteResume(resumeId),
    onSuccess: invalidateCandidateLists,
  })
  const removeCandidate = useMutation({
    mutationFn: (candidateId: string) => api.deleteCandidate(jobId!, candidateId),
    onSuccess: invalidateCandidateLists,
  })

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="font-[family-name:var(--font-display)] text-3xl font-semibold">Candidate results</h1>
          <p className="text-[var(--ink-muted)] mt-1">
            Review candidate experience, qualifications, and assessment status.
          </p>
        </div>
      </div>

      {job.data ? (
        <JdStaleBanner
          jobId={jobId!}
          staleMatchCount={job.data.stale_match_count}
          rematchInProgress={job.data.rematch_in_progress}
          activeRematchBatchId={job.data.active_rematch_batch_id}
        />
      ) : null}

      <div className="sticky top-16 z-20 flex flex-wrap gap-2 bg-[var(--bg)]/90 backdrop-blur py-2">
        {VIEWS.map((v) => (
          <button
            key={v.key}
            type="button"
            onClick={() => {
              setView(v.key)
              setOffset(0)
            }}
            className={`rounded-full px-3 py-1.5 text-xs font-medium ${
              view === v.key ? 'bg-[var(--signal)] text-white' : 'bg-white/80 border border-[var(--line)]'
            }`}
          >
            {v.label}
            {counts.data ? ` (${counts.data[v.key]})` : ''}
          </button>
        ))}
      </div>

      {results.isLoading ? <p className="text-[var(--ink-muted)]">Loading rankings…</p> : null}
      {results.isError ? (
        <p className="text-[var(--danger)]">
          {results.error instanceof Error ? results.error.message : 'Unable to load candidate results.'}
        </p>
      ) : null}
      {removeCv.isError || removeCandidate.isError ? (
        <p className="text-[var(--danger)]" role="alert">
          {(removeCv.error instanceof Error && removeCv.error.message) ||
            (removeCandidate.error instanceof Error && removeCandidate.error.message) ||
            'Unable to delete this record.'}
        </p>
      ) : null}
      {!results.isLoading && !results.isError && (results.data?.items.length ?? 0) === 0 ? (
        <EmptyState
          title="No candidates in this view"
          description="Ingest CVs first, or switch tabs. Best fit only shows must-have passers — try All or Failed filters."
          action={
            <Link to={`/jobs/${jobId}/ingest`}>
              <Button>Go to ingest</Button>
            </Link>
          }
        />
      ) : (
        <Panel className="overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-white/70 text-left text-[var(--ink-muted)]">
                <tr>
                  <th className="px-3 py-3 font-medium">Candidate Name</th>
                  <th className="px-3 py-3 font-medium">Score</th>
                  <th className="px-3 py-3 font-medium">Relevant Experience</th>
                  <th className="px-3 py-3 font-medium">Total Experience</th>
                  <th className="px-3 py-3 font-medium">No of Relevant Projects + Certificates</th>
                  <th className="px-3 py-3 font-medium">Status</th>
                  <th className="px-3 py-3 font-medium">Comment</th>
                  <th className="px-3 py-3 font-medium">Action</th>
                </tr>
              </thead>
              <tbody>
                {results.data?.items.map((row, i) => (
                  <motion.tr
                    key={row.id}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: Math.min(i * 0.02, 0.25) }}
                    className="border-t border-[var(--line)] hover:bg-white/60"
                  >
                    <td className="px-3 py-3">
                      <span className="font-medium">{row.candidate.name || 'Unknown'}</span>
                      <p className="text-xs text-[var(--ink-muted)]">{row.candidate.emails[0]}</p>
                      {row.stale ? <Tag tone="warn">Outdated</Tag> : null}
                    </td>
                    <td className="px-3 py-3 font-medium tabular-nums">{Math.round(row.score)}</td>
                    <td className="px-3 py-3 tabular-nums whitespace-nowrap">
                      {numeric(row.rank_signals.relevant_work_years) != null
                        ? `${numeric(row.rank_signals.relevant_work_years)!.toFixed(2)} years`
                        : '—'}
                    </td>
                    <td className="px-3 py-3 tabular-nums whitespace-nowrap">
                      {numeric(row.rank_signals.total_experience_years) != null
                        ? `${numeric(row.rank_signals.total_experience_years)!.toFixed(2)} years`
                        : '—'}
                    </td>
                    <td className="px-3 py-3 text-center tabular-nums">
                      {row.rank_signals.projects_certificates_count ?? '—'}
                    </td>
                    <td className="px-3 py-3">
                      <Tag tone={row.hard_filters?.unknown ? 'warn' : row.hard_filters?.passed ? 'ok' : 'danger'}>
                        {resultStatus(row.hard_filters)}
                      </Tag>
                    </td>
                    <td className="px-3 py-3 max-w-[220px]">
                      <span className="text-[var(--ink-muted)]">
                        {row.rank_signals.comment || String(row.explanation?.summary || '—')}
                      </span>
                    </td>
                    <td className="px-3 py-3">
                      <div className="flex flex-wrap gap-1">
                        <Button
                          size="sm"
                          variant={row.shortlisted ? 'secondary' : 'primary'}
                          onClick={() => shortlist.mutate({ id: row.id, value: !row.shortlisted })}
                        >
                          {row.shortlisted ? 'Shortlisted' : 'Shortlist'}
                        </Button>
                        <Link to={`/jobs/${jobId}/candidates/${row.id}`}>
                          <Button size="sm" variant="ghost">View Details</Button>
                        </Link>
                        <Button
                          size="sm"
                          variant="danger"
                          disabled={removeCv.isPending || removeCandidate.isPending}
                          onClick={() => {
                            if (window.confirm(`Delete the CV for ${row.candidate.name || 'this candidate'}?`)) {
                              removeCv.mutate(row.resume_id)
                            }
                          }}
                        >
                          Delete CV
                        </Button>
                        <Button
                          size="sm"
                          variant="danger"
                          disabled={removeCv.isPending || removeCandidate.isPending}
                          onClick={() => {
                            if (
                              window.confirm(
                                `Delete ${row.candidate.name || 'this candidate'} and all of their CVs from this job?`,
                              )
                            ) {
                              removeCandidate.mutate(row.candidate_id)
                            }
                          }}
                        >
                          Delete candidate
                        </Button>
                      </div>
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
          {results.data && results.data.total > PAGE_SIZE ? (
            <div className="flex items-center justify-between border-t border-[var(--line)] p-3">
              <span className="text-xs text-[var(--ink-muted)]">
                {pageRange(results.data.total, offset, PAGE_SIZE)[0]}–
                {pageRange(results.data.total, offset, PAGE_SIZE)[1]} of {results.data.total}
              </span>
              <div className="flex gap-2">
                <Button
                  size="sm"
                  variant="ghost"
                  disabled={offset === 0}
                  onClick={() => setOffset((value) => Math.max(0, value - PAGE_SIZE))}
                >
                  Previous
                </Button>
                <Button
                  size="sm"
                  variant="ghost"
                  disabled={offset + PAGE_SIZE >= results.data.total}
                  onClick={() => setOffset((value) => value + PAGE_SIZE)}
                >
                  Next
                </Button>
              </div>
            </div>
          ) : null}
        </Panel>
      )}
    </div>
  )
}
