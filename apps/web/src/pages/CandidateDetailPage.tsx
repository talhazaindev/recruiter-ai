import { useEffect, useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { api } from '../api/client'
import { Button, Panel, ScoreMeter, Tag } from '../components/ui'
import { numeric, resultStatus } from '../utils/resultSafety'

export function CandidateDetailPage() {
  const { jobId, resultId } = useParams()
  const navigate = useNavigate()
  const qc = useQueryClient()
  const [showPreview, setShowPreview] = useState(false)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [previewError, setPreviewError] = useState('')

  const detail = useQuery({
    queryKey: ['result', jobId, resultId],
    queryFn: () => api.getResult(jobId!, resultId!),
    enabled: Boolean(jobId && resultId),
  })

  const shortlist = useMutation({
    mutationFn: (value: boolean) => api.shortlist(resultId!, value),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['result', jobId, resultId] })
      qc.invalidateQueries({ queryKey: ['results', jobId] })
      qc.invalidateQueries({ queryKey: ['shortlist', jobId] })
    },
  })
  const afterDelete = () => {
    qc.invalidateQueries({ queryKey: ['results', jobId] })
    qc.invalidateQueries({ queryKey: ['result-counts', jobId] })
    qc.invalidateQueries({ queryKey: ['shortlist', jobId] })
    qc.invalidateQueries({ queryKey: ['review', jobId] })
    qc.invalidateQueries({ queryKey: ['job', jobId] })
    navigate(`/jobs/${jobId}/results`)
  }
  const removeCv = useMutation({
    mutationFn: (resumeId: string) => api.deleteResume(resumeId),
    onSuccess: afterDelete,
  })
  const removeCandidate = useMutation({
    mutationFn: (candidateId: string) => api.deleteCandidate(jobId!, candidateId),
    onSuccess: afterDelete,
  })

  useEffect(() => {
    let objectUrl: string | null = null
    let cancelled = false

    async function loadPreview() {
      if (!showPreview || !detail.data?.resume_id) return
      setPreviewError('')
      try {
        const blob = await api.fetchResumeBlob(detail.data.resume_id)
        if (cancelled) return
        objectUrl = URL.createObjectURL(blob)
        setPreviewUrl(objectUrl)
      } catch (err) {
        if (!cancelled) {
          setPreviewError(err instanceof Error ? err.message : 'Could not load CV')
          setPreviewUrl(null)
        }
      }
    }

    loadPreview()
    return () => {
      cancelled = true
      if (objectUrl) URL.revokeObjectURL(objectUrl)
    }
  }, [showPreview, detail.data?.resume_id])

  if (detail.isLoading) return <p className="text-[var(--ink-muted)]">Loading…</p>
  if (detail.isError) {
    return (
      <p className="text-[var(--danger)]">
        {detail.error instanceof Error ? detail.error.message : 'Unable to load this job result.'}
      </p>
    )
  }
  if (!detail.data) return <p className="text-[var(--danger)]">Not found</p>

  const row = detail.data
  const resume = row.resume as
    | {
        skills?: string[]
        experience?: {
          company: string
          designation: string
          start_date: string
          end_date: string
          description: string
        }[]
        education?: { degree: string; institution: string; cgpa: string; graduation_date: string }[]
        professional_summary?: string
        projects?: string[]
        certifications?: string[]
      }
    | undefined

  const filename = row.source_ref?.original_filename || 'resume.pdf'
  const isPdf = filename.toLowerCase().endsWith('.pdf')
  const assessment = row.explanation.details

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <Link to={`/jobs/${jobId}/results`} className="text-sm text-[var(--ink-muted)] hover:text-[var(--ink)]">
            ← Results
          </Link>
          <h1 className="font-[family-name:var(--font-display)] text-3xl font-semibold mt-2">
            {row.candidate.name}
          </h1>
          <p className="text-sm text-[var(--ink-muted)] mt-1">
            {filename}
            {row.parse_meta?.provenance?.parser
              ? ` · parser: ${String(row.parse_meta.provenance.parser)}`
              : ''}
            {row.parse_meta?.confidence != null
              ? ` · confidence ${Math.round(row.parse_meta.confidence * 100)}%`
              : ''}
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button variant="secondary" onClick={() => setShowPreview((v) => !v)}>
            {showPreview ? 'Hide CV preview' : 'Preview CV'}
          </Button>
          <Button onClick={() => shortlist.mutate(!row.shortlisted)}>
            {row.shortlisted ? 'Remove shortlist' : 'Shortlist'}
          </Button>
          <Button
            variant="danger"
            disabled={removeCv.isPending || removeCandidate.isPending}
            onClick={() => {
              if (window.confirm(`Delete ${filename}? This cannot be undone.`)) {
                removeCv.mutate(row.resume_id)
              }
            }}
          >
            Delete CV
          </Button>
          <Button
            variant="danger"
            disabled={removeCv.isPending || removeCandidate.isPending}
            onClick={() => {
              if (window.confirm(`Delete ${row.candidate.name || 'this candidate'} from this job?`)) {
                removeCandidate.mutate(row.candidate_id)
              }
            }}
          >
            Delete candidate
          </Button>
        </div>
      </div>
      {removeCv.isError || removeCandidate.isError ? (
        <p className="text-sm text-[var(--danger)]" role="alert">
          {(removeCv.error instanceof Error && removeCv.error.message) ||
            (removeCandidate.error instanceof Error && removeCandidate.error.message) ||
            'Unable to delete this record.'}
        </p>
      ) : null}

      {showPreview ? (
        <Panel className="p-3 overflow-hidden">
          <div className="flex items-center justify-between gap-2 mb-2 px-1">
            <h2 className="font-semibold text-sm">Original CV</h2>
            {previewUrl ? (
              <a
                href={previewUrl}
                download={filename}
                className="text-xs text-[var(--signal-strong)] hover:underline"
              >
                Download
              </a>
            ) : null}
          </div>
          {previewError ? (
            <p className="text-sm text-[var(--danger)] p-4">{previewError}</p>
          ) : !previewUrl ? (
            <p className="text-sm text-[var(--ink-muted)] p-4">Loading preview…</p>
          ) : isPdf ? (
            <iframe
              title={`CV preview for ${row.candidate.name}`}
              src={previewUrl}
              className="w-full h-[min(80vh,900px)] rounded-lg border border-[var(--line)] bg-white"
            />
          ) : (
            <div className="p-4 text-sm">
              <p className="text-[var(--ink-muted)] mb-3">
                Inline preview is best for PDFs. This file type can be downloaded instead.
              </p>
              <a href={previewUrl} download={filename}>
                <Button size="sm">Download {filename}</Button>
              </a>
            </div>
          )}
        </Panel>
      ) : null}

      <div className="grid lg:grid-cols-2 gap-4">
        <Panel className="p-5 space-y-4">
          <h2 className="font-semibold">Structured resume</h2>
          <p className="text-sm text-[var(--ink-muted)]">{resume?.professional_summary || '—'}</p>
          <div>
            <h3 className="text-xs uppercase tracking-wide text-[var(--ink-muted)] mb-2">Skills</h3>
            <div className="flex flex-wrap gap-1.5">
              {(resume?.skills || []).map((s) => (
                <Tag key={s}>{s}</Tag>
              ))}
              {(resume?.skills || []).length === 0 ? <span className="text-sm text-[var(--ink-muted)]">—</span> : null}
            </div>
          </div>
          <div className="space-y-3">
            <h3 className="text-xs uppercase tracking-wide text-[var(--ink-muted)]">Experience</h3>
            {(resume?.experience || []).length === 0 ? (
              <p className="text-sm text-[var(--ink-muted)]">—</p>
            ) : null}
            {(resume?.experience || []).map((exp, i) => (
              <div key={i} className="text-sm border-t border-[var(--line)] pt-3">
                <p className="font-medium">
                  {[exp.designation, exp.company].filter(Boolean).join(' · ') || 'Role'}
                </p>
                <p className="text-xs text-[var(--ink-muted)]">
                  {exp.start_date || '—'} – {exp.end_date || '—'}
                </p>
                <p className="mt-1 whitespace-pre-line text-[var(--ink-muted)]">{exp.description}</p>
              </div>
            ))}
          </div>
          <div className="space-y-2">
            <h3 className="text-xs uppercase tracking-wide text-[var(--ink-muted)]">Education</h3>
            {(resume?.education || []).length === 0 ? (
              <p className="text-sm text-[var(--ink-muted)]">—</p>
            ) : null}
            {(resume?.education || []).map((ed, i) => (
              <p key={i} className="text-sm whitespace-pre-line">
                {[ed.degree, ed.institution, ed.cgpa ? `CGPA ${ed.cgpa}` : '', ed.graduation_date]
                  .filter(Boolean)
                  .join(' · ') || '—'}
              </p>
            ))}
          </div>
          {(resume?.projects || []).length > 0 ? (
            <div className="space-y-2">
              <h3 className="text-xs uppercase tracking-wide text-[var(--ink-muted)]">Projects</h3>
              {(resume?.projects || []).map((p, i) => (
                <p key={i} className="text-sm text-[var(--ink-muted)] whitespace-pre-line">
                  {p}
                </p>
              ))}
            </div>
          ) : null}
        </Panel>

        <Panel className="p-5 space-y-4">
          <h2 className="font-semibold">Match rationale</h2>
          <ScoreMeter score={row.score} />
          <Tag tone={row.hard_filters?.unknown ? 'warn' : row.hard_filters?.passed ? 'ok' : 'danger'}>
            {resultStatus(row.hard_filters)}
          </Tag>
          {row.rank_signals.comment ? (
            <p className="font-medium">{row.rank_signals.comment}</p>
          ) : null}
          <p className="text-sm text-[var(--ink-muted)]">{String(row.explanation?.summary || '')}</p>
          {Array.isArray(row.explanation?.matched_skills) ? (
            <p className="text-sm">Matched skills: {(row.explanation.matched_skills as string[]).join(', ')}</p>
          ) : null}
          {(row.hard_filters?.failed_rules || []).length > 0 ? (
            <p className="text-sm text-[var(--danger)]">{row.hard_filters.failed_rules.join('; ')}</p>
          ) : null}

          <div className="grid grid-cols-3 gap-2 border-t border-[var(--line)] pt-4">
            <div className="rounded-lg bg-white/60 p-3">
              <p className="text-xs text-[var(--ink-muted)]">Relevant experience</p>
              <p className="mt-1 font-semibold tabular-nums">
                {numeric(row.rank_signals.relevant_work_years) != null
                  ? `${numeric(row.rank_signals.relevant_work_years)!.toFixed(2)} years`
                  : '—'}
              </p>
            </div>
            <div className="rounded-lg bg-white/60 p-3">
              <p className="text-xs text-[var(--ink-muted)]">Total experience</p>
              <p className="mt-1 font-semibold tabular-nums">
                {numeric(row.rank_signals.total_experience_years) != null
                  ? `${numeric(row.rank_signals.total_experience_years)!.toFixed(2)} years`
                  : '—'}
              </p>
            </div>
            <div className="rounded-lg bg-white/60 p-3">
              <p className="text-xs text-[var(--ink-muted)]">Relevant projects + certificates</p>
              <p className="mt-1 font-semibold tabular-nums">
                {row.rank_signals.projects_certificates_count ?? '—'}
              </p>
            </div>
          </div>

          {assessment?.steps?.length ? (
            <div className="border-t border-[var(--line)] pt-4 space-y-3">
              <h3 className="font-semibold">Assessment details</h3>
              {assessment.steps.map((step) => (
                <div key={step.step} className="rounded-lg border border-[var(--line)] bg-white/50 p-3">
                  <div className="flex items-center justify-between gap-2">
                    <p className="text-sm font-medium">
                      {step.step}. {step.title}
                    </p>
                    <Tag
                      tone={step.status === 'failed' ? 'danger' : step.status === 'passed' ? 'ok' : 'neutral'}
                    >
                      {step.status}
                    </Tag>
                  </div>
                  {step.message ? (
                    <p className="mt-2 text-xs text-[var(--ink-muted)]">{step.message}</p>
                  ) : null}
                  {(step.summary || []).map((line, index) => (
                    <p key={index} className="mt-1 text-xs text-[var(--ink-muted)]">{line}</p>
                  ))}
                  {(step.failed_requirements || []).map((failure, index) => (
                    <p key={index} className="mt-2 text-xs text-[var(--danger)]">
                      {failure.reason || failure.requirement}
                    </p>
                  ))}
                  {step.relevant_projects?.length ? (
                    <p className="mt-2 text-xs">
                      Relevant projects: {step.relevant_projects.join('; ')}
                    </p>
                  ) : null}
                  {step.relevant_certifications?.length ? (
                    <p className="mt-2 text-xs">
                      Relevant certificates: {step.relevant_certifications.join('; ')}
                    </p>
                  ) : null}
                </div>
              ))}
            </div>
          ) : null}

          <div className="border-t border-[var(--line)] pt-4">
            <h3 className="font-semibold mb-2">Contact</h3>
            {row.candidate.contact_revealed || row.shortlisted ? (
              <div className="text-sm space-y-1">
                <p>{row.candidate.emails.join(', ') || '—'}</p>
                <p>{row.candidate.phones.join(', ') || '—'}</p>
              </div>
            ) : (
              <p className="text-sm text-[var(--ink-muted)]">
                Contact masked until shortlisted ({row.candidate.emails[0]})
              </p>
            )}
          </div>
        </Panel>
      </div>
    </div>
  )
}
