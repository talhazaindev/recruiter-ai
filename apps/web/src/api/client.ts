/** API client for Recruiter AI backend. */

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export type JobDescription = {
  job_title: string
  job_summary: string
  key_responsibilities: string[]
  requirements_must_have: {
    education: {
      degree: string | null
      discipline: string | null
      minimum_cgpa: number | null
      must_be_completed: boolean | null
    }
    experience: { minimum_total_years: number | null }
    skills: string[]
  }
  minimum_relevant_years: number | null
  tech_stack: string[]
  preferred_skills: string[]
  nice_to_have: {
    skills: string[]
    certifications: string[]
    education: string[]
    experience: string[]
    companies: string[]
  }
  keywords: string[]
}

export type Job = {
  id: string
  org_id: string
  status: string
  jd: JobDescription
  created_at: string
  updated_at: string
  candidate_count: number
  needs_review_count: number
  shortlisted_count: number
}

export type MatchRow = {
  id: string
  job_id: string
  resume_id: string
  candidate_id: string
  score: number
  hard_filters: { passed: boolean; failed_rules: string[] }
  rank_signals: Record<string, unknown>
  explanation: Record<string, unknown>
  shortlisted: boolean
  review_status: string
  candidate: {
    name: string
    emails: string[]
    phones: string[]
    links: string[]
    contact_revealed: boolean
  }
  parse: {
    status?: string
    confidence?: number
    needs_review?: boolean
    warnings?: string[]
  }
  skills: string[]
  resume?: Record<string, unknown>
}

export type Batch = {
  id: string
  job_id: string
  source: string
  status: string
  counters: Record<string, number>
  meta?: Record<string, unknown>
  created_at: string
  updated_at: string
}

function authHeaders(): HeadersInit {
  const token = localStorage.getItem('access_token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers)
  if (!headers.has('Content-Type') && !(init.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json')
  }
  const auth = authHeaders()
  Object.entries(auth).forEach(([k, v]) => headers.set(k, v as string))

  const res = await fetch(`${API_BASE}${path}`, { ...init, headers })
  if (res.status === 401) {
    localStorage.removeItem('access_token')
    if (!path.includes('/auth/login')) {
      window.location.href = '/login'
    }
  }
  if (!res.ok) {
    let detail = res.statusText
    try {
      const body = await res.json()
      detail = body.detail || JSON.stringify(body)
    } catch {
      /* ignore */
    }
    throw new Error(typeof detail === 'string' ? detail : 'Request failed')
  }
  if (res.status === 204) return undefined as T
  return res.json() as Promise<T>
}

export const api = {
  login: (email: string, password: string) =>
    request<{ access_token: string }>('/v1/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }),
  me: () => request<{ id: string; email: string; role: string; org_id: string }>('/v1/auth/me'),
  listJobs: () => request<Job[]>('/v1/jobs'),
  getJob: (id: string) => request<Job>(`/v1/jobs/${id}`),
  createJob: (jd: JobDescription, status: string = 'draft') =>
    request<Job>('/v1/jobs', { method: 'POST', body: JSON.stringify({ jd, status }) }),
  updateJob: (id: string, patch: { jd?: JobDescription; status?: string }) =>
    request<Job>(`/v1/jobs/${id}`, { method: 'PATCH', body: JSON.stringify(patch) }),
  uploadCvs: async (jobId: string, files: File[]) => {
    const fd = new FormData()
    files.forEach((f) => fd.append('files', f))
    return request<{ batch_id: string; file_count: number; status: string }>(
      `/v1/jobs/${jobId}/ingest/upload`,
      { method: 'POST', body: fd },
    )
  },
  ingestDrive: (jobId: string, folder_url: string) =>
    request<{ batch_id: string; folder_id: string; status: string }>(
      `/v1/jobs/${jobId}/ingest/drive`,
      { method: 'POST', body: JSON.stringify({ folder_url }) },
    ),
  getBatch: (batchId: string) => request<Batch>(`/v1/batches/${batchId}`),
  listResults: (jobId: string, view: string = 'best_fit') =>
    request<MatchRow[]>(`/v1/jobs/${jobId}/results?view=${view}`),
  getResult: (id: string) => request<MatchRow & {
    resume?: Record<string, unknown>
    raw_resume_text?: string
    source_ref?: { original_filename?: string; content_type?: string; storage_key?: string }
    parse_meta?: { status?: string; confidence?: number; warnings?: string[]; provenance?: Record<string, unknown> }
  }>(`/v1/match-results/${id}`),
  resumeFileUrl: (resumeId: string) => `${API_BASE}/v1/resumes/${resumeId}/file`,
  fetchResumeBlob: async (resumeId: string) => {
    const headers = new Headers(authHeaders())
    const res = await fetch(`${API_BASE}/v1/resumes/${resumeId}/file`, { headers })
    if (!res.ok) throw new Error('Failed to load CV file')
    return res.blob()
  },
  shortlist: (id: string, shortlisted: boolean) =>
    request<MatchRow>(`/v1/match-results/${id}/shortlist`, {
      method: 'POST',
      body: JSON.stringify({ shortlisted }),
    }),
  shortlistContacts: (jobId: string) => request<MatchRow[]>(`/v1/jobs/${jobId}/shortlist`),
  reviewQueue: (jobId: string) => request<MatchRow[]>(`/v1/jobs/${jobId}/review-queue`),
  updateReview: (id: string, review_status: string, notes: string = '') =>
    request<MatchRow>(`/v1/match-results/${id}/review`, {
      method: 'PATCH',
      body: JSON.stringify({ review_status, notes }),
    }),
  driveStatus: () =>
    request<{ configured: boolean; connected: boolean }>('/v1/integrations/drive/status'),
  driveAuthUrl: () => request<{ url: string }>('/v1/integrations/drive/auth-url'),
  listSkills: () => request<{ skills: string[] }>('/v1/reference/skills'),
  listDegrees: () => request<{ degrees: string[]; aliases: Record<string, string[]> }>('/v1/reference/degrees'),
  listDisciplines: () =>
    request<{ disciplines: string[]; aliases: Record<string, string[]> }>('/v1/reference/disciplines'),
  health: () => request<{ status: string }>('/v1/health'),
}

export function emptyJd(): JobDescription {
  return {
    job_title: '',
    job_summary: '',
    key_responsibilities: [],
    requirements_must_have: {
      education: {
        degree: null,
        discipline: null,
        minimum_cgpa: null,
        must_be_completed: null,
      },
      experience: { minimum_total_years: null },
      skills: [],
    },
    minimum_relevant_years: null,
    tech_stack: [],
    preferred_skills: [],
    nice_to_have: {
      skills: [],
      certifications: [],
      education: [],
      experience: [],
      companies: [],
    },
    keywords: [],
  }
}
