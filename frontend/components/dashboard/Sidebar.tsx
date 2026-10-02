"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  LayoutDashboard,
  MessageSquare,
  BookOpen,
  Settings,
  Sparkles,
} from "lucide-react"

type SidebarProps = {
  mobile?: boolean
  onNavigate?: () => void
}

const links = [
  {
    name: "Dashboard",
    href: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    name: "AI Tutor",
    href: "/tutor",
    icon: MessageSquare,
  },
]

export default function Sidebar({
  mobile = false,
  onNavigate,
}: SidebarProps) {
  const pathname = usePathname()

  return (
    <aside
      className={
        mobile
          ? "h-full w-full bg-white"
          : "fixed left-0 top-0 z-40 hidden h-screen w-64 border-r border-slate-200 bg-white lg:block"
      }
    >
      <div className="flex h-full flex-col">
        {/* Brand */}
        <div className="flex h-20 items-center px-6">
          <Link
            href="/dashboard"
            onClick={onNavigate}
            className="flex items-center gap-2.5"
          >
            <div className="grid h-9 w-9 place-items-center rounded-xl bg-slate-950 text-white">
              <Sparkles size={17} />
            </div>

            <div>
              <p className="text-lg font-black tracking-tight text-slate-950">
                NEXA
              </p>

              <p className="text-[9px] font-semibold uppercase tracking-[0.16em] text-slate-400">
                Learn smarter
              </p>
            </div>
          </Link>
        </div>

        {/* Navigation */}
        <div className="flex-1 px-3 py-5">
          <p className="px-3 pb-3 text-[10px] font-bold uppercase tracking-[0.16em] text-slate-400">
            Workspace
          </p>

          <nav className="space-y-1">
            {links.map((item) => {
              const Icon = item.icon

              const active =
                pathname === item.href ||
                pathname.startsWith(`${item.href}/`)

              return (
                <Link
                  key={item.name}
                  href={item.href}
                  onClick={onNavigate}
                  className={[
                    "flex h-11 items-center gap-3 rounded-xl px-3 text-sm font-medium transition",
                    active
                      ? "bg-slate-950 text-white shadow-sm"
                      : "text-slate-500 hover:bg-slate-50 hover:text-slate-900",
                  ].join(" ")}
                >
                  <Icon
                    size={17}
                    strokeWidth={active ? 2.2 : 1.9}
                  />

                  <span>{item.name}</span>

                  {active && (
                    <span className="ml-auto h-1.5 w-1.5 rounded-full bg-white" />
                  )}
                </Link>
              )
            })}
          </nav>
        </div>

        {/* NEXA CTA */}
        <div className="border-t border-slate-100 p-4">
          <div className="rounded-2xl bg-slate-50 p-4">
            <div className="flex items-center gap-2">
              <Sparkles
                size={15}
                className="text-blue-600"
              />

              <p className="text-xs font-bold text-slate-900">
                NEXA AI
              </p>
            </div>

            <p className="mt-2 text-[11px] leading-5 text-slate-500">
              Your intelligent study companion for understanding difficult
              concepts.
            </p>

            <Link
              href="/tutor"
              onClick={onNavigate}
              className="mt-3 flex h-9 items-center justify-center rounded-lg bg-white text-[11px] font-semibold text-slate-700 ring-1 ring-slate-200 transition hover:bg-slate-100"
            >
              Ask NEXA
            </Link>
          </div>
        </div>
      </div>
    </aside>
  )
}