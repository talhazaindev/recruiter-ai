import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'
import { useParams, Link } from 'react-router-dom'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { api } from '../api/client'
import { Button, Input, LiveRegion, Panel, ProgressRing, Tag } from '../components/ui'

export function IngestPage() {
  const { jobId } = useParams()
  const queryClient = useQueryClient()
  const [files, setFiles] = useState<File[]>([])
  const [folderUrl, setFolderUrl] = useState('')
  const [batchId, setBatchId] = useState<string | null>(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)

  const drive = useQuery({ queryKey: ['drive-status'], queryFn: api.driveStatus })
  const batch = useQuery({
    queryKey: ['batch', batchId],
    queryFn: () => api.getBatch(batchId!),
    enabled: Boolean(batchId),
    refetchInterval: (q) => {
      const status = q.state.data?.status
      return status === 'completed' || status === 'completed_with_errors' || status === 'failed'
        ? false
        : 1500
    },
  })

  useEffect(() => {
    const stored = sessionStorage.getItem(`batch:${jobId}`)
    if (stored) setBatchId(stored)
  }, [jobId])

  useEffect(() => {
    const status = batch.data?.status
    if (!jobId || !['completed', 'completed_with_errors', 'failed'].includes(status || '')) return
    queryClient.invalidateQueries({ queryKey: ['results', jobId] })
    queryClient.invalidateQueries({ queryKey: ['result-counts', jobId] })
    queryClient.invalidateQueries({ queryKey: ['job', jobId] })
    queryClient.invalidateQueries({ queryKey: ['jobs'] })
  }, [batch.data?.status, jobId, queryClient])

  async function onUpload(e: FormEvent) {
    e.preventDefault()
    if (!jobId || files.length === 0) return
    setBusy(true)
    setError('')
    try {
      const res = await api.uploadCvs(jobId, files)
      setBatchId(res.batch_id)
      sessionStorage.setItem(`batch:${jobId}`, res.batch_id)
      setFiles([])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed')
    } finally {
      setBusy(false)
    }
  }

  async function onDrive(e: FormEvent) {
    e.preventDefault()
    if (!jobId || !folderUrl.trim()) return
    setBusy(true)
    setError('')
    try {
      const res = await api.ingestDrive(jobId, folderUrl.trim())
      setBatchId(res.batch_id)
      sessionStorage.setItem(`batch:${jobId}`, res.batch_id)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Drive ingest failed')
    } finally {
      setBusy(false)
    }
  }

  async function connectDrive() {
    try {
      const { url } = await api.driveAuthUrl()
      window.location.href = url
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Drive not configured')
    }
  }

  const c = batch.data?.counters || {}
  const total = c.total || 0
  const done = (c.matched || 0) + (c.failed || 0)
  const stages = [
    { label: 'Queued', active: batch.data?.status === 'queued' },
    { label: 'Parsing', active: (c.parsing || 0) > 0 || ((c.parsed || 0) < total && total > 0) },
    { label: 'Matching', active: (c.matching || 0) > 0 },
    {
      label: 'Done',
      active:
        batch.data?.status === 'completed' ||
        batch.data?.status === 'completed_with_errors' ||
        batch.data?.status === 'failed',
    },
  ]

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h1 className="font-[family-name:var(--font-display)] text-3xl font-semibold">Ingest theater</h1>
        <p className="text-[var(--ink-muted)] mt-1">
          Upload PDFs/DOCX or pull a Google Drive folder into the parse → match pipeline.
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-4">
        <Panel className="p-5">
          <h2 className="font-semibold mb-3">Upload CVs</h2>
          <form onSubmit={onUpload} className="space-y-3">
            <label className="block rounded-[var(--radius)] border border-dashed border-[var(--line)] bg-white/60 px-4 py-8 text-center cursor-pointer hover:bg-white/90">
              <input
                type="file"
                multiple
                accept=".pdf,.docx,.doc"
                className="sr-only"
                onChange={(e) => setFiles(Array.from(e.target.files || []))}
              />
              <p className="text-sm font-medium">Drop or browse files</p>
              <p className="text-xs text-[var(--ink-muted)] mt-1">PDF / DOCX · max 15MB each</p>
              {files.length > 0 ? (
                <p className="text-sm text-[var(--signal-strong)] mt-3">{files.length} file(s) selected</p>
              ) : null}
            </label>
            <Button type="submit" disabled={busy || files.length === 0}>
              Start upload pipeline
            </Button>
          </form>
        </Panel>

        <Panel className="p-5">
          <h2 className="font-semibold mb-3">Google Drive folder</h2>
          <div className="mb-3 flex items-center gap-2 text-xs">
            <Tag tone={drive.data?.connected ? 'ok' : 'warn'}>
              {drive.data?.connected ? 'Connected' : 'Not connected'}
            </Tag>
            {!drive.data?.connected ? (
              <Button variant="ghost" size="sm" type="button" onClick={connectDrive}>
                Connect Drive
              </Button>
            ) : null}
          </div>
          <form onSubmit={onDrive} className="space-y-3">
            <label className="block text-sm">
              <span className="text-[var(--ink-muted)]">Folder URL or ID</span>
              <Input
                className="mt-1"
                value={folderUrl}
                onChange={(e) => setFolderUrl(e.target.value)}
                placeholder="https://drive.google.com/drive/folders/..."
              />
            </label>
            <Button type="submit" variant="secondary" disabled={busy || !folderUrl.trim()}>
              Ingest from Drive
            </Button>
          </form>
        </Panel>
      </div>

      {error ? (
        <p className="text-[var(--danger)]" role="alert">
          {error}
        </p>
      ) : null}

      {batchId && batch.data ? (
        <Panel className="p-5">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <h2 className="font-semibold">Pipeline progress</h2>
              <p className="text-sm text-[var(--ink-muted)] mt-1">
                Batch {batch.data.id.slice(-8)} · {batch.data.status} · source {batch.data.source}
              </p>
              <LiveRegion>
                Parsed {c.parsed || 0} of {total}, matched {c.matched || 0}
              </LiveRegion>
            </div>
            <ProgressRing value={Math.max(c.matched || 0, c.parsed || 0)} total={total || 1} />
          </div>

          <div className="mt-5 flex flex-wrap gap-2">
            {stages.map((s) => (
              <Tag key={s.label} tone={s.active ? 'signal' : 'neutral'}>
                {s.label}
              </Tag>
            ))}
          </div>

          <dl className="mt-5 grid grid-cols-2 sm:grid-cols-4 gap-3 text-sm">
            <div>
              <dt className="text-[var(--ink-muted)]">Total</dt>
              <dd className="font-semibold tabular-nums">{total}</dd>
            </div>
            <div>
              <dt className="text-[var(--ink-muted)]">Parsed</dt>
              <dd className="font-semibold tabular-nums">{c.parsed || 0}</dd>
            </div>
            <div>
              <dt className="text-[var(--ink-muted)]">Matched</dt>
              <dd className="font-semibold tabular-nums">{c.matched || 0}</dd>
            </div>
            <div>
              <dt className="text-[var(--ink-muted)]">Needs review</dt>
              <dd className="font-semibold tabular-nums">{c.needs_review || 0}</dd>
            </div>
          </dl>

          {(batch.data as { last_error?: string }).last_error ? (
            <p className="mt-4 text-sm text-[var(--danger)]">{(batch.data as { last_error?: string }).last_error}</p>
          ) : null}

          {(c.matched || 0) > 0 || done > 0 ? (
            <div className="mt-5">
              <Link to={`/jobs/${jobId}/results`}>
                <Button>View results</Button>
              </Link>
            </div>
          ) : null}
        </Panel>
      ) : null}
    </div>
  )
}
