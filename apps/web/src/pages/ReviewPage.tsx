import { useEffect, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { api } from '../api/client'
import { Button, EmptyState, Panel, ScoreMeter, Tag } from '../components/ui'

export function ReviewPage() {
  const { jobId } = useParams()
  const qc = useQueryClient()
  const queue = useQuery({
    queryKey: ['review', jobId],
    queryFn: () => api.reviewQueue(jobId!),
    enabled: Boolean(jobId),
  })
  const [index, setIndex] = useState(0)

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return
      if (e.key === 'j' || e.key === 'J') setIndex((i) => Math.min(i + 1, (queue.data?.length || 1) - 1))
      if (e.key === 'k' || e.key === 'K') setIndex((i) => Math.max(i - 1, 0))
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [queue.data?.length])

  useEffect(() => {
    setIndex((current) => Math.max(0, Math.min(current, (queue.data?.length || 1) - 1)))
  }, [queue.data?.length])

  const review = useMutation({
    mutationFn: ({ id, status }: { id: string; status: string }) => api.updateReview(id, status),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['review', jobId] })
      qc.invalidateQueries({ queryKey: ['results', jobId] })
      qc.invalidateQueries({ queryKey: ['job', jobId] })
    },
  })

  const current = queue.data?.[index]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-[family-name:var(--font-display)] text-3xl font-semibold">Review queue</h1>
        <p className="text-[var(--ink-muted)] mt-1">
          Focus mode for low-confidence / partial parses. Keyboard: J next · K previous.
        </p>
      </div>

      {!queue.isLoading && (queue.data?.length ?? 0) === 0 ? (
        <EmptyState
          title="Review queue is clear"
          description="Nothing needs manual review right now."
          action={
            <Link to={`/jobs/${jobId}/results`}>
              <Button>Back to results</Button>
            </Link>
          }
        />
      ) : (
        <div className="grid lg:grid-cols-[240px_1fr] gap-4">
          <Panel className="p-2 max-h-[70vh] overflow-y-auto">
            {queue.data?.map((row, i) => (
              <button
                key={row.id}
                type="button"
                onClick={() => setIndex(i)}
                className={`w-full text-left rounded-lg px-3 py-2 text-sm mb-1 ${
                  i === index ? 'bg-[var(--signal-soft)]' : 'hover:bg-white/70'
                }`}
              >
                <span className="font-medium block truncate">{row.candidate.name}</span>
                <span className="text-xs text-[var(--ink-muted)]">{Math.round(row.score)}</span>
              </button>
            ))}
          </Panel>

          {current ? (
            <Panel className="p-6 space-y-4">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <h2 className="text-xl font-semibold">{current.candidate.name}</h2>
                  <p className="text-sm text-[var(--ink-muted)] mt-1">
                    {index + 1} of {queue.data?.length}
                  </p>
                </div>
                <ScoreMeter score={current.score} />
              </div>

              <div className="flex flex-wrap gap-2">
                <Tag tone="warn">Needs review</Tag>
                <Tag tone={current.hard_filters?.passed ? 'ok' : 'danger'}>
                  Filters {current.hard_filters?.passed ? 'passed' : 'failed'}
                </Tag>
                {current.parse?.confidence != null ? (
                  <Tag>Confidence {Math.round(current.parse.confidence * 100)}%</Tag>
                ) : null}
              </div>

              {(current.parse?.warnings || []).length > 0 ? (
                <div className="rounded-lg bg-amber-50 px-3 py-2 text-sm text-amber-900">
                  Warnings: {current.parse.warnings?.join('; ')}
                </div>
              ) : null}

              <div className="text-sm">
                <h3 className="font-semibold mb-1">Why ranked</h3>
                <p className="text-[var(--ink-muted)]">{String(current.explanation?.summary || '—')}</p>
              </div>

              <div className="flex flex-wrap gap-2 pt-2">
                <Button
                  onClick={() => review.mutate({ id: current.id, status: 'approved' })}
                  disabled={review.isPending}
                >
                  Approve
                </Button>
                <Button
                  variant="danger"
                  onClick={() => review.mutate({ id: current.id, status: 'rejected' })}
                  disabled={review.isPending}
                >
                  Reject
                </Button>
                <Button variant="ghost" onClick={() => setIndex((i) => Math.min(i + 1, (queue.data?.length || 1) - 1))}>
                  Skip
                </Button>
              </div>
            </Panel>
          ) : null}
        </div>
      )}
    </div>
  )
}
