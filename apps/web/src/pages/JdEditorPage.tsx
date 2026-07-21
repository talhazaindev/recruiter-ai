import { useEffect, useMemo, useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { api, emptyJd, type JobDescription } from '../api/client'
import { Button, Input, Panel, Tag, TextArea } from '../components/ui'

const STEPS = ['Summary', 'Must-have', 'Tech', 'Nice-to-have', 'Keywords', 'Review'] as const

function listFromLines(value: string): string[] {
  return value.split('\n')
}

function compactList(values: string[]): string[] {
  return values.map((value) => value.trim()).filter(Boolean)
}

function normalizedJd(jd: JobDescription): JobDescription {
  return {
    ...jd,
    key_responsibilities: compactList(jd.key_responsibilities),
    requirements_must_have: {
      ...jd.requirements_must_have,
      skills: compactList(jd.requirements_must_have.skills),
    },
    tech_stack: compactList(jd.tech_stack),
    preferred_skills: compactList(jd.preferred_skills),
    nice_to_have: {
      skills: compactList(jd.nice_to_have.skills),
      certifications: compactList(jd.nice_to_have.certifications),
      education: compactList(jd.nice_to_have.education),
      experience: compactList(jd.nice_to_have.experience),
      companies: compactList(jd.nice_to_have.companies),
    },
    keywords: compactList(jd.keywords),
  }
}

export function JdEditorPage() {
  const { jobId } = useParams()
  const qc = useQueryClient()
  const job = useQuery({ queryKey: ['job', jobId], queryFn: () => api.getJob(jobId!), enabled: Boolean(jobId) })
  const skillsRef = useQuery({ queryKey: ['ref-skills'], queryFn: () => api.listSkills() })
  const degreesRef = useQuery({ queryKey: ['ref-degrees'], queryFn: () => api.listDegrees() })
  const disciplinesRef = useQuery({ queryKey: ['ref-disciplines'], queryFn: () => api.listDisciplines() })

  const [step, setStep] = useState(0)
  const [jd, setJd] = useState<JobDescription>(emptyJd())
  const [saved, setSaved] = useState(false)
  const [skillQuery, setSkillQuery] = useState('')

  useEffect(() => {
    if (job.data) setJd(job.data.jd)
  }, [job.data])

  const save = useMutation({
    mutationFn: () => api.updateJob(jobId!, { jd: normalizedJd(jd) }),
    onSuccess: (updatedJob) => {
      qc.invalidateQueries({ queryKey: ['job', jobId] })
      qc.invalidateQueries({ queryKey: ['jobs'] })
      setJd(updatedJob.jd)
      setSaved(true)
      setTimeout(() => setSaved(false), 2000)
    },
  })

  function update<K extends keyof JobDescription>(key: K, value: JobDescription[K]) {
    setJd((prev) => ({ ...prev, [key]: value }))
  }

  function setMustSkills(skills: string[]) {
    setJd((prev) => ({
      ...prev,
      requirements_must_have: { ...prev.requirements_must_have, skills },
    }))
  }

  function addSkill(skill: string) {
    const key = skill.trim()
    if (!key) return
    const existing = jd.requirements_must_have.skills
    if (existing.some((s) => s.toLowerCase() === key.toLowerCase())) return
    setMustSkills([...existing, key])
    setSkillQuery('')
  }

  function removeSkill(skill: string) {
    setMustSkills(jd.requirements_must_have.skills.filter((s) => s !== skill))
  }

  const filteredSkills = useMemo(() => {
    const all = skillsRef.data?.skills || []
    const q = skillQuery.trim().toLowerCase()
    const selected = new Set(jd.requirements_must_have.skills.map((s) => s.toLowerCase()))
    return all
      .filter((s) => !selected.has(s.toLowerCase()))
      .filter((s) => !q || s.toLowerCase().includes(q))
      .slice(0, 40)
  }, [skillsRef.data, skillQuery, jd.requirements_must_have.skills])

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
              <span className="text-[var(--ink-muted)]">Key responsibilities (one per line; commas allowed)</span>
              <TextArea
                className="mt-1"
                value={jd.key_responsibilities.join('\n')}
                onChange={(e) => update('key_responsibilities', listFromLines(e.target.value))}
              />
            </label>
          </>
        )}

        {step === 1 && (
          <>
            <div className="space-y-2">
              <span className="text-sm text-[var(--ink-muted)]">Must-have skills</span>
              <div className="flex flex-wrap gap-1.5 min-h-[2rem]">
                {jd.requirements_must_have.skills.map((skill) => (
                  <button
                    key={skill}
                    type="button"
                    onClick={() => removeSkill(skill)}
                    className="inline-flex items-center gap-1 rounded-md border border-[var(--line)] bg-white/80 px-2 py-1 text-xs"
                    title="Remove"
                  >
                    {skill}
                    <span aria-hidden>×</span>
                  </button>
                ))}
                {jd.requirements_must_have.skills.length === 0 ? (
                  <span className="text-xs text-[var(--ink-muted)]">No skills selected yet</span>
                ) : null}
              </div>
              <div className="flex gap-2">
                <Input
                  className="flex-1"
                  placeholder="Search skills catalog…"
                  value={skillQuery}
                  onChange={(e) => setSkillQuery(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                      e.preventDefault()
                      if (filteredSkills[0]) addSkill(filteredSkills[0])
                      else if (skillQuery.trim()) addSkill(skillQuery.trim())
                    }
                  }}
                />
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => {
                    if (skillQuery.trim()) addSkill(skillQuery.trim())
                  }}
                >
                  Add
                </Button>
              </div>
              {filteredSkills.length > 0 ? (
                <div className="max-h-40 overflow-y-auto rounded-md border border-[var(--line)] bg-white/70 p-2">
                  <div className="flex flex-wrap gap-1.5">
                    {filteredSkills.map((skill) => (
                      <button
                        key={skill}
                        type="button"
                        onClick={() => addSkill(skill)}
                        className="rounded-md px-2 py-1 text-xs hover:bg-[var(--signal)]/10"
                      >
                        {skill}
                      </button>
                    ))}
                  </div>
                </div>
              ) : null}
            </div>

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
                <select
                  className="mt-1 w-full rounded-md border border-[var(--line)] bg-white/80 px-3 py-2 text-sm"
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
                >
                  <option value="">No degree requirement</option>
                  {(degreesRef.data?.degrees || []).map((d) => (
                    <option key={d} value={d}>
                      {d}
                    </option>
                  ))}
                </select>
              </label>
              <label className="block text-sm">
                <span className="text-[var(--ink-muted)]">Discipline</span>
                <select
                  className="mt-1 w-full rounded-md border border-[var(--line)] bg-white/80 px-3 py-2 text-sm"
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
                >
                  <option value="">Any discipline</option>
                  {(disciplinesRef.data?.disciplines || []).map((d) => (
                    <option key={d} value={d}>
                      {d}
                    </option>
                  ))}
                </select>
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
                onChange={(e) => update('tech_stack', listFromLines(e.target.value))}
              />
            </label>
            <label className="block text-sm">
              <span className="text-[var(--ink-muted)]">Preferred skills</span>
              <TextArea
                className="mt-1"
                value={jd.preferred_skills.join('\n')}
                onChange={(e) => update('preferred_skills', listFromLines(e.target.value))}
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
                      nice_to_have: { ...prev.nice_to_have, [key]: listFromLines(e.target.value) },
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
              onChange={(e) => update('keywords', listFromLines(e.target.value))}
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
            <p>
              Education: {jd.requirements_must_have.education.degree || '—'}
              {jd.requirements_must_have.education.discipline
                ? ` / ${jd.requirements_must_have.education.discipline}`
                : ''}
            </p>
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
