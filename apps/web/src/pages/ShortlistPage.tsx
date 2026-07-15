import { useQuery } from '@tanstack/react-query'
import { useParams, Link } from 'react-router-dom'
import { api } from '../api/client'
import { Button, EmptyState, Panel, ScoreMeter } from '../components/ui'

export function ShortlistPage() {
  const { jobId } = useParams()
  const rows = useQuery({
    queryKey: ['shortlist', jobId],
    queryFn: () => api.shortlistContacts(jobId!),
    enabled: Boolean(jobId),
  })

  async function copy(text: string) {
    await navigator.clipboard.writeText(text)
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="font-[family-name:var(--font-display)] text-3xl font-semibold">Shortlist contacts</h1>
        <p className="text-[var(--ink-muted)] mt-1">Full contact roster for outreach.</p>
      </div>

      {!rows.isLoading && (rows.data?.length ?? 0) === 0 ? (
        <EmptyState
          title="No shortlisted candidates yet"
          description="Shortlist from the results command center to reveal full contact details here."
          action={
            <Link to={`/jobs/${jobId}/results`}>
              <Button>Open results</Button>
            </Link>
          }
        />
      ) : (
        <div className="space-y-3">
          {rows.data?.map((row) => (
            <Panel key={row.id} className="p-4">
              <div className="flex flex-wrap items-start justify-between gap-4">
                <div>
                  <h2 className="font-semibold text-lg">{row.candidate.name}</h2>
                  <div className="mt-2 space-y-1 text-sm">
                    <p>
                      Email:{' '}
                      <button
                        type="button"
                        className="text-[var(--signal-strong)] underline-offset-2 hover:underline"
                        onClick={() => copy(row.candidate.emails[0] || '')}
                      >
                        {row.candidate.emails[0] || '—'}
                      </button>
                    </p>
                    <p>
                      Phone:{' '}
                      <button
                        type="button"
                        className="text-[var(--signal-strong)] underline-offset-2 hover:underline"
                        onClick={() => copy(row.candidate.phones[0] || '')}
                      >
                        {row.candidate.phones[0] || '—'}
                      </button>
                    </p>
                    {row.candidate.links?.length ? (
                      <p className="text-[var(--ink-muted)]">{row.candidate.links.join(' · ')}</p>
                    ) : null}
                  </div>
                </div>
                <div className="space-y-3 text-right">
                  <ScoreMeter score={row.score} />
                  <a href={`tel:${row.candidate.phones[0] || ''}`}>
                    <Button variant="secondary" size="sm">
                      Call manually
                    </Button>
                  </a>
                </div>
              </div>
            </Panel>
          ))}
        </div>
      )}
    </div>
  )
}
