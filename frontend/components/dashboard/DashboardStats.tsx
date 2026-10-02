"use client"

import {
  BookOpen,
  Clock3,
  MessageSquare,
  TrendingUp,
} from "lucide-react"
import { useEffect, useState } from "react"

import { ai } from "@/lib/api"
import { dashboardStats } from "@/lib/dashboard/data"

export default function DashboardStats() {
  const [aiSessionCount, setAiSessionCount] = useState(
    dashboardStats.aiSessions,
  )

  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let mounted = true

    async function loadAiSessions() {
      try {
        const sessions = await ai.sessions()

        if (mounted) {
          setAiSessionCount(sessions.length)
        }
      } catch (error) {
        console.error(
          "Failed to load AI session count:",
          error,
        )
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    loadAiSessions()

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
    },
    {
      label: "AI Sessions",
      value: loading
        ? "—"
        : aiSessionCount.toString(),
      description: "Conversations with NEXA",
      icon: MessageSquare,
    },
    {
      label: "Study Time",
      value: `${dashboardStats.studyHours}h`,
      description: "This week",
      icon: Clock3,
    },
    {
      label: "Semester Progress",
      value: `${dashboardStats.semesterProgress}%`,
      description: "Overall completion",
      icon: TrendingUp,
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

              <span className="rounded-full bg-emerald-50 px-2 py-1 text-[10px] font-semibold text-emerald-600">
                Active
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