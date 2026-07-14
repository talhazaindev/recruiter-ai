import { useEffect, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { api, emptyJd, type JobDescription } from '../api/client'
import { Button, Input, Panel, Tag, TextArea } from '../components/ui'

const STEPS = ['Summary', 'Must-have', 'Tech', 'Nice-to-have', 'Keywords', 'Review'] as const

function listFromText(value: string): string[] {
  return value
    .split(/[\n,]/)
    .map((s) => s.trim())
    .filter(Boolean)
}

export function JdEditorPage() {
  const { jobId } = useParams()
  const qc = useQueryClient()
  const job = useQuery({ queryKey: ['job', jobId], queryFn: () => api.getJob(jobId!), enabled: Boolean(jobId) })
  const [step, setStep] = useState(0)
  const [jd, setJd] = useState<JobDescription>(emptyJd())
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    if (job.data) setJd(job.data.jd)
  }, [job.data])

  const save = useMutation({
    mutationFn: () => api.updateJob(jobId!, { jd }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['job', jobId] })
      qc.invalidateQueries({ queryKey: ['jobs'] })
      setSaved(true)
      setTimeout(() => setSaved(false), 2000)
    },
  })

  function update<K extends keyof JobDescription>(key: K, value: JobDescription[K]) {
    setJd((prev) => ({ ...prev, [key]: value }))
  }

  return (
    <div className="space-y-6 max-w-3xl">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h1 className="font-[family-name:var(--font-display)] text-3xl font-semibold">Job description</h1>
          <p className="text-[var(--ink-muted)] mt-1">Structured JD schema — must-haves drive hybrid hard filters.</p>
        </div>
        <div className="flex items-center gap-2">
          {saved ? <Tag tone="ok">Saved</Tag> : null}
          <Button onClick={() => save.mutate()} disabled={save.isPending}>
            {save.isPending ? 'Saving…' : 'Save draft'}
          </Button>
        </div>
      </div>

      <div className="flex flex-wrap gap-2" role="tablist" aria-label="JD sections">
        {STEPS.map((label, i) => (
          <button
            key={label}
            type="button"
            role="tab"
            aria-selected={step === i}
            onClick={() => setStep(i)}
            className={`rounded-full px-3 py-1.5 text-xs font-medium ${
              step === i ? 'bg-[var(--signal)] text-white' : 'bg-white/70 border border-[var(--line)]'
            }`}
          >
            {i + 1}. {label}
          </button>
        ))}
      </div>

      <Panel className="p-6 space-y-4">
        {step === 0 && (
          <>
            <label className="block text-sm">
              <span className="text-[var(--ink-muted)]">Job title</span>
              <Input
                className="mt-1"
                value={jd.job_title}
                onChange={(e) => update('job_title', e.target.value)}
              />
            </label>
            <label className="block text-sm">
              <span className="text-[var(--ink-muted)]">Summary</span>
              <TextArea
                className="mt-1"
                value={jd.job_summary}
                onChange={(e) => update('job_summary', e.target.value)}
              />
            </label>
            <label className="block text-sm">
              <span className="text-[var(--ink-muted)]">Key responsibilities (comma or newline)</span>
              <TextArea
                className="mt-1"
                value={jd.key_responsibilities.join('\n')}
                onChange={(e) => update('key_responsibilities', listFromText(e.target.value))}
              />
            </label>
          </>
        )}

        {step === 1 && (
          <>
            <label className="block text-sm">
              <span className="text-[var(--ink-muted)]">Must-have skills</span>
              <TextArea
                className="mt-1"
                value={jd.requirements_must_have.skills.join('\n')}
                onChange={(e) =>
                  setJd((prev) => ({
                    ...prev,
                    requirements_must_have: {
                      ...prev.requirements_must_have,
                      skills: listFromText(e.target.value),
                    },
                  }))
                }
              />
            </label>
            <div className="grid sm:grid-cols-2 gap-3">
              <label className="block text-sm">
                <span className="text-[var(--ink-muted)]">Min total years</span>
                <Input
                  className="mt-1"
                  type="number"
                  value={jd.requirements_must_have.experience.minimum_total_years ?? ''}
                  onChange={(e) =>
                    setJd((prev) => ({
                      ...prev,
                      requirements_must_have: {
                        ...prev.requirements_must_have,
                        experience: {
                          minimum_total_years: e.target.value ? Number(e.target.value) : null,
                        },
                      },
                    }))
                  }
                />
              </label>
              <label className="block text-sm">
                <span className="text-[var(--ink-muted)]">Min relevant years</span>
                <Input
                  className="mt-1"
                  type="number"
                  value={jd.minimum_relevant_years ?? ''}
                  onChange={(e) =>
                    update('minimum_relevant_years', e.target.value ? Number(e.target.value) : null)
                  }
                />
              </label>
              <label className="block text-sm">
                <span className="text-[var(--ink-muted)]">Degree</span>
                <Input
                  className="mt-1"
                  value={jd.requirements_must_have.education.degree ?? ''}
                  onChange={(e) =>
                    setJd((prev) => ({
                      ...prev,
                      requirements_must_have: {
                        ...prev.requirements_must_have,
                        education: {
                          ...prev.requirements_must_have.education,
                          degree: e.target.value || null,
                        },
                      },
                    }))
                  }
                />
              </label>
              <label className="block text-sm">
                <span className="text-[var(--ink-muted)]">Discipline</span>
                <Input
                  className="mt-1"
                  value={jd.requirements_must_have.education.discipline ?? ''}
                  onChange={(e) =>
                    setJd((prev) => ({
                      ...prev,
                      requirements_must_have: {
                        ...prev.requirements_must_have,
                        education: {
                          ...prev.requirements_must_have.education,
                          discipline: e.target.value || null,
                        },
                      },
                    }))
                  }
                />
              </label>
            </div>
          </>
        )}

        {step === 2 && (
          <>
            <label className="block text-sm">
              <span className="text-[var(--ink-muted)]">Tech stack</span>
              <TextArea
                className="mt-1"
                value={jd.tech_stack.join('\n')}
                onChange={(e) => update('tech_stack', listFromText(e.target.value))}
              />
            </label>
            <label className="block text-sm">
              <span className="text-[var(--ink-muted)]">Preferred skills</span>
              <TextArea
                className="mt-1"
                value={jd.preferred_skills.join('\n')}
                onChange={(e) => update('preferred_skills', listFromText(e.target.value))}
              />
            </label>
          </>
        )}

        {step === 3 && (
          <>
            {(['skills', 'certifications', 'education', 'experience', 'companies'] as const).map((key) => (
              <label key={key} className="block text-sm">
                <span className="text-[var(--ink-muted)] capitalize">Nice to have — {key}</span>
                <TextArea
                  className="mt-1"
                  value={jd.nice_to_have[key].join('\n')}
                  onChange={(e) =>
                    setJd((prev) => ({
                      ...prev,
                      nice_to_have: { ...prev.nice_to_have, [key]: listFromText(e.target.value) },
                    }))
                  }
                />
              </label>
            ))}
          </>
        )}

        {step === 4 && (
          <label className="block text-sm">
            <span className="text-[var(--ink-muted)]">Keywords</span>
            <TextArea
              className="mt-1"
              value={jd.keywords.join('\n')}
              onChange={(e) => update('keywords', listFromText(e.target.value))}
            />
          </label>
        )}

        {step === 5 && (
          <div className="space-y-3 text-sm">
            <p>
              <strong>{jd.job_title || 'Untitled'}</strong>
            </p>
            <p className="text-[var(--ink-muted)]">{jd.job_summary || 'No summary'}</p>
            <p>Must-have skills: {jd.requirements_must_have.skills.join(', ') || '—'}</p>
            <p>Tech stack: {jd.tech_stack.join(', ') || '—'}</p>
            <div className="flex gap-2 pt-2">
              <Button onClick={() => save.mutate()}>Save & continue</Button>
              <Link to={`/jobs/${jobId}/ingest`}>
                <Button variant="secondary">Go to ingest</Button>
              </Link>
            </div>
          </div>
        )}

        <div className="flex justify-between pt-2 border-t border-[var(--line)]">
          <Button variant="ghost" disabled={step === 0} onClick={() => setStep((s) => s - 1)}>
            Back
          </Button>
          <Button variant="secondary" disabled={step === STEPS.length - 1} onClick={() => setStep((s) => s + 1)}>
            Next
          </Button>
        </div>
      </Panel>
    </div>
  )
}
