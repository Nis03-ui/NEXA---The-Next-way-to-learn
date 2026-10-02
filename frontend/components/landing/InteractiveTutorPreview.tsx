"use client"

import { useState } from "react"
import {
  ArrowRight,
  Brain,
  CheckCircle2,
  Sparkles,
} from "lucide-react"

const questions = [
  {
    label: "TCP vs UDP",
    question: "Explain the difference between TCP and UDP.",
    answer:
      "TCP is connection-oriented and provides reliable, ordered delivery. UDP is connectionless and focuses on speed with lower overhead.",
    points: ["Reliable delivery", "Ordered packets", "Connection-oriented"],
  },
  {
    label: "What is polymorphism?",
    question: "Explain polymorphism in object-oriented programming.",
    answer:
      "Polymorphism allows objects of different classes to be treated through a common interface while each class provides its own behavior.",
    points: ["Multiple forms", "Common interface", "Flexible behavior"],
  },
  {
    label: "Explain recursion",
    question: "Explain recursion in simple terms.",
    answer:
      "Recursion is a technique where a function solves a problem by calling itself on a smaller version of that problem until it reaches a base case.",
    points: ["Self-reference", "Smaller problem", "Base case"],
  },
]

export function InteractiveTutorPreview() {
  const [selected, setSelected] = useState(0)

  const current = questions[selected]

  return (
    <div className="relative">
      <div className="absolute -inset-10 rounded-[3rem] bg-blue-100/50 blur-3xl" />

      <div className="relative overflow-hidden rounded-[1.5rem] border border-slate-200 bg-white shadow-[0_30px_80px_rgba(15,23,42,0.12)]">

        {/* HEADER */}

        <div className="flex items-center justify-between border-b border-slate-200 px-5 py-4">
          <div className="flex items-center gap-3">
            <div className="grid h-9 w-9 place-items-center rounded-xl bg-slate-950 text-sm font-bold text-white">
              N
            </div>

            <div>
              <p className="text-sm font-semibold text-slate-950">
                NEXA Tutor
              </p>

              <p className="text-xs text-slate-500">
                AI learning assistant
              </p>
            </div>
          </div>

          <div className="flex items-center gap-1.5 text-xs font-medium text-emerald-600">
            <span className="h-2 w-2 rounded-full bg-emerald-500" />
            Ready
          </div>
        </div>

        {/* QUESTION SELECTOR */}

        <div className="border-b border-slate-200 bg-white px-5 py-4">
          <p className="mb-3 text-[11px] font-semibold uppercase tracking-wider text-slate-400">
            Try a question
          </p>

          <div className="flex flex-wrap gap-2">
            {questions.map((item, index) => (
              <button
                key={item.label}
                onClick={() => setSelected(index)}
                className={`rounded-lg border px-3 py-2 text-xs font-semibold transition ${
                  selected === index
                    ? "border-slate-950 bg-slate-950 text-white"
                    : "border-slate-200 bg-white text-slate-600 hover:border-slate-300 hover:bg-slate-50"
                }`}
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>

        {/* CHAT */}

        <div className="space-y-5 bg-slate-50 p-5 sm:p-7">

          <div className="ml-auto max-w-[82%] rounded-2xl rounded-tr-md bg-slate-950 px-4 py-3 text-sm leading-6 text-white">
            {current.question}
          </div>

          <div className="max-w-[92%] rounded-2xl rounded-tl-md border border-slate-200 bg-white p-5 shadow-sm">

            <div className="mb-3 flex items-center gap-2">
              <div className="grid h-7 w-7 place-items-center rounded-lg bg-blue-50 text-blue-600">
                <Brain size={14} />
              </div>

              <span className="text-xs font-bold text-slate-900">
                NEXA
              </span>

              <span className="text-[11px] text-slate-400">
                AI Tutor
              </span>
            </div>

            <p className="text-sm leading-7 text-slate-700">
              {current.answer}
            </p>

            <div className="mt-4 grid gap-3 sm:grid-cols-3">
              {current.points.map((point) => (
                <div
                  key={point}
                  className="rounded-xl border border-slate-200 bg-slate-50 p-3"
                >
                  <div className="flex items-center gap-2">
                    <CheckCircle2
                      size={14}
                      className="text-emerald-500"
                    />

                    <span className="text-xs font-semibold text-slate-800">
                      {point}
                    </span>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-4 flex items-center gap-2 rounded-xl border border-blue-100 bg-blue-50 px-3 py-2.5 text-xs text-blue-700">
              <Sparkles size={13} />
              NEXA adapts the explanation to your learning context.
            </div>
          </div>
        </div>

        {/* INPUT */}

        <div className="border-t border-slate-200 bg-white p-4">
          <div className="flex items-center gap-3 rounded-xl border border-slate-200 px-4 py-3">
            <span className="flex-1 text-sm text-slate-400">
              Ask NEXA anything...
            </span>

            <button className="grid h-8 w-8 place-items-center rounded-lg bg-slate-950 text-white transition hover:bg-slate-800">
              <ArrowRight size={15} />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}