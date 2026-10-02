"use client"

import { useEffect, useState } from "react"
import Link from "next/link"
import { ArrowRight, ClipboardCheck } from "lucide-react"

import AppShell from "@/components/layout/AppShell"
import DashboardHeader from "@/components/dashboard/DashboardHeader"
import DashboardStats from "@/components/dashboard/DashboardStats"
import WeeklyStudyChart from "@/components/dashboard/WeeklyStudyChart"
import SemesterProgress from "@/components/dashboard/SemesterProgress"
import AcademicCalendar from "@/components/dashboard/AcademicCalendar"
import ContinueLearning from "@/components/dashboard/ContinueLearning"
import NexaDashboardCard from "@/components/dashboard/NexaDashboardCard"

import { auth } from "@/lib/api"
import type { AuthUser } from "@/lib/api"

export default function DashboardPage() {
  const [user, setUser] = useState<AuthUser | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let mounted = true

    async function loadUser() {
      try {
        const currentUser = await auth.me()

        if (mounted) {
          setUser(currentUser)
        }
      } catch {
        if (mounted) {
          setUser(null)
        }
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    loadUser()

    return () => {
      mounted = false
    }
  }, [])

  return (
    <AppShell allowedRoles={["STUDENT"]}>
      <div className="mx-auto max-w-7xl space-y-6 sm:space-y-8">
        <DashboardHeader
          name={user?.name || ""}
          loading={loading}
        />

        <DashboardStats />

        <section className="grid gap-6 xl:grid-cols-[1.5fr_1fr]">
          <WeeklyStudyChart />
          <SemesterProgress />
        </section>

        <AcademicCalendar />

        <section className="grid gap-6 xl:grid-cols-[1.5fr_1fr]">
          <ContinueLearning />
          <NexaDashboardCard />
        </section>

        <section className="nexa-card overflow-hidden">
          <div className="flex flex-col gap-5 p-6 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-start gap-4">
              <div className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-blue-50 text-blue-600">
                <ClipboardCheck size={19} />
              </div>

              <div>
                <h2 className="text-base font-bold text-slate-950">
                  Ready to test your understanding?
                </h2>

                <p className="mt-1 max-w-xl text-xs leading-5 text-slate-500">
                  Take an assessment created by your teacher and
                  see how well you understand the course material.
                </p>
              </div>
            </div>

            <Link
              href="/quizzes"
              className="inline-flex h-10 shrink-0 items-center justify-center gap-2 rounded-xl bg-slate-950 px-4 text-xs font-bold text-white transition hover:bg-slate-800"
            >
              View assessments
              <ArrowRight size={14} />
            </Link>
          </div>
        </section>
      </div>
    </AppShell>
  )
}
