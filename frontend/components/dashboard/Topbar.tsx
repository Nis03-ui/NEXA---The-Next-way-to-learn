"use client"

import { Menu, Bell, Sparkles } from "lucide-react"
import { useState } from "react"

import Sidebar from "@/components/dashboard/Sidebar"

export default function Topbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <>
      <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-slate-200 bg-white/95 px-4 backdrop-blur sm:h-20 sm:px-6 lg:px-8">
        {/* Mobile menu */}
        <button
          type="button"
          onClick={() => setMobileMenuOpen(true)}
          className="grid h-10 w-10 place-items-center rounded-xl text-slate-600 transition hover:bg-slate-100 lg:hidden"
          aria-label="Open navigation"
        >
          <Menu size={20} />
        </button>

        {/* Desktop workspace information */}
        <div className="hidden lg:block">
          <h2 className="text-sm font-semibold text-slate-900">
            Learning Workspace
          </h2>

          <p className="mt-0.5 text-xs text-slate-400">
            AI-powered education assistant
          </p>
        </div>

        {/* Mobile brand */}
        <div className="flex items-center gap-2 lg:hidden">
          <div className="grid h-8 w-8 place-items-center rounded-lg bg-slate-950 text-white">
            <Sparkles size={15} />
          </div>

          <span className="text-sm font-black tracking-tight text-slate-950">
            NEXA
          </span>
        </div>

        {/* Right actions */}
        <div className="flex items-center gap-2">
          <button
            type="button"
            className="grid h-9 w-9 place-items-center rounded-xl text-slate-400 transition hover:bg-slate-100 hover:text-slate-700"
            aria-label="Notifications"
          >
            <Bell size={17} />
          </button>

          <div className="grid h-9 w-9 place-items-center rounded-full bg-slate-950 text-xs font-bold text-white">
            N
          </div>
        </div>
      </header>

      {/* Mobile navigation */}
      {mobileMenuOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          {/* Backdrop */}
          <button
            type="button"
            onClick={() => setMobileMenuOpen(false)}
            className="absolute inset-0 bg-slate-950/30 backdrop-blur-[2px]"
            aria-label="Close navigation"
          />

          {/* Drawer */}
          <div className="absolute left-0 top-0 h-full w-[280px] bg-white shadow-2xl">
            <Sidebar
              mobile
              onNavigate={() => setMobileMenuOpen(false)}
            />
          </div>
        </div>
      )}
    </>
  )
}