import React, { useState, useEffect } from 'react';
import {
  Building2,
  CheckCircle2,
  TrendingUp,
  ShieldCheck,
  Lightbulb,
  Award,
  Sparkles,
  Zap,
  BarChart3,
  MapPin,
  Cpu
} from 'lucide-react';

// Count-Up Custom React Hook for smooth price animation
function useCountUp(targetValue, duration = 1200) {
  const [count, setCount] = useState(0);

  useEffect(() => {
    if (!targetValue) {
      setCount(0);
      return;
    }

    let start = 0;
    const end = parseInt(targetValue, 10);
    const totalSteps = 40;
    const increment = (end - start) / totalSteps;
    const stepTime = Math.abs(Math.floor(duration / totalSteps));

    let currentStep = 0;
    const timer = setInterval(() => {
      currentStep += 1;
      start += increment;
      if (currentStep >= totalSteps) {
        setCount(end);
        clearInterval(timer);
      } else {
        setCount(Math.round(start));
      }
    }, stepTime);

    return () => clearInterval(timer);
  }, [targetValue, duration]);

  return count;
}

export default function ValuationResultCard({ prediction, formData, realMetrics }) {
  const animatedPrice = useCountUp(prediction, 1200);

  if (!prediction) {
    return (
      <div className="glass-card result-card" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        <div style={{ textAlign: 'center', padding: '1rem 0 0.5rem' }}>
          <div className="placeholder-icon" style={{ margin: '0 auto 1rem' }}>
            <Building2 size={32} />
          </div>
          <h3 style={{ fontSize: '1.4rem', fontWeight: '700', fontFamily: 'Outfit, sans-serif' }}>
            EstimaHouse AI Valuation Ready
          </h3>
          <p style={{ color: '#94a3b8', fontSize: '0.9rem', maxWidth: '420px', margin: '0.4rem auto 0', lineHeight: '1.5' }}>
            Fill out property parameters on the left and click <strong>Calculate EstimaHouse Value</strong> for real-time ML valuation.
          </p>
        </div>

        {/* Regional Market Benchmarks Card */}
        <div className="breakdown-card">
          <h4 className="breakdown-title" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <MapPin size={16} color="#3b82f6" /> Regional King County Market Benchmarks
          </h4>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', marginTop: '0.75rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.6rem 0.85rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', fontSize: '0.85rem' }}>
              <span>Bellevue, WA (98004)</span>
              <strong style={{ color: '#3b82f6' }}>$845,000 Avg ($325 / sqft)</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.6rem 0.85rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', fontSize: '0.85rem' }}>
              <span>Redmond, WA (98052)</span>
              <strong style={{ color: '#8b5cf6' }}>$710,000 Avg ($295 / sqft)</strong>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '0.6rem 0.85rem', background: 'rgba(255,255,255,0.03)', borderRadius: '8px', fontSize: '0.85rem' }}>
              <span>Seattle, WA (98115)</span>
              <strong style={{ color: '#10b981' }}>$620,000 Avg ($280 / sqft)</strong>
            </div>
          </div>
        </div>

        {/* Model Intelligence Specs */}
        <div className="stats-row" style={{ background: 'rgba(15,23,42,0.5)', padding: '1rem', borderRadius: '12px' }}>
          <div className="stat-item">
            <span className="stat-val" style={{ color: '#3b82f6' }}>83.2%</span>
            <span className="stat-lbl">Log-R² Fit</span>
          </div>
          <div className="stat-item">
            <span className="stat-val" style={{ color: '#8b5cf6' }}>Ensemble</span>
            <span className="stat-lbl">CatBoost & LightGBM</span>
          </div>
          <div className="stat-item">
            <span className="stat-val" style={{ color: '#10b981' }}>4,551</span>
            <span className="stat-lbl">Training Records</span>
          </div>
          <div className="stat-item">
            <span className="stat-val" style={{ color: '#f59e0b' }}>&plusmn;6.5%</span>
            <span className="stat-lbl">Confidence Bound</span>
          </div>
        </div>
      </div>
    );
  }

  // Calculate market average estimate per sqft for comparison ($280/sqft average for King County)
  const avgSqftPrice = 280;
  const avgMarketPrice = formData.sqft_living * avgSqftPrice;
  const priceDiff = prediction - avgMarketPrice;
  const priceDiffPct = ((priceDiff / avgMarketPrice) * 100).toFixed(1);

  // Derive Property Badges
  const badges = [];
  if (['Bellevue', 'Mercer Island', 'Medina', 'Seattle', 'Kirkland', 'Sammamish'].includes(formData.city)) {
    badges.push({ name: 'Premium Location', color: '#3b82f6' });
  }
  if (formData.waterfront === 1) {
    badges.push({ name: 'Waterfront Premium', color: '#06b6d4' });
  }
  if (formData.sqft_living >= 2800) {
    badges.push({ name: 'Large Living Area', color: '#8b5cf6' });
  }
  if (formData.condition >= 4) {
    badges.push({ name: 'Excellent Condition', color: '#10b981' });
  }
  if (formData.yr_built >= 2000 || formData.yr_renovated >= 2010) {
    badges.push({ name: 'Modern Construction', color: '#f59e0b' });
  }

  return (
    <div className="glass-card result-card">
      <div className="result-header">
        <span className="result-tag"><CheckCircle2 size={14} /> Valuation Complete</span>
        <h3 className="result-subtitle">EstimaHouse Value</h3>
      </div>

      {/* Animated Count Up Price */}
      <div className="price-display">
        <span className="currency-symbol">$</span>
        <span>{animatedPrice.toLocaleString('en-US')}</span>
      </div>

      {/* Dynamic Confidence Interval (±6.5%) */}
      <div className="range-box">
        <div className="range-label">Model Uncertainty Bound (&plusmn;6.5%)</div>
        <div className="range-values">
          <span>${Math.round(prediction * 0.935).toLocaleString('en-US')}</span>
          <span className="range-separator">&mdash;</span>
          <span>${Math.round(prediction * 1.065).toLocaleString('en-US')}</span>
        </div>
      </div>

      {/* Property Insights Badges */}
      {badges.length > 0 && (
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem', margin: '1rem 0' }}>
          {badges.map((b, i) => (
            <span
              key={i}
              style={{
                background: `rgba(255,255,255,0.06)`,
                border: `1px solid ${b.color}`,
                color: b.color,
                padding: '0.25rem 0.65rem',
                borderRadius: '50px',
                fontSize: '0.75rem',
                fontWeight: '600',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.35rem'
              }}
            >
              <Award size={12} /> {b.name}
            </span>
          ))}
        </div>
      )}

      {/* Metrics Row */}
      <div className="metrics-grid">
        <div className="metric-box">
          <div className="metric-icon"><TrendingUp size={18} /></div>
          <div className="metric-info">
            <span className="metric-title">Price per Sqft</span>
            <span className="metric-value">${(prediction / formData.sqft_living).toFixed(2)} / sqft</span>
          </div>
        </div>
        <div className="metric-box">
          <div className="metric-icon"><ShieldCheck size={18} /></div>
          <div className="metric-info">
            <span className="metric-title">Model Fit (Log-R²)</span>
            <span className="metric-value">{realMetrics?.["Log R2 Score"] || "0.832"} R²</span>
          </div>
        </div>
      </div>

      {/* AI Property Valuation Summary */}
      <div className="breakdown-card" style={{ marginTop: '1rem' }}>
        <h4 className="breakdown-title" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <Sparkles size={16} color="#3b82f6" /> AI Property Valuation Summary
        </h4>
        <p style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: '1.5', marginTop: '0.4rem' }}>
          This property in <strong>{formData.city}, WA {formData.zipcode}</strong> commands a projected valuation of <strong>${prediction.toLocaleString('en-US')}</strong> based on its <strong>{formData.sqft_living.toLocaleString()} sqft</strong> living area ({formData.bedrooms} beds, {formData.bathrooms} baths).
          {formData.waterfront === 1 ? ' The waterfront location provides a high market valuation premium.' : ''}
          {formData.condition >= 4 ? ' Excellent condition rating further boosts market appeal.' : ''}
        </p>
      </div>

      {/* Market Price Comparison */}
      <div className="breakdown-card" style={{ marginTop: '0.85rem' }}>
        <h4 className="breakdown-title" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <BarChart3 size={16} color="#10b981" /> Market Benchmark Comparison
        </h4>
        <div style={{ marginTop: '0.5rem', fontSize: '0.82rem', color: '#94a3b8' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.35rem' }}>
            <span>EstimaHouse Valuation:</span>
            <strong style={{ color: '#10b981' }}>${prediction.toLocaleString('en-US')}</strong>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.35rem' }}>
            <span>County Market Average ({formData.sqft_living} sqft):</span>
            <span>${avgMarketPrice.toLocaleString('en-US')}</span>
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', paddingTop: '0.35rem', borderTop: '1px dashed rgba(255,255,255,0.1)' }}>
            <span>Market Differential:</span>
            <span style={{ color: priceDiff >= 0 ? '#10b981' : '#f59e0b', fontWeight: '700' }}>
              {priceDiff >= 0 ? `+${priceDiffPct}% Above Average` : `${priceDiffPct}% Below Average`}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
