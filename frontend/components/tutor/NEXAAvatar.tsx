"use client"

import {
  Brain,
  Check,
  Sparkles,
} from "lucide-react"

type AvatarState =
  | "idle"
  | "thinking"
  | "responding"

type NEXAAvatarProps = {
  state: AvatarState
  compact?: boolean
}

export default function NEXAAvatar({
  state,
  compact = false,
}: NEXAAvatarProps) {
  const thinking = state === "thinking"
  const responding = state === "responding"

  const statusText = thinking
    ? "Thinking..."
    : responding
      ? "Responding..."
      : "Ready to learn"

  /*
   * Compact mode
   * Used inside the tutor header.
   */
  if (compact) {
    return (
      <div className="relative flex items-center">
        {/* Glow */}
        <div
          className={[
            "absolute inset-0 rounded-full bg-blue-400/25 blur-lg transition-all duration-500",
            thinking
              ? "scale-125 opacity-100"
              : responding
                ? "scale-110 opacity-90"
                : "scale-90 opacity-60",
          ].join(" ")}
        />

        {/* Avatar */}
        <div
          className={[
            "relative grid h-10 w-10 place-items-center overflow-hidden rounded-xl border border-slate-200 bg-slate-950 shadow-sm transition-all duration-500",
            thinking
              ? "scale-105 shadow-blue-200"
              : responding
                ? "scale-[1.03] shadow-blue-100"
                : "scale-100",
          ].join(" ")}
        >
          {/* Inner light */}
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_35%,rgba(59,130,246,0.32),transparent_60%)]" />

          {/* Active ring */}
          {(thinking || responding) && (
            <div
              className={[
                "absolute inset-1.5 rounded-lg border border-blue-400/30",
                thinking ? "animate-pulse" : "opacity-70",
              ].join(" ")}
            />
          )}

          {/* NEXA mark */}
          <div
            className={[
              "relative flex flex-col items-center transition-transform duration-500",
              thinking
                ? "scale-105"
                : responding
                  ? "scale-110"
                  : "scale-100",
            ].join(" ")}
          >
            <Sparkles
              size={7}
              className={[
                "mb-0.5 text-blue-400",
                thinking
                  ? "animate-pulse"
                  : responding
                    ? "animate-bounce"
                    : "",
              ].join(" ")}
            />

            <span className="text-base font-black leading-none text-white">
              N
            </span>
          </div>

          {/* Thinking */}
          {thinking && (
            <div className="absolute bottom-1 flex gap-0.5">
              <span className="h-0.5 w-0.5 animate-bounce rounded-full bg-blue-400 [animation-delay:-0.3s]" />
              <span className="h-0.5 w-0.5 animate-bounce rounded-full bg-blue-400 [animation-delay:-0.15s]" />
              <span className="h-0.5 w-0.5 animate-bounce rounded-full bg-blue-400" />
            </div>
          )}

          {/* Responding */}
          {responding && (
            <div className="absolute bottom-1 right-1">
              <span className="grid h-3 w-3 place-items-center rounded-full bg-blue-500">
                <Check size={7} className="text-white" />
              </span>
            </div>
          )}
        </div>

        {/* Status */}
        <div className="ml-2 hidden md:block">
          <p className="text-[10px] font-semibold text-slate-700">
            NEXA
          </p>

          <div className="flex items-center gap-1">
            <span
              className={[
                "h-1.5 w-1.5 rounded-full",
                thinking
                  ? "animate-pulse bg-amber-400"
                  : responding
                    ? "animate-pulse bg-blue-500"
                    : "bg-emerald-500",
              ].join(" ")}
            />

            <span className="text-[9px] text-slate-400">
              {statusText}
            </span>
          </div>
        </div>
      </div>
    )
  }

  /*
   * Full avatar
   * Used when NEXA needs to be the visual centerpiece.
   */
  return (
    <div className="flex flex-col items-center">
      <div className="relative">
        {/* Ambient glow */}
        <div
          className={[
            "absolute inset-0 rounded-[28%] bg-blue-400/20 blur-2xl transition-all duration-700",
            thinking
              ? "scale-125 opacity-100"
              : responding
                ? "scale-110 opacity-90"
                : "scale-90 opacity-60",
          ].join(" ")}
        />

        {/* Avatar */}
        <div
          className={[
            "relative grid h-24 w-24 place-items-center overflow-hidden rounded-[28%] border border-slate-200 bg-slate-950 shadow-xl transition-all duration-500 sm:h-28 sm:w-28",
            thinking
              ? "scale-105 shadow-blue-200"
              : responding
                ? "scale-[1.03] shadow-blue-100"
                : "scale-100",
          ].join(" ")}
        >
          {/* Inner light */}
          <div
            className={[
              "absolute inset-0 transition-opacity duration-500",
              "bg-[radial-gradient(circle_at_50%_35%,rgba(59,130,246,0.28),transparent_55%)]",
              thinking
                ? "opacity-100"
                : responding
                  ? "opacity-90"
                  : "opacity-70",
            ].join(" ")}
          />

          {/* Animated ring */}
          {(thinking || responding) && (
            <div
              className={[
                "absolute inset-3 rounded-[24%] border border-blue-400/30",
                thinking
                  ? "animate-pulse"
                  : "opacity-70",
              ].join(" ")}
            />
          )}

          {/* NEXA mark */}
          <div
            className={[
              "relative flex flex-col items-center transition-transform duration-500",
              thinking
                ? "scale-105"
                : responding
                  ? "scale-110"
                  : "scale-100",
            ].join(" ")}
          >
            <Sparkles
              size={14}
              className={[
                "mb-1 text-blue-400",
                thinking
                  ? "animate-pulse"
                  : responding
                    ? "animate-bounce"
                    : "",
              ].join(" ")}
            />

            <span className="text-3xl font-black tracking-tight text-white">
              N
            </span>
          </div>

          {/* Thinking dots */}
          {thinking && (
            <div className="absolute bottom-2 flex gap-1">
              <span className="h-1 w-1 animate-bounce rounded-full bg-blue-400 [animation-delay:-0.3s]" />
              <span className="h-1 w-1 animate-bounce rounded-full bg-blue-400 [animation-delay:-0.15s]" />
              <span className="h-1 w-1 animate-bounce rounded-full bg-blue-400" />
            </div>
          )}

          {/* Responding */}
          {responding && (
            <div className="absolute bottom-2 flex items-center gap-1 rounded-full bg-blue-500/20 px-2 py-0.5">
              <Check
                size={9}
                className="text-blue-300"
              />

              <span className="text-[8px] font-semibold text-blue-300">
                Answering
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Identity */}
      <div className="mt-4 flex items-center gap-2">
        <h2 className="text-sm font-bold text-slate-950">
          NEXA
        </h2>

        <span className="grid h-5 w-5 place-items-center rounded-md bg-blue-50 text-blue-600">
          <Brain size={11} />
        </span>
      </div>

      {/* Status */}
      <div className="mt-1 flex items-center gap-1.5">
        <span
          className={[
            "h-1.5 w-1.5 rounded-full transition-colors",
            thinking
              ? "animate-pulse bg-amber-400"
              : responding
                ? "animate-pulse bg-blue-500"
                : "bg-emerald-500",
          ].join(" ")}
        />

        <p className="text-xs text-slate-500">
          {statusText}
        </p>
      </div>
    </div>
  )
}