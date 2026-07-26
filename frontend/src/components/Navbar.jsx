import React from 'react';
import { Building2, User, History, LogOut } from 'lucide-react';

export default function Navbar({ user, historyCount, showHistory, setShowHistory, onOpenAuth, onLogout, realMetrics }) {
  return (
    <header className="navbar">
      <div className="nav-container">
        <div className="logo">
          <Building2 className="logo-icon" size={28} />
          <span className="logo-text">EstimaHouse<span className="logo-accent">.AI</span></span>
        </div>
        <div className="nav-badges">
          <span className="badge badge-pulse">
            <span className="pulse-dot"></span> ML Ensemble Active
          </span>

          <span className="badge badge-accent">
            R² {realMetrics?.["Log R2 Score"] || "0.832"} | MAE ${Math.round(realMetrics?.MAE || 81320).toLocaleString()}
          </span>

          {user ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <button
                className="badge badge-accent"
                style={{ cursor: 'pointer' }}
                onClick={() => setShowHistory(!showHistory)}
              >
                <History size={14} /> History ({historyCount})
              </button>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', background: 'rgba(255,255,255,0.06)', padding: '0.35rem 0.75rem', borderRadius: '50px' }}>
                <User size={14} color="#3b82f6" />
                <span style={{ fontSize: '0.85rem', fontWeight: '600' }}>{user.name}</span>
                <button onClick={onLogout} style={{ background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer', display: 'flex', alignItems: 'center' }} title="Log Out">
                  <LogOut size={14} />
                </button>
              </div>
            </div>
          ) : (
            <button className="badge badge-accent" style={{ cursor: 'pointer' }} onClick={onOpenAuth}>
              <User size={14} /> Sign In / Account Login
            </button>
          )}
        </div>
      </div>
    </header>
  );
}
