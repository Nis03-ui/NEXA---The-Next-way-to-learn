import Link from "next/link"
import {
  ArrowUpRight,
  Brain,
  Github,
  Mail,
} from "lucide-react"

export function LandingFooter() {
  return (
    <footer className="bg-slate-950 text-white">
      <div className="mx-auto max-w-7xl px-6">

        {/* CTA */}

        <div className="border-b border-white/10 py-20 lg:py-24">
          <div className="grid gap-10 lg:grid-cols-[1fr_auto] lg:items-end">
            <div>
              <div className="mb-5 flex items-center gap-3">
                <div className="grid h-10 w-10 place-items-center rounded-xl bg-white text-sm font-bold text-slate-950">
                  N
                </div>

                <span className="text-sm font-bold tracking-wide">
                  NEXA
                </span>
              </div>

              <h2 className="max-w-2xl text-4xl font-bold tracking-[-0.035em] sm:text-5xl">
                Your next way to learn
                <span className="block text-slate-500">
                  starts here.
                </span>
              </h2>

              <p className="mt-5 max-w-xl text-base leading-7 text-slate-400">
                Understand your courses, ask better questions, and build
                stronger knowledge with an AI study companion.
              </p>
            </div>

            <Link
              href="/register"
              className="inline-flex h-12 items-center justify-center gap-2 rounded-xl bg-white px-6 text-sm font-semibold text-slate-950 transition hover:bg-slate-200"
            >
              Start learning
              <ArrowUpRight size={16} />
            </Link>
          </div>
        </div>

        {/* LINKS */}

        <div className="grid gap-12 py-12 sm:grid-cols-2 lg:grid-cols-[1.5fr_1fr_1fr_1fr]">

          <div>
            <div className="flex items-center gap-2 text-sm font-semibold">
              <Brain size={16} />
              Intelligent learning
            </div>

            <p className="mt-3 max-w-xs text-sm leading-6 text-slate-500">
              NEXA connects conversational AI with your learning material.
            </p>
          </div>

          <div>
            <p className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Product
            </p>

            <div className="mt-4 space-y-3">
              <a
                href="#how-it-works"
                className="block text-sm text-slate-400 transition hover:text-white"
              >
                How it works
              </a>

              <a
                href="#features"
                className="block text-sm text-slate-400 transition hover:text-white"
              >
                Features
              </a>

              <a
                href="#demo"
                className="block text-sm text-slate-400 transition hover:text-white"
              >
                AI Tutor
              </a>
            </div>
          </div>

          <div>
            <p className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Account
            </p>

            <div className="mt-4 space-y-3">
              <Link
                href="/login"
                className="block text-sm text-slate-400 transition hover:text-white"
              >
                Log in
              </Link>

              <Link
                href="/register"
                className="block text-sm text-slate-400 transition hover:text-white"
              >
                Create account
              </Link>
            </div>
          </div>

          <div>
            <p className="text-xs font-bold uppercase tracking-wider text-slate-500">
              Connect
            </p>

            <div className="mt-4 flex gap-2">
              <a
                href="#"
                aria-label="GitHub"
                className="grid h-9 w-9 place-items-center rounded-lg border border-white/10 text-slate-400 transition hover:border-white/20 hover:text-white"
              >
                <Github size={16} />
              </a>

              <a
                href="mailto:hello@nexa.local"
                aria-label="Email"
                className="grid h-9 w-9 place-items-center rounded-lg border border-white/10 text-slate-400 transition hover:border-white/20 hover:text-white"
              >
                <Mail size={16} />
              </a>
            </div>
          </div>
        </div>

        {/* BOTTOM */}

        <div className="flex flex-col gap-3 border-t border-white/10 py-6 text-xs text-slate-500 sm:flex-row sm:items-center sm:justify-between">
          <p>
            © {new Date().getFullYear()} NEXA. Built for better learning.
          </p>

          <p>
            The Next Way to Learn
          </p>
        </div>
      </div>
    </footer>
  )
}