"use client"

import { ArrowRight, Sparkles } from "lucide-react"

import { ChatWindow } from "@/components/chat/ChatWindow"

export function ChatDemoSection() {
  return (
    <section
      id="demo"
      className="border-b border-slate-200 bg-[#f8fafc] py-24 lg:py-32"
    >
      <div className="mx-auto max-w-7xl px-6">

        <div className="mx-auto max-w-2xl text-center">
          <div className="mb-4 inline-flex items-center gap-2 text-sm font-semibold text-blue-600">
            <Sparkles size={16} />
            Meet your AI tutor
          </div>

          <h2 className="text-4xl font-bold tracking-[-0.035em] text-slate-950 sm:text-5xl">
            Don't just search.
            <span className="block text-slate-400">
              Learn through conversation.
            </span>
          </h2>

          <p className="mt-5 text-lg leading-8 text-slate-600">
            Ask questions, follow the explanation, and explore concepts
            naturally with NEXA.
          </p>
        </div>

        <div className="mx-auto mt-14 max-w-4xl">
          <ChatWindow />
        </div>

        <div className="mt-8 flex justify-center">
          <a
            href="/register"
            className="inline-flex h-11 items-center gap-2 rounded-xl bg-slate-950 px-5 text-sm font-semibold text-white transition hover:bg-slate-800"
          >
            Start learning with NEXA
            <ArrowRight size={16} />
          </a>
        </div>
      </div>
    </section>
  )
}