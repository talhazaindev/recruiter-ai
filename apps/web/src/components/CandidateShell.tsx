// CandidateShell.tsx (New - Create this file)
import { Outlet, Link } from 'react-router-dom'

export function CandidateShell() {
  return (
    <div className="min-h-screen bg-[var(--bg)]">
      {/* Simple header - no sidebar */}
      <header className="border-b border-[var(--line)] bg-white/80 backdrop-blur sticky top-0 z-50">
        <div className="container mx-auto flex items-center justify-between px-4 py-3">
          <Link to="/candidate/viewjobs" className="text-lg font-semibold hover:text-[var(--signal)]">
            ← Browse Jobs
          </Link>
          <div className="text-sm text-[var(--ink-muted)]">
            Candidate Portal
          </div>
        </div>
      </header>
      
      {/* Page content */}
      <main className="container mx-auto px-4 py-8">
        <Outlet /> {/* This renders CandidateViewJob or Applyjob */}
      </main>
    </div>
  )
}