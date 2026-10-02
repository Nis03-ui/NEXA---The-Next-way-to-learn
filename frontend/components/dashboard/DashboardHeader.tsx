"use client"

import { Brain, Sparkles } from "lucide-react"
import Link from "next/link"

type DashboardHeaderProps = {
  name: string
  loading?: boolean
}

export default function DashboardHeader({
  name,
  loading = false,
}: DashboardHeaderProps) {
  const firstName = name?.split(" ")[0] || "Student"

  return (
    <section className="flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
      <div>
        <div className="flex items-center gap-2 text-sm font-medium text-blue-600">
          <Sparkles size={15} />
          <span>BCA · Semester 4</span>
        </div>

        <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
          {loading
            ? "Welcome back"
            : `Welcome back, ${firstName}`}
        </h1>

        <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
          Track your academic progress, continue your studies, and use
          NEXA whenever you need help understanding a concept.
        </p>
      </div>

      <Link
        href="/tutor"
        className="inline-flex h-11 items-center justify-center gap-2 rounded-xl bg-slate-950 px-5 text-sm font-semibold text-white transition hover:bg-slate-800"
      >
        <Brain size={17} />
        Ask NEXA
      </Link>
    </section>
  )
}