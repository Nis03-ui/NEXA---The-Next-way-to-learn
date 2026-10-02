"use client"

import { useEffect, useState } from "react"

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
    async function loadUser() {
      try {
        const currentUser = await auth.me()
        setUser(currentUser)
      } catch {
        setUser(null)
      } finally {
        setLoading(false)
      }
    }

    loadUser()
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
      </div>
    </AppShell>
  )
}