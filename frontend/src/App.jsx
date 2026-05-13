import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Upload, Zap, Image as ImageIcon, Layout, ArrowRight, Play, RefreshCw } from 'lucide-react';

const API_BASE = 'http://localhost:8000';

function App() {
  const [file, setFile] = useState(null);
  const [segments, setSegments] = useState(null);
  const [ads, setAds] = useState([]);
  const [loading, setLoading] = useState(false);
  const [winnerId, setWinnerId] = useState(null);
  const [context, setContext] = useState({
    product_name: '',
    product_description: '',
    brand_tone: 'Professional'
  });

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    try {
      const res = await axios.post(`${API_BASE}/upload`, formData);
      setSegments(res.data.segments);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/generate-ads`, context);
      setAds(res.data);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  const handleSimulate = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/simulate-optimization`);
      setAds(res.data.ads);
      setWinnerId(res.data.winner_id);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  const getSampleData = async () => {
    try {
      const res = await axios.get(`${API_BASE}/sample-data`);
      const blob = new Blob([res.data.csv], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'sample_transactions.csv';
      a.click();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 py-4 px-8 flex justify-between items-center sticky top-0 z-50">
        <div className="flex items-center gap-2">
          <div className="bg-indigo-600 p-2 rounded-lg">
            <Zap className="text-white w-6 h-6" />
          </div>
          <h1 className="text-xl font-bold tracking-tight">Agency-in-a-Box</h1>
        </div>
        <button 
          onClick={getSampleData}
          className="text-sm font-medium text-indigo-600 hover:text-indigo-700 transition"
        >
          Download Sample CSV
        </button>
      </header>

      <main className="max-w-7xl mx-auto p-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Config */}
        <div className="space-y-6">
          <section className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Layout className="w-5 h-5 text-indigo-500" />
              1. Customer Data
            </h2>
            <div className="space-y-4">
              <div className="border-2 border-dashed border-gray-200 rounded-xl p-6 text-center hover:border-indigo-300 transition cursor-pointer bg-gray-50">
                <input 
                  type="file" 
                  onChange={(e) => setFile(e.target.files[0])}
                  className="hidden" 
                  id="fileInput"
                />
                <label htmlFor="fileInput" className="cursor-pointer">
                  <Upload className="mx-auto w-8 h-8 text-gray-400 mb-2" />
                  <p className="text-sm text-gray-600">
                    {file ? file.name : "Upload transaction CSV"}
                  </p>
                </label>
              </div>
              <button 
                onClick={handleUpload}
                disabled={!file || loading}
                className="w-full bg-indigo-600 text-white py-2.5 rounded-xl font-medium hover:bg-indigo-700 disabled:opacity-50 transition shadow-lg shadow-indigo-200"
              >
                {loading ? "Processing..." : "Analyze Segments"}
              </button>
            </div>

            {segments && (
              <div className="mt-6 space-y-2">
                <p className="text-xs font-bold text-gray-400 uppercase tracking-wider">Results</p>
                {Object.entries(segments).map(([name, count]) => (
                  <div key={name} className="flex justify-between items-center text-sm bg-gray-50 p-2 rounded-lg">
                    <span className="text-gray-600">{name}</span>
                    <span className="font-bold text-indigo-600">{count}</span>
                  </div>
                ))}
              </div>
            )}
          </section>

          <section className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Zap className="w-5 h-5 text-indigo-500" />
              2. Campaign Vibe
            </h2>
            <div className="space-y-4">
              <div>
                <label className="text-xs font-bold text-gray-400 uppercase">Product Name</label>
                <input 
                  className="w-full mt-1 px-4 py-2 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none transition"
                  placeholder="e.g. Zen Coffee"
                  value={context.product_name}
                  onChange={e => setContext({...context, product_name: e.target.value})}
                />
              </div>
              <div>
                <label className="text-xs font-bold text-gray-400 uppercase">Description</label>
                <textarea 
                  className="w-full mt-1 px-4 py-2 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none transition h-24"
                  placeholder="What makes it special?"
                  value={context.product_description}
                  onChange={e => setContext({...context, product_description: e.target.value})}
                />
              </div>
              <div>
                <label className="text-xs font-bold text-gray-400 uppercase">Brand Tone</label>
                <select 
                  className="w-full mt-1 px-4 py-2 bg-gray-50 border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none transition"
                  value={context.brand_tone}
                  onChange={e => setContext({...context, brand_tone: e.target.value})}
                >
                  <option>Professional</option>
                  <option>Playful</option>
                  <option>Luxury</option>
                  <option>Aggressive</option>
                </select>
              </div>
              <button 
                onClick={handleGenerate}
                disabled={!context.product_name || loading}
                className="w-full bg-black text-white py-2.5 rounded-xl font-medium hover:bg-gray-800 disabled:opacity-50 transition"
              >
                Generate Hyper-Ads
              </button>
            </div>
          </section>
        </div>

        {/* Right Column: Ads Gallery */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">Generated Variations</h2>
            {ads.length > 0 && (
              <button 
                onClick={handleSimulate}
                className="flex items-center gap-2 bg-green-500 text-white px-4 py-2 rounded-xl text-sm font-bold hover:bg-green-600 transition shadow-lg shadow-green-100"
              >
                <Play className="w-4 h-4" /> Simulate A/B Test
              </button>
            )}
          </div>

          {ads.length === 0 ? (
            <div className="bg-white border-2 border-dashed border-gray-100 rounded-3xl h-[600px] flex flex-col items-center justify-center text-gray-400">
              <ImageIcon className="w-16 h-16 mb-4 opacity-20" />
              <p>Your AI-generated ads will appear here</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {ads.map((ad) => (
                <div 
                  key={ad.id} 
                  className={`bg-white rounded-3xl overflow-hidden shadow-xl transition-all duration-500 border-4 ${winnerId === ad.id ? 'border-green-400 scale-[1.02]' : 'border-transparent opacity-90'}`}
                >
                  <div className="relative aspect-square">
                    <img src={ad.image_url} alt="Ad" className="w-full h-full object-cover" />
                    <div className="absolute top-4 left-4 bg-white/90 backdrop-blur px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-tighter shadow-sm">
                      {ad.segment}
                    </div>
                    {winnerId === ad.id && (
                      <div className="absolute top-4 right-4 bg-green-500 text-white px-3 py-1 rounded-full text-[10px] font-black uppercase shadow-lg animate-pulse">
                        Winning Varation
                      </div>
                    )}
                  </div>
                  <div className="p-6 space-y-3">
                    <h3 className="font-black text-xl leading-tight">{ad.copy.split('\n')[0].replace('Headline: ', '')}</h3>
                    <p className="text-gray-500 text-sm leading-relaxed">
                      {ad.copy.split('\n')[1]?.replace('Body: ', '')}
                    </p>
                    <div className="pt-4 flex justify-between items-center border-t border-gray-50">
                      <button className="bg-indigo-600 text-white px-6 py-2 rounded-lg text-sm font-bold hover:bg-indigo-700 transition">
                         {ad.copy.split('\n')[2]?.replace('CTA: ', '') || 'Shop Now'}
                      </button>
                      <div className="text-right">
                        <p className="text-[10px] font-bold text-gray-400 uppercase">Performance</p>
                        <p className="text-xs font-black text-indigo-600">CTR: {(ad.clicks / ad.impressions * 100).toFixed(2)}%</p>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
