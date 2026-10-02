export type StudyDay = {
  day: string
  hours: number
}

export type SubjectProgress = {
  id: string
  name: string
  code: string
  progress: number
  lastActivity: string
}

export type CalendarEventType =
  | "lecture"
  | "assignment"
  | "exam"
  | "deadline"

export type CalendarEvent = {
  id: string
  date: string
  title: string
  type: CalendarEventType
  subject?: string
}

export type DashboardStats = {
  subjects: number
  aiSessions: number
  studyHours: number
  semesterProgress: number
}