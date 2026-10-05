import { useEffect, useMemo, useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Link, useNavigate, useParams } from 'react-router-dom'
import {
  api,
  type ExperienceEvaluation,
  type ExperienceGap,
  type ItemMatchDetail,
} from '../api/client'
import { Button, Panel, ScoreMeter, Tag } from '../components/ui'
import { numeric, resultStatus } from '../utils/resultSafety'

function reasonLabel(reason?: string): string {
  switch (reason) {
    case 'relevant':
      return 'Counted toward relevant years'
    case 'title_mismatch':
      return 'Title did not match JD'
    case 'tech_below_threshold':
      return 'Tech stack match below threshold'
    case 'invalid_dates':
      return 'Invalid or missing dates'
    default:
      return reason || 'No evaluation detail'
  }
}

function findExperienceEvaluation(
  evaluations: ExperienceEvaluation[],
  exp: { company?: string; designation?: string; start_date?: string; end_date?: string },
  index: number,
): ExperienceEvaluation | undefined {
  const exact = evaluations.find(
    (row) =>
      (row.company || '') === (exp.company || '') &&
      (row.designation || '') === (exp.designation || '') &&
      (row.start_date || '') === (exp.start_date || '') &&
      (row.end_date || '') === (exp.end_date || ''),
  )
  if (exact) return exact
  return evaluations[index]
}

function findItemMatch(
  matches: Record<string, ItemMatchDetail> | undefined,
  text: string,
): ItemMatchDetail | undefined {
  if (!matches) return undefined
  if (matches[text]) return matches[text]
  const lower = text.toLowerCase()
  const key = Object.keys(matches).find((entry) => entry.toLowerCase() === lower || lower.includes(entry.toLowerCase()))
  return key ? matches[key] : undefined
}

function RelevanceBadge({
  evaluation,
}: {
  evaluation?: { is_relevant?: boolean; reason?: string; match_percentage?: number; tech_matches?: number; tech_stack_size?: number }
}) {
  if (!evaluation) return null
  const relevant = Boolean(evaluation.is_relevant)
  const detailParts: string[] = [reasonLabel(evaluation.reason)]
  if (evaluation.tech_stack_size != null && evaluation.tech_matches != null) {
    detailParts.push(
      `${evaluation.tech_matches}/${evaluation.tech_stack_size}` +
        (evaluation.match_percentage != null ? ` (${evaluation.match_percentage}%)` : ''),
    )
  } else if (evaluation.match_percentage != null) {
    detailParts.push(`${evaluation.match_percentage}%`)
  }
  return (
    <div className="mt-1 flex flex-wrap items-center gap-2">
      <Tag tone={relevant ? 'ok' : 'danger'}>{relevant ? 'Relevant' : 'Not relevant'}</Tag>
      <span className="text-xs text-[var(--ink-muted)]">{detailParts.join(' · ')}</span>
    </div>
  )
}

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

  const row = detail.data
  const assessment = row?.explanation?.details
  const step3 = assessment?.steps?.find((step) => step.step === 3)
  const step4 = assessment?.steps?.find((step) => step.step === 4)

  const experienceEvaluations = useMemo(() => {
    const fromSignals = row?.rank_signals.experience_evaluations
    if (Array.isArray(fromSignals) && fromSignals.length) return fromSignals
    return step3?.experience_evaluations || []
  }, [row, step3])

  const projectMatches = useMemo(() => {
    const fromSignals = row?.rank_signals.project_matches
    if (fromSignals && typeof fromSignals === 'object') return fromSignals as Record<string, ItemMatchDetail>
    return step4?.project_matches
  }, [row, step4])

  const certificationMatches = useMemo(() => {
    const fromSignals = row?.rank_signals.certification_matches
    if (fromSignals && typeof fromSignals === 'object') {
      return fromSignals as Record<string, ItemMatchDetail>
    }
    return step4?.certification_matches
  }, [row, step4])

  const gaps = useMemo(() => {
    const fromSignals = row?.rank_signals.gaps
    if (Array.isArray(fromSignals) && fromSignals.length) return fromSignals as ExperienceGap[]
    return (step3?.gaps || []) as ExperienceGap[]
  }, [row, step3])

  const hasBreakdown = experienceEvaluations.length > 0 || Boolean(projectMatches) || Boolean(certificationMatches)

  if (detail.isLoading) return <p className="text-[var(--ink-muted)]">Loading…</p>
  if (detail.isError) {
    return (
      <p className="text-[var(--danger)]">
        {detail.error instanceof Error ? detail.error.message : 'Unable to load this job result.'}
      </p>
    )
  }
  if (!row) return <p className="text-[var(--danger)]">Not found</p>

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
  const missingSkills = Array.isArray(row.rank_signals.missing_skills)
    ? (row.rank_signals.missing_skills as string[])
    : []
  const verification = row.explanation.verification || {}

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

      {!hasBreakdown ? (
        <p className="text-sm text-[var(--ink-muted)] rounded-lg border border-[var(--line)] bg-white/60 px-3 py-2">
          Relevance breakdown is unavailable for this older match. Rematch the job to see which
          experience, projects, and certifications were counted.
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
            {(resume?.experience || []).map((exp, i) => {
              const evaluation = findExperienceEvaluation(experienceEvaluations, exp, i)
              return (
                <div key={i} className="text-sm border-t border-[var(--line)] pt-3">
                  <p className="font-medium">
                    {[exp.designation, exp.company].filter(Boolean).join(' · ') || 'Role'}
                  </p>
                  <p className="text-xs text-[var(--ink-muted)]">
                    {exp.start_date || '—'} – {exp.end_date || '—'}
                  </p>
                  <RelevanceBadge evaluation={evaluation} />
                  <p className="mt-1 whitespace-pre-line text-[var(--ink-muted)]">{exp.description}</p>
                </div>
              )
            })}
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
              {(resume?.projects || []).map((p, i) => {
                const match = findItemMatch(projectMatches, p)
                return (
                  <div key={i} className="text-sm border-t border-[var(--line)] pt-3">
                    <p className="whitespace-pre-line text-[var(--ink-muted)]">{p}</p>
                    <RelevanceBadge
                      evaluation={
                        match
                          ? {
                              is_relevant: match.is_relevant,
                              reason: match.is_relevant ? 'relevant' : 'tech_below_threshold',
                              match_percentage: match.match_percentage,
                              tech_matches: match.tech_matches,
                            }
                          : undefined
                      }
                    />
                  </div>
                )
              })}
            </div>
          ) : null}
          {(resume?.certifications || []).length > 0 ? (
            <div className="space-y-2">
              <h3 className="text-xs uppercase tracking-wide text-[var(--ink-muted)]">Certifications</h3>
              {(resume?.certifications || []).map((cert, i) => {
                const match = findItemMatch(certificationMatches, cert)
                return (
                  <div key={i} className="text-sm border-t border-[var(--line)] pt-3">
                    <p className="whitespace-pre-line text-[var(--ink-muted)]">{cert}</p>
                    <RelevanceBadge
                      evaluation={
                        match
                          ? {
                              is_relevant: match.is_relevant,
                              reason: match.is_relevant ? 'relevant' : 'tech_below_threshold',
                              match_percentage: match.match_percentage,
                              tech_matches: match.tech_matches,
                            }
                          : undefined
                      }
                    />
                  </div>
                )
              })}
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
          {missingSkills.length > 0 ? (
            <p className="text-sm text-[var(--danger)]">Missing skills: {missingSkills.join(', ')}</p>
          ) : null}
          {(row.hard_filters?.failed_rules || []).length > 0 ? (
            <p className="text-sm text-[var(--danger)]">{row.hard_filters.failed_rules.join('; ')}</p>
          ) : null}

          {Object.values(verification).some(Boolean) ? (
            <div className="rounded-lg border border-[var(--line)] bg-white/50 p-3 space-y-1">
              <p className="text-xs uppercase tracking-wide text-[var(--ink-muted)]">Verification</p>
              {Object.entries(verification).map(([key, value]) =>
                value ? (
                  <p key={key} className="text-xs text-[var(--ink-muted)]">
                    <span className="font-medium capitalize text-[var(--ink)]">{key}:</span> {String(value)}
                  </p>
                ) : null,
              )}
            </div>
          ) : null}

          <div className="grid grid-cols-3 gap-2 border-t border-[var(--line)] pt-4">
            <div className="rounded-lg bg-white/60 p-3">
              <p className="text-xs text-[var(--ink-muted)]">Relevant experience</p>
              <p className="mt-1 font-semibold tabular-nums">
                {numeric(row.rank_signals.relevant_work_years) != null
                  ? `${numeric(row.rank_signals.relevant_work_years)!.toFixed(2)} years`
                  : '—'}
              </p>
              {step3?.minimum_required != null ? (
                <p className="mt-1 text-[10px] text-[var(--ink-muted)]">
                  Required {Number(step3.minimum_required).toFixed(1)}y
                </p>
              ) : null}
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

          {(row.rank_signals.gap_found || gaps.length > 0) ? (
            <div className="rounded-lg border border-[var(--line)] bg-white/50 p-3 space-y-2">
              <div className="flex items-center gap-2">
                <p className="text-sm font-medium">Experience gaps</p>
                <Tag tone={row.rank_signals.gap_found ? 'warn' : 'ok'}>
                  {row.rank_signals.gap_found ? 'Gap found' : 'No major gaps'}
                </Tag>
              </div>
              {gaps.length === 0 ? (
                <p className="text-xs text-[var(--ink-muted)]">No gap details recorded.</p>
              ) : (
                gaps.map((gap, index) => (
                  <p key={index} className="text-xs text-[var(--ink-muted)]">
                    {(gap.gap_months != null ? `${gap.gap_months.toFixed(1)} months` : 'Gap')} between{' '}
                    {[gap.from_designation, gap.from_company].filter(Boolean).join(' at ') || 'prior role'}
                    {gap.from_end ? ` (ended ${gap.from_end})` : ''} and{' '}
                    {[gap.to_designation, gap.to_company].filter(Boolean).join(' at ') || 'next role'}
                    {gap.to_start ? ` (started ${gap.to_start})` : ''}
                  </p>
                ))
              )}
            </div>
          ) : null}

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
                  {step.step === 3 && step.relevant_experience != null ? (
                    <p className="mt-2 text-xs text-[var(--ink-muted)]">
                      Relevant {Number(step.relevant_experience).toFixed(2)}y
                      {step.minimum_required != null
                        ? ` vs required ${Number(step.minimum_required).toFixed(1)}y`
                        : ''}
                    </p>
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
