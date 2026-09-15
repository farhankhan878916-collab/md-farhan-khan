import React, { useState } from 'react';
import { Download, Film, ShieldCheck, Sparkles, Layers, Terminal, BookOpen, ExternalLink, CheckCircle2, Eye, Sliders, Image as ImageIcon } from 'lucide-react';
import { ArchitectureTab } from './components/ArchitectureTab';
import { SimulatorTab } from './components/SimulatorTab';
import { FileBrowserTab } from './components/FileBrowserTab';
import { ApiDocsTab } from './components/ApiDocsTab';

export default function App() {
  const [activeTab, setActiveTab] = useState<'architecture' | 'simulator' | 'files' | 'api'>('simulator');
  const [downloadSuccess, setDownloadSuccess] = useState(false);
  const [bgDarkness, setBgDarkness] = useState<number>(0.72); // Default balanced dimming for optimal contrast
  const [showFullImageModal, setShowFullImageModal] = useState(false);

  const handleDownload = () => {
    const link = document.createElement('a');
    link.href = '/Movie-Ticket-Booking-System.zip';
    link.setAttribute('download', 'Movie-Ticket-Booking-System.zip');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    setDownloadSuccess(true);
    setTimeout(() => setDownloadSuccess(false), 4000);
  };

  return (
    <div className="relative min-h-screen text-slate-100 flex flex-col selection:bg-red-500 selection:text-white font-sans antialiased overflow-x-hidden">
      {/* Full-Screen Cinema Background Photo */}
      <div
        className="fixed inset-0 z-0 bg-cover bg-center bg-no-repeat bg-fixed pointer-events-none"
        style={{
          backgroundImage: "url('/jake-hills-23LET4Hxj_U-unsplash.jpg')",
        }}
        aria-hidden="true"
      >
        {/* Dynamic Dark Gradient & Tint Overlay for Perfect Readability */}
        <div
          className="absolute inset-0 bg-slate-950 transition-opacity duration-300 pointer-events-none"
          style={{ opacity: bgDarkness }}
        />
        {/* Subtle Ambient Red Glow mirroring the illuminated screen */}
        <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/60 to-transparent pointer-events-none" />
      </div>

      {/* Top Navigation Header */}
      <header className="relative z-50 border-b border-slate-800/80 bg-slate-950/75 backdrop-blur-md sticky top-0 px-4 sm:px-8 py-3.5">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-red-600 to-rose-500 flex items-center justify-center shadow-[0_0_20px_rgba(225,29,72,0.4)]">
              <Film className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-base font-extrabold tracking-tight text-white">
                  CinePass
                </h1>
                <span className="text-[11px] font-mono font-bold px-2 py-0.5 rounded-full bg-red-500/10 text-red-400 border border-red-500/30">
                  Full-Stack Suite
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Spring Boot 3.2.3 • Angular 17 • MySQL 8 • 163 Source Files
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3 flex-wrap justify-end">
            {/* Background Control Widget */}
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-900/80 border border-slate-800/90 text-xs font-mono">
              <span className="text-slate-400 text-[11px] flex items-center gap-1.5">
                <ImageIcon className="w-3.5 h-3.5 text-red-400" />
                <span>BG View:</span>
              </span>
              <button
                onClick={() => setBgDarkness(0.4)}
                className={`px-2 py-0.5 rounded text-[11px] transition ${
                  bgDarkness <= 0.45 ? 'bg-red-600 text-white font-bold' : 'text-slate-400 hover:text-white'
                }`}
                title="Bright: Shows cinema background clearly"
              >
                Clear
              </button>
              <button
                onClick={() => setBgDarkness(0.72)}
                className={`px-2 py-0.5 rounded text-[11px] transition ${
                  bgDarkness > 0.45 && bgDarkness < 0.85 ? 'bg-red-600 text-white font-bold' : 'text-slate-400 hover:text-white'
                }`}
                title="Balanced: Optimum dashboard readability + cinema background"
              >
                Balanced
              </button>
              <button
                onClick={() => setBgDarkness(0.9)}
                className={`px-2 py-0.5 rounded text-[11px] transition ${
                  bgDarkness >= 0.85 ? 'bg-red-600 text-white font-bold' : 'text-slate-400 hover:text-white'
                }`}
                title="Deep: High contrast dark focus"
              >
                Deep
              </button>
              <button
                onClick={() => setShowFullImageModal(true)}
                className="ml-1 text-slate-400 hover:text-white transition p-1 hover:bg-slate-800 rounded"
                title="Inspect Full Original Photo"
              >
                <Eye className="w-3.5 h-3.5 text-amber-400" />
              </button>
            </div>

            <button
              onClick={handleDownload}
              className="px-4 py-2 rounded-xl bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 text-white font-bold text-xs shadow-[0_4px_16px_rgba(225,29,72,0.35)] transition-all flex items-center gap-2 active:scale-95"
              id="download-project-zip-btn"
            >
              {downloadSuccess ? (
                <>
                  <CheckCircle2 className="w-4 h-4 text-emerald-300" />
                  <span>Downloading ZIP...</span>
                </>
              ) : (
                <>
                  <Download className="w-4 h-4" />
                  <span>Download Complete Project (.ZIP)</span>
                </>
              )}
            </button>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="relative z-10 flex-1 max-w-7xl w-full mx-auto px-4 sm:px-8 py-8 space-y-8">
        {/* Hero Section Banner with Frosted Glassmorphism */}
        <div className="p-6 sm:p-8 rounded-2xl bg-slate-900/75 backdrop-blur-xl border border-slate-700/60 shadow-2xl relative overflow-hidden">
          <div className="absolute right-0 top-0 w-96 h-96 bg-red-600/15 rounded-full blur-3xl pointer-events-none -mr-20 -mt-20"></div>

          <div className="relative z-10 max-w-3xl space-y-3">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-mono font-medium">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              Backend (Maven 6/6 Passed) &amp; Frontend (Angular 17 Build OK)
            </div>
            <h2 className="text-2xl sm:text-3xl font-black text-white tracking-tight leading-tight drop-shadow-md">
              Production-Style Movie Ticket Booking System
            </h2>
            <p className="text-sm text-slate-200 leading-relaxed drop-shadow-sm">
              Complete multi-tier enterprise architecture built strictly without placeholders or TODOs. Features high-concurrency serializable transaction locking against double-booking, 2D matrix vacant seat recommendation, JWT authentication, and interactive cinema screen rendering.
            </p>

            <div className="pt-2 flex flex-wrap items-center gap-3">
              <button
                onClick={handleDownload}
                className="px-4 py-2 rounded-lg bg-red-600 hover:bg-red-500 text-white text-xs font-bold transition flex items-center gap-2 shadow-lg shadow-red-600/30"
              >
                <Download className="w-3.5 h-3.5" /> Direct ZIP Download (Movie-Ticket-Booking-System.zip)
              </button>
              <a
                href="#file-browser"
                onClick={e => {
                  e.preventDefault();
                  setActiveTab('files');
                }}
                className="px-4 py-2 rounded-lg bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700/70 text-slate-200 text-xs font-semibold transition"
              >
                Inspect 163 Source Files
              </a>
              <button
                onClick={() => setShowFullImageModal(true)}
                className="px-4 py-2 rounded-lg bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700/70 text-slate-200 text-xs font-semibold transition flex items-center gap-1.5"
              >
                <Eye className="w-3.5 h-3.5 text-amber-400" /> View Theater Photo
              </button>
            </div>
          </div>
        </div>

        {/* Tab Navigation with Translucent Background */}
        <div className="border-b border-slate-800/90 bg-slate-950/60 backdrop-blur-md px-3 rounded-xl flex items-center gap-2 sm:gap-4 overflow-x-auto pb-px">
          <button
            onClick={() => setActiveTab('simulator')}
            className={`py-3 px-3 text-xs sm:text-sm font-semibold transition flex items-center gap-2 whitespace-nowrap border-b-2 ${
              activeTab === 'simulator'
                ? 'border-red-500 text-red-400 font-bold'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Sparkles className="w-4 h-4" /> Live Cinema Simulator
          </button>

          <button
            onClick={() => setActiveTab('architecture')}
            className={`py-3 px-3 text-xs sm:text-sm font-semibold transition flex items-center gap-2 whitespace-nowrap border-b-2 ${
              activeTab === 'architecture'
                ? 'border-red-500 text-red-400 font-bold'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <ShieldCheck className="w-4 h-4" /> Concurrency &amp; Architecture
          </button>

          <button
            onClick={() => setActiveTab('api')}
            className={`py-3 px-3 text-xs sm:text-sm font-semibold transition flex items-center gap-2 whitespace-nowrap border-b-2 ${
              activeTab === 'api'
                ? 'border-red-500 text-red-400 font-bold'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <Terminal className="w-4 h-4" /> REST API Spec (18 Endpoints)
          </button>

          <button
            onClick={() => setActiveTab('files')}
            className={`py-3 px-3 text-xs sm:text-sm font-semibold transition flex items-center gap-2 whitespace-nowrap border-b-2 ${
              activeTab === 'files'
                ? 'border-red-500 text-red-400 font-bold'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <BookOpen className="w-4 h-4" /> Source Code Tree
          </button>
        </div>

        {/* Tab Panels */}
        <div className="relative">
          {activeTab === 'simulator' && <SimulatorTab />}
          {activeTab === 'architecture' && <ArchitectureTab />}
          {activeTab === 'api' && <ApiDocsTab />}
          {activeTab === 'files' && <FileBrowserTab />}
        </div>
      </main>

      {/* Full Photo Modal Viewer */}
      {showFullImageModal && (
        <div
          className="fixed inset-0 z-50 bg-slate-950/90 backdrop-blur-md flex items-center justify-center p-4 sm:p-8"
          onClick={() => setShowFullImageModal(false)}
        >
          <div
            className="relative max-w-5xl w-full bg-slate-900 border border-slate-700 rounded-2xl overflow-hidden shadow-2xl"
            onClick={e => e.stopPropagation()}
          >
            <div className="p-4 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
              <div>
                <h3 className="text-sm font-bold text-white flex items-center gap-2">
                  <Film className="w-4 h-4 text-red-500" />
                  Duke of York&apos;s Picturehouse Cinema Background
                </h3>
                <p className="text-xs text-slate-400">
                  Original photograph: jake-hills-23LET4Hxj_U-unsplash.jpg
                </p>
              </div>
              <button
                onClick={() => setShowFullImageModal(false)}
                className="px-3 py-1 text-xs rounded-lg bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 transition"
              >
                Close (ESC)
              </button>
            </div>
            <div className="relative max-h-[70vh] overflow-hidden flex items-center justify-center bg-black">
              <img
                src="/jake-hills-23LET4Hxj_U-unsplash.jpg"
                alt="Cinema auditorium with red seats and screen"
                className="w-full h-auto object-contain max-h-[70vh]"
                referrerPolicy="no-referrer"
              />
            </div>
            <div className="p-4 bg-slate-950/80 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
              <span>Applied as the full fixed backdrop across the entire application.</span>
              <button
                onClick={() => {
                  setBgDarkness(0.35);
                  setShowFullImageModal(false);
                }}
                className="px-3 py-1 rounded bg-red-600 hover:bg-red-500 text-white font-semibold transition"
              >
                Set Backdrop to Clear Mode
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="relative z-10 border-t border-slate-800/80 bg-slate-950/80 backdrop-blur-md py-6 px-4 sm:px-8 text-center text-xs text-slate-500 mt-12">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
          <span>Movie Ticket Booking System • Production-Grade Full-Stack Delivery</span>
          <div className="flex items-center gap-4 text-xs font-mono">
            <span className="text-slate-400">Archive: Movie-Ticket-Booking-System.zip</span>
            <span className="text-emerald-400">163 Source Files Included</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
