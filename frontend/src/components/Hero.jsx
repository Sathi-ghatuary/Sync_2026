import { ArrowRight, Shield, Zap, TrendingUp, BadgeCheck, FileCheck2, CheckCircle2 } from 'lucide-react';

export default function Hero() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-blue-950 text-white pt-24 pb-16 flex items-center">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <div className="animate-fadeIn">
            <div className="inline-flex items-center gap-2 bg-white/10 border border-white/25 rounded-full px-4 py-2 mb-6">
              <Zap size={16} className="text-cyan-300" />
              <span className="text-sm font-semibold text-slate-100">Powered by AI & NLP</span>
            </div>

            <h1 className="text-5xl lg:text-6xl font-bold mb-6 leading-tight">
              Verify Your
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-300 to-blue-200">
                {' '}Publication Title
              </span>
            </h1>

            <p className="text-xl text-slate-100 mb-8 leading-relaxed">
              Ensure your publication title is unique, compliant with guidelines, and ready for registration with the Press Registrar General of India.
            </p>

            {/* Features */}
            <div className="space-y-4 mb-8">
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 bg-cyan-300 rounded-full" />
                <p className="text-slate-100">Real-time similarity detection across 160,000+ titles</p>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 bg-cyan-300 rounded-full" />
                <p className="text-slate-100">Comprehensive compliance rule enforcement</p>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-2 h-2 bg-cyan-300 rounded-full" />
                <p className="text-slate-100">Instant verification probability scoring</p>
              </div>
            </div>

            {/* CTA Button */}
            <a
              href="#verify"
              className="inline-flex items-center gap-2 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-white font-bold py-4 px-8 rounded-lg shadow-lg hover:shadow-xl transition-all duration-300"
            >
              Start Verification
              <ArrowRight size={20} />
            </a>
          </div>

          {/* Right Visual */}
          <div className="relative hidden lg:block">
            <div className="relative w-full aspect-square">
              {/* Floating verification symbols */}
              <div className="absolute -top-5 -right-5 z-20 bg-emerald-50 text-emerald-900 rounded-xl px-3 py-2 shadow-xl border border-emerald-200 flex items-center gap-2">
                <BadgeCheck size={16} className="text-emerald-700" />
                <span className="text-xs font-semibold">Verified</span>
              </div>
              <div className="absolute -bottom-5 -left-5 z-20 bg-amber-500/15 text-amber-100 rounded-xl px-3 py-2 shadow-xl border border-amber-300/40 flex items-center gap-2">
                <FileCheck2 size={16} className="text-amber-300" />
                <span className="text-xs font-semibold">Compliance Ready</span>
              </div>
              <div className="absolute top-1/2 left-1/2 z-10 -translate-x-1/2 -translate-y-1/2">
                <div className="relative flex items-center justify-center w-28 h-28 rounded-full border border-emerald-200/35 bg-emerald-300/10 backdrop-blur-sm">
                  <div className="absolute w-36 h-36 rounded-full border border-amber-300/20" />
                  <div className="absolute w-48 h-48 rounded-full border border-emerald-200/10" />
                  <CheckCircle2 size={24} className="text-amber-300" />
                </div>
              </div>

              {/* Background gradient circles */}
              <div className="absolute inset-0 bg-gradient-to-br from-emerald-400/25 to-amber-400/20 rounded-3xl blur-3xl" />

              {/* Main card */}
              <div className="relative bg-slate-900/72 backdrop-blur-xl border border-emerald-300/25 rounded-2xl p-8 h-full flex flex-col justify-between shadow-2xl">
                {/* Icon */}
                <div className="bg-gradient-to-br from-emerald-500 to-teal-600 p-4 rounded-lg w-fit">
                  <Shield size={32} className="text-white" />
                </div>

                {/* Stats */}
                <div className="space-y-6">
                  <div>
                    <p className="text-emerald-200 text-sm font-semibold mb-2">Titles Verified</p>
                    <p className="text-4xl font-bold text-white">160k+</p>
                  </div>

                  <div className="flex items-center gap-4 pt-4 border-t border-emerald-200/20">
                    <div>
                      <p className="text-slate-200 text-xs mb-1">Approval Rate</p>
                      <p className="text-2xl font-bold text-amber-300">87%</p>
                    </div>
                    <div className="flex-1">
                      <div className="bg-slate-600 rounded-full h-2">
                        <div className="bg-gradient-to-r from-amber-400 to-emerald-400 h-2 rounded-full" style={{ width: '87%' }} />
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center gap-4 pt-4 border-t border-emerald-200/20">
                    <TrendingUp size={20} className="text-emerald-300" />
                    <span className="text-slate-100">Real-time processing</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
