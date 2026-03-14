import * as React from "react";
import { X, AlertCircle, CheckCircle, Info, AlertTriangle } from "lucide-react";
import { useToast, type Toast, type ToastType } from "@/lib/toast";
import { cn } from "@/lib/utils";

const TOAST_STYLES: Record<
  ToastType,
  { container: string; icon: React.ReactNode }
> = {
  error: {
    container:
      "border-red-500/40 bg-[#1a0f0f] text-red-200",
    icon: <AlertCircle className="size-4 shrink-0 text-red-400" />,
  },
  warning: {
    container:
      "border-yellow-500/40 bg-[#1a1500] text-yellow-200",
    icon: <AlertTriangle className="size-4 shrink-0 text-yellow-400" />,
  },
  success: {
    container:
      "border-[#9FEF00]/40 bg-[#0d1a00] text-[#c8ff60]",
    icon: <CheckCircle className="size-4 shrink-0 text-[#9FEF00]" />,
  },
  info: {
    container:
      "border-white/20 bg-[#0D1117] text-white/80",
    icon: <Info className="size-4 shrink-0 text-white/60" />,
  },
};

function ToastItem({ toast }: { toast: Toast }) {
  const { dismiss } = useToast();
  const style = TOAST_STYLES[toast.type];

  return (
    <div
      role="alert"
      aria-live="assertive"
      className={cn(
        "flex items-start gap-3 rounded-lg border px-4 py-3 shadow-lg",
        "animate-in slide-in-from-right-4 fade-in duration-200",
        "max-w-sm w-full text-sm",
        style.container
      )}
    >
      {style.icon}
      <p className="flex-1 leading-snug">{toast.message}</p>
      <button
        onClick={() => dismiss(toast.id)}
        aria-label="Dismiss notification"
        className="ml-1 shrink-0 opacity-60 hover:opacity-100 transition-opacity"
      >
        <X className="size-4" />
      </button>
    </div>
  );
}

/** Drop this inside the layout; it renders all active toasts. */
export function ToastContainer() {
  const { toasts } = useToast();

  if (toasts.length === 0) return null;

  return (
    <div
      aria-label="Notifications"
      className="fixed bottom-6 right-6 z-[9999] flex flex-col gap-2 pointer-events-none"
    >
      {toasts.map((t) => (
        <div key={t.id} className="pointer-events-auto">
          <ToastItem toast={t} />
        </div>
      ))}
    </div>
  );
}
