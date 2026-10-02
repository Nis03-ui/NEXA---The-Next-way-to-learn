"use client"

import { useEffect, useMemo, useRef, useState } from "react"
import {
  ArrowUp,
  Menu,
  Plus,
  Sparkles,
  X,
} from "lucide-react"

import AppShell from "@/components/layout/AppShell"
import ChatMessage from "@/components/tutor/ChatMessage"
import ChatSidebar from "@/components/tutor/ChatSidebar"
import NEXAAvatar from "@/components/tutor/NEXAAvatar"
import SourceCard from "@/components/tutor/SourceCard"
import TutorMode from "@/components/tutor/TutorMode"

import {
  ai,
  type AISource,
  type ChatMessage as ApiChatMessage,
  type TutorMode as ApiTutorMode,
} from "@/lib/api"

type UIMessage = {
  id: number
  role: "user" | "assistant"
  content: string
}

export default function TutorPage() {
  const [messages, setMessages] = useState<UIMessage[]>([])
  const [input, setInput] = useState("")
  const [sessionId, setSessionId] = useState<number | null>(null)
  const [refreshKey, setRefreshKey] = useState(0)

  const [tutorMode, setTutorMode] =
    useState<ApiTutorMode>("normal")

  const [loading, setLoading] = useState(false)
  const [loadingSession, setLoadingSession] = useState(false)
  const [mobileSidebarOpen, setMobileSidebarOpen] =
    useState(false)

  const [sources, setSources] = useState<AISource[]>([])

  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const avatarState =
    loading
      ? "thinking"
      : messages.some((message) => message.role === "assistant")
        ? "responding"
        : "idle"

  /*
   * Auto-scroll whenever messages or loading state changes.
   */
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    })
  }, [messages, loading])

  /*
   * Focus input when the page opens.
   */
  useEffect(() => {
    textareaRef.current?.focus()
  }, [])

  /*
   * Load session from URL if present.
   */
  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    const requestedSession = params.get("session")

    if (!requestedSession) {
      return
    }

    const id = Number(requestedSession)

    if (!Number.isInteger(id) || id <= 0) {
      return
    }

    async function loadSession() {
      setLoadingSession(true)

      try {
        const session = await ai.session(id)

        setSessionId(session.id)

        setMessages(
          session.messages.map(
            (message: ApiChatMessage) => ({
              id: message.id,
              role:
                message.role === "user"
                  ? "user"
                  : "assistant",
              content: message.content,
            }),
          ),
        )

        setSources([])
      } catch {
        setSessionId(null)
        setMessages([])
        setSources([])
      } finally {
        setLoadingSession(false)
      }
    }

    loadSession()
  }, [])

  /*
   * Keep URL synchronized with current session.
   */
  useEffect(() => {
    const url = new URL(window.location.href)

    if (sessionId) {
      url.searchParams.set(
        "session",
        String(sessionId),
      )
    } else {
      url.searchParams.delete("session")
    }

    window.history.replaceState(
      {},
      "",
      url.toString(),
    )
  }, [sessionId])

  /*
   * Auto-grow textarea.
   */
  function resizeTextarea() {
    const textarea = textareaRef.current

    if (!textarea) {
      return
    }

    textarea.style.height = "auto"
    textarea.style.height =
      `${Math.min(textarea.scrollHeight, 180)}px`
  }

  /*
   * Send message.
   */
  async function handleSend() {
    const message = input.trim()

    if (!message || loading) {
      return
    }

    const temporaryId = Date.now()

    const userMessage: UIMessage = {
      id: temporaryId,
      role: "user",
      content: message,
    }

    setMessages((previous) => [
      ...previous,
      userMessage,
    ])

    setInput("")
    setLoading(true)
    setSources([])

    if (textareaRef.current) {
      textareaRef.current.style.height = "auto"
    }

    try {
      const response = await ai.chat(
        message,
        sessionId ?? undefined,
        tutorMode,
      )

      setSessionId(response.session_id)

      const assistantMessage: UIMessage = {
        id: temporaryId + 1,
        role: "assistant",
        content: response.answer,
      }

      setMessages((previous) => [
        ...previous,
        assistantMessage,
      ])

      setSources(response.sources ?? [])

      /*
       * Refresh sidebar so the newly created
       * conversation appears immediately.
       */
      setRefreshKey((value) => value + 1)
    } catch (error) {
      const errorMessage =
        error instanceof Error
          ? error.message
          : "Something went wrong."

      const assistantMessage: UIMessage = {
        id: temporaryId + 1,
        role: "assistant",
        content:
          `I couldn't process that request.\n\n${errorMessage}`,
      }

      setMessages((previous) => [
        ...previous,
        assistantMessage,
      ])
    } finally {
      setLoading(false)

      setTimeout(() => {
        textareaRef.current?.focus()
      }, 0)
    }
  }

  /*
   * Enter = send
   * Shift + Enter = newline
   */
  function handleKeyDown(
    event: React.KeyboardEvent<HTMLTextAreaElement>,
  ) {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault()
      handleSend()
    }
  }

  /*
   * Start a new conversation.
   */
  function handleNewChat() {
    setSessionId(null)
    setMessages([])
    setInput("")
    setSources([])
    setTutorMode("normal")
    setMobileSidebarOpen(false)

    const url = new URL(window.location.href)
    url.searchParams.delete("session")

    window.history.replaceState(
      {},
      "",
      url.toString(),
    )

    setTimeout(() => {
      textareaRef.current?.focus()
    }, 0)
  }

  /*
   * Select existing conversation.
   */
  async function handleSelectSession(
    id: number,
  ) {
    setLoadingSession(true)
    setMobileSidebarOpen(false)

    try {
      const session = await ai.session(id)

      setSessionId(session.id)

      setMessages(
        session.messages.map(
          (message: ApiChatMessage) => ({
            id: message.id,
            role:
              message.role === "user"
                ? "user"
                : "assistant",
            content: message.content,
          }),
        ),
      )

      setSources([])
    } catch {
      setMessages([])
      setSessionId(null)
    } finally {
      setLoadingSession(false)

      setTimeout(() => {
        textareaRef.current?.focus()
      }, 0)
    }
  }

  /*
   * Remove duplicate RAG sources.
   */
  const uniqueSources = useMemo(() => {
    const map = new Map<
      string,
      AISource
    >()

    for (const source of sources) {
      const key =
        `${source.content_id}-${source.chunk_index}`

      if (!map.has(key)) {
        map.set(key, source)
      }
    }

    return Array.from(map.values())
  }, [sources])

  const isEmpty = messages.length === 0

  return (
    <AppShell allowedRoles={["STUDENT"]}>
      <div className="mx-auto w-full max-w-[1600px]">
        <div className="relative flex h-[calc(100vh-5rem)] min-h-[600px] w-full overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm sm:rounded-3xl">

          {/* ================================================= */}
          {/* DESKTOP SIDEBAR */}
          {/* ================================================= */}

          <aside className="hidden w-64 shrink-0 border-r border-slate-200 bg-slate-50/60 lg:flex xl:w-72">
            <div className="min-h-0 flex-1">
              <ChatSidebar
                currentSessionId={sessionId}
                refreshKey={refreshKey}
                onSelect={handleSelectSession}
                onNew={handleNewChat}
              />
            </div>
          </aside>

          {/* ================================================= */}
          {/* MOBILE SIDEBAR OVERLAY */}
          {/* ================================================= */}

          {mobileSidebarOpen && (
            <div
              className="absolute inset-0 z-40 bg-slate-950/20 backdrop-blur-[2px] lg:hidden"
              onClick={() => setMobileSidebarOpen(false)}
              aria-hidden="true"
            />
          )}

          <aside
            className={[
              "absolute inset-y-0 left-0 z-50 flex w-[min(88vw,320px)] flex-col border-r border-slate-200 bg-white shadow-2xl transition-transform duration-300 lg:hidden",
              mobileSidebarOpen
                ? "translate-x-0"
                : "-translate-x-full",
            ].join(" ")}
          >
            <div className="flex items-center justify-between border-b border-slate-200 px-4 py-3">
              <div>
                <p className="text-sm font-bold text-slate-950">
                  Conversations
                </p>
                <p className="text-xs text-slate-500">
                  Your learning history
                </p>
              </div>

              <button
                type="button"
                onClick={() =>
                  setMobileSidebarOpen(false)
                }
                className="grid h-10 w-10 place-items-center rounded-xl text-slate-500 transition hover:bg-slate-100 hover:text-slate-900"
                aria-label="Close conversations"
              >
                <X size={18} />
              </button>
            </div>

            <div className="min-h-0 flex-1">
              <ChatSidebar
                currentSessionId={sessionId}
                refreshKey={refreshKey}
                onSelect={handleSelectSession}
                onNew={handleNewChat}
              />
            </div>
          </aside>

          {/* ================================================= */}
          {/* MAIN TUTOR */}
          {/* ================================================= */}

          <main className="relative flex min-w-0 flex-1 flex-col bg-white">

            {/* ================================================= */}
            {/* HEADER */}
            {/* ================================================= */}

            <header className="flex h-16 shrink-0 items-center justify-between border-b border-slate-200 px-4 sm:px-6">
              <div className="flex min-w-0 items-center gap-3">

                <button
                  type="button"
                  onClick={() =>
                    setMobileSidebarOpen(true)
                  }
                  className="grid h-10 w-10 shrink-0 place-items-center rounded-xl text-slate-600 transition hover:bg-slate-100 hover:text-slate-950 lg:hidden"
                  aria-label="Open conversations"
                >
                  <Menu size={19} />
                </button>

                <div className="grid h-9 w-9 shrink-0 place-items-center rounded-xl bg-slate-950 text-white">
                  <Sparkles size={16} />
                </div>

                <div className="min-w-0">
                  <h1 className="truncate text-sm font-bold text-slate-950 sm:text-base">
                    NEXA Tutor
                  </h1>

                  <div className="flex items-center gap-1.5">
                    <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
                    <span className="text-[11px] text-slate-500">
                      AI learning assistant
                    </span>
                  </div>
                </div>
              </div>

              <button
                type="button"
                onClick={handleNewChat}
                className="inline-flex h-9 shrink-0 items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 text-xs font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50"
              >
                <Plus size={14} />
                <span className="hidden sm:inline">
                  New chat
                </span>
              </button>
            </header>

            {/* ================================================= */}
            {/* CHAT AREA */}
            {/* ================================================= */}

            <div className="min-h-0 flex-1 overflow-y-auto">
              <div className="mx-auto flex min-h-full w-full max-w-4xl flex-col px-4 py-6 sm:px-6 sm:py-8">

                {/* ================================================= */}
                {/* EMPTY STATE */}
                {/* ================================================= */}

                {isEmpty && !loadingSession && (
                  <div className="flex flex-1 flex-col items-center justify-center py-10 text-center">

                    <div className="mb-6">
                      <NEXAAvatar
                        state={avatarState}
                      />
                    </div>

                    <div className="max-w-xl">
                      <p className="mb-2 text-xs font-bold uppercase tracking-[0.18em] text-blue-600">
                        Meet NEXA
                      </p>

                      <h2 className="text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
                        What do you want to learn?
                      </h2>

                      <p className="mx-auto mt-3 max-w-lg text-sm leading-6 text-slate-500 sm:text-base">
                        Ask questions, understand difficult
                        concepts, solve problems, or study
                        directly from your course material.
                      </p>
                    </div>

                    <div className="mt-8 grid w-full max-w-2xl gap-3 sm:grid-cols-2">
                      {[
                        {
                          title: "Explain a concept",
                          prompt:
                            "Explain polymorphism with a simple example.",
                        },
                        {
                          title: "Study my notes",
                          prompt:
                            "According to the notes, explain TCP and UDP.",
                        },
                        {
                          title: "Practice coding",
                          prompt:
                            "Teach me TypeScript generics with an example.",
                        },
                        {
                          title: "Test my knowledge",
                          prompt:
                            "Give me a short quiz on computer networks.",
                        },
                      ].map((suggestion) => (
                        <button
                          key={suggestion.title}
                          type="button"
                          onClick={() => {
                            setInput(suggestion.prompt)

                            setTimeout(() => {
                              textareaRef.current?.focus()
                            }, 0)
                          }}
                          className="group rounded-2xl border border-slate-200 bg-white p-4 text-left transition hover:-translate-y-0.5 hover:border-slate-300 hover:shadow-md"
                        >
                          <p className="text-sm font-semibold text-slate-900">
                            {suggestion.title}
                          </p>

                          <p className="mt-1 text-xs leading-5 text-slate-500">
                            {suggestion.prompt}
                          </p>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* ================================================= */}
                {/* LOADING SESSION */}
                {/* ================================================= */}

                {loadingSession && (
                  <div className="flex flex-1 items-center justify-center">
                    <div className="flex flex-col items-center gap-4">
                      <NEXAAvatar state="thinking" compact />

                      <div className="text-center">
                        <p className="text-sm font-semibold text-slate-800">
                          Loading conversation
                        </p>

                        <p className="mt-1 text-xs text-slate-500">
                          NEXA is getting things ready...
                        </p>
                      </div>
                    </div>
                  </div>
                )}

                {/* ================================================= */}
                {/* MESSAGES */}
                {/* ================================================= */}

                {!loadingSession && !isEmpty && (
                  <div className="space-y-6">
                    {messages.map((message) => (
                      <ChatMessage
                        key={message.id}
                        role={message.role}
                        content={message.content}
                      />
                    ))}

                    {/* ================================================= */}
                    {/* THINKING */}
                    {/* ================================================= */}

                    {loading && (
                      <div className="flex w-full justify-start">
                        <div className="flex max-w-[92%] items-start gap-3 sm:max-w-[82%]">
                          <div className="shrink-0">
                            <NEXAAvatar
                              state="thinking"
                              compact
                            />
                          </div>

                          <div className="rounded-2xl border border-slate-200 bg-white px-4 py-3.5 shadow-sm">
                            <div className="flex items-center gap-1.5">
                              <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-slate-400 [animation-delay:-0.3s]" />
                              <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-slate-400 [animation-delay:-0.15s]" />
                              <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-slate-400" />
                              <span className="ml-2 text-xs text-slate-400">
                                NEXA is thinking...
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* ================================================= */}
                    {/* SOURCES */}
                    {/* ================================================= */}

                    {!loading && uniqueSources.length > 0 && (
                      <section className="pt-2">
                        <div className="mb-3 flex items-center gap-2">
                          <div className="h-px flex-1 bg-slate-200" />

                          <span className="text-[10px] font-bold uppercase tracking-[0.16em] text-slate-400">
                            Sources
                          </span>

                          <div className="h-px flex-1 bg-slate-200" />
                        </div>

                        <div className="grid gap-2 sm:grid-cols-2">
                          {uniqueSources.map((source) => (
                            <SourceCard
                              key={`${source.content_id}-${source.chunk_index}`}
                              title={source.title}
                              subject={source.subject}
                            />
                          ))}
                        </div>
                      </section>
                    )}

                    <div ref={messagesEndRef} />
                  </div>
                )}
              </div>
            </div>

            {/* ================================================= */}
            {/* COMPOSER */}
            {/* ================================================= */}

            <div className="shrink-0 border-t border-slate-200 bg-white px-4 pb-4 pt-3 sm:px-6 sm:pb-6">
              <div className="mx-auto w-full max-w-4xl">

                <div className="mb-3">
                   <TutorMode
  mode={tutorMode}
  onChange={setTutorMode}
/>

                </div>

                <form
                  onSubmit={(event) => {
                    event.preventDefault()
                    handleSend()
                  }}
                  className="relative rounded-2xl border border-slate-300 bg-white shadow-sm transition focus-within:border-slate-400 focus-within:shadow-md"
                >
                  <textarea
                    ref={textareaRef}
                    value={input}
                    onChange={(event) => {
                      setInput(event.target.value)
                      resizeTextarea()
                    }}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask NEXA anything..."
                    rows={1}
                    disabled={loading}
                    className="block max-h-[180px] min-h-[56px] w-full resize-none bg-transparent px-4 pb-14 pt-4 pr-14 text-sm leading-6 text-slate-900 outline-none placeholder:text-slate-400 disabled:cursor-not-allowed disabled:opacity-60"
                    aria-label="Message NEXA"
                  />

                  <div className="absolute bottom-2.5 left-3 text-[10px] text-slate-400">
                    <span className="hidden sm:inline">
                      Enter to send · Shift + Enter for new line
                    </span>
                    <span className="sm:hidden">
                      Enter to send
                    </span>
                  </div>

                  <button
                    type="submit"
                    disabled={!input.trim() || loading}
                    className="absolute bottom-2.5 right-2.5 grid h-10 w-10 place-items-center rounded-xl bg-slate-950 text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-200 disabled:text-slate-400"
                    aria-label="Send message"
                  >
                    <ArrowUp size={17} />
                  </button>
                </form>

                <p className="mt-2 text-center text-[10px] text-slate-400">
                  NEXA can make mistakes. Verify important information.
                </p>
              </div>
            </div>
          </main>
        </div>
      </div>
    </AppShell>
  )
}