import { useState, useRef } from 'react'
import { useMutation, useQuery } from '@tanstack/react-query'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { api } from '../api/client'
import { Button, Panel, Tag } from '../components/ui'

interface FormData {
  firstName: string
  lastName: string
  email: string
  phone: string
  currentLocation: string
  university: string
  degree: string
  graduationYear: string
  workExperience: string
  yearsOfExperience: string
  currentCompany: string
  linkedinProfile: string
  portfolioGithub: string
  cvFile: File | null
}

export function Applyjob() {
  // ✅ Extract jobId from URL
  const { jobId } = useParams<{ jobId: string }>()
  const navigate = useNavigate()
  const fileInputRef = useRef<HTMLInputElement>(null)
  
  console.log('Job ID from URL:', jobId) // Debug: check if jobId is received

  const [formData, setFormData] = useState<FormData>({
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    currentLocation: '',
    university: '',
    degree: '',
    graduationYear: '',
    workExperience: '',
    yearsOfExperience: '',
    currentCompany: '',
    linkedinProfile: '',
    portfolioGithub: '',
    cvFile: null,
  })
  
  const [fileName, setFileName] = useState<string>('')
  const [isAutoFilling, setIsAutoFilling] = useState(false)
  const [errors, setErrors] = useState<Partial<Record<keyof FormData, string>>>({})

  // ✅ Fetch job details using jobId from URL
  const job = useQuery({
    queryKey: ['job', jobId],
    queryFn: () => {
      if (!jobId) {
        throw new Error('Job ID is missing')
      }
      return api.getJob(jobId)
    },
    enabled: Boolean(jobId), // Only fetch if jobId exists
  })

  // ✅ Submit application with jobId
  const submitApplication = useMutation({
    mutationFn: async (data: FormData) => {
      if (!jobId) {
        throw new Error('Job ID is missing')
      }

      const formDataToSend = new FormData()
      
      Object.entries(data).forEach(([key, value]) => {
        if (key === 'cvFile' && value instanceof File) {
          formDataToSend.append('cv', value)
        } else if (value !== null && value !== undefined) {
          formDataToSend.append(key, value.toString())
        }
      })
      
      // ✅ Include jobId in the request
      formDataToSend.append('jobId', jobId)
      
      const response = await fetch(`/api/jobs/${jobId}/apply`, {
        method: 'POST',
        body: formDataToSend,
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      })
      
      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.message || 'Failed to submit application')
      }
      
      return response.json()
    },
    onSuccess: () => {
      navigate(`/candidate/apply/${jobId}/success`)
    },
    onError: (error) => {
      console.error('Application submission failed:', error)
      setErrors(prev => ({
        ...prev,
        submit: error instanceof Error ? error.message : 'Failed to submit application. Please try again.'
      }))
    },
  })

  // Auto-fill function
  const handleAutoFill = async () => {
    if (!formData.cvFile) {
      setErrors(prev => ({
        ...prev,
        cvFile: 'Please upload your CV first to use auto-fill'
      }))
      document.getElementById('cv-upload-section')?.scrollIntoView({ behavior: 'smooth' })
      return
    }

    setIsAutoFilling(true)
    
    try {
      // TODO: Replace with actual parser API call
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      const parsedData = {
        firstName: 'John',
        lastName: 'Doe',
        email: 'john.doe@email.com',
        phone: '+1 (555) 123-4567',
        currentLocation: 'San Francisco, CA',
        university: 'Stanford University',
        degree: 'Master of Science in Computer Science',
        graduationYear: '2023',
        workExperience: 'Senior Software Engineer at TechCorp (2021-2024)\n' +
                        'Led development of AI-powered features\n' +
                        'Managed team of 5 engineers\n\n' +
                        'AI Research Intern at AI Labs (2020-2021)\n' +
                        'Developed NLP models for text classification',
        yearsOfExperience: '4',
        currentCompany: 'TechCorp',
        linkedinProfile: 'https://linkedin.com/in/johndoe',
        portfolioGithub: 'https://github.com/johndoe',
      }
      
      setFormData(prev => ({
        ...prev,
        ...parsedData,
        cvFile: prev.cvFile,
      }))
      
      if (errors.cvFile) {
        setErrors(prev => ({ ...prev, cvFile: undefined }))
      }
      
    } catch (error) {
      console.error('Auto-fill failed:', error)
      setErrors(prev => ({
        ...prev,
        submit: 'Failed to parse CV. Please try again or fill manually.'
      }))
    } finally {
      setIsAutoFilling(false)
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setFormData(prev => ({ ...prev, cvFile: file }))
      setFileName(file.name)
      
      if (errors.cvFile) {
        setErrors(prev => ({ ...prev, cvFile: undefined }))
      }
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    
    if (errors[name as keyof FormData]) {
      setErrors(prev => ({ ...prev, [name]: undefined }))
    }
  }

  const validateForm = (): boolean => {
    const newErrors: Partial<Record<keyof FormData, string>> = {}
    
    if (!formData.firstName.trim()) newErrors.firstName = 'First name is required'
    if (!formData.lastName.trim()) newErrors.lastName = 'Last name is required'
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required'
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address'
    }
    if (!formData.phone.trim()) newErrors.phone = 'Phone number is required'
    if (!formData.university.trim()) newErrors.university = 'University is required'
    if (!formData.degree.trim()) newErrors.degree = 'Degree is required'
    if (!formData.workExperience.trim()) newErrors.workExperience = 'Work experience is required'
    if (!formData.yearsOfExperience.trim()) newErrors.yearsOfExperience = 'Years of experience is required'
    if (!formData.cvFile) newErrors.cvFile = 'CV/Resume is required'
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (validateForm()) {
      submitApplication.mutate(formData)
    }
  }

  const currentYear = new Date().getFullYear()
  const graduationYears = Array.from({ length: 50 }, (_, i) => String(currentYear - i))

  // ✅ Show error if jobId is missing
  if (!jobId) {
    return (
      <div className="max-w-4xl mx-auto py-16 text-center">
        <Panel tone="danger" className="p-6">
          <h2 className="text-xl font-semibold">Invalid Job</h2>
          <p className="text-[var(--ink-muted)] mt-2">Job ID is missing. Please go back and try again.</p>
          <Link to="/candidate/jobs">
            <Button className="mt-4">View All Jobs</Button>
          </Link>
        </Panel>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6 py-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <Link to={`/candidate/jobs/${jobId}`} className="text-sm text-[var(--ink-muted)] hover:text-[var(--ink)] transition-colors">
            ← Back to job details
          </Link>
          <h1 className="font-[family-name:var(--font-display)] text-3xl font-semibold mt-2">
            Apply for Position
          </h1>
          <p className="text-[var(--ink-muted)] mt-1">
            {job.isLoading ? 'Loading...' : job.data?.jd?.job_title || 'Position not found'}
          </p>
        </div>
        {job.data?.jd?.job_title && (
          <Tag tone="signal">{job.data.status || 'Active'}</Tag>
        )}
      </div>

      {/* Job Not Found */}
      {job.isError && (
        <Panel tone="danger" className="p-6">
          <p className="text-[var(--danger)]">
            {(job.error as Error).message || 'Unable to load job details. Please try again.'}
          </p>
        </Panel>
      )}

      {/* Rest of the form... (same as before) */}
      {/* Auto-fill Banner */}
      <Panel className="bg-[var(--bg)] border border-[var(--line)] p-4">
        <div className="flex items-center justify-between flex-wrap gap-3">
          <div className="flex items-center gap-3">
            <span className="text-2xl">⚡</span>
            <div>
              <p className="font-medium">Quick Apply with Auto-fill</p>
              <p className="text-sm text-[var(--ink-muted)]">
                Upload your CV and click auto-fill to populate the form
              </p>
            </div>
          </div>
          <div className="flex gap-2">
            <Button
              variant="secondary"
              onClick={() => fileInputRef.current?.click()}
              disabled={isAutoFilling}
            >
              📄 Upload CV
            </Button>
            <Button
              variant="primary"
              onClick={handleAutoFill}
              disabled={isAutoFilling || !formData.cvFile}
            >
              {isAutoFilling ? '⏳ Parsing CV...' : '⚡ Auto-fill Form'}
            </Button>
          </div>
        </div>
        {fileName && (
          <div className="mt-2 text-sm text-[var(--signal)]">
            📎 Uploaded: {fileName}
          </div>
        )}
        {!formData.cvFile && (
          <div className="mt-2 text-sm text-[var(--ink-muted)]">
            💡 Upload your CV first to enable auto-fill
          </div>
        )}
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.doc,.docx,.txt"
          onChange={handleFileChange}
          className="hidden"
        />
      </Panel>

      {/* Application Form */}
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Basic Information */}
        <Panel className="p-6 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold font-[family-name:var(--font-display)]">
              Basic Candidate Information
            </h2>
            {isAutoFilling && (
              <span className="text-xs text-[var(--signal)] animate-pulse">
                ⏳ Filling fields...
              </span>
            )}
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* First Name */}
            <div>
              <label className="block text-sm font-medium mb-1">
                First Name <span className="text-[var(--danger)]">*</span>
              </label>
              <input
                type="text"
                name="firstName"
                value={formData.firstName}
                onChange={handleChange}
                className={`w-full rounded-lg border ${errors.firstName ? 'border-[var(--danger)]' : 'border-[var(--line)]'} px-3 py-2 text-sm focus:border-[var(--signal)] focus:outline-none focus:ring-1 focus:ring-[var(--signal)] transition-colors`}
                placeholder="Enter your first name"
                disabled={isAutoFilling}
              />
              {errors.firstName && (
                <p className="mt-1 text-xs text-[var(--danger)]">{errors.firstName}</p>
              )}
            </div>

            {/* Last Name */}
            <div>
              <label className="block text-sm font-medium mb-1">
                Last Name <span className="text-[var(--danger)]">*</span>
              </label>
              <input
                type="text"
                name="lastName"
                value={formData.lastName}
                onChange={handleChange}
                className={`w-full rounded-lg border ${errors.lastName ? 'border-[var(--danger)]' : 'border-[var(--line)]'} px-3 py-2 text-sm focus:border-[var(--signal)] focus:outline-none focus:ring-1 focus:ring-[var(--signal)] transition-colors`}
                placeholder="Enter your last name"
                disabled={isAutoFilling}
              />
              {errors.lastName && (
                <p className="mt-1 text-xs text-[var(--danger)]">{errors.lastName}</p>
              )}
            </div>

            {/* Email */}
            <div>
              <label className="block text-sm font-medium mb-1">
                Email <span className="text-[var(--danger)]">*</span>
              </label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className={`w-full rounded-lg border ${errors.email ? 'border-[var(--danger)]' : 'border-[var(--line)]'} px-3 py-2 text-sm focus:border-[var(--signal)] focus:outline-none focus:ring-1 focus:ring-[var(--signal)] transition-colors`}
                placeholder="your.email@example.com"
                disabled={isAutoFilling}
              />
              {errors.email && (
                <p className="mt-1 text-xs text-[var(--danger)]">{errors.email}</p>
              )}
            </div>

            {/* Phone */}
            <div>
              <label className="block text-sm font-medium mb-1">
                Phone <span className="text-[var(--danger)]">*</span>
              </label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                className={`w-full rounded-lg border ${errors.phone ? 'border-[var(--danger)]' : 'border-[var(--line)]'} px-3 py-2 text-sm focus:border-[var(--signal)] focus:outline-none focus:ring-1 focus:ring-[var(--signal)] transition-colors`}
                placeholder="+1 (555) 123-4567"
                disabled={isAutoFilling}
              />
              {errors.phone && (
                <p className="mt-1 text-xs text-[var(--danger)]">{errors.phone}</p>
              )}
            </div>

            {/* Current Location */}
            <div className="md:col-span-2">
              <label className="block text-sm font-medium mb-1">
                Current Location <span className="text-[var(--ink-muted)]">(Optional)</span>
              </label>
              <input
                type="text"
                name="currentLocation"
                value={formData.currentLocation}
                onChange={handleChange}
                className="w-full rounded-lg border border-[var(--line)] px-3 py-2 text-sm focus:border-[var(--signal)] focus:outline-none focus:ring-1 focus:ring-[var(--signal)] transition-colors"
                placeholder="City, State, Country"
                disabled={isAutoFilling}
              />
            </div>
          </div>
        </Panel>

        {/* Education */}
        <Panel className="p-6 space-y-4">
          <h2 className="text-lg font-semibold font-[family-name:var(--font-display)]">
            Education
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* University */}
            <div className="md:col-span-2">
              <label className="block text-sm font-medium mb-1">
                University <span className="text-[var(--danger)]">*</span>
              </label>
              <input
                type="text"
                name="university"
                value={formData.university}
                onChange={handleChange}
                className={`w-full rounded-lg border ${errors.university ? 'border-[var(--danger)]' : 'border-[var(--line)]'} px-3 py-2 text-sm focus:border-[var(--signal)] focus:outline-none focus:ring-1 focus:ring-[var(--signal)] transition-colors`}
                placeholder="University name"
                disabled={isAutoFilling}
              />
              {errors.university && (
                <p className="mt-1 text-xs text-[var(--danger)]">{errors.university}</p>
              )}
            </div>

            {/* Degree */}
            <div>
              <label className="block text-sm font-medium mb-1">
                Degree <span className="text-[var(--danger)]">*</span>
              </label>
              <input
                type="text"
                name="degree"
                value={formData.degree}
                onChange={handleChange}
                className={`w-full rounded-lg border ${errors.degree ? 'border-[var(--danger)]' : 'border-[var(--line)]'} px-3 py-2 text-sm focus:border-[var(--signal)] focus:outline-none focus:ring-1 focus:ring-[var(--signal)] transition-colors`}
                placeholder="Bachelor of Science in CS"
                disabled={isAutoFilling}
              />
              {errors.degree && (
                <p className="mt-1 text-xs text-[var(--danger)]">{errors.degree}</p>
              )}
            </div>

            {/* Graduation Year */}
            <div>
              <label className="block text-sm font-medium mb-1">
                Graduation Year <span className="text-[var(--ink-muted)]">(Optional)</span>
              </label>
              <select
                name="graduationYear"
                value={formData.graduationYear}
                onChange={handleChange}
                className="w-full rounded-lg border border-[var(--line)] px-3 py-2 text-sm focus:border-[var(--signal)] focus:outline-none focus:ring-1 focus:ring-[var(--signal)] bg-white transition-colors"
                disabled={isAutoFilling}
              >
                <option value="">Select year</option>
                {graduationYears.map(year => (
                  <option key={year} value={year}>{year}</option>
                ))}
              </select>
            </div>
          </div>
        </Panel>

        {/* Work Experience */}
        <Panel className="p-6 space-y-4">
          <h2 className="text-lg font-semibold font-[family-name:var(--font-display)]">
            Work Experience
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Work Experience Description */}
            <div className="md:col-span-2">
              <label className="block text-sm font-medium mb-1">
                Work Experience <span className="text-[var(--danger)]">*</span>
              </label>
              <textarea
                name="workExperience"
                value={formData.workExperience}
                onChange={handleChange}
                rows={4}
                className={`w-full rounded-lg border ${errors.workExperience ? 'border-[var(--danger)]' : 'border-[var(--line)]'} px-3 py-2 text-sm focus:border-[var(--signal)] focus:outline-none focus:ring-1 focus:ring-[var(--signal)] resize-none transition-colors`}
                placeholder="Describe your work experience, including roles, responsibilities, and achievements..."
                disabled={isAutoFilling}
              />
              {errors.workExperience && (
                <p className="mt-1 text-xs text-[var(--danger)]">{errors.workExperience}</p>
              )}
            </div>

            {/* Years of Experience */}
            <div>
              <label className="block text-sm font-medium mb-1">
                Years of Experience <span className="text-[var(--danger)]">*</span>
              </label>
              <input
                type="number"
                name="yearsOfExperience"
                value={formData.yearsOfExperience}
                onChange={handleChange}
                min="0"
                max="50"
                step="0.5"
                className={`w-full rounded-lg border ${errors.yearsOfExperience ? 'border-[var(--danger)]' : 'border-[var(--line)]'} px-3 py-2 text-sm focus:border-[var(--signal)] focus:outline-none focus:ring-1 focus:ring-[var(--signal)] transition-colors`}
                placeholder="e.g., 3"
                disabled={isAutoFilling}
              />
              {errors.yearsOfExperience && (
                <p className="mt-1 text-xs text-[var(--danger)]">{errors.yearsOfExperience}</p>
              )}
            </div>

            {/* Current/Previous Company */}
            <div>
              <label className="block text-sm font-medium mb-1">
                Current/Previous Company <span className="text-[var(--ink-muted)]">(Optional)</span>
              </label>
              <input
                type="text"
                name="currentCompany"
                value={formData.currentCompany}
                onChange={handleChange}
                className="w-full rounded-lg border border-[var(--line)] px-3 py-2 text-sm focus:border-[var(--signal)] focus:outline-none focus:ring-1 focus:ring-[var(--signal)] transition-colors"
                placeholder="Company name"
                disabled={isAutoFilling}
              />
            </div>
          </div>
        </Panel>

        {/* Links */}
        <Panel className="p-6 space-y-4">
          <h2 className="text-lg font-semibold font-[family-name:var(--font-display)]">
            Professional Links
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* LinkedIn */}
            <div>
              <label className="block text-sm font-medium mb-1">
                LinkedIn Profile <span className="text-[var(--ink-muted)]">(Optional)</span>
              </label>
              <input
                type="url"
                name="linkedinProfile"
                value={formData.linkedinProfile}
                onChange={handleChange}
                className="w-full rounded-lg border border-[var(--line)] px-3 py-2 text-sm focus:border-[var(--signal)] focus:outline-none focus:ring-1 focus:ring-[var(--signal)] transition-colors"
                placeholder="https://linkedin.com/in/username"
                disabled={isAutoFilling}
              />
            </div>

            {/* Portfolio/GitHub */}
            <div>
              <label className="block text-sm font-medium mb-1">
                Portfolio/GitHub <span className="text-[var(--ink-muted)]">(Optional)</span>
              </label>
              <input
                type="url"
                name="portfolioGithub"
                value={formData.portfolioGithub}
                onChange={handleChange}
                className="w-full rounded-lg border border-[var(--line)] px-3 py-2 text-sm focus:border-[var(--signal)] focus:outline-none focus:ring-1 focus:ring-[var(--signal)] transition-colors"
                placeholder="https://github.com/username or portfolio link"
                disabled={isAutoFilling}
              />
            </div>
          </div>
        </Panel>

        {/* CV/Resume */}
        <Panel 
          id="cv-upload-section"
          className={`p-6 space-y-4 border-2 border-dashed ${
            errors.cvFile ? 'border-[var(--danger)]' : 'border-[var(--line)]'
          } hover:border-[var(--signal)] transition-colors`}
        >
          <div className="text-center">
            <div className="text-4xl mb-2">📄</div>
            <h3 className="font-semibold">Upload CV/Resume</h3>
            <p className="text-sm text-[var(--ink-muted)] mt-1">
              Drag and drop or click to upload (PDF, DOC, DOCX)
            </p>
            <p className="text-xs text-[var(--ink-muted)] mt-1">
              <span className="text-[var(--danger)]">*</span> Required
            </p>
            
            <div className="mt-4 flex justify-center gap-3">
              <Button
                variant="secondary"
                onClick={() => fileInputRef.current?.click()}
                disabled={isAutoFilling}
              >
                Choose File
              </Button>
              {fileName && (
                <Button
                  variant="danger"
                  size="sm"
                  onClick={() => {
                    setFormData(prev => ({ ...prev, cvFile: null }))
                    setFileName('')
                    if (fileInputRef.current) {
                      fileInputRef.current.value = ''
                    }
                  }}
                  disabled={isAutoFilling}
                >
                  Remove
                </Button>
              )}
            </div>
            
            {fileName && (
              <div className="mt-2 text-sm text-[var(--signal)]">
                ✅ {fileName} uploaded successfully
              </div>
            )}
            
            {errors.cvFile && (
              <p className="mt-2 text-xs text-[var(--danger)]">{errors.cvFile}</p>
            )}
          </div>
        </Panel>

        {/* Submit Section */}
        <div className="flex items-center justify-between gap-4 pt-4 border-t border-[var(--line)]">
          <div className="text-sm text-[var(--ink-muted)]">
            <span className="text-[var(--danger)]">*</span> Required fields
          </div>
          <div className="flex gap-3">
            <Button
              type="button"
              variant="ghost"
              onClick={() => navigate(`/candidate/jobs/${jobId}`)}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="primary"
              disabled={submitApplication.isPending}
              className="min-w-[120px]"
            >
              {submitApplication.isPending ? '⏳ Submitting...' : '📤 Submit Application'}
            </Button>
          </div>
        </div>

        {/* Submit Error */}
        {errors.submit && (
          <Panel tone="danger" className="p-4">
            <p className="text-sm text-[var(--danger)]">{errors.submit}</p>
          </Panel>
        )}
      </form>
    </div>
  )
}