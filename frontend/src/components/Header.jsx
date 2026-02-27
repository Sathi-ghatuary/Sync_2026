import { CheckCircle2, Menu, X } from 'lucide-react';
import { useState } from 'react';

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="bg-gradient-to-r from-slate-900 to-slate-800 text-white shadow-xl fixed w-full top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 p-2 rounded-lg">
              <CheckCircle2 size={24} />
            </div>
            <div>
              <h1 className="text-2xl font-bold">TitleVerify</h1>
              <p className="text-xs text-blue-300">PRGI System</p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-8">
            <a href="#verify" className="hover:text-blue-400 transition">Verify</a>
            <a href="#applications" className="hover:text-blue-400 transition">Applications</a>
            <a href="#dashboard" className="hover:text-blue-400 transition">Dashboard</a>
            <a href="#about" className="hover:text-blue-400 transition">About</a>
          </nav>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <nav className="md:hidden pb-4 flex flex-col gap-4">
            <a href="#verify" className="hover:text-blue-400 transition">Verify Title</a>
            <a href="#applications" className="hover:text-blue-400 transition">My Applications</a>
            <a href="#dashboard" className="hover:text-blue-400 transition">Dashboard</a>
            <a href="#about" className="hover:text-blue-400 transition">About</a>
          </nav>
        )}
      </div>
    </header>
  );
}
