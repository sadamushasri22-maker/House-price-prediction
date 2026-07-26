import React, { useState } from 'react';
import { Calculator, DollarSign, TrendingUp, ShieldAlert, Percent, Calendar } from 'lucide-react';

export default function FinancialCalculatorsCard({ prediction }) {
  const price = prediction || 600000;
  
  // Mortgage Controls
  const [downPaymentPct, setDownPaymentPct] = useState(20);
  const [interestRate, setInterestRate] = useState(6.5);
  const [loanTenureYears, setLoanTenureYears] = useState(30);

  // Financial Calculations
  const downPaymentAmount = (price * downPaymentPct) / 100;
  const loanAmount = price - downPaymentAmount;
  const monthlyRate = interestRate / 100 / 12;
  const totalMonths = loanTenureYears * 12;

  // Monthly EMI Formula: P * r * (1+r)^n / ((1+r)^n - 1)
  const monthlyEMI = Math.round(
    (loanAmount * monthlyRate * Math.pow(1 + monthlyRate, totalMonths)) /
    (Math.pow(1 + monthlyRate, totalMonths) - 1)
  );

  // Property Tax (~0.95% annual rate in WA)
  const annualTax = Math.round(price * 0.0095);
  const monthlyTax = Math.round(annualTax / 12);

  // Insurance (~$1,200 annual)
  const monthlyInsurance = Math.round((price * 0.002) / 12 + 40);

  // Total Monthly Outflow
  const totalMonthlyPayment = monthlyEMI + monthlyTax + monthlyInsurance;

  // Future Appreciation Predictions
  const val3yr = Math.round(price * 1.12);
  const val5yr = Math.round(price * 1.22);
  const val10yr = Math.round(price * 1.48);

  return (
    <div className="glass-card" style={{ marginTop: '1.5rem' }}>
      <div className="info-card-header" style={{ marginBottom: '1rem' }}>
        <Calculator size={20} color="#10b981" />
        <h4 style={{ fontSize: '1.05rem', fontWeight: '700' }}>Financial Suite & Mortgage EMI Calculator</h4>
      </div>

      {/* Mortgage Settings Sliders */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '1.25rem' }}>
        <div>
          <label style={{ fontSize: '0.78rem', color: '#94a3b8' }}>Down Payment ({downPaymentPct}%): ${downPaymentAmount.toLocaleString()}</label>
          <input
            type="range"
            min="5"
            max="50"
            step="5"
            value={downPaymentPct}
            onChange={(e) => setDownPaymentPct(Number(e.target.value))}
            style={{ width: '100%', accentColor: '#3b82f6', marginTop: '0.35rem' }}
          />
        </div>
        <div>
          <label style={{ fontSize: '0.78rem', color: '#94a3b8' }}>Interest Rate ({interestRate}%):</label>
          <input
            type="range"
            min="3.0"
            max="10.0"
            step="0.25"
            value={interestRate}
            onChange={(e) => setInterestRate(Number(e.target.value))}
            style={{ width: '100%', accentColor: '#10b981', marginTop: '0.35rem' }}
          />
        </div>
        <div>
          <label style={{ fontSize: '0.78rem', color: '#94a3b8' }}>Loan Tenure:</label>
          <select
            value={loanTenureYears}
            onChange={(e) => setLoanTenureYears(Number(e.target.value))}
            style={{ width: '100%', padding: '0.4rem', background: 'rgba(15,23,42,0.6)', color: '#f8fafc', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '6px', marginTop: '0.35rem' }}
          >
            <option value={30}>30-Year Fixed Loan</option>
            <option value={15}>15-Year Fixed Loan</option>
          </select>
        </div>
      </div>

      {/* Monthly Payment Breakdown Grid */}
      <div className="stats-row" style={{ background: 'rgba(15,23,42,0.5)', padding: '1rem', borderRadius: '10px', marginBottom: '1.25rem' }}>
        <div className="stat-item">
          <span className="stat-val" style={{ color: '#3b82f6' }}>${monthlyEMI.toLocaleString()}</span>
          <span className="stat-lbl">Principal & Interest (EMI)</span>
        </div>
        <div className="stat-item">
          <span className="stat-val" style={{ color: '#f59e0b' }}>${monthlyTax.toLocaleString()}</span>
          <span className="stat-lbl">Estimated Property Tax</span>
        </div>
        <div className="stat-item">
          <span className="stat-val" style={{ color: '#06b6d4' }}>${monthlyInsurance.toLocaleString()}</span>
          <span className="stat-lbl">Home Insurance / mo</span>
        </div>
        <div className="stat-item">
          <span className="stat-val" style={{ color: '#10b981' }}>${totalMonthlyPayment.toLocaleString()}</span>
          <span className="stat-lbl">Total Monthly Outflow</span>
        </div>
      </div>

      {/* Future Price Appreciation Predictor */}
      <div className="breakdown-card">
        <h4 className="breakdown-title" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <TrendingUp size={16} color="#10b981" /> Investment ROI & Future Appreciation
        </h4>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.75rem', marginTop: '0.65rem', textAlign: 'center' }}>
          <div style={{ background: 'rgba(255,255,255,0.03)', padding: '0.65rem', borderRadius: '8px' }}>
            <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>3-Yr Projected</span>
            <div style={{ fontSize: '1rem', fontWeight: '700', color: '#f8fafc', marginTop: '0.2rem' }}>${val3yr.toLocaleString()}</div>
            <span style={{ fontSize: '0.7rem', color: '#10b981' }}>+12% ROI</span>
          </div>
          <div style={{ background: 'rgba(255,255,255,0.03)', padding: '0.65rem', borderRadius: '8px' }}>
            <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>5-Yr Projected</span>
            <div style={{ fontSize: '1rem', fontWeight: '700', color: '#f8fafc', marginTop: '0.2rem' }}>${val5yr.toLocaleString()}</div>
            <span style={{ fontSize: '0.7rem', color: '#10b981' }}>+22% ROI</span>
          </div>
          <div style={{ background: 'rgba(255,255,255,0.03)', padding: '0.65rem', borderRadius: '8px' }}>
            <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>10-Yr Projected</span>
            <div style={{ fontSize: '1rem', fontWeight: '700', color: '#f8fafc', marginTop: '0.2rem' }}>${val10yr.toLocaleString()}</div>
            <span style={{ fontSize: '0.7rem', color: '#10b981' }}>+48% ROI</span>
          </div>
        </div>
      </div>
    </div>
  );
}
