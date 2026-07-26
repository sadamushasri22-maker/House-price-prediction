import React from 'react';
import {
  Sliders,
  Bed,
  Bath,
  Building2,
  Maximize,
  Square,
  ArrowUp,
  ArrowDown,
  MapPin,
  Mail,
  Droplets,
  Eye,
  Star,
  Hammer,
  PaintRoller,
  Wand2,
  Loader2
} from 'lucide-react';

export default function PropertyForm({ formData, onChange, onSubmit, loading, CITIES, ZIPCODES }) {
  return (
    <div className="glass-card form-card">
      <div className="card-header">
        <h2 className="card-title"><Sliders size={22} color="#3b82f6" /> Property Parameters</h2>
        <p className="card-desc">Enter property details below for an instant ML valuation.</p>
      </div>

      <form onSubmit={onSubmit}>
        {/* Section 1: Specifications */}
        <div className="form-section">
          <h3 className="section-title"><Bed size={16} color="#8b5cf6" /> Core Specifications</h3>
          <div className="input-grid grid-3">
            <div className="input-group">
              <label>Bedrooms</label>
              <div className="input-wrapper">
                <Bed className="input-icon" size={16} />
                <input type="number" name="bedrooms" min="1" max="10" value={formData.bedrooms} onChange={onChange} required />
              </div>
            </div>
            <div className="input-group">
              <label>Bathrooms</label>
              <div className="input-wrapper">
                <Bath className="input-icon" size={16} />
                <input type="number" name="bathrooms" step="0.25" min="0.5" max="10" value={formData.bathrooms} onChange={onChange} required />
              </div>
            </div>
            <div className="input-group">
              <label>Floors</label>
              <div className="input-wrapper">
                <Building2 className="input-icon" size={16} />
                <input type="number" name="floors" step="0.5" min="1" max="4" value={formData.floors} onChange={onChange} required />
              </div>
            </div>
          </div>
        </div>

        {/* Section 2: Area & Dimensions */}
        <div className="form-section">
          <h3 className="section-title"><Maximize size={16} color="#8b5cf6" /> Living Space & Lot (sq. ft.)</h3>
          <div className="input-grid grid-2">
            <div className="input-group">
              <label>Living Area (sqft)</label>
              <div className="input-wrapper">
                <Maximize className="input-icon" size={16} />
                <input type="number" name="sqft_living" min="300" max="15000" value={formData.sqft_living} onChange={onChange} required />
              </div>
            </div>
            <div className="input-group">
              <label>Lot Size (sqft)</label>
              <div className="input-wrapper">
                <Square className="input-icon" size={16} />
                <input type="number" name="sqft_lot" min="500" max="500000" value={formData.sqft_lot} onChange={onChange} required />
              </div>
            </div>
            <div className="input-group">
              <label>Above Ground (sqft)</label>
              <div className="input-wrapper">
                <ArrowUp className="input-icon" size={16} />
                <input type="number" name="sqft_above" min="300" max="12000" value={formData.sqft_above} onChange={onChange} required />
              </div>
            </div>
            <div className="input-group">
              <label>Basement (sqft)</label>
              <div className="input-wrapper">
                <ArrowDown className="input-icon" size={16} />
                <input type="number" name="sqft_basement" min="0" max="5000" value={formData.sqft_basement} onChange={onChange} required />
              </div>
            </div>
          </div>
        </div>

        {/* Section 3: Location & Feature Ratings */}
        <div className="form-section">
          <h3 className="section-title"><MapPin size={16} color="#8b5cf6" /> Location & Ratings</h3>
          <div className="input-grid grid-2">
            <div className="input-group">
              <label>City</label>
              <div className="input-wrapper">
                <MapPin className="input-icon" size={16} />
                <select name="city" value={formData.city} onChange={onChange} required>
                  {CITIES.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>
            </div>
            <div className="input-group">
              <label>Zipcode</label>
              <div className="input-wrapper">
                <Mail className="input-icon" size={16} />
                <select name="zipcode" value={formData.zipcode} onChange={onChange} required>
                  {ZIPCODES.map(z => <option key={z} value={z}>WA {z}</option>)}
                </select>
              </div>
            </div>
            <div className="input-group">
              <label>Waterfront Property</label>
              <div className="input-wrapper">
                <Droplets className="input-icon" size={16} />
                <select name="waterfront" value={formData.waterfront} onChange={onChange} required>
                  <option value={0}>No (Standard Property)</option>
                  <option value={1}>Yes (Waterfront Access)</option>
                </select>
              </div>
            </div>
            <div className="input-group">
              <label>View Rating (0 - 4)</label>
              <div className="input-wrapper">
                <Eye className="input-icon" size={16} />
                <select name="view" value={formData.view} onChange={onChange} required>
                  <option value={0}>0 - Standard View</option>
                  <option value={1}>1 - Fair View</option>
                  <option value={2}>2 - Good View</option>
                  <option value={3}>3 - Excellent View</option>
                  <option value={4}>4 - Premium View</option>
                </select>
              </div>
            </div>
            <div className="input-group full-width">
              <label>Property Condition (1 - 5)</label>
              <div className="input-wrapper">
                <Star className="input-icon" size={16} />
                <select name="condition" value={formData.condition} onChange={onChange} required>
                  <option value={1}>1 - Poor / Fixer Upper</option>
                  <option value={2}>2 - Fair Condition</option>
                  <option value={3}>3 - Good / Average</option>
                  <option value={4}>4 - Very Good</option>
                  <option value={5}>5 - Excellent / Turnkey</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        {/* Section 4: Construction & Renovation */}
        <div className="form-section">
          <h3 className="section-title"><Hammer size={16} color="#8b5cf6" /> Age & Renovation</h3>
          <div className="input-grid grid-2">
            <div className="input-group">
              <label>Year Built</label>
              <div className="input-wrapper">
                <Hammer className="input-icon" size={16} />
                <input type="number" name="yr_built" min="1900" max="2026" value={formData.yr_built} onChange={onChange} required />
              </div>
            </div>
            <div className="input-group">
              <label>Year Renovated (0 if none)</label>
              <div className="input-wrapper">
                <PaintRoller className="input-icon" size={16} />
                <input type="number" name="yr_renovated" min="0" max="2026" value={formData.yr_renovated} onChange={onChange} required />
              </div>
            </div>
          </div>
        </div>

        <button type="submit" disabled={loading} className="btn btn-primary btn-block">
          {loading ? (
            <span><Loader2 className="animate-spin" size={18} /> Estimating Value...</span>
          ) : (
            <span><Wand2 size={18} /> Calculate EstimaHouse Value</span>
          )}
        </button>
      </form>
    </div>
  );
}
