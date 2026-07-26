import React from 'react';
import { Lock, Mail, User, X } from 'lucide-react';

export default function AuthModal({ show, onClose, authEmail, setAuthEmail, authName, setAuthName, onSubmit }) {
  if (!show) return null;

  return (
    <div style={{ position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh', background: 'rgba(0,0,0,0.75)', backdropFilter: 'blur(10px)', zIndex: 100, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div className="glass-card" style={{ width: '90%', maxWidth: '420px', position: 'relative' }}>
        <button onClick={onClose} style={{ position: 'absolute', top: '1.25rem', right: '1.25rem', background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer' }}>
          <X size={20} />
        </button>
        <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
          <div style={{ width: '50px', height: '50px', background: 'rgba(59,130,246,0.15)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 0.75rem', color: '#3b82f6' }}>
            <Lock size={24} />
          </div>
          <h3 style={{ fontSize: '1.3rem', fontWeight: '700' }}>Sign In / Account Login</h3>
          <p style={{ fontSize: '0.85rem', color: '#94a3b8', marginTop: '0.25rem' }}>Enter your email to save predictions & view history</p>
        </div>

        <form onSubmit={onSubmit} style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
          <div className="input-group">
            <label>Your Email Address</label>
            <div className="input-wrapper">
              <Mail className="input-icon" size={16} />
              <input
                type="email"
                placeholder="user@example.com"
                value={authEmail}
                onChange={(e) => setAuthEmail(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="input-group">
            <label>Your Name (Optional)</label>
            <div className="input-wrapper">
              <User className="input-icon" size={16} />
              <input
                type="text"
                placeholder="John Doe"
                value={authName}
                onChange={(e) => setAuthName(e.target.value)}
              />
            </div>
          </div>

          <button type="submit" className="btn btn-primary btn-block">
            Sign In & Save Predictions
          </button>
        </form>
      </div>
    </div>
  );
}
