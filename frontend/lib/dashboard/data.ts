import type {
  CalendarEvent,
  DashboardStats,
  StudyDay,
  SubjectProgress,
} from "./types"

export const dashboardStats: DashboardStats = {
  subjects: 4,
  aiSessions: 12,
  studyHours: 8.5,
  semesterProgress: 72,
}

export const weeklyStudyData: StudyDay[] = [
  { day: "Mon", hours: 1.2 },
  { day: "Tue", hours: 2.1 },
  { day: "Wed", hours: 0.8 },
  { day: "Thu", hours: 1.7 },
  { day: "Fri", hours: 1.1 },
  { day: "Sat", hours: 1.0 },
  { day: "Sun", hours: 0.6 },
]

export const subjectProgress: SubjectProgress[] = [
  {
    id: "dcn",
    name: "Data Communication & Networking",
    code: "DCN",
    progress: 78,
    lastActivity: "Studied 2 hours ago",
  },
  {
    id: "numerical-methods",
    name: "Numerical Methods",
    code: "NM",
    progress: 64,
    lastActivity: "Studied yesterday",
  },
  {
    id: "web-technology",
    name: "Web Technology",
    code: "WT",
    progress: 82,
    lastActivity: "Studied 2 days ago",
  },
  {
    id: "dotnet",
    name: "C# & .NET",
    code: ".NET",
    progress: 51,
    lastActivity: "Studied 3 days ago",
  },
]

export const calendarEvents: CalendarEvent[] = [
  {
    id: "1",
    date: "2026-10-05",
    title: "DCN Assignment",
    type: "assignment",
    subject: "DCN",
  },
  {
    id: "2",
    date: "2026-10-08",
    title: "Web Technology Lecture",
    type: "lecture",
    subject: "WT",
  },
  {
    id: "3",
    date: "2026-10-12",
    title: "Numerical Methods Assignment",
    type: "deadline",
    subject: "NM",
  },
  {
    id: "4",
    date: "2026-10-19",
    title: "DCN Internal Exam",
    type: "exam",
    subject: "DCN",
  },
  {
    id: "5",
    date: "2026-10-24",
    title: "C# & .NET Assignment",
    type: "deadline",
    subject: ".NET",
  },
]