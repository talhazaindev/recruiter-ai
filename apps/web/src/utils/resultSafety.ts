/** Runtime guards for legacy or partially migrated match-result values. */

export function numeric(value: unknown): number | null {
  return typeof value === 'number' && Number.isFinite(value) ? value : null
}

export function resultStatus(hardFilters: {
  passed?: boolean
  unknown?: boolean
}): 'Pass' | 'Fail' | 'Needs review' {
  if (hardFilters.unknown) return 'Needs review'
  return hardFilters.passed ? 'Pass' : 'Fail'
}

export function pageRange(total: number, offset: number, limit: number): [number, number] {
  if (total <= 0) return [0, 0]
  return [Math.min(offset + 1, total), Math.min(offset + limit, total)]
}
