"use client"

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Filler,
} from "chart.js"
import { Line } from "react-chartjs-2"

import { weeklyStudyData } from "@/lib/dashboard/data"

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Filler,
)

export default function WeeklyStudyChart() {
  const data = {
    labels: weeklyStudyData.map((item) => item.day),

    datasets: [
      {
        data: weeklyStudyData.map((item) => item.hours),
        borderWidth: 2,
        tension: 0.4,
        fill: true,
        pointRadius: 3,
        pointHoverRadius: 5,
      },
    ],
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,

    plugins: {
      legend: {
        display: false,
      },

      tooltip: {
        displayColors: false,

        callbacks: {
          label: (context: { parsed: { y: number | null } }) =>
            `${context.parsed.y ?? 0} hours`,
        },
      },
    },

    scales: {
      x: {
        grid: {
          display: false,
        },

        border: {
          display: false,
        },

        ticks: {
          color: "#94a3b8",
          font: {
            size: 11,
          },
        },
      },

      y: {
        beginAtZero: true,

        border: {
          display: false,
        },

        grid: {
          color: "#f1f5f9",
        },

        ticks: {
          color: "#94a3b8",
          font: {
            size: 11,
          },

          callback: (value: string | number) => `${value}h`,
        },
      },
    },
  }

  return (
    <div className="nexa-card p-6">
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-base font-bold text-slate-950">
            Weekly study activity
          </h2>

          <p className="mt-1 text-xs text-slate-500">
            Your study time over the last seven days.
          </p>
        </div>

        <div className="rounded-lg bg-blue-50 px-3 py-1.5">
          <span className="text-xs font-semibold text-blue-600">
            8.5h total
          </span>
        </div>
      </div>

      <div className="mt-6 h-64">
        <Line data={data} options={options} />
      </div>
    </div>
  )
}