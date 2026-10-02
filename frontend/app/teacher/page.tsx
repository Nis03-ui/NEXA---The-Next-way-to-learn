"use client"

import { useEffect, useMemo, useState } from "react"
import {
  BookOpen,
  Check,
  Edit3,
  FileText,
  Loader2,
  Plus,
  Search,
  Trash2,
  X,
} from "lucide-react"
import AppShell from "@/components/layout/AppShell"
import {
  teacher,
  type Content,
  type ContentCreate,
} from "@/lib/api"

type FormState = {
  title: string
  description: string
  subject: string
  body: string
  published: boolean
}

const emptyForm: FormState = {
  title: "",
  description: "",
  subject: "",
  body: "",
  published: false,
}

export default function TeacherPage() {
  const [content, setContent] = useState<Content[]>([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [deletingId, setDeletingId] = useState<number | null>(null)

  const [formOpen, setFormOpen] = useState(false)
  const [editingId, setEditingId] = useState<number | null>(null)
  const [form, setForm] = useState<FormState>(emptyForm)

  const [search, setSearch] = useState("")
  const [subjectFilter, setSubjectFilter] = useState("all")

  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")

  useEffect(() => {
    loadContent()
  }, [])

  async function loadContent() {
    try {
      setLoading(true)
      setError("")

      const data = await teacher.getContent()
      setContent(data)
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Unable to load teaching content.",
      )
    } finally {
      setLoading(false)
    }
  }

  function openCreate() {
    setEditingId(null)
    setForm(emptyForm)
    setFormOpen(true)
    setError("")
    setSuccess("")
  }

  function openEdit(item: Content) {
    setEditingId(item.id)

    setForm({
      title: item.title,
      description: item.description ?? "",
      subject: item.subject,
      body: item.body,
      published: item.published,
    })

    setFormOpen(true)
    setError("")
    setSuccess("")
  }

  function closeForm() {
    if (saving) return

    setFormOpen(false)
    setEditingId(null)
    setForm(emptyForm)
  }

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault()

    if (
      !form.title.trim() ||
      !form.subject.trim() ||
      !form.body.trim()
    ) {
      setError(
        "Title, subject, and content are required.",
      )
      return
    }

    try {
      setSaving(true)
      setError("")
      setSuccess("")

      const payload: ContentCreate = {
        title: form.title.trim(),
        description:
          form.description.trim() || null,
        subject: form.subject.trim(),
        body: form.body.trim(),
        published: form.published,
      }

      if (editingId !== null) {
        const updated =
          await teacher.updateContent(
            editingId,
            payload,
          )

        setContent((current) =>
          current.map((item) =>
            item.id === editingId
              ? updated
              : item,
          ),
        )

        setSuccess(
          "Content updated successfully.",
        )
      } else {
        const created =
          await teacher.createContent(payload)

        setContent((current) => [
          created,
          ...current,
        ])

        setSuccess(
          "Content created successfully.",
        )
      }

      setFormOpen(false)
      setEditingId(null)
      setForm(emptyForm)
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Unable to save this content.",
      )
    } finally {
      setSaving(false)
    }
  }

  async function handleDelete(id: number) {
    const item = content.find(
      (contentItem) =>
        contentItem.id === id,
    )

    if (!item) return

    const confirmed = window.confirm(
      `Delete "${item.title}"?\n\nThis action cannot be undone.`,
    )

    if (!confirmed) return

    try {
      setDeletingId(id)
      setError("")
      setSuccess("")

      await teacher.deleteContent(id)

      setContent((current) =>
        current.filter(
          (item) => item.id !== id,
        ),
      )

      setSuccess(
        "Content deleted successfully.",
      )
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Unable to delete this content.",
      )
    } finally {
      setDeletingId(null)
    }
  }

  async function togglePublished(
    item: Content,
  ) {
    try {
      setError("")
      setSuccess("")

      const updated =
        await teacher.updateContent(
          item.id,
          {
            published: !item.published,
          },
        )

      setContent((current) =>
        current.map((contentItem) =>
          contentItem.id === item.id
            ? updated
            : contentItem,
        ),
      )

      setSuccess(
        updated.published
          ? "Content published and available to NEXA."
          : "Content unpublished.",
      )
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Unable to update publishing status.",
      )
    }
  }

  const subjects = useMemo(() => {
    return Array.from(
      new Set(
        content.map(
          (item) => item.subject,
        ),
      ),
    ).sort()
  }, [content])

  const filteredContent = useMemo(() => {
    const query =
      search.trim().toLowerCase()

    return content.filter((item) => {
      const matchesSearch =
        !query ||
        item.title
          .toLowerCase()
          .includes(query) ||
        item.subject
          .toLowerCase()
          .includes(query) ||
        item.body
          .toLowerCase()
          .includes(query)

      const matchesSubject =
        subjectFilter === "all" ||
        item.subject === subjectFilter

      return (
        matchesSearch &&
        matchesSubject
      )
    })
  }, [
    content,
    search,
    subjectFilter,
  ])

  const publishedCount =
    content.filter(
      (item) => item.published,
    ).length

  return (
    <AppShell
      allowedRoles={[
        "TEACHER",
        "ADMIN",
      ]}
    >
      <div className="mx-auto max-w-7xl space-y-8">
        {/* Header */}
        <section className="flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
          <div>
            <p className="text-sm font-medium text-blue-600">
              Teacher workspace
            </p>

            <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
              Knowledge Base
            </h1>

            <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
              Create and manage learning material that NEXA can use
              when helping students.
            </p>
          </div>

          <button
            type="button"
            onClick={openCreate}
            className="inline-flex h-11 items-center justify-center gap-2 rounded-xl bg-slate-950 px-5 text-sm font-semibold text-white transition hover:bg-slate-800"
          >
            <Plus size={17} />
            Create content
          </button>
        </section>

        {/* Alerts */}
        {error && (
          <div className="flex items-start gap-3 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            <X
              size={17}
              className="mt-0.5 shrink-0"
            />

            <span>{error}</span>
          </div>
        )}

        {success && (
          <div className="flex items-start gap-3 rounded-xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700">
            <Check
              size={17}
              className="mt-0.5 shrink-0"
            />

            <span>{success}</span>
          </div>
        )}

        {/* Stats */}
        <section className="grid gap-4 sm:grid-cols-3">
          <StatCard
            icon={<FileText size={18} />}
            label="Total content"
            value={content.length}
          />

          <StatCard
            icon={<Check size={18} />}
            label="Published"
            value={publishedCount}
          />

          <StatCard
            icon={<BookOpen size={18} />}
            label="Subjects"
            value={subjects.length}
          />
        </section>

        {/* Content */}
        <section className="nexa-card overflow-hidden">
          <div className="border-b border-slate-200 p-5">
            <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
              <div>
                <h2 className="text-base font-bold text-slate-950">
                  Learning material
                </h2>

                <p className="mt-1 text-xs text-slate-500">
                  Published material becomes available to NEXA&apos;s
                  knowledge agent.
                </p>
              </div>

              <div className="flex flex-col gap-2 sm:flex-row">
                <div className="flex h-10 items-center gap-2 rounded-xl border border-slate-200 bg-white px-3 sm:w-64">
                  <Search
                    size={15}
                    className="shrink-0 text-slate-400"
                  />

                  <input
                    value={search}
                    onChange={(event) =>
                      setSearch(
                        event.target.value,
                      )
                    }
                    placeholder="Search content..."
                    className="min-w-0 flex-1 bg-transparent text-xs text-slate-900 outline-none placeholder:text-slate-400"
                  />
                </div>

                <select
                  value={subjectFilter}
                  onChange={(event) =>
                    setSubjectFilter(
                      event.target.value,
                    )
                  }
                  className="h-10 rounded-xl border border-slate-200 bg-white px-3 text-xs font-medium text-slate-700 outline-none focus:border-blue-400 focus:ring-4 focus:ring-blue-50"
                >
                  <option value="all">
                    All subjects
                  </option>

                  {subjects.map(
                    (subject) => (
                      <option
                        key={subject}
                        value={subject}
                      >
                        {subject}
                      </option>
                    ),
                  )}
                </select>
              </div>
            </div>
          </div>

          {loading ? (
            <div className="space-y-3 p-6">
              {[1, 2, 3].map(
                (item) => (
                  <div
                    key={item}
                    className="h-24 animate-pulse rounded-2xl bg-slate-100"
                  />
                ),
              )}
            </div>
          ) : filteredContent.length === 0 ? (
            <div className="px-6 py-20 text-center">
              <div className="mx-auto grid h-12 w-12 place-items-center rounded-2xl bg-slate-100 text-slate-400">
                <FileText size={21} />
              </div>

              <h3 className="mt-4 text-sm font-bold text-slate-900">
                {content.length === 0
                  ? "No content yet"
                  : "No matching content"}
              </h3>

              <p className="mx-auto mt-1 max-w-sm text-xs leading-5 text-slate-500">
                {content.length === 0
                  ? "Create your first learning resource to start building NEXA's knowledge base."
                  : "Try changing your search or subject filter."}
              </p>

              {content.length === 0 && (
                <button
                  type="button"
                  onClick={openCreate}
                  className="mt-5 inline-flex h-10 items-center gap-2 rounded-xl bg-slate-950 px-4 text-xs font-semibold text-white hover:bg-slate-800"
                >
                  <Plus size={15} />
                  Create content
                </button>
              )}
            </div>
          ) : (
            <div className="divide-y divide-slate-100">
              {filteredContent.map(
                (item) => (
                  <ContentRow
                    key={item.id}
                    item={item}
                    deleting={
                      deletingId === item.id
                    }
                    onEdit={() =>
                      openEdit(item)
                    }
                    onDelete={() =>
                      handleDelete(item.id)
                    }
                    onTogglePublished={() =>
                      togglePublished(item)
                    }
                  />
                ),
              )}
            </div>
          )}
        </section>
      </div>

      {/* Modal */}
      {formOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/30 p-4 backdrop-blur-sm">
          <div className="flex max-h-[90vh] w-full max-w-3xl flex-col overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-200 px-6 py-5">
              <div>
                <h2 className="text-lg font-bold text-slate-950">
                  {editingId !== null
                    ? "Edit content"
                    : "Create content"}
                </h2>

                <p className="mt-1 text-xs text-slate-500">
                  Add clear course material for students and NEXA.
                </p>
              </div>

              <button
                type="button"
                onClick={closeForm}
                className="grid h-9 w-9 place-items-center rounded-xl text-slate-400 transition hover:bg-slate-100 hover:text-slate-700"
                aria-label="Close"
              >
                <X size={18} />
              </button>
            </div>

            <form
              onSubmit={handleSubmit}
              className="min-h-0 overflow-y-auto"
            >
              <div className="space-y-5 p-6">
                <div className="grid gap-5 sm:grid-cols-[1fr_220px]">
                  <Field
                    label="Title"
                    required
                  >
                    <input
                      value={form.title}
                      onChange={(event) =>
                        setForm(
                          (current) => ({
                            ...current,
                            title:
                              event.target
                                .value,
                          }),
                        )
                      }
                      maxLength={200}
                      placeholder="e.g. TCP vs UDP"
                      className={inputClass}
                    />
                  </Field>

                  <Field
                    label="Subject"
                    required
                  >
                    <input
                      value={form.subject}
                      onChange={(event) =>
                        setForm(
                          (current) => ({
                            ...current,
                            subject:
                              event.target
                                .value,
                          }),
                        )
                      }
                      maxLength={100}
                      placeholder="e.g. DCN"
                      className={inputClass}
                    />
                  </Field>
                </div>

                <Field label="Description">
                  <textarea
                    value={form.description}
                    onChange={(event) =>
                      setForm(
                        (current) => ({
                          ...current,
                          description:
                            event.target
                              .value,
                        }),
                      )
                    }
                    maxLength={500}
                    rows={3}
                    placeholder="Short description of this learning resource..."
                    className={`${inputClass} resize-none`}
                  />
                </Field>

                <Field
                  label="Content"
                  required
                >
                  <textarea
                    value={form.body}
                    onChange={(event) =>
                      setForm(
                        (current) => ({
                          ...current,
                          body:
                            event.target
                              .value,
                        }),
                      )
                    }
                    rows={14}
                    placeholder="Write the learning material here..."
                    className={`${inputClass} resize-y`}
                  />
                </Field>

                <label className="flex cursor-pointer items-center gap-3 rounded-2xl border border-slate-200 bg-slate-50 p-4">
                  <input
                    type="checkbox"
                    checked={form.published}
                    onChange={(event) =>
                      setForm(
                        (current) => ({
                          ...current,
                          published:
                            event.target
                              .checked,
                        }),
                      )
                    }
                    className="h-4 w-4 accent-blue-600"
                  />

                  <span>
                    <span className="block text-sm font-semibold text-slate-900">
                      Publish immediately
                    </span>

                    <span className="mt-1 block text-xs leading-5 text-slate-500">
                      Published material can be retrieved by
                      NEXA&apos;s knowledge agent.
                    </span>
                  </span>
                </label>
              </div>

              <div className="flex justify-end gap-3 border-t border-slate-200 bg-slate-50 px-6 py-4">
                <button
                  type="button"
                  onClick={closeForm}
                  disabled={saving}
                  className="h-10 rounded-xl border border-slate-200 bg-white px-4 text-xs font-semibold text-slate-700 hover:bg-slate-50 disabled:opacity-50"
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  disabled={saving}
                  className="inline-flex h-10 items-center gap-2 rounded-xl bg-slate-950 px-5 text-xs font-semibold text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {saving && (
                    <Loader2
                      size={14}
                      className="animate-spin"
                    />
                  )}

                  {editingId !== null
                    ? "Save changes"
                    : "Create content"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </AppShell>
  )
}

function StatCard({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode
  label: string
  value: number
}) {
  return (
    <div className="nexa-card nexa-card-hover p-5">
      <div className="grid h-10 w-10 place-items-center rounded-xl bg-slate-100 text-slate-700">
        {icon}
      </div>

      <p className="mt-5 text-xs font-medium text-slate-500">
        {label}
      </p>

      <p className="mt-1 text-2xl font-bold tracking-tight text-slate-950">
        {value}
      </p>
    </div>
  )
}

function ContentRow({
  item,
  deleting,
  onEdit,
  onDelete,
  onTogglePublished,
}: {
  item: Content
  deleting: boolean
  onEdit: () => void
  onDelete: () => void
  onTogglePublished: () => void
}) {
  return (
    <div className="group px-5 py-5 transition hover:bg-slate-50 sm:px-6">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <div className="flex min-w-0 gap-4">
          <div className="hidden h-11 w-11 shrink-0 place-items-center rounded-xl bg-blue-50 text-blue-600 sm:grid">
            <FileText size={18} />
          </div>

          <div className="min-w-0">
            <div className="flex flex-wrap items-center gap-2">
              <h3 className="truncate text-sm font-bold text-slate-900">
                {item.title}
              </h3>

              <span className="rounded-full bg-slate-100 px-2 py-1 text-[10px] font-semibold text-slate-600">
                {item.subject}
              </span>

              <span
                className={`rounded-full px-2 py-1 text-[10px] font-semibold ${
                  item.published
                    ? "bg-emerald-50 text-emerald-700"
                    : "bg-amber-50 text-amber-700"
                }`}
              >
                {item.published
                  ? "Published"
                  : "Draft"}
              </span>
            </div>

            <p className="mt-2 line-clamp-2 text-xs leading-5 text-slate-500">
              {item.description ||
                item.body.slice(0, 180)}
            </p>

            <p className="mt-2 text-[10px] text-slate-400">
              Updated{" "}
              {new Date(
                item.updated_at ??
                  item.created_at,
              ).toLocaleDateString()}
            </p>
          </div>
        </div>

        <div className="flex shrink-0 items-center gap-2">
          <button
            type="button"
            onClick={onTogglePublished}
            className={`h-9 rounded-lg px-3 text-[11px] font-semibold transition ${
              item.published
                ? "border border-amber-200 bg-amber-50 text-amber-700 hover:bg-amber-100"
                : "border border-emerald-200 bg-emerald-50 text-emerald-700 hover:bg-emerald-100"
            }`}
          >
            {item.published
              ? "Unpublish"
              : "Publish"}
          </button>

          <button
            type="button"
            onClick={onEdit}
            className="grid h-9 w-9 place-items-center rounded-lg border border-slate-200 bg-white text-slate-500 transition hover:border-slate-300 hover:text-slate-900"
            aria-label={`Edit ${item.title}`}
          >
            <Edit3 size={14} />
          </button>

          <button
            type="button"
            onClick={onDelete}
            disabled={deleting}
            className="grid h-9 w-9 place-items-center rounded-lg border border-slate-200 bg-white text-slate-400 transition hover:border-red-200 hover:bg-red-50 hover:text-red-600 disabled:opacity-40"
            aria-label={`Delete ${item.title}`}
          >
            {deleting ? (
              <Loader2
                size={14}
                className="animate-spin"
              />
            ) : (
              <Trash2 size={14} />
            )}
          </button>
        </div>
      </div>
    </div>
  )
}

function Field({
  label,
  required,
  children,
}: {
  label: string
  required?: boolean
  children: React.ReactNode
}) {
  return (
    <label className="block">
      <span className="mb-2 block text-xs font-semibold text-slate-700">
        {label}

        {required && (
          <span className="ml-1 text-red-500">
            *
          </span>
        )}
      </span>

      {children}
    </label>
  )
}

const inputClass =
  "w-full rounded-xl border border-slate-200 bg-white px-3.5 py-3 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-blue-400 focus:ring-4 focus:ring-blue-50"