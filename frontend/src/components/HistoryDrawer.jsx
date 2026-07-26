import React from 'react';
import { History, X } from 'lucide-react';

export default function HistoryDrawer({ show, onClose, user, history }) {
  if (!show || !user) return null;

  return (
    <div className="glass-card" style={{ marginBottom: '2rem', border: '1px solid rgba(59, 130, 246, 0.4)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.75rem' }}>
        <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '1.1rem', fontWeight: '700' }}>
          <History size={18} color="#3b82f6" /> Saved Valuation History ({user.email})
        </h3>
        <button onClick={onClose} style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer' }}>
          <X size={18} />
        </button>
      </div>
      {history.length === 0 ? (
        <p style={{ color: '#94a3b8', fontSize: '0.9rem' }}>No saved predictions yet. Generate an estimate to log it in the database!</p>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '0.85rem' }}>
          {history.map((h, i) => (
            <div key={i} style={{ background: 'rgba(15,23,42,0.6)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '10px', padding: '0.85rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', color: '#94a3b8', marginBottom: '0.35rem' }}>
                <span>{h.city}, WA {h.zipcode}</span>
                <span>{h.created_at}</span>
              </div>
              <div style={{ fontSize: '1.25rem', fontWeight: '800', color: '#10b981' }}>
                ${Number(h.estimated_price).toLocaleString('en-US')}
              </div>
              <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '0.2rem' }}>
                {h.sqft_living} sqft • {h.bedrooms} Bed • {h.bathrooms} Bath
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
