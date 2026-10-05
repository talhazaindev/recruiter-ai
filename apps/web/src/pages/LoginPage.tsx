import { useState } from 'react'
import type { FormEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { api } from '../api/client'
import { Button, Input, Panel } from '../components/ui'

export function LoginPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('admin@recruiter.ai')
  const [password, setPassword] = useState('admin123456')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError('')
    try {
      const { access_token } = await api.login(email, password)
      localStorage.setItem('access_token', access_token)
      navigate('/')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35 }}
        className="w-full max-w-md"
      >
        <div className="mb-8 text-center">
          <p className="font-[family-name:var(--font-display)] text-4xl font-semibold tracking-tight">
            Recruiter<span className="text-[var(--signal)]">AI</span>
          </p>
          <p className="mt-2 text-[var(--ink-muted)]">Precision hiring ops for modern software teams.</p>
        </div>
        <Panel className="p-6">
          <form onSubmit={onSubmit} className="space-y-4">
            <label className="block text-sm">
              <span className="mb-1.5 block text-[var(--ink-muted)]">Email</span>
              <Input
                type="email"
                autoComplete="username"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </label>
            <label className="block text-sm">
              <span className="mb-1.5 block text-[var(--ink-muted)]">Password</span>
              <Input
                type="password"
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </label>
            {error ? (
              <p className="text-sm text-[var(--danger)]" role="alert">
                {error}
              </p>
            ) : null}
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Signing in…' : 'Sign in'}
            </Button>
          </form>
        </Panel>
      </motion.div>
    </div>
  )
}
