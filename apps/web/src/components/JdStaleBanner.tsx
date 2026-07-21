import { useEffect, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api } from '../api/client'
import { Button, LiveRegion, Panel, Tag } from './ui'

type JdStaleBannerProps = {
  jobId: string
  staleMatchCount: number
  rematchInProgress: boolean
  activeRematchBatchId: string | null
}

export function JdStaleBanner({
  jobId,
  staleMatchCount,
  rematchInProgress,
  activeRematchBatchId,
}: JdStaleBannerProps) {
  const qc = useQueryClient()
  const [batchId, setBatchId] = useState<string | null>(activeRematchBatchId)
  const [error, setError] = useState('')

  useEffect(() => {
    if (activeRematchBatchId) setBatchId(activeRematchBatchId)
  }, [activeRematchBatchId])

  const batch = useQuery({
    queryKey: ['batch', batchId],
    queryFn: () => api.getBatch(batchId!),
    enabled: Boolean(batchId),
    refetchInterval: (query) => {
      const status = query.state.data?.status
      return status === 'completed' || status === 'completed_with_errors' || status === 'failed'
        ? false
        : 1500
    },
  })

  useEffect(() => {
    const status = batch.data?.status
    if (!jobId || !['completed', 'completed_with_errors', 'failed'].includes(status || '')) return
    qc.invalidateQueries({ queryKey: ['job', jobId] })
    qc.invalidateQueries({ queryKey: ['results', jobId] })
    qc.invalidateQueries({ queryKey: ['result-counts', jobId] })
    qc.invalidateQueries({ queryKey: ['shortlist', jobId] })
    qc.invalidateQueries({ queryKey: ['review-queue', jobId] })
    qc.invalidateQueries({ queryKey: ['jobs'] })
  }, [batch.data?.status, jobId, qc])

  const rematch = useMutation({
    mutationFn: () => api.rematchJob(jobId),
    onSuccess: (res) => {
      setError('')
      setBatchId(res.batch_id)
      qc.invalidateQueries({ queryKey: ['job', jobId] })
    },
    onError: (err) => {
      setError(err instanceof Error ? err.message : 'Rematch failed')
    },
  })

  const batchRunning =
    Boolean(batchId) &&
    (!batch.data || batch.data.status === 'processing' || batch.data.status === 'queued')
  const showBanner = staleMatchCount > 0 || rematchInProgress || rematch.isPending || batchRunning
  if (!showBanner) return null

  const counters = batch.data?.counters || {}
  const total = counters.total || 0
  const matched = counters.matched || 0
  const matching = counters.matching || 0
  const running = rematchInProgress || rematch.isPending || matching > 0 || batch.data?.status === 'processing'

  return (
    <Panel className="p-4 border-amber-200 bg-amber-50/80">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <Tag tone="warn">JD changed</Tag>
            {running ? <Tag tone="signal">Rematching</Tag> : null}
          </div>
          <p className="text-sm text-amber-950">
            This job description has changed. Existing candidate scores may be outdated. Rerun the
            matching pipeline for the best fit.
          </p>
          {staleMatchCount > 0 ? (
            <p className="text-xs text-amber-900/80">
              {staleMatchCount} candidate{staleMatchCount === 1 ? '' : 's'} need rematching.
            </p>
          ) : null}
          {batchId && batch.data ? (
            <LiveRegion>
              Rematch progress: matched {matched} of {total}
              {matching > 0 ? `, ${matching} in progress` : ''}
            </LiveRegion>
          ) : null}
          {error ? (
            <p className="text-sm text-[var(--danger)]" role="alert">
              {error}
            </p>
          ) : null}
        </div>
        <Button
          onClick={() => rematch.mutate()}
          disabled={running || staleMatchCount <= 0}
        >
          {running ? 'Rematching…' : 'Rerun matching pipeline'}
        </Button>
      </div>
    </Panel>
  )
}
