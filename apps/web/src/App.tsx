import { Navigate, Outlet, Route, Routes } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AppShell } from './components/AppShell'
import { LoginPage } from './pages/LoginPage'
import { JobsPage } from './pages/JobsPage'
import { JobOverviewPage } from './pages/JobOverviewPage'
import { JdEditorPage } from './pages/JdEditorPage'
import { IngestPage } from './pages/IngestPage'
import { ResultsPage } from './pages/ResultsPage'
import { ShortlistPage } from './pages/ShortlistPage'
import { ReviewPage } from './pages/ReviewPage'
import { CandidateDetailPage } from './pages/CandidateDetailPage'
import { DriveSettingsPage } from './pages/DriveSettingsPage'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: 1, refetchOnWindowFocus: false },
  },
})

function Protected() {
  const token = localStorage.getItem('access_token')
  if (!token) return <Navigate to="/login" replace />
  return <Outlet />
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route element={<Protected />}>
          <Route element={<AppShell />}>
            <Route path="/" element={<JobsPage />} />
            <Route path="/jobs/:jobId" element={<JobOverviewPage />} />
            <Route path="/jobs/:jobId/jd" element={<JdEditorPage />} />
            <Route path="/jobs/:jobId/ingest" element={<IngestPage />} />
            <Route path="/jobs/:jobId/results" element={<ResultsPage />} />
            <Route path="/jobs/:jobId/shortlist" element={<ShortlistPage />} />
            <Route path="/jobs/:jobId/review" element={<ReviewPage />} />
            <Route path="/jobs/:jobId/candidates/:resultId" element={<CandidateDetailPage />} />
            <Route path="/settings/drive" element={<DriveSettingsPage />} />
          </Route>
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </QueryClientProvider>
  )
}
