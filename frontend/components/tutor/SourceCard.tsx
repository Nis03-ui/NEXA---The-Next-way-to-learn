import {
  BookOpen,
  ChevronRight,
} from "lucide-react"

type SourceCardProps = {
  title: string
  subject: string
}

export default function SourceCard({
  title,
  subject,
}: SourceCardProps) {
  return (
    <div className="group flex items-center gap-3 rounded-xl border border-slate-200 bg-white p-3 transition hover:border-slate-300 hover:bg-slate-50">
      <div className="grid h-8 w-8 shrink-0 place-items-center rounded-lg bg-blue-50 text-blue-600">
        <BookOpen size={14} />
      </div>

      <div className="min-w-0 flex-1">
        <p className="truncate text-xs font-semibold text-slate-800">
          {title}
        </p>

        <p className="mt-0.5 truncate text-[10px] text-slate-400">
          {subject}
        </p>
      </div>

      <ChevronRight
        size={14}
        className="shrink-0 text-slate-300 transition group-hover:translate-x-0.5 group-hover:text-slate-500"
      />
    </div>
  )
}