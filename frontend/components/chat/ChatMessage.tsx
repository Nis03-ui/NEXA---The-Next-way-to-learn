"use client"

import { Brain, User } from "lucide-react"

type ChatMessageProps = {
  role: "user" | "assistant"
  content: string
}

export function ChatMessage({ role, content }: ChatMessageProps) {
  const isUser = role === "user"

  return (
    <div className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}>
      {!isUser && (
        <div className="mt-1 grid h-8 w-8 shrink-0 place-items-center rounded-lg bg-blue-50 text-blue-600">
          <Brain size={15} />
        </div>
      )}

      <div
        className={`max-w-[78%] rounded-2xl px-4 py-3 text-sm leading-7 ${
          isUser
            ? "rounded-tr-md bg-slate-950 text-white"
            : "rounded-tl-md border border-slate-200 bg-white text-slate-700 shadow-sm"
        }`}
      >
        {content}
      </div>

      {isUser && (
        <div className="mt-1 grid h-8 w-8 shrink-0 place-items-center rounded-lg bg-slate-100 text-slate-600">
          <User size={15} />
        </div>
      )}
    </div>
  )
}