"use client"

import {
  BookOpen,
  Brain,
  FileText,
  MessageSquare,
  Search,
  Sparkles,
} from "lucide-react"

const features = [
  {
    icon: Brain,
    label: "AI TUTOR",
    title: "An AI tutor that explains.",
    description:
      "Ask questions naturally and get explanations designed to help you understand the concept instead of simply giving you an answer.",
    className: "lg:col-span-2",
  },
  {
    icon: Search,
    label: "RAG",
    title: "Answers grounded in your material.",
    description:
      "NEXA can retrieve relevant course content and use it as context when answering your questions.",
    className: "",
  },
  {
    icon: FileText,
    label: "SOURCES",
    title: "Know where the answer came from.",
    description:
      "Relevant learning sources can be surfaced alongside an AI response.",
    className: "",
  },
  {
    icon: MessageSquare,
    label: "CONVERSATION",
    title: "Keep the conversation going.",
    description:
      "Ask follow-up questions without restarting the learning process.",
    className: "",
  },
  {
    icon: BookOpen,
    label: "LEARNING",
    title: "Built around your courses.",
    description:
      "NEXA is designed to connect AI assistance with the material you're actually studying.",
    className: "lg:col-span-2",
  },
]

export function FeatureShowcase() {
  return (
    <section
      id="features"
      className="border-b border-slate-200 bg-white py-24 lg:py-32"
    >
      <div className="mx-auto max-w-7xl px-6">

        {/* HEADER */}

        <div className="max-w-2xl">
          <div className="mb-4 inline-flex items-center gap-2 text-sm font-semibold text-blue-600">
            <Sparkles size={16} />
            Built for learning
          </div>

          <h2 className="text-4xl font-bold tracking-[-0.035em] text-slate-950 sm:text-5xl">
            Everything you need
            <span className="block text-slate-400">
              to learn with AI.
            </span>
          </h2>

          <p className="mt-5 text-lg leading-8 text-slate-600">
            NEXA combines conversational AI with your learning material to
            create a more useful study experience.
          </p>
        </div>

        {/* FEATURES */}

        <div className="mt-16 grid gap-4 lg:grid-cols-3">
          {features.map((feature) => {
            const Icon = feature.icon

            return (
              <article
                key={feature.label}
                className={`group relative overflow-hidden rounded-3xl border border-slate-200 bg-slate-50 p-7 transition duration-300 hover:-translate-y-1 hover:border-slate-300 hover:bg-white hover:shadow-xl hover:shadow-slate-900/5 ${feature.className}`}
              >
                <div className="absolute -right-12 -top-12 h-32 w-32 rounded-full bg-blue-100/50 blur-3xl transition group-hover:bg-blue-200/60" />

                <div className="relative">
                  <div className="grid h-11 w-11 place-items-center rounded-xl bg-white text-slate-900 shadow-sm ring-1 ring-slate-200">
                    <Icon size={19} />
                  </div>

                  <div className="mt-8">
                    <span className="text-[10px] font-bold tracking-[0.18em] text-blue-600">
                      {feature.label}
                    </span>

                    <h3 className="mt-2 text-2xl font-bold tracking-[-0.025em] text-slate-950">
                      {feature.title}
                    </h3>

                    <p className="mt-3 max-w-lg text-sm leading-7 text-slate-600">
                      {feature.description}
                    </p>
                  </div>

                  {/* MINI PRODUCT VISUAL */}

                  <div className="mt-8 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
                    {feature.label === "AI TUTOR" && (
                      <div className="space-y-3">
                        <div className="ml-auto w-2/3 rounded-xl bg-slate-950 px-3 py-2 text-xs text-white">
                          Why does recursion need a base case?
                        </div>

                        <div className="w-4/5 rounded-xl border border-slate-200 bg-slate-50 px-3 py-3 text-xs leading-5 text-slate-600">
                          The base case tells the recursive function when to
                          stop calling itself.
                        </div>
                      </div>
                    )}

                    {feature.label === "RAG" && (
                      <div className="space-y-2">
                        <div className="flex items-center gap-2 rounded-lg bg-blue-50 px-3 py-2 text-xs text-blue-700">
                          <Search size={13} />
                          Searching course material...
                        </div>

                        <div className="rounded-lg border border-slate-200 p-3">
                          <p className="text-xs font-semibold text-slate-800">
                            Computer Networks
                          </p>

                          <p className="mt-1 text-[11px] text-slate-500">
                            TCP / UDP fundamentals
                          </p>
                        </div>
                      </div>
                    )}

                    {feature.label === "SOURCES" && (
                      <div className="space-y-2">
                        <div className="flex items-center gap-2">
                          <FileText size={14} className="text-blue-600" />

                          <span className="text-xs font-semibold text-slate-800">
                            Retrieved source
                          </span>
                        </div>

                        <div className="rounded-lg bg-slate-50 p-3 text-[11px] leading-5 text-slate-500">
                          Computer Networks · Transport Layer
                        </div>
                      </div>
                    )}

                    {feature.label === "CONVERSATION" && (
                      <div className="flex items-center gap-2">
                        <div className="grid h-8 w-8 place-items-center rounded-lg bg-blue-50 text-blue-600">
                          <MessageSquare size={14} />
                        </div>

                        <div className="flex-1">
                          <div className="h-2 w-3/4 rounded-full bg-slate-200" />
                          <div className="mt-2 h-2 w-1/2 rounded-full bg-slate-100" />
                        </div>
                      </div>
                    )}

                    {feature.label === "LEARNING" && (
                      <div className="flex items-center gap-3">
                        <div className="grid h-9 w-9 place-items-center rounded-lg bg-blue-50 text-blue-600">
                          <BookOpen size={15} />
                        </div>

                        <div className="flex-1">
                          <div className="flex items-center justify-between">
                            <span className="text-xs font-semibold text-slate-800">
                              Course progress
                            </span>

                            <span className="text-[10px] font-medium text-slate-400">
                              68%
                            </span>
                          </div>

                          <div className="mt-2 h-1.5 overflow-hidden rounded-full bg-slate-100">
                            <div className="h-full w-[68%] rounded-full bg-blue-600" />
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </article>
            )
          })}
        </div>
      </div>
    </section>
  )
}