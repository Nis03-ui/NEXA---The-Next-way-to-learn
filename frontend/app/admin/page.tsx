"use client"

import AppShell from "@/components/layout/AppShell"

import {
  Users,
  Shield,
  BookOpen,
  Activity,
} from "lucide-react"

export default function AdminPage() {
  return (
    <AppShell allowedRoles={["ADMIN"]}>
      <div className="space-y-8">

        <div>
          <p className="cyan text-sm">
            ADMIN CONTROL CENTER
          </p>

          <h1 className="text-4xl font-bold">
            NEXA Administration
          </h1>

          <p className="text-white/50 mt-2">
            Manage users, resources and AI system health.
          </p>
        </div>

        <div
          className="
            grid
            md:grid-cols-4
            gap-5
          "
        >
          <Card
            icon={<Users />}
            value="--"
            label="Users"
          />

          <Card
            icon={<Shield />}
            value="--"
            label="Teachers"
          />

          <Card
            icon={<BookOpen />}
            value="--"
            label="Resources"
          />

          <Card
            icon={<Activity />}
            value="OK"
            label="System"
          />
        </div>

        <section
          className="
            glass
            rounded-3xl
            p-8
          "
        >
          <h2 className="text-xl font-semibold">
            Platform Overview
          </h2>

          <p className="text-white/50 mt-3">
            NEXA AI learning platform management dashboard.
          </p>

          <div
            className="
              mt-6
              grid
              md:grid-cols-3
              gap-4
            "
          >
            <div
              className="
                bg-white/5
                rounded-2xl
                p-5
              "
            >
              Users
            </div>

            <div
              className="
                bg-white/5
                rounded-2xl
                p-5
              "
            >
              AI Sessions
            </div>

            <div
              className="
                bg-white/5
                rounded-2xl
                p-5
              "
            >
              Knowledge Base
            </div>
          </div>
        </section>

      </div>
    </AppShell>
  )
}

function Card({
  icon,
  value,
  label,
}: {
  icon: React.ReactNode
  value: string
  label: string
}) {
  return (
    <div
      className="
        glass
        rounded-3xl
        p-6
      "
    >
      <div className="text-cyan-400">
        {icon}
      </div>

      <div className="text-3xl font-bold mt-5">
        {value}
      </div>

      <p className="text-white/50">
        {label}
      </p>
    </div>
  )
}