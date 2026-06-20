// Display helpers: humanise snake_case enums, format dates, map status -> tone.

export function humanize(value: string | null | undefined): string {
  if (!value) return "—";
  return value
    .split("_")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}

export function formatDate(iso: string | null | undefined): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
}

export function formatDateTime(iso: string | null | undefined): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

type Tone = "neutral" | "green" | "amber" | "red" | "blue" | "violet";

const STATUS_TONE: Record<string, Tone> = {
  // generic
  draft: "neutral",
  active: "green",
  approved: "green",
  completed: "blue",
  archived: "neutral",
  paused: "amber",
  cancelled: "neutral",
  pending_review: "amber",
  under_review: "amber",
  confirmed: "red",
  remediated: "green",
  closed: "neutral",
  expired: "amber",
  revoked: "red",
  generated: "blue",
  final: "green",
  // severity
  informational: "neutral",
  low: "blue",
  medium: "amber",
  high: "red",
  critical: "red",
  // detection
  detected: "green",
  not_detected: "amber",
  blocked: "blue",
  // result
  executed: "blue",
  failed: "red",
  skipped: "neutral",
};

export function statusTone(value: string | null | undefined): Tone {
  if (!value) return "neutral";
  return STATUS_TONE[value] ?? "neutral";
}

export function formatBytes(bytes: number | null | undefined): string {
  if (bytes == null) return "—";
  if (bytes === 0) return "0 B";
  const units = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  return `${(bytes / 1024 ** i).toFixed(i === 0 ? 0 : 1)} ${units[i]}`;
}
