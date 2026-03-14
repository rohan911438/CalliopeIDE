import * as React from "react";
import { cn } from "@/lib/utils";

interface SpinnerProps {
  /** Tailwind size class, default "size-4" */
  className?: string;
  /** Accessible label shown to screen readers */
  label?: string;
}

/**
 * Lightweight SVG spinner that matches the existing dark theme.
 * Uses the `#9FEF00` accent colour for the active arc.
 */
export function Spinner({ className, label = "Loading…" }: SpinnerProps) {
  return (
    <span role="status" aria-label={label} className="inline-flex">
      <svg
        className={cn("animate-spin", className ?? "size-4")}
        viewBox="0 0 24 24"
        fill="none"
        aria-hidden="true"
      >
        {/* Track */}
        <circle
          className="opacity-20"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          strokeWidth="3"
        />
        {/* Active arc */}
        <path
          className="opacity-80"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        />
      </svg>
      <span className="sr-only">{label}</span>
    </span>
  );
}
