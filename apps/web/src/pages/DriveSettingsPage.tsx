import { Link, useSearchParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { api } from '../api/client'
import { Button, Panel, Tag } from '../components/ui'

export function DriveSettingsPage() {
  const [params] = useSearchParams()
  const status = useQuery({ queryKey: ['drive-status'], queryFn: api.driveStatus })

  async function connect() {
    const { url } = await api.driveAuthUrl()
    window.location.href = url
  }

  return (
    <div className="max-w-lg space-y-4">
      <h1 className="font-[family-name:var(--font-display)] text-3xl font-semibold">Google Drive</h1>
      <Panel className="p-5 space-y-3">
        {params.get('connected') === '1' ? <Tag tone="ok">Connected successfully</Tag> : null}
        <p className="text-sm text-[var(--ink-muted)]">
          Configure OAuth credentials in the API env, then connect your Google account to ingest CV folders.
        </p>
        <div className="flex gap-2 items-center">
          <Tag tone={status.data?.connected ? 'ok' : 'warn'}>
            {status.data?.connected ? 'Connected' : 'Not connected'}
          </Tag>
          <Tag tone={status.data?.configured ? 'signal' : 'neutral'}>
            {status.data?.configured ? 'Configured' : 'Missing client id'}
          </Tag>
        </div>
        <Button onClick={connect}>Connect Drive</Button>
        <Link to="/" className="block text-sm text-[var(--signal-strong)]">
          Back to jobs
        </Link>
      </Panel>
    </div>
  )
}
