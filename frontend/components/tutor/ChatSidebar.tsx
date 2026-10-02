"use client"

import { useEffect, useState } from "react"
import {
  MessageSquare,
  Plus,
  Trash2,
} from "lucide-react"

import { ai, type ChatSession } from "@/lib/api"

type ChatSidebarProps = {
  currentSessionId: number | null
  refreshKey: number
  onSelect: (id: number) => void
  onNew: () => void
}

export default function ChatSidebar({
  currentSessionId,
  refreshKey,
  onSelect,
  onNew,
}: ChatSidebarProps) {
  const [sessions, setSessions] = useState<ChatSession[]>([])
  const [loading, setLoading] = useState(true)
  const [deletingId, setDeletingId] =
    useState<number | null>(null)

  useEffect(() => {
    let cancelled = false

    async function loadSessions() {
      setLoading(true)

      try {
        const data = await ai.sessions()

        if (!cancelled) {
          setSessions(data)
        }
      } catch {
        if (!cancelled) {
          setSessions([])
        }
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    loadSessions()

    return () => {
      cancelled = true
    }
  }, [refreshKey])

  async function handleDelete(
    event: React.MouseEvent,
    id: number,
  ) {
    event.stopPropagation()

    if (deletingId !== null) {
      return
    }

    setDeletingId(id)

    try {
      await ai.deleteSession(id)

      setSessions((previous) =>
        previous.filter(
          (session) => session.id !== id,
        ),
      )

      if (currentSessionId === id) {
        onNew()
      }
    } finally {
      setDeletingId(null)
    }
  }

  function formatDate(dateString: string) {
    const date = new Date(dateString)

    if (Number.isNaN(date.getTime())) {
      return ""
    }

    const now = new Date()

    if (
      date.toDateString() ===
      now.toDateString()
    ) {
      return date.toLocaleTimeString([], {
        hour: "numeric",
        minute: "2-digit",
      })
    }

    return date.toLocaleDateString([], {
      month: "short",
      day: "numeric",
    })
  }

  return (
    <div className="flex h-full min-h-0 w-full flex-col overflow-hidden">

      {/* ================================================= */}
      {/* FIXED SIDEBAR TOP */}
      {/* ================================================= */}

      <div className="w-full shrink-0">

        <div className="mx-auto w-full max-w-[280px] px-4 pt-4">

          <button
            type="button"
            onClick={onNew}
            className="flex h-10 w-full items-center justify-center gap-2 rounded-xl border border-slate-200 bg-white px-3 text-xs font-semibold text-slate-700 shadow-sm transition hover:border-slate-300 hover:bg-slate-50 active:scale-[0.99]"
          >
            <Plus
              size={15}
              strokeWidth={2.2}
            />

            <span className="truncate">
              New conversation
            </span>
          </button>

        </div>

        {/* Section heading */}
        <div className="mx-auto w-full max-w-[280px] px-4 pb-2 pt-5">

          <div className="flex items-center justify-between">

            <p className="truncate text-[10px] font-bold uppercase tracking-wider text-slate-400">
              Recent conversations
            </p>

            {sessions.length > 0 && (
              <span className="ml-2 shrink-0 text-[10px] font-medium text-slate-400">
                {sessions.length}
              </span>
            )}

          </div>

        </div>

      </div>

      {/* ================================================= */}
      {/* SCROLLABLE CONVERSATIONS */}
      {/* ================================================= */}

      <div className="min-h-0 w-full flex-1 overflow-y-auto overflow-x-hidden">

        <div className="mx-auto w-full max-w-[280px] px-4 pb-6">

          {loading ? (

            <div className="space-y-2">

              {[1, 2, 3, 4].map((item) => (
                <div
                  key={item}
                  className="h-[58px] w-full animate-pulse rounded-xl bg-slate-100"
                />
              ))}

            </div>

          ) : sessions.length === 0 ? (

            <div className="flex flex-col items-center px-3 py-10 text-center">

              <div className="grid h-10 w-10 place-items-center rounded-xl bg-slate-100 text-slate-400">
                <MessageSquare size={17} />
              </div>

              <p className="mt-3 text-xs font-semibold text-slate-600">
                No conversations yet
              </p>

              <p className="mt-1 max-w-[180px] text-[10px] leading-5 text-slate-400">
                Start a conversation with NEXA.
              </p>

            </div>

          ) : (

            <div className="flex w-full flex-col gap-1">

              {sessions.map((session) => {

                const active =
                  session.id ===
                  currentSessionId

                return (
                  <div
                    key={session.id}
                    className={[
                      "flex w-full min-w-0 items-center overflow-hidden rounded-xl transition",
                      active
                        ? "bg-slate-200/80"
                        : "hover:bg-slate-100",
                    ].join(" ")}
                  >

                    {/* Conversation button */}
                    <button
                      type="button"
                      onClick={() =>
                        onSelect(session.id)
                      }
                      className="min-w-0 flex-1 overflow-hidden px-3 py-2.5 text-left"
                    >

                      <div className="flex min-w-0 items-center gap-2">

                        <MessageSquare
                          size={14}
                          className={[
                            "shrink-0",
                            active
                              ? "text-slate-700"
                              : "text-slate-400",
                          ].join(" ")}
                        />

                        <span
                          className={[
                            "min-w-0 flex-1 truncate text-xs font-medium",
                            active
                              ? "text-slate-900"
                              : "text-slate-600",
                          ].join(" ")}
                        >
                          {session.title ||
                            "New conversation"}
                        </span>

                      </div>

                      <p className="mt-1 truncate pl-6 text-[9px] text-slate-400">
                        {formatDate(
                          session.created_at,
                        )}
                      </p>

                    </button>

                    {/* Delete */}
                    <button
                      type="button"
                      onClick={(event) =>
                        handleDelete(
                          event,
                          session.id,
                        )
                      }
                      disabled={
                        deletingId ===
                        session.id
                      }
                      className="mr-2 grid h-7 w-7 shrink-0 place-items-center rounded-lg text-slate-300 transition hover:bg-white hover:text-red-500 disabled:cursor-not-allowed disabled:opacity-40 lg:opacity-0 lg:group-hover:opacity-100"
                      aria-label="Delete conversation"
                    >
                      <Trash2 size={13} />
                    </button>

                  </div>
                )
              })}

            </div>

          )}

        </div>

      </div>

      {/* ================================================= */}
      {/* SIDEBAR FOOTER */}
      {/* ================================================= */}

      <div className="w-full shrink-0 border-t border-slate-200 bg-slate-50/80 px-4 py-3">

        <div className="mx-auto flex max-w-[280px] items-center justify-center">

          <p className="text-center text-[9px] text-slate-400">
            NEXA AI Tutor
          </p>

        </div>

      </div>

    </div>
  )
}