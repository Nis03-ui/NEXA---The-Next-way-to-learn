"use client"

import Link from "next/link"
import { ArrowRight } from "lucide-react"

export function LandingNavbar() {
  return (
    <header className="sticky top-0 z-50 border-b border-slate-200/80 bg-white/90 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
        <Link href="/" className="flex items-center gap-2.5">
          <div className="grid h-9 w-9 place-items-center rounded-xl bg-slate-950 text-sm font-bold text-white">
            N
          </div>

          <div>
            <div className="text-sm font-bold tracking-tight text-slate-950">
              NEXA
            </div>
            <div className="text-[10px] font-medium uppercase tracking-[0.18em] text-slate-400">
              Learn differently
            </div>
          </div>
        </Link>

        <nav className="hidden items-center gap-8 md:flex">
          <a
            href="#how-it-works"
            className="text-sm font-medium text-slate-600 transition hover:text-slate-950"
          >
            How it works
          </a>

          <a
            href="#features"
            className="text-sm font-medium text-slate-600 transition hover:text-slate-950"
          >
            Features
          </a>

          <a
            href="#demo"
            className="text-sm font-medium text-slate-600 transition hover:text-slate-950"
          >
            AI Tutor
          </a>
        </nav>

        <div className="flex items-center gap-3">
          <Link
            href="/login"
            className="hidden text-sm font-semibold text-slate-700 transition hover:text-slate-950 sm:block"
          >
            Log in
          </Link>

          <Link
            href="/register"
            className="inline-flex h-10 items-center gap-2 rounded-xl bg-slate-950 px-4 text-sm font-semibold text-white transition hover:bg-slate-800"
          >
            Start learning
            <ArrowRight size={15} />
          </Link>
        </div>
      </div>
    </header>
  )
}