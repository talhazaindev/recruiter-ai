import { useMemo, useState } from 'react'
import type { CatalogItem } from '../api/client'
import { Button, Input } from './ui'

type CatalogChipInputProps = {
  label: string
  values: string[]
  onChange: (values: string[]) => void
  items: CatalogItem[]
  aliases?: Record<string, string[]>
  placeholder?: string
  emptyHint?: string
  query: string
  onQueryChange: (query: string) => void
  loading?: boolean
}

function resolveCanonical(
  raw: string,
  items: CatalogItem[],
  aliases: Record<string, string[]> | undefined,
): string {
  const trimmed = raw.trim()
  if (!trimmed) return trimmed
  const lower = trimmed.toLowerCase()

  const exactItem = items.find(
    (item) => item.id.toLowerCase() === lower || item.label.toLowerCase() === lower,
  )
  if (exactItem) return exactItem.id

  if (aliases) {
    for (const [key, aliasList] of Object.entries(aliases)) {
      if (key.toLowerCase() === lower) return key
      if (aliasList.some((alias) => alias.toLowerCase() === lower)) return key
    }
  }

  const viaMatch = items.find((item) => item.matched_via?.toLowerCase() === lower)
  if (viaMatch) return viaMatch.id

  return trimmed
}

export function CatalogChipInput({
  label,
  values,
  onChange,
  items,
  aliases,
  placeholder = 'Search catalog…',
  emptyHint = 'Nothing selected yet',
  query,
  onQueryChange,
  loading = false,
}: CatalogChipInputProps) {
  const [showSuggestions, setShowSuggestions] = useState(false)

  const selected = useMemo(
    () => new Set(values.map((value) => value.toLowerCase())),
    [values],
  )

  const suggestions = useMemo(
    () => items.filter((item) => !selected.has(item.id.toLowerCase())).slice(0, 40),
    [items, selected],
  )

  function addValue(raw: string) {
    const key = resolveCanonical(raw, items, aliases)
    if (!key) return
    if (values.some((value) => value.toLowerCase() === key.toLowerCase())) {
      onQueryChange('')
      return
    }
    onChange([...values, key])
    onQueryChange('')
    setShowSuggestions(false)
  }

  function removeValue(value: string) {
    onChange(values.filter((entry) => entry !== value))
  }

  return (
    <div className="space-y-2">
      <span className="text-sm text-[var(--ink-muted)]">{label}</span>
      <div className="flex flex-wrap gap-1.5 min-h-[2rem]">
        {values.map((value) => (
          <button
            key={value}
            type="button"
            onClick={() => removeValue(value)}
            className="inline-flex items-center gap-1 rounded-md border border-[var(--line)] bg-white/80 px-2 py-1 text-xs"
            title="Remove"
          >
            {value}
            <span aria-hidden>×</span>
          </button>
        ))}
        {values.length === 0 ? (
          <span className="text-xs text-[var(--ink-muted)]">{emptyHint}</span>
        ) : null}
      </div>
      <div className="flex gap-2">
        <Input
          className="flex-1"
          placeholder={placeholder}
          value={query}
          onChange={(e) => {
            onQueryChange(e.target.value)
            setShowSuggestions(true)
          }}
          onFocus={() => setShowSuggestions(true)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              e.preventDefault()
              if (suggestions[0]) addValue(suggestions[0].id)
              else if (query.trim()) addValue(query.trim())
            }
            if (e.key === 'Escape') setShowSuggestions(false)
          }}
        />
        <Button
          type="button"
          variant="secondary"
          onClick={() => {
            if (query.trim()) addValue(query.trim())
          }}
        >
          Add
        </Button>
      </div>
      {loading ? <p className="text-xs text-[var(--ink-muted)]">Searching catalog…</p> : null}
      {showSuggestions && suggestions.length > 0 ? (
        <div className="max-h-40 overflow-y-auto rounded-md border border-[var(--line)] bg-white/70 p-2">
          <div className="flex flex-wrap gap-1.5">
            {suggestions.map((item) => (
              <button
                key={item.id}
                type="button"
                onClick={() => addValue(item.id)}
                className="rounded-md px-2 py-1 text-xs hover:bg-[var(--signal)]/10 text-left"
                title={item.matched_via ? `Matched via ${item.matched_via}` : item.id}
              >
                {item.label}
                {item.matched_via ? (
                  <span className="text-[var(--ink-muted)]"> · via {item.matched_via}</span>
                ) : null}
                {item.kind === 'compound' ? (
                  <span className="text-[var(--ink-muted)]"> · stack</span>
                ) : null}
              </button>
            ))}
          </div>
        </div>
      ) : null}
    </div>
  )
}
