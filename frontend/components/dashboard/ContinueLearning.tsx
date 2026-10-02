"use client"

import Link from "next/link"
import {
  ArrowRight,
  MessageSquare,
  Sparkles,
} from "lucide-react"
import { useEffect, useState } from "react"

import { ai } from "@/lib/api"
import type { ChatSession } from "@/lib/api"

export default function ContinueLearning() {
  const [sessions, setSessions] = useState<ChatSession[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let mounted = true

    async function loadSessions() {
      try {
        const data = await ai.sessions()

        if (mounted) {
          setSessions(data.slice(0, 4))
        }
      } catch (error) {
        console.error(
          "Failed to load learning sessions:",
          error,
        )
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    loadSessions()

    return () => {
      mounted = false
    }
  }, [])

  return (
    <section className="nexa-card overflow-hidden">
      <div className="flex items-center justify-between border-b border-slate-200 px-6 py-5">
        <div>
          <h2 className="text-base font-bold text-slate-950">
            Continue learning
          </h2>

          <p className="mt-1 text-xs text-slate-500">
            Pick up where you left off with NEXA.
          </p>
        </div>

        <Link
          href="/tutor"
          className="flex items-center gap-1 text-xs font-semibold text-blue-600 transition hover:text-blue-700"
        >
          Study with NEXA
          <ArrowRight size={13} />
        </Link>
      </div>

      <div className="divide-y divide-slate-100">
        {loading ? (
          <LoadingState />
        ) : sessions.length === 0 ? (
          <EmptyState />
        ) : (
          sessions.map((session) => (
            <Link
              key={session.id}
              href={`/tutor?session=${session.id}`}
              className="block px-6 py-5 transition hover:bg-slate-50"
            >
              <div className="flex items-start gap-4">
                <div className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-blue-50 text-blue-600">
                  <MessageSquare size={17} />
                </div>

                <div className="min-w-0 flex-1">
                  <div className="flex items-start justify-between gap-4">
                    <div className="min-w-0">
                      <p className="truncate text-sm font-semibold text-slate-900">
                        {session.title}
                      </p>

                      <p className="mt-1 text-xs text-slate-400">
                        {formatSessionDate(session.created_at)}
                      </p>
                    </div>

                    <ArrowRight
                      size={15}
                      className="mt-0.5 shrink-0 text-slate-300 transition group-hover:text-blue-500"
                    />
                  </div>

                  <div className="mt-3 flex items-center gap-2">
                    <span className="inline-flex items-center gap-1 rounded-full bg-slate-100 px-2 py-1 text-[10px] font-semibold text-slate-500">
                      <Sparkles size={10} />
                      NEXA session
                    </span>
                  </div>
                </div>
              </div>
            </Link>
          ))
        )}
      </div>
    </section>
  )
}

function LoadingState() {
  return (
    <div className="space-y-4 px-6 py-5">
      {[1, 2, 3].map((item) => (
        <div
          key={item}
          className="flex animate-pulse items-center gap-4"
        >
          <div className="h-10 w-10 rounded-xl bg-slate-100" />

          <div className="flex-1">
            <div className="h-4 w-2/3 rounded bg-slate-100" />

            <div className="mt-2 h-3 w-1/3 rounded bg-slate-100" />
          </div>
        </div>
      ))}
    </div>
  )
}

function EmptyState() {
  return (
    <div className="px-6 py-10 text-center">
      <div className="mx-auto grid h-11 w-11 place-items-center rounded-xl bg-slate-100 text-slate-500">
        <MessageSquare size={18} />
      </div>

      <p className="mt-4 text-sm font-semibold text-slate-900">
        No study sessions yet
      </p>

      <p className="mx-auto mt-1 max-w-sm text-xs leading-5 text-slate-500">
        Start a conversation with NEXA and your learning
        sessions will appear here.
      </p>

      <Link
        href="/tutor"
        className="mt-5 inline-flex items-center gap-2 rounded-xl bg-slate-950 px-4 py-2.5 text-xs font-bold text-white transition hover:bg-slate-800"
      >
        Start learning
        <ArrowRight size={13} />
      </Link>
    </div>
  )
}

function formatSessionDate(dateString: string) {
  const date = new Date(dateString)

  if (Number.isNaN(date.getTime())) {
    return "Recent session"
  }

  return new Intl.DateTimeFormat("en", {
    month: "short",
    day: "numeric",
    year: "numeric",
  }).format(date)
}