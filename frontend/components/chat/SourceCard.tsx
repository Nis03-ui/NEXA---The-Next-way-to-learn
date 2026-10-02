"use client"

import { FileText } from "lucide-react"

type SourceCardProps = {
  title: string
  description?: string
}

export function SourceCard({
  title,
  description,
}: SourceCardProps) {
  return (
    <div className="flex items-start gap-3 rounded-xl border border-slate-200 bg-slate-50 p-3">
      <div className="grid h-8 w-8 shrink-0 place-items-center rounded-lg bg-white text-blue-600 ring-1 ring-slate-200">
        <FileText size={14} />
      </div>

      <div className="min-w-0">
        <p className="truncate text-xs font-semibold text-slate-800">
          {title}
        </p>

        {description && (
          <p className="mt-1 text-[11px] leading-5 text-slate-500">
            {description}
          </p>
        )}
      </div>
    </div>
  )
}