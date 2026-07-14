import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { Link, useParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { api, type MatchRow } from '../api/client'
import { Button, Drawer, EmptyState, Panel, ScoreMeter, Tag } from '../components/ui'

const VIEWS = [
  { key: 'best_fit', label: 'Best fit' },
  { key: 'all', label: 'All' },
  { key: 'shortlisted', label: 'Shortlisted' },
  { key: 'needs_review', label: 'Needs review' },
  { key: 'failed_filters', label: 'Failed filters' },
] as const

export function ResultsPage() {
  const { jobId } = useParams()
  const qc = useQueryClient()
  const [view, setView] = useState<(typeof VIEWS)[number]['key']>('all')
  const [selected, setSelected] = useState<MatchRow | null>(null)
  const [checked, setChecked] = useState<Set<string>>(new Set())

  const results = useQuery({
    queryKey: ['results', jobId, view],
    queryFn: () => api.listResults(jobId!, view),
    enabled: Boolean(jobId),
  })

  const counts = useQuery({
    queryKey: ['result-counts', jobId],
    queryFn: async () => {
      const [all, best_fit, shortlisted, needs_review, failed_filters] = await Promise.all([
        api.listResults(jobId!, 'all'),
        api.listResults(jobId!, 'best_fit'),
        api.listResults(jobId!, 'shortlisted'),
        api.listResults(jobId!, 'needs_review'),
        api.listResults(jobId!, 'failed_filters'),
      ])
      return {
        all: all.length,
        best_fit: best_fit.length,
        shortlisted: shortlisted.length,
        needs_review: needs_review.length,
        failed_filters: failed_filters.length,
      }
    },
    enabled: Boolean(jobId),
  })

  const shortlist = useMutation({
    mutationFn: ({ id, value }: { id: string; value: boolean }) => api.shortlist(id, value),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['results', jobId] })
      qc.invalidateQueries({ queryKey: ['result-counts', jobId] })
      qc.invalidateQueries({ queryKey: ['shortlist', jobId] })
      qc.invalidateQueries({ queryKey: ['job', jobId] })
    },
  })

  async function bulkShortlist() {
    for (const id of checked) {
      await api.shortlist(id, true)
    }
    setChecked(new Set())
    qc.invalidateQueries({ queryKey: ['results', jobId] })
    qc.invalidateQueries({ queryKey: ['shortlist', jobId] })
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h1 className="font-[family-name:var(--font-display)] text-3xl font-semibold">Results command center</h1>
          <p className="text-[var(--ink-muted)] mt-1">
            Hybrid scores with hard-filter badges. Press S on a focused row pattern via Shortlist actions.
          </p>
        </div>
        {checked.size > 0 ? (
          <Button onClick={bulkShortlist}>Shortlist selected ({checked.size})</Button>
        ) : null}
      </div>

      <div className="sticky top-16 z-20 flex flex-wrap gap-2 bg-[var(--bg)]/90 backdrop-blur py-2">
        {VIEWS.map((v) => (
          <button
            key={v.key}
            type="button"
            onClick={() => setView(v.key)}
            className={`rounded-full px-3 py-1.5 text-xs font-medium ${
              view === v.key ? 'bg-[var(--signal)] text-white' : 'bg-white/80 border border-[var(--line)]'
            }`}
          >
            {v.label}
            {counts.data ? ` (${counts.data[v.key]})` : ''}
          </button>
        ))}
      </div>

      {results.isLoading ? <p className="text-[var(--ink-muted)]">Loading rankings…</p> : null}
      {!results.isLoading && (results.data?.length ?? 0) === 0 ? (
        <EmptyState
          title="No candidates in this view"
          description="Ingest CVs first, or switch tabs. Best fit only shows must-have passers — try All or Failed filters."
          action={
            <Link to={`/jobs/${jobId}/ingest`}>
              <Button>Go to ingest</Button>
            </Link>
          }
        />
      ) : (
        <Panel className="overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-white/70 text-left text-[var(--ink-muted)]">
                <tr>
                  <th className="px-3 py-3 w-8" />
                  <th className="px-3 py-3 font-medium">Candidate</th>
                  <th className="px-3 py-3 font-medium">Score</th>
                  <th className="px-3 py-3 font-medium">Filters</th>
                  <th className="px-3 py-3 font-medium">Skills</th>
                  <th className="px-3 py-3 font-medium">Confidence</th>
                  <th className="px-3 py-3 font-medium">Actions</th>
                </tr>
              </thead>
              <tbody>
                {results.data?.map((row, i) => (
                  <motion.tr
                    key={row.id}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: Math.min(i * 0.02, 0.25) }}
                    className="border-t border-[var(--line)] hover:bg-white/60"
                  >
                    <td className="px-3 py-3">
                      <input
                        type="checkbox"
                        aria-label={`Select ${row.candidate.name}`}
                        checked={checked.has(row.id)}
                        onChange={(e) => {
                          setChecked((prev) => {
                            const next = new Set(prev)
                            if (e.target.checked) next.add(row.id)
                            else next.delete(row.id)
                            return next
                          })
                        }}
                      />
                    </td>
                    <td className="px-3 py-3">
                      <button type="button" className="text-left font-medium" onClick={() => setSelected(row)}>
                        {row.candidate.name || 'Unknown'}
                      </button>
                      <p className="text-xs text-[var(--ink-muted)]">{row.candidate.emails[0]}</p>
                    </td>
                    <td className="px-3 py-3">
                      <ScoreMeter score={row.score} />
                    </td>
                    <td className="px-3 py-3">
                      <Tag tone={row.hard_filters?.passed ? 'ok' : 'danger'}>
                        {row.hard_filters?.passed ? 'Passed' : 'Failed'}
                      </Tag>
                    </td>
                    <td className="px-3 py-3 max-w-[200px]">
                      <span className="line-clamp-1 text-[var(--ink-muted)]">
                        {(row.skills || []).slice(0, 4).join(', ') || '—'}
                      </span>
                    </td>
                    <td className="px-3 py-3 tabular-nums">
                      {row.parse?.confidence != null ? Math.round(row.parse.confidence * 100) + '%' : '—'}
                    </td>
                    <td className="px-3 py-3">
                      <div className="flex gap-1">
                        <Button
                          size="sm"
                          variant={row.shortlisted ? 'secondary' : 'primary'}
                          onClick={() => shortlist.mutate({ id: row.id, value: !row.shortlisted })}
                        >
                          {row.shortlisted ? 'Listed' : 'Shortlist'}
                        </Button>
                        <Button size="sm" variant="ghost" onClick={() => setSelected(row)}>
                          Open
                        </Button>
                      </div>
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </Panel>
      )}

      <Drawer
        open={Boolean(selected)}
        onClose={() => setSelected(null)}
        title={selected?.candidate.name || 'Candidate'}
      >
        {selected ? (
          <div className="space-y-4 text-sm">
            <ScoreMeter score={selected.score} />
            <div>
              <h3 className="font-semibold mb-1">Match explanation</h3>
              <p className="text-[var(--ink-muted)]">
                {String(selected.explanation?.summary || 'No explanation')}
              </p>
              {Array.isArray(selected.explanation?.matched_skills) ? (
                <p className="mt-2">Matched: {(selected.explanation.matched_skills as string[]).join(', ')}</p>
              ) : null}
              {(selected.hard_filters?.failed_rules || []).length > 0 ? (
                <p className="mt-2 text-[var(--danger)]">
                  Failed: {selected.hard_filters.failed_rules.join('; ')}
                </p>
              ) : null}
            </div>
            <div>
              <h3 className="font-semibold mb-1">Contact</h3>
              {selected.candidate.contact_revealed || selected.shortlisted ? (
                <>
                  <p>{selected.candidate.emails.join(', ') || '—'}</p>
                  <p>{selected.candidate.phones.join(', ') || '—'}</p>
                </>
              ) : (
                <p className="text-[var(--ink-muted)]">Masked until shortlisted · {selected.candidate.emails[0]}</p>
              )}
            </div>
            <div className="flex flex-wrap gap-2">
              <Button
                onClick={() => shortlist.mutate({ id: selected.id, value: !selected.shortlisted })}
              >
                {selected.shortlisted ? 'Remove shortlist' : 'Shortlist'}
              </Button>
              <Link to={`/jobs/${jobId}/candidates/${selected.id}`}>
                <Button variant="secondary">Full detail + CV preview</Button>
              </Link>
            </div>
          </div>
        ) : null}
      </Drawer>
    </div>
  )
}
