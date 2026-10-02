"use client"

import { useState } from "react"
import { Sparkles } from "lucide-react"

import { ChatInput } from "./ChatInput"
import { ChatMessage } from "./ChatMessage"
import { SourceCard } from "./SourceCard"

type Message = {
  id: number
  role: "user" | "assistant"
  content: string
}

export function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      role: "assistant",
      content:
        "Hi! I'm NEXA. Ask me about something you're studying and I'll help you understand it.",
    },
  ])

  const [nextId, setNextId] = useState(2)

  function handleSubmit(message: string) {
    const userMessage: Message = {
      id: nextId,
      role: "user",
      content: message,
    }

    const response: Message = {
      id: nextId + 1,
      role: "assistant",
      content:
        "That's a great question. In the full NEXA experience, I'll use your course context and relevant learning material to build the answer.",
    }

    setMessages((current) => [...current, userMessage, response])
    setNextId((current) => current + 2)
  }

  return (
    <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-[0_25px_70px_rgba(15,23,42,0.08)]">

      {/* HEADER */}

      <div className="flex items-center justify-between border-b border-slate-200 px-5 py-4">
        <div className="flex items-center gap-3">
          <div className="grid h-10 w-10 place-items-center rounded-xl bg-slate-950 text-sm font-bold text-white">
            N
          </div>

          <div>
            <p className="text-sm font-bold text-slate-950">
              NEXA Tutor
            </p>

            <p className="text-xs text-slate-500">
              Your AI study companion
            </p>
          </div>
        </div>

        <div className="flex items-center gap-1.5 text-xs font-medium text-emerald-600">
          <span className="h-2 w-2 rounded-full bg-emerald-500" />
          Online
        </div>
      </div>

      {/* MESSAGES */}

      <div className="min-h-[380px] space-y-5 bg-slate-50 p-5 sm:p-7">
        {messages.map((message) => (
          <ChatMessage
            key={message.id}
            role={message.role}
            content={message.content}
          />
        ))}

        <div className="max-w-[78%]">
          <div className="mb-2 flex items-center gap-2 text-[11px] font-semibold text-blue-600">
            <Sparkles size={13} />
            NEXA can ground answers in your course material
          </div>

          <SourceCard
            title="Example course material"
            description="Relevant sources will appear here when the AI retrieves supporting content."
          />
        </div>
      </div>

      {/* INPUT */}

      <ChatInput onSubmit={handleSubmit} />
    </div>
  )
}