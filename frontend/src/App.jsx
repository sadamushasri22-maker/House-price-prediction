import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import PropertyForm from './components/PropertyForm';
import ValuationResultCard from './components/ValuationResultCard';
import FeatureImportanceCard from './components/FeatureImportanceCard';
import FinancialCalculatorsCard from './components/FinancialCalculatorsCard';
import BatchPredictionCard from './components/BatchPredictionCard';
import AuthModal from './components/AuthModal';
import HistoryDrawer from './components/HistoryDrawer';

const CITIES = [
  "Algona", "Auburn", "Beaux Arts", "Bellevue", "Black Diamond", "Bothell", "Burien",
  "Carnation", "Clyde Hill", "Covington", "Des Moines", "Duvall", "Enumclaw", "Fall City",
  "Federal Way", "Inglewood-Finn Hill", "Issaquah", "Kenmore", "Kent", "Kirkland",
  "Lake Forest Park", "Maple Valley", "Medina", "Mercer Island", "Milton", "Newcastle",
  "Normandy Park", "North Bend", "Pacific", "Preston", "Ravensdale", "Redmond", "Redondo",
  "Renton", "Sammamish", "SeaTac", "Seattle", "Shoreline", "Skykomish", "Snoqualmie",
  "Snoqualmie Pass", "Tukwila", "Vashon", "Woodinville"
];

const ZIPCODES = [
  "98001", "98002", "98003", "98004", "98005", "98006", "98007", "98008", "98010", "98011",
  "98014", "98019", "98022", "98023", "98024", "98027", "98028", "98029", "98030", "98031",
  "98032", "98033", "98034", "98038", "98039", "98040", "98042", "98045", "98047", "98052",
  "98053", "98055", "98056", "98058", "98059", "98065", "98070", "98072", "98074", "98075",
  "98077", "98092", "98102", "98103", "98105", "98106", "98107", "98108", "98109", "98112",
  "98115", "98116", "98117", "98118", "98119", "98122", "98125", "98126", "98133", "98136",
  "98144", "98146", "98148", "98155", "98166", "98168", "98177", "98178", "98188", "98198", "98199"
];

export default function App() {
  const [formData, setFormData] = useState({
    bedrooms: 3,
    bathrooms: 2.25,
    sqft_living: 2000,
    sqft_lot: 7500,
    floors: 2,
    waterfront: 0,
    view: 0,
    condition: 3,
    sqft_above: 1600,
    sqft_basement: 400,
    yr_built: 1985,
    yr_renovated: 0,
    city: 'Seattle',
    zipcode: '98115'
  });

  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [realMetrics, setRealMetrics] = useState(null);
  
  // Auth & Database State
  const [user, setUser] = useState(null);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authEmail, setAuthEmail] = useState('');
  const [authName, setAuthName] = useState('');
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);

  useEffect(() => {
    // Load real metrics from backend API
    fetch('/api/metrics')
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success' && data.metrics) {
          setRealMetrics(data.metrics);
        }
      })
      .catch(err => console.warn('Metrics API load fallback', err));

    // Load persisted user session from localStorage
    const savedUser = localStorage.getItem('estimahouse_user');
    if (savedUser) {
      try {
        const u = JSON.parse(savedUser);
        setUser(u);
        fetchHistory(u.email);
      } catch (err) {
        console.error('Failed to load user session', err);
      }
    }
  }, []);

  const handleManualEmailLogin = async (e) => {
    e.preventDefault();
    if (!authEmail) return;

    const emailUser = {
      email: authEmail,
      name: authName || authEmail.split('@')[0]
    };

    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(emailUser)
      });
      if (res.ok) {
        const data = await res.json();
        if (data.status === 'success') {
          setUser(data.user);
          localStorage.setItem('estimahouse_user', JSON.stringify(data.user));
          fetchHistory(data.user.email);
          setShowAuthModal(false);
          return;
        }
      }
    } catch (err) {
      console.warn('Email login fallback');
    }

    setUser(emailUser);
    localStorage.setItem('estimahouse_user', JSON.stringify(emailUser));
    setShowAuthModal(false);
  };

  const fetchHistory = async (email) => {
    try {
      const res = await fetch(`/api/history?email=${encodeURIComponent(email)}`);
      if (res.ok) {
        const data = await res.json();
        if (data.status === 'success') {
          setHistory(data.history || []);
        }
      }
    } catch (err) {
      console.warn('Could not fetch history from database', err);
    }
  };

  const handleLogout = () => {
    setUser(null);
    setHistory([]);
    localStorage.removeItem('estimahouse_user');
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'city' || name === 'zipcode' ? value : Number(value)
    }));
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    setLoading(true);

    const payload = {
      ...formData,
      user_email: user ? user.email : null
    };

    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        const data = await response.json();
        if (data.status === 'success') {
          setPrediction(data.estimated_price);
          setLoading(false);
          if (user) fetchHistory(user.email);
          return;
        }
      }
    } catch (err) {
      console.warn('Backend API request failed, calculating local estimate fallback...', err);
    }

    setTimeout(() => {
      let basePrice = formData.sqft_living * 260;
      basePrice += formData.bedrooms * 15000;
      basePrice += formData.bathrooms * 22000;
      if (formData.waterfront === 1) basePrice *= 1.45;
      if (formData.view > 0) basePrice *= (1 + formData.view * 0.08);
      if (formData.condition > 3) basePrice *= (1 + (formData.condition - 3) * 0.05);
      if (['Bellevue', 'Mercer Island', 'Medina'].includes(formData.city)) basePrice *= 1.35;
      
      const resPrice = Math.round(basePrice);
      setPrediction(resPrice);
      setLoading(false);

      if (user) {
        setHistory(prev => [
          {
            id: Date.now(),
            city: formData.city,
            zipcode: formData.zipcode,
            sqft_living: formData.sqft_living,
            bedrooms: formData.bedrooms,
            bathrooms: formData.bathrooms,
            estimated_price: resPrice,
            created_at: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          },
          ...prev
        ]);
      }
    }, 600);
  };

  return (
    <div>
      <div className="background-glow">
        <div className="glow-sphere sphere-1"></div>
        <div className="glow-sphere sphere-2"></div>
        <div className="glow-sphere sphere-3"></div>
      </div>

      {/* Navigation Bar */}
      <Navbar
        user={user}
        historyCount={history.length}
        showHistory={showHistory}
        setShowHistory={setShowHistory}
        onOpenAuth={() => setShowAuthModal(true)}
        onLogout={handleLogout}
        realMetrics={realMetrics}
      />

      {/* Main Content */}
      <main className="main-container">
        <section className="hero-section">
          <h1 className="hero-title">EstimaHouse <span className="gradient-text">Valuation Engine</span></h1>
          <p className="hero-subtitle">Instant, high-precision house price estimation powered by XGBoost, CatBoost, LightGBM, and SHAP analytics.</p>
        </section>

        {/* History Panel Drawer */}
        <HistoryDrawer
          show={showHistory}
          onClose={() => setShowHistory(false)}
          user={user}
          history={history}
        />

        <div className="app-grid">
          {/* Left Column: Parameter Form & Batch CSV Engine */}
          <div>
            <PropertyForm
              formData={formData}
              onChange={handleChange}
              onSubmit={handlePredict}
              loading={loading}
              CITIES={CITIES}
              ZIPCODES={ZIPCODES}
            />
            <BatchPredictionCard />
          </div>

          {/* Right Column: Result Card, Feature Importance & Financial Suite */}
          <div className="results-column">
            <ValuationResultCard
              prediction={prediction}
              formData={formData}
              realMetrics={realMetrics}
            />
            <FeatureImportanceCard formData={formData} />
            <FinancialCalculatorsCard prediction={prediction} />
          </div>
        </div>
      </main>

      {/* Auth Modal */}
      <AuthModal
        show={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        authEmail={authEmail}
        setAuthEmail={setAuthEmail}
        authName={authName}
        setAuthName={setAuthName}
        onSubmit={handleManualEmailLogin}
      />

      <footer className="footer">
        <p>&copy; 2026 EstimaHouse AI. Intelligent Real Estate Valuation Platform.</p>
      </footer>
    </div>
  );
}
