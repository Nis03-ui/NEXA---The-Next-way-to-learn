import {
  CalendarDays,
  CheckCircle2,
  GraduationCap,
} from "lucide-react"

import { dashboardStats } from "@/lib/dashboard/data"

export default function SemesterProgress() {
  const progress = dashboardStats.semesterProgress

  return (
    <section className="nexa-card p-6">
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-xl bg-blue-50 text-blue-600">
            <GraduationCap size={18} />
          </div>

          <div>
            <h2 className="text-base font-bold text-slate-950">
              Semester progress
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              BCA · Semester 4
            </p>
          </div>
        </div>

        <span className="text-2xl font-bold tracking-tight text-slate-950">
          {progress}%
        </span>
      </div>

      <div className="mt-6">
        <div className="h-3 overflow-hidden rounded-full bg-slate-100">
          <div
            className="h-full rounded-full bg-slate-950 transition-all duration-700"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      <div className="mt-5 grid grid-cols-3 gap-3">
        <div className="rounded-xl bg-slate-50 p-3">
          <p className="text-[10px] font-semibold uppercase tracking-wide text-slate-400">
            Completed
          </p>

          <div className="mt-2 flex items-center gap-1.5">
            <CheckCircle2 size={14} className="text-emerald-500" />

            <span className="text-sm font-bold text-slate-900">
              72%
            </span>
          </div>
        </div>

        <div className="rounded-xl bg-slate-50 p-3">
          <p className="text-[10px] font-semibold uppercase tracking-wide text-slate-400">
            Remaining
          </p>

          <p className="mt-2 text-sm font-bold text-slate-900">
            28%
          </p>
        </div>

        <div className="rounded-xl bg-slate-50 p-3">
          <p className="text-[10px] font-semibold uppercase tracking-wide text-slate-400">
            Semester
          </p>

          <div className="mt-2 flex items-center gap-1.5">
            <CalendarDays size={14} className="text-blue-500" />

            <span className="text-sm font-bold text-slate-900">
              4 / 8
            </span>
          </div>
        </div>
      </div>

      <div className="mt-5 border-t border-slate-100 pt-4">
        <p className="text-xs leading-5 text-slate-500">
          Keep your weekly study consistency high to stay on track with
          your semester goals.
        </p>
      </div>
    </section>
  )
}