import Link from "next/link"
import {
  ArrowRight,
  Brain,
  CheckCircle2,
  Sparkles,
} from "lucide-react"

export default function NexaDashboardCard() {
  return (
    <section className="nexa-card overflow-hidden">
      <div className="border-b border-slate-200 px-6 py-5">
        <div className="flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-xl bg-blue-50 text-blue-600">
            <Sparkles size={18} />
          </div>

          <div>
            <h2 className="text-base font-bold text-slate-950">
              Learn with NEXA
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              Your intelligent study companion.
            </p>
          </div>
        </div>
      </div>

      <div className="p-6">
        <div className="rounded-2xl bg-slate-950 p-5 text-white">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-white/10">
            <Brain size={19} />
          </div>

          <h3 className="mt-5 text-base font-bold">
            What are you studying today?
          </h3>

          <p className="mt-2 text-xs leading-5 text-slate-300">
            Ask NEXA to explain a difficult concept, solve a problem,
            or help you understand your course material.
          </p>

          <Link
            href="/tutor"
            className="mt-5 flex h-10 items-center justify-center gap-2 rounded-xl bg-white text-xs font-bold text-slate-950 transition hover:bg-slate-100"
          >
            Start learning
            <ArrowRight size={14} />
          </Link>
        </div>

        <div className="mt-5 space-y-3">
          <FeatureItem text="Explain difficult concepts" />
          <FeatureItem text="Answer course questions" />
          <FeatureItem text="Use relevant study material" />
          <FeatureItem text="Help solve problems" />
        </div>
      </div>
    </section>
  )
}

function FeatureItem({ text }: { text: string }) {
  return (
    <div className="flex items-center gap-2 text-xs text-slate-600">
      <CheckCircle2
        size={14}
        className="shrink-0 text-emerald-500"
      />

      {text}
    </div>
  )
}