"use client"

import {
  BookOpen,
  Clock3,
  MessageSquare,
  ClipboardCheck,
} from "lucide-react"
import { useEffect, useState } from "react"

import { ai, quizzes } from "@/lib/api"
import { dashboardStats } from "@/lib/dashboard/data"

export default function DashboardStats() {
  const [aiSessionCount, setAiSessionCount] = useState<number | null>(null)
  const [quizCount, setQuizCount] = useState<number | null>(null)

  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let mounted = true

    async function loadStats() {
      try {
        const [sessions, availableQuizzes] = await Promise.all([
          ai.sessions(),
          quizzes.getAll(),
        ])

        if (!mounted) return

        setAiSessionCount(sessions.length)
        setQuizCount(availableQuizzes.length)
      } catch (error) {
        console.error("Failed to load dashboard stats:", error)
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    loadStats()

    return () => {
      mounted = false
    }
  }, [])

  const stats = [
    {
      label: "Subjects",
      value: dashboardStats.subjects.toString(),
      description: "Active this semester",
      icon: BookOpen,
      badge: "Academic",
      badgeClass: "bg-slate-100 text-slate-500",
    },
    {
      label: "AI Sessions",
      value: loading
        ? "—"
        : (aiSessionCount ?? 0).toString(),
      description: "Conversations with NEXA",
      icon: MessageSquare,
      badge: "Live",
      badgeClass: "bg-emerald-50 text-emerald-600",
    },
    {
      label: "Assessments",
      value: loading
        ? "—"
        : (quizCount ?? 0).toString(),
      description: "Available quizzes",
      icon: ClipboardCheck,
      badge: "Available",
      badgeClass: "bg-blue-50 text-blue-600",
    },
    {
      label: "Study Time",
      value: `${dashboardStats.studyHours}h`,
      description: "This week",
      icon: Clock3,
      badge: "Tracking",
      badgeClass: "bg-slate-100 text-slate-500",
    },
  ]

  return (
    <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {stats.map((stat) => {
        const Icon = stat.icon

        return (
          <div
            key={stat.label}
            className="nexa-card nexa-card-hover p-5"
          >
            <div className="flex items-start justify-between">
              <div className="grid h-10 w-10 place-items-center rounded-xl bg-slate-100 text-slate-700">
                <Icon size={18} />
              </div>

              <span
                className={`rounded-full px-2 py-1 text-[10px] font-semibold ${stat.badgeClass}`}
              >
                {stat.badge}
              </span>
            </div>

            <p className="mt-5 text-xs font-medium text-slate-500">
              {stat.label}
            </p>

            <p className="mt-1 text-2xl font-bold tracking-tight text-slate-950">
              {stat.value}
            </p>

            <p className="mt-1 text-xs text-slate-400">
              {stat.description}
            </p>
          </div>
        )
      })}
    </section>
  )
}
