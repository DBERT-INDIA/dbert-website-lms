'use client';

import s from '../admin.module.css';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function AdminLoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg('');

    try {
      const res = await fetch('/api/admin/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      if (res.ok) {
        router.push('/admin/leads');
        router.refresh(); // Ensure the layout picks up the new cookie if needed
      } else {
        const data = await res.json();
        setErrorMsg(data.error || 'Login failed');
      }
    } catch (err) {
      setErrorMsg('Network error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={s.loginShell}>
      <div className={`card ${s.loginCard}`}>
        <h1 className={s.loginTitle}>
          DBERT Admin
        </h1>
        {errorMsg && <div className={s.loginError}>{errorMsg}</div>}
        <form onSubmit={handleLogin}>
          <div className={s.field}>
            <label className={s.label}>Username</label>
            <input 
              type="text" 
              required
              value={username}
              onChange={e => setUsername(e.target.value)}
              className={s.input}
            />
          </div>
          <div className={s.fieldLast}>
            <label className={s.label}>Password</label>
            <input 
              type="password" 
              required
              value={password}
              onChange={e => setPassword(e.target.value)}
              className={s.input}
            />
          </div>
          <button type="submit" className={`btn btn-primary ${s.submit}`} disabled={loading}>
            {loading ? 'Authenticating...' : 'Login'}
          </button>
        </form>
      </div>
    </div>
  );
}
