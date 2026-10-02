"use client"

import { useState } from "react"
import {
  ArrowRight,
  BookOpen,
  Brain,
  CheckCircle2,
  MessageSquare,
  Sparkles,
} from "lucide-react"

const steps = [
  {
    number: "01",
    label: "ASK",
    title: "Ask without hesitation.",
    description:
      "Ask NEXA about a difficult topic, a confusing definition, or something you simply want to understand better.",
    icon: MessageSquare,
    items: [
      "Ask questions naturally",
      "Follow up on explanations",
      "Explore difficult concepts",
    ],
  },
  {
    number: "02",
    label: "UNDERSTAND",
    title: "Turn confusion into clarity.",
    description:
      "NEXA explains concepts in a structured way and can ground answers in the course material available to you.",
    icon: Brain,
    items: [
      "Clear explanations",
      "Course-aware context",
      "Source-backed answers",
    ],
  },
  {
    number: "03",
    label: "PRACTICE",
    title: "Make knowledge stick.",
    description:
      "Move beyond reading. Use what you learned to test your understanding and strengthen your knowledge.",
    icon: CheckCircle2,
    items: [
      "Practice concepts",
      "Test your understanding",
      "Build stronger recall",
    ],
  },
]

export function HowNexaWorks() {
  const [active, setActive] = useState(0)
  const step = steps[active]
  const Icon = step.icon

  return (
    <section
      id="how-it-works"
      className="border-b border-slate-200 bg-[#f8fafc] py-24 lg:py-32"
    >
      <div className="mx-auto max-w-7xl px-6">

        {/* HEADER */}

        <div className="max-w-2xl">
          <div className="mb-4 inline-flex items-center gap-2 text-sm font-semibold text-blue-600">
            <Sparkles size={16} />
            How NEXA works
          </div>

          <h2 className="text-4xl font-bold tracking-[-0.035em] text-slate-950 sm:text-5xl">
            From question to
            <span className="block text-slate-400">
              understanding.
            </span>
          </h2>

          <p className="mt-5 text-lg leading-8 text-slate-600">
            NEXA turns studying into a simple loop: ask what you don't
            understand, learn the concept, then practice it.
          </p>
        </div>

        {/* WORKFLOW */}

        <div className="mt-16 grid gap-10 lg:grid-cols-[0.8fr_1.2fr]">

          {/* STEPS */}

          <div className="space-y-3">
            {steps.map((item, index) => {
              const ItemIcon = item.icon
              const isActive = index === active

              return (
                <button
                  key={item.label}
                  onClick={() => setActive(index)}
                  className={`group flex w-full items-center gap-4 rounded-2xl border p-5 text-left transition ${
                    isActive
                      ? "border-slate-900 bg-white shadow-lg shadow-slate-900/5"
                      : "border-transparent bg-transparent hover:border-slate-200 hover:bg-white"
                  }`}
                >
                  <div
                    className={`grid h-12 w-12 shrink-0 place-items-center rounded-xl transition ${
                      isActive
                        ? "bg-slate-950 text-white"
                        : "bg-white text-slate-400 group-hover:text-slate-700"
                    }`}
                  >
                    <ItemIcon size={19} />
                  </div>

                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <span className="text-[11px] font-bold tracking-widest text-slate-400">
                        {item.number}
                      </span>

                      <span
                        className={`text-sm font-bold ${
                          isActive
                            ? "text-slate-950"
                            : "text-slate-600"
                        }`}
                      >
                        {item.label}
                      </span>
                    </div>

                    <p
                      className={`mt-1 text-sm ${
                        isActive
                          ? "text-slate-600"
                          : "text-slate-400"
                      }`}
                    >
                      {item.title}
                    </p>
                  </div>

                  <ArrowRight
                    size={17}
                    className={`transition ${
                      isActive
                        ? "translate-x-0 text-slate-950"
                        : "-translate-x-1 text-slate-300"
                    }`}
                  />
                </button>
              )
            })}
          </div>

          {/* DETAIL PANEL */}

          <div className="relative overflow-hidden rounded-3xl border border-slate-200 bg-white p-7 shadow-[0_20px_60px_rgba(15,23,42,0.06)] sm:p-10">

            <div className="absolute right-0 top-0 h-48 w-48 rounded-full bg-blue-100/50 blur-3xl" />

            <div className="relative">

              <div className="flex items-center justify-between">
                <div className="grid h-12 w-12 place-items-center rounded-2xl bg-slate-950 text-white">
                  <Icon size={21} />
                </div>

                <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-[11px] font-bold tracking-wider text-slate-500">
                  {step.number}
                </span>
              </div>

              <h3 className="mt-10 text-3xl font-bold tracking-[-0.03em] text-slate-950">
                {step.title}
              </h3>

              <p className="mt-4 max-w-xl text-base leading-7 text-slate-600">
                {step.description}
              </p>

              <div className="mt-8 space-y-3">
                {step.items.map((item) => (
                  <div
                    key={item}
                    className="flex items-center gap-3 rounded-xl border border-slate-200 bg-slate-50 px-4 py-3"
                  >
                    <CheckCircle2
                      size={16}
                      className="shrink-0 text-emerald-500"
                    />

                    <span className="text-sm font-medium text-slate-700">
                      {item}
                    </span>
                  </div>
                ))}
              </div>

              <div className="mt-8 flex items-center gap-3 border-t border-slate-200 pt-6">
                <div className="grid h-9 w-9 place-items-center rounded-lg bg-blue-50 text-blue-600">
                  <BookOpen size={16} />
                </div>

                <div>
                  <p className="text-xs font-semibold text-slate-900">
                    Built around your learning
                  </p>

                  <p className="mt-0.5 text-xs text-slate-500">
                    Learn concepts instead of memorizing answers.
                  </p>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>
    </section>
  )
}