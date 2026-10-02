"use client"

import {
  BookOpen,
  Check,
  Code2,
  HelpCircle,
  Lightbulb,
  Sparkles,
  ChevronUp,
  ChevronDown,
} from "lucide-react"
import { useEffect, useRef, useState } from "react"

export type TutorMode =
  | "normal"
  | "explain"
  | "study"
  | "code"
  | "quiz"

type TutorModeProps = {
  mode: TutorMode
  onChange: (mode: TutorMode) => void
}

const MODE_CONFIG = {
  normal: {
    label: "Normal",
    description: "General NEXA tutoring",
    icon: Sparkles,
  },
  explain: {
    label: "Explain",
    description: "Break down difficult concepts",
    icon: Lightbulb,
  },
  study: {
    label: "Study",
    description: "Learn a topic step by step",
    icon: BookOpen,
  },
  code: {
    label: "Code",
    description: "Understand and work with code",
    icon: Code2,
  },
  quiz: {
    label: "Quiz",
    description: "Test your understanding",
    icon: HelpCircle,
  },
} as const

const MODES: TutorMode[] = [
  "normal",
  "explain",
  "study",
  "code",
  "quiz",
]

export default function TutorMode({
  mode,
  onChange,
}: TutorModeProps) {
  const [open, setOpen] = useState(false)
  const containerRef = useRef<HTMLDivElement>(null)

  const current = MODE_CONFIG[mode]
  const CurrentIcon = current.icon

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        containerRef.current &&
        !containerRef.current.contains(event.target as Node)
      ) {
        setOpen(false)
      }
    }

    document.addEventListener("mousedown", handleClickOutside)

    return () => {
      document.removeEventListener("mousedown", handleClickOutside)
    }
  }, [])

  function selectMode(nextMode: TutorMode) {
    onChange(nextMode)
    setOpen(false)
  }

  return (
    <div
      ref={containerRef}
      className="relative"
    >
      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        className="inline-flex min-h-10 items-center gap-2 rounded-xl px-2.5 text-xs font-semibold text-slate-600 transition hover:bg-slate-100 hover:text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
        aria-haspopup="menu"
        aria-expanded={open}
      >
        <span className="grid h-6 w-6 place-items-center rounded-lg bg-slate-100 text-slate-600">
          <CurrentIcon size={13} />
        </span>

        <span className="hidden sm:inline">
          NEXA · {current.label}
        </span>

        <span className="sm:hidden">
          {current.label}
        </span>

        {open ? (
          <ChevronUp size={14} className="text-slate-400" />
        ) : (
          <ChevronDown size={14} className="text-slate-400" />
        )}
      </button>

      {open && (
        <div
          className="absolute bottom-full left-0 z-50 mb-2 w-[280px] overflow-hidden rounded-2xl border border-slate-200 bg-white p-1.5 shadow-xl shadow-slate-900/10"
          role="menu"
        >
          <div className="px-3 pb-2 pt-2">
            <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
              NEXA learning mode
            </p>
          </div>

          {MODES.map((modeKey) => {
            const config = MODE_CONFIG[modeKey]
            const Icon = config.icon
            const selected = modeKey === mode

            return (
              <button
                key={modeKey}
                type="button"
                role="menuitem"
                onClick={() => selectMode(modeKey)}
                className={[
                  "flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left transition",
                  selected
                    ? "bg-blue-50"
                    : "hover:bg-slate-50",
                ].join(" ")}
              >
                <span
                  className={[
                    "grid h-9 w-9 shrink-0 place-items-center rounded-xl",
                    selected
                      ? "bg-white text-blue-600 shadow-sm"
                      : "bg-slate-100 text-slate-500",
                  ].join(" ")}
                >
                  <Icon size={16} />
                </span>

                <span className="min-w-0 flex-1">
                  <span
                    className={[
                      "block text-xs font-semibold",
                      selected
                        ? "text-blue-700"
                        : "text-slate-800",
                    ].join(" ")}
                  >
                    {config.label}
                  </span>

                  <span className="mt-0.5 block text-[10px] leading-4 text-slate-500">
                    {config.description}
                  </span>
                </span>

                {selected && (
                  <Check
                    size={15}
                    className="shrink-0 text-blue-600"
                  />
                )}
              </button>
            )
          })}
        </div>
      )}
    </div>
  )
}