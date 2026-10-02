"use client"

import { useMemo, useState } from "react"
import {
  CalendarDays,
  ChevronLeft,
  ChevronRight,
  ClipboardCheck,
  GraduationCap,
  BookOpen,
  Clock3,
} from "lucide-react"

import { calendarEvents } from "@/lib/dashboard/data"
import type {
  CalendarEvent,
  CalendarEventType,
} from "@/lib/dashboard/types"

const eventStyles: Record<
  CalendarEventType,
  {
    label: string
    icon: typeof BookOpen
    className: string
    dotClassName: string
  }
> = {
  lecture: {
    label: "Lecture",
    icon: BookOpen,
    className: "bg-blue-50 text-blue-600",
    dotClassName: "bg-blue-500",
  },
  assignment: {
    label: "Assignment",
    icon: ClipboardCheck,
    className: "bg-amber-50 text-amber-600",
    dotClassName: "bg-amber-500",
  },
  exam: {
    label: "Exam",
    icon: GraduationCap,
    className: "bg-red-50 text-red-600",
    dotClassName: "bg-red-500",
  },
  deadline: {
    label: "Deadline",
    icon: Clock3,
    className: "bg-purple-50 text-purple-600",
    dotClassName: "bg-purple-500",
  },
}

function parseLocalDate(value: string) {
  const [year, month, day] = value.split("-").map(Number)

  return new Date(year, month - 1, day)
}

function isSameDay(first: Date, second: Date) {
  return (
    first.getFullYear() === second.getFullYear() &&
    first.getMonth() === second.getMonth() &&
    first.getDate() === second.getDate()
  )
}

function formatDate(date: Date) {
  return [
    date.getFullYear(),
    String(date.getMonth() + 1).padStart(2, "0"),
    String(date.getDate()).padStart(2, "0"),
  ].join("-")
}

export default function AcademicCalendar() {
  const [currentMonth, setCurrentMonth] = useState(
    new Date(2026, 9, 1),
  )

  const [selectedDate, setSelectedDate] = useState(
    new Date(2026, 9, 5),
  )

  const days = useMemo(() => {
    const year = currentMonth.getFullYear()
    const month = currentMonth.getMonth()

    const firstDay = new Date(year, month, 1)
    const lastDay = new Date(year, month + 1, 0)

    const startOffset = firstDay.getDay()
    const totalDays = lastDay.getDate()

    const calendarDays: (Date | null)[] = []

    for (let index = 0; index < startOffset; index++) {
      calendarDays.push(null)
    }

    for (let day = 1; day <= totalDays; day++) {
      calendarDays.push(new Date(year, month, day))
    }

    return calendarDays
  }, [currentMonth])

  const selectedEvents = calendarEvents.filter((event) =>
    isSameDay(parseLocalDate(event.date), selectedDate),
  )

  const monthEvents = calendarEvents.filter((event) => {
    const date = parseLocalDate(event.date)

    return (
      date.getFullYear() === currentMonth.getFullYear() &&
      date.getMonth() === currentMonth.getMonth()
    )
  })

  function goToPreviousMonth() {
    setCurrentMonth(
      new Date(
        currentMonth.getFullYear(),
        currentMonth.getMonth() - 1,
        1,
      ),
    )
  }

  function goToNextMonth() {
    setCurrentMonth(
      new Date(
        currentMonth.getFullYear(),
        currentMonth.getMonth() + 1,
        1,
      ),
    )
  }

  function goToToday() {
    const today = new Date()

    setCurrentMonth(
      new Date(
        today.getFullYear(),
        today.getMonth(),
        1,
      ),
    )

    setSelectedDate(today)
  }

  return (
    <section className="nexa-card overflow-hidden">
      {/* Header */}
      <div className="flex flex-col gap-4 border-b border-slate-200 px-4 py-5 sm:px-6 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-3">
          <div className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-blue-50 text-blue-600">
            <CalendarDays size={18} />
          </div>

          <div>
            <h2 className="text-base font-bold text-slate-950">
              Academic calendar
            </h2>

            <p className="mt-1 text-xs text-slate-500">
              Semester 4 · Academic events and deadlines
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={goToToday}
          className="self-start rounded-lg border border-slate-200 px-3 py-2 text-xs font-semibold text-slate-600 transition hover:bg-slate-50 sm:self-auto"
        >
          Today
        </button>
      </div>

      <div className="grid lg:grid-cols-[1fr_280px]">
        {/* Calendar */}
        <div className="p-3 sm:p-6">
          {/* Month navigation */}
          <div className="mb-4 flex items-center justify-between sm:mb-5">
            <h3 className="text-sm font-bold text-slate-950">
              {currentMonth.toLocaleDateString("en-US", {
                month: "long",
                year: "numeric",
              })}
            </h3>

            <div className="flex items-center gap-1">
              <button
                type="button"
                onClick={goToPreviousMonth}
                className="grid h-8 w-8 place-items-center rounded-lg text-slate-500 transition hover:bg-slate-100 hover:text-slate-900"
                aria-label="Previous month"
              >
                <ChevronLeft size={16} />
              </button>

              <button
                type="button"
                onClick={goToNextMonth}
                className="grid h-8 w-8 place-items-center rounded-lg text-slate-500 transition hover:bg-slate-100 hover:text-slate-900"
                aria-label="Next month"
              >
                <ChevronRight size={16} />
              </button>
            </div>
          </div>

          {/* Weekdays */}
          <div className="grid grid-cols-7 border-b border-slate-100 pb-2 sm:pb-3">
            {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map(
              (day) => (
                <div
                  key={day}
                  className="text-center text-[9px] font-bold uppercase tracking-wide text-slate-400 sm:text-[10px]"
                >
                  {day}
                </div>
              ),
            )}
          </div>

          {/* Calendar days */}
          <div className="grid grid-cols-7">
            {days.map((day, index) => {
              if (!day) {
                return (
                  <div
                    key={`empty-${index}`}
                    className="h-12 border-b border-r border-slate-100 sm:h-16"
                  />
                )
              }

              const dayEvents = calendarEvents.filter((event) =>
                isSameDay(parseLocalDate(event.date), day),
              )

              const selected = isSameDay(day, selectedDate)
              const today = isSameDay(day, new Date())

              return (
                <button
                  key={formatDate(day)}
                  type="button"
                  onClick={() => setSelectedDate(day)}
                  className={[
                    "relative flex h-12 flex-col items-center border-b border-r border-slate-100 p-1.5 transition",
                    "hover:bg-slate-50 sm:h-16 sm:items-start sm:p-2",
                    selected ? "bg-blue-50/60" : "",
                  ].join(" ")}
                >
                  <div
                    className={[
                      "grid h-6 w-6 place-items-center rounded-full text-[11px] font-semibold sm:h-7 sm:w-7 sm:text-xs",
                      today
                        ? "bg-slate-950 text-white"
                        : selected
                          ? "bg-blue-600 text-white"
                          : "text-slate-700",
                    ].join(" ")}
                  >
                    {day.getDate()}
                  </div>

                  {dayEvents.length > 0 && (
                    <div className="mt-1 flex gap-0.5 sm:gap-1">
                      {dayEvents.slice(0, 3).map((event) => (
                        <span
                          key={event.id}
                          className={[
                            "h-1.5 w-1.5 rounded-full",
                            eventStyles[event.type].dotClassName,
                          ].join(" ")}
                        />
                      ))}
                    </div>
                  )}
                </button>
              )
            })}
          </div>

          {/* Legend */}
          <div className="mt-4 flex flex-wrap gap-x-4 gap-y-2 sm:mt-5 sm:gap-x-5">
            {Object.entries(eventStyles).map(([type, config]) => (
              <div
                key={type}
                className="flex items-center gap-1.5 text-[10px] text-slate-500 sm:gap-2 sm:text-[11px]"
              >
                <span
                  className={[
                    "h-2 w-2 rounded-full",
                    config.dotClassName,
                  ].join(" ")}
                />

                {config.label}
              </div>
            ))}
          </div>
        </div>

        {/* Selected day */}
        <aside className="border-t border-slate-200 bg-slate-50/60 p-4 sm:p-6 lg:border-l lg:border-t-0">
          <p className="text-[10px] font-bold uppercase tracking-[0.16em] text-slate-400">
            Selected day
          </p>

          <h3 className="mt-2 text-lg font-bold text-slate-950">
            {selectedDate.toLocaleDateString("en-US", {
              weekday: "long",
              month: "long",
              day: "numeric",
            })}
          </h3>

          <div className="mt-5 space-y-3">
            {selectedEvents.length === 0 ? (
              <div className="rounded-xl border border-dashed border-slate-200 bg-white p-4 text-center">
                <p className="text-xs font-medium text-slate-500">
                  No academic events
                </p>

                <p className="mt-1 text-[11px] leading-5 text-slate-400">
                  Enjoy the day or use it for revision.
                </p>
              </div>
            ) : (
              selectedEvents.map((event: CalendarEvent) => {
                const config = eventStyles[event.type]
                const Icon = config.icon

                return (
                  <div
                    key={event.id}
                    className="rounded-xl border border-slate-200 bg-white p-4"
                  >
                    <div className="flex items-start gap-3">
                      <div
                        className={[
                          "grid h-9 w-9 shrink-0 place-items-center rounded-lg",
                          config.className,
                        ].join(" ")}
                      >
                        <Icon size={16} />
                      </div>

                      <div className="min-w-0">
                        <p className="text-xs font-bold text-slate-900">
                          {event.title}
                        </p>

                        {event.subject && (
                          <p className="mt-1 text-[11px] text-slate-400">
                            {event.subject}
                          </p>
                        )}

                        <p className="mt-2 text-[10px] font-semibold uppercase tracking-wide text-slate-400">
                          {config.label}
                        </p>
                      </div>
                    </div>
                  </div>
                )
              })
            )}
          </div>

          <div className="mt-5 rounded-xl bg-white p-4 ring-1 ring-slate-200">
            <p className="text-[10px] font-bold uppercase tracking-wide text-slate-400">
              This month
            </p>

            <p className="mt-1 text-xl font-bold text-slate-950">
              {monthEvents.length}
            </p>

            <p className="mt-1 text-[11px] text-slate-500">
              academic events scheduled
            </p>
          </div>
        </aside>
      </div>
    </section>
  )
}