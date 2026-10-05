import { describe, expect, it } from 'vitest'
import { numeric, pageRange, resultStatus } from './resultSafety'

describe('result runtime safety', () => {
  it('rejects legacy string and non-finite numeric signals', () => {
    expect(numeric('3.5')).toBeNull()
    expect(numeric(Number.NaN)).toBeNull()
    expect(numeric(3.5)).toBe(3.5)
  })

  it('keeps unknown parse quality separate from candidate failure', () => {
    expect(resultStatus({ passed: false, unknown: true })).toBe('Needs review')
    expect(resultStatus({ passed: true })).toBe('Pass')
    expect(resultStatus({ passed: false })).toBe('Fail')
  })

  it('reports stable server-backed page ranges', () => {
    expect(pageRange(101, 50, 50)).toEqual([51, 100])
    expect(pageRange(0, 0, 50)).toEqual([0, 0])
  })
})
