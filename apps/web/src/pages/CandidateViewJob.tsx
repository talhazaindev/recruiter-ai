import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { motion, AnimatePresence } from 'framer-motion'
import { api } from '../api/client'
import { Button, EmptyState, Panel, Tag } from '../components/ui'
import { useNavigate } from 'react-router-dom'


// Types for job application
interface JobApplication {
  id: string
  job_id: string
  candidate_id: string
  status: 'pending' | 'reviewing' | 'shortlisted' | 'rejected'
  applied_at: string
}

export function CandidateViewJob() {
  const qc = useQueryClient()
  const navigate = useNavigate()

  // State for selected job (to show description)
  const [selectedJobId, setSelectedJobId] = useState<string | null>(null)
  
  // State for job application status tracking
  const [appliedJobs, setAppliedJobs] = useState<Set<string>>(new Set())

  // Fetch all available jobs
  const jobs = useQuery({
    queryKey: ['jobs'],
    queryFn: api.listJobs,
  })

  // Fetch candidate's applications (assuming we have candidate_id from auth context)
  const applications = useQuery({
    queryKey: ['candidate-applications'],
    queryFn: () => api.getCandidateApplications(),
    enabled: !!jobs.data,
  })

  // ❌ REMOVE this mutation - we're navigating instead
  // const applyForJob = useMutation({ ... })

  // Get application status for a job
  const getApplicationStatus = (jobId: string): string | null => {
    if (!applications.data) return null
    const app = applications.data.find((a: JobApplication) => a.job_id === jobId)
    return app ? app.status : null
  }

  // Check if user has applied to a job
  const hasApplied = (jobId: string): boolean => {
    return appliedJobs.has(jobId) || !!getApplicationStatus(jobId)
  }

  // Get the selected job details
  const selectedJob = jobs.data?.find(job => job.id === selectedJobId)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="font-[family-name:var(--font-display)] text-3xl font-semibold tracking-tight">
            Available Positions
          </h1>
          <p className="mt-1 text-[var(--ink-muted)]">
            Browse job openings, review descriptions, and apply to positions that match your skills.
          </p>
        </div>
        <div className="text-sm text-[var(--ink-muted)]">
          {jobs.data ? `${jobs.data.length} positions available` : 'Loading...'}
        </div>
      </div>

      {/* Loading & Error States */}
      {jobs.isLoading ? (
        <div className="flex items-center justify-center py-12">
          <p className="text-[var(--ink-muted)]">Loading available positions...</p>
        </div>
      ) : null}

      {jobs.isError ? (
        <Panel tone="danger" className="p-4">
          <p className="text-[var(--danger)]" role="alert">
            {(jobs.error as Error).message || 'Unable to load job listings. Please try again later.'}
          </p>
        </Panel>
      ) : null}

      {/* Empty State */}
      {!jobs.isLoading && (jobs.data?.length ?? 0) === 0 ? (
        <EmptyState
          title="No positions available"
          description="There are currently no open positions. Please check back later for new opportunities."
        />
      ) : (
        <>
          {/* Job Cards Grid */}
          <div className="grid grid-cols-1 gap-4 lg:grid-cols-2 xl:grid-cols-3">
            {jobs.data?.map((job, i) => {
              const isApplied = hasApplied(job.id)
              const status = getApplicationStatus(job.id)
              
              return (
                <motion.div
                  key={job.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: Math.min(i * 0.05, 0.3) }}
                  className="flex"
                >
                  <Panel className="flex w-full flex-col p-5 hover:shadow-lg transition-shadow duration-200">
                    {/* Job Title & Status */}
                    <div className="flex items-start justify-between gap-2">
                      <h2 className="font-[family-name:var(--font-display)] text-lg font-semibold line-clamp-2 flex-1">
                        {job.jd.job_title || 'Untitled position'}
                      </h2>
                      {isApplied && (
                        <Tag tone={status === 'shortlisted' ? 'ok' : status === 'rejected' ? 'danger' : 'signal'}>
                          {status === 'shortlisted' ? '⭐ Shortlisted' : 
                           status === 'rejected' ? 'Not selected' : 
                           status === 'reviewing' ? '📋 Reviewing' : '✅ Applied'}
                        </Tag>
                      )}
                    </div>

                    {/* Tech Stack / Skills Summary */}
                    {job.jd.tech_stack && job.jd.tech_stack.length > 0 && (
                      <div className="mt-2 flex flex-wrap gap-1">
                        {job.jd.tech_stack.slice(0, 4).map((tech: string, idx: number) => (
                          <span key={idx} className="rounded-full bg-[var(--bg)] px-2 py-0.5 text-xs text-[var(--ink-muted)]">
                            {tech}
                          </span>
                        ))}
                        {job.jd.tech_stack.length > 4 && (
                          <span className="text-xs text-[var(--ink-muted)]">
                            +{job.jd.tech_stack.length - 4} more
                          </span>
                        )}
                      </div>
                    )}

                    {/* Job Summary */}
                    <p className="text-sm text-[var(--ink-muted)] mt-3 line-clamp-3 flex-1">
                      {job.jd.job_summary || 'No description available for this position.'}
                    </p>

                    {/* Job Details */}
                    <div className="mt-3 flex flex-wrap items-center gap-2 text-xs text-[var(--ink-muted)]">
                      {job.jd.requirements_must_have?.experience?.minimum_total_years !== undefined && (
                        <span className="flex items-center gap-1">
                          🎯 {job.jd.requirements_must_have.experience.minimum_total_years}+ years exp
                        </span>
                      )}
                      {job.jd.requirements_must_have?.education?.degree && (
                        <span className="flex items-center gap-1">
                          🎓 {job.jd.requirements_must_have.education.degree}
                        </span>
                      )}
                      {job.jd.requirements_must_have?.skills && job.jd.requirements_must_have.skills.length > 0 && (
                        <span className="flex items-center gap-1">
                          🔧 {job.jd.requirements_must_have.skills.length} skills required
                        </span>
                      )}
                    </div>

                    {/* Job Metadata */}
                    <div className="mt-3 flex items-center justify-between border-t border-[var(--line)] pt-3">
                      <div className="flex items-center gap-2 text-xs text-[var(--ink-muted)]">
                        <span>📄 {job.candidate_count} applicants</span>
                        {job.created_at && (
                          <span>• {new Date(job.created_at).toLocaleDateString()}</span>
                        )}
                      </div>
                      <div className="flex gap-2">
                        {/* View Details Button */}
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => setSelectedJobId(job.id)}
                        >
                          View Details
                        </Button>
                        
                        {/* ✅ Apply Button - Navigate to apply page */}
                        <Button
                          size="sm"
                          variant={isApplied ? 'secondary' : 'primary'}
                          disabled={isApplied}
                          onClick={() => navigate(`/candidate/apply/${job.id}`)}
                        >
                          {isApplied ? 'Applied ✓' : 'Apply Now'}
                        </Button>
                      </div>
                    </div>
                  </Panel>
                </motion.div>
              )
            })}
          </div>
        </>
      )}

      {/* Job Details Modal */}
      <AnimatePresence>
        {selectedJobId && selectedJob && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
            onClick={() => setSelectedJobId(null)}
          >
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              className="relative max-h-[90vh] w-full max-w-4xl overflow-y-auto rounded-xl bg-white p-6 shadow-2xl"
              onClick={(e) => e.stopPropagation()}
            >
              {/* Close Button */}
              <button
                onClick={() => setSelectedJobId(null)}
                className="absolute right-4 top-4 text-[var(--ink-muted)] hover:text-[var(--ink)] transition-colors"
                aria-label="Close details"
              >
                ✕
              </button>

              {/* Job Details Content */}
              <div className="space-y-6 pr-8">
                {/* Header */}
                <div>
                  <h2 className="font-[family-name:var(--font-display)] text-2xl font-semibold">
                    {selectedJob.jd.job_title || 'Untitled position'}
                  </h2>
                  <p className="text-[var(--ink-muted)] mt-1">
                    {selectedJob.jd.requirements_must_have?.education?.degree && (
                      <span>🎓 {selectedJob.jd.requirements_must_have.education.degree}</span>
                    )}
                    {selectedJob.jd.requirements_must_have?.experience?.minimum_total_years !== undefined && (
                      <span className="ml-2">
                        • {selectedJob.jd.requirements_must_have.experience.minimum_total_years}+ years experience
                      </span>
                    )}
                  </p>
                </div>

                {/* Job Summary */}
                {selectedJob.jd.job_summary && (
                  <div>
                    <h3 className="text-sm font-semibold text-[var(--ink-muted)] uppercase tracking-wider mb-2">
                      About This Position
                    </h3>
                    <p className="text-sm leading-relaxed text-[var(--ink)] whitespace-pre-wrap">
                      {selectedJob.jd.job_summary}
                    </p>
                  </div>
                )}

                {/* Key Responsibilities */}
                {selectedJob.jd.key_responsibilities && selectedJob.jd.key_responsibilities.length > 0 && (
                  <div>
                    <h3 className="text-sm font-semibold text-[var(--ink-muted)] uppercase tracking-wider mb-2">
                      Key Responsibilities
                    </h3>
                    <ul className="list-disc pl-5 text-sm space-y-1 text-[var(--ink)]">
                      {selectedJob.jd.key_responsibilities.map((resp: string, idx: number) => (
                        <li key={idx}>{resp}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Must-Have Requirements */}
                <div>
                  <h3 className="text-sm font-semibold text-[var(--ink-muted)] uppercase tracking-wider mb-2">
                    Requirements
                  </h3>
                  
                  {/* Education */}
                  {selectedJob.jd.requirements_must_have?.education && (
                    <div className="mb-3">
                      <h4 className="text-xs font-medium text-[var(--ink-muted)] mb-1">Education</h4>
                      <ul className="list-disc pl-5 text-sm space-y-0.5 text-[var(--ink)]">
                        <li>
                          Degree: {selectedJob.jd.requirements_must_have.education.degree || 'Not specified'}
                          {selectedJob.jd.requirements_must_have.education.discipline && 
                            ` in ${selectedJob.jd.requirements_must_have.education.discipline}`
                          }
                        </li>
                        {selectedJob.jd.requirements_must_have.education.minimum_cgpa && (
                          <li>Minimum CGPA: {selectedJob.jd.requirements_must_have.education.minimum_cgpa}</li>
                        )}
                      </ul>
                    </div>
                  )}

                  {/* Experience */}
                  {selectedJob.jd.requirements_must_have?.experience && (
                    <div className="mb-3">
                      <h4 className="text-xs font-medium text-[var(--ink-muted)] mb-1">Experience</h4>
                      <ul className="list-disc pl-5 text-sm space-y-0.5 text-[var(--ink)]">
                        <li>
                          Minimum {selectedJob.jd.requirements_must_have.experience.minimum_total_years || 0} years of experience
                        </li>
                      </ul>
                    </div>
                  )}

                  {/* Skills */}
                  {selectedJob.jd.requirements_must_have?.skills && selectedJob.jd.requirements_must_have.skills.length > 0 && (
                    <div className="mb-3">
                      <h4 className="text-xs font-medium text-[var(--ink-muted)] mb-1">Required Skills</h4>
                      <div className="flex flex-wrap gap-1.5">
                        {selectedJob.jd.requirements_must_have.skills.map((skill: string, idx: number) => (
                          <span key={idx} className="rounded-full bg-[var(--bg)] px-3 py-1 text-xs">
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Preferred Skills */}
                {selectedJob.jd.preferred_skills && selectedJob.jd.preferred_skills.length > 0 && (
                  <div>
                    <h3 className="text-sm font-semibold text-[var(--ink-muted)] uppercase tracking-wider mb-2">
                      Preferred Skills
                    </h3>
                    <div className="flex flex-wrap gap-1.5">
                      {selectedJob.jd.preferred_skills.map((skill: string, idx: number) => (
                        <span key={idx} className="rounded-full border border-[var(--line)] px-3 py-1 text-xs">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Tech Stack */}
                {selectedJob.jd.tech_stack && selectedJob.jd.tech_stack.length > 0 && (
                  <div>
                    <h3 className="text-sm font-semibold text-[var(--ink-muted)] uppercase tracking-wider mb-2">
                      Tech Stack
                    </h3>
                    <div className="flex flex-wrap gap-1.5">
                      {selectedJob.jd.tech_stack.map((tech: string, idx: number) => (
                        <span key={idx} className="rounded-full bg-[var(--bg)] px-3 py-1 text-xs">
                          {tech}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Nice to Have */}
                {selectedJob.jd.nice_to_have && (
                  <div>
                    <h3 className="text-sm font-semibold text-[var(--ink-muted)] uppercase tracking-wider mb-2">
                      Nice to Have
                    </h3>
                    <ul className="list-disc pl-5 text-sm space-y-0.5 text-[var(--ink)]">
                      {selectedJob.jd.nice_to_have.skills?.map((item: string, idx: number) => (
                        <li key={`skill-${idx}`}>Skill: {item}</li>
                      ))}
                      {selectedJob.jd.nice_to_have.certifications?.map((item: string, idx: number) => (
                        <li key={`cert-${idx}`}>Certification: {item}</li>
                      ))}
                      {selectedJob.jd.nice_to_have.education?.map((item: string, idx: number) => (
                        <li key={`edu-${idx}`}>Education: {item}</li>
                      ))}
                      {selectedJob.jd.nice_to_have.experience?.map((item: string, idx: number) => (
                        <li key={`exp-${idx}`}>Experience: {item}</li>
                      ))}
                      {selectedJob.jd.nice_to_have.companies?.map((item: string, idx: number) => (
                        <li key={`company-${idx}`}>Company: {item}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Application Stats & Actions */}
                <div className="flex items-center justify-between border-t border-[var(--line)] pt-4 mt-4">
                  <div className="text-sm text-[var(--ink-muted)]">
                    <span>{selectedJob.candidate_count} applicants</span>
                    {selectedJob.shortlisted_count > 0 && (
                      <span className="ml-3">• {selectedJob.shortlisted_count} shortlisted</span>
                    )}
                    {selectedJob.created_at && (
                      <span className="ml-3">• Posted {new Date(selectedJob.created_at).toLocaleDateString()}</span>
                    )}
                  </div>
                  <div className="flex gap-2">
                    <Button
                      variant="ghost"
                      onClick={() => setSelectedJobId(null)}
                    >
                      Close
                    </Button>
                    {/* ✅ Modal Apply Button - Navigate to apply page */}
                    <Button
                      variant={hasApplied(selectedJob.id) ? 'secondary' : 'primary'}
                      disabled={hasApplied(selectedJob.id)}
                      onClick={() => {
                        navigate(`/candidate/apply/${selectedJob.id}`)
                        setSelectedJobId(null) // Close the modal
                      }}
                    >
                      {hasApplied(selectedJob.id) ? 'Already Applied ✓' : 'Apply Now'}
                    </Button>
                  </div>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}