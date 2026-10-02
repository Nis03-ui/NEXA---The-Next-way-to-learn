"use client"

import { ArrowUp } from "lucide-react"
import { FormEvent, useState } from "react"

type ChatInputProps = {
  onSubmit: (message: string) => void
  disabled?: boolean
}

export function ChatInput({
  onSubmit,
  disabled = false,
}: ChatInputProps) {
  const [value, setValue] = useState("")

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const message = value.trim()

    if (!message || disabled) return

    onSubmit(message)
    setValue("")
  }

  return (
    <form onSubmit={handleSubmit} className="border-t border-slate-200 p-4">
      <div className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white px-4 py-2.5 transition focus-within:border-slate-400 focus-within:ring-4 focus-within:ring-slate-100">
        <input
          value={value}
          onChange={(event) => setValue(event.target.value)}
          disabled={disabled}
          placeholder="Ask NEXA anything..."
          className="flex-1 bg-transparent text-sm text-slate-900 outline-none placeholder:text-slate-400 disabled:cursor-not-allowed"
        />

        <button
          type="submit"
          disabled={disabled || !value.trim()}
          className="grid h-9 w-9 shrink-0 place-items-center rounded-lg bg-slate-950 text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-30"
        >
          <ArrowUp size={16} />
        </button>
      </div>
    </form>
  )
}