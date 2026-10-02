"use client"

import Link from "next/link"
import { ArrowRight, CheckCircle2, Sparkles } from "lucide-react"
import { InteractiveTutorPreview } from "./InteractiveTutorPreview"

export function HeroSection() {
  return (
    <section className="relative overflow-hidden border-b border-slate-200 bg-white">
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#e2e8f0_1px,transparent_1px),linear-gradient(to_bottom,#e2e8f0_1px,transparent_1px)] bg-[size:48px_48px] opacity-30" />

      <div className="relative mx-auto max-w-7xl px-6">
        <div className="grid min-h-[calc(100vh-64px)] items-center gap-16 py-20 lg:grid-cols-[0.9fr_1.1fr]">

          {/* CONTENT */}

          <div>
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-blue-200 bg-blue-50 px-3.5 py-1.5 text-xs font-semibold text-blue-700">
              <Sparkles size={14} />
              AI-powered learning
            </div>

            <h1 className="max-w-3xl text-5xl font-bold tracking-[-0.045em] text-slate-950 sm:text-6xl lg:text-[72px] lg:leading-[1.02]">
              Learn smarter.
              <span className="block bg-gradient-to-r from-blue-600 to-violet-600 bg-clip-text text-transparent">
                Understand deeper.
              </span>
            </h1>

            <p className="mt-7 max-w-xl text-lg leading-8 text-slate-600">
              NEXA is your personal AI study companion. Ask questions,
              understand difficult concepts, and learn directly from your
              course materials.
            </p>

            <div className="mt-9 flex flex-wrap items-center gap-3">
              <Link
                href="/register"
                className="inline-flex h-12 items-center gap-2 rounded-xl bg-slate-950 px-6 text-sm font-semibold text-white shadow-lg shadow-slate-900/10 transition hover:-translate-y-0.5 hover:bg-slate-800"
              >
                Start learning
                <ArrowRight size={17} />
              </Link>

              <a
                href="#demo"
                className="inline-flex h-12 items-center rounded-xl border border-slate-300 bg-white px-6 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
              >
                Try the experience
              </a>
            </div>

            <div className="mt-10 flex flex-wrap gap-x-6 gap-y-3">
              <div className="flex items-center gap-2 text-sm text-slate-500">
                <CheckCircle2 size={16} className="text-emerald-500" />
                Course-aware answers
              </div>

              <div className="flex items-center gap-2 text-sm text-slate-500">
                <CheckCircle2 size={16} className="text-emerald-500" />
                AI explanations
              </div>

              <div className="flex items-center gap-2 text-sm text-slate-500">
                <CheckCircle2 size={16} className="text-emerald-500" />
                Source-backed learning
              </div>
            </div>
          </div>

          {/* INTERACTIVE PRODUCT */}

          <InteractiveTutorPreview />

        </div>
      </div>
    </section>
  )
}