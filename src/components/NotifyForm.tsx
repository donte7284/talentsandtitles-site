"use client";

import { useId, useRef, useState } from "react";
import { usePathname } from "next/navigation";

type Props = {
  /** Set on state pages so you know which pack the subscriber is waiting for. */
  stateName?: string;
  buttonLabel?: string;
  tone?: "light" | "dark";
};

type Status = "idle" | "loading" | "success" | "error";

const FALLBACK_ERROR = "Something went wrong. Please check your connection and try again.";

export function NotifyForm({ stateName, buttonLabel = "Notify me", tone = "light" }: Props) {
  const id = useId();
  const pathname = usePathname();
  const formRef = useRef<HTMLFormElement>(null);
  const honeypotRef = useRef<HTMLInputElement>(null);
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<Status>("idle");
  const [error, setError] = useState("");

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    if (status === "loading") return;
    setStatus("loading");
    setError("");

    try {
      const res = await fetch("/api/subscribe", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          email,
          state: stateName ?? "",
          sourcePage: pathname,
          website: honeypotRef.current?.value ?? "",
        }),
      });
      const data: { ok?: boolean; error?: string } = await res.json().catch(() => ({}));
      if (res.ok && data.ok) {
        setStatus("success");
      } else {
        setError(data.error || FALLBACK_ERROR);
        setStatus("error");
      }
    } catch {
      setError(FALLBACK_ERROR);
      setStatus("error");
    }
  }

  const dark = tone === "dark";
  const loading = status === "loading";

  if (status === "success") {
    return (
      <p
        role="status"
        className={`flex items-start gap-3 rounded-xl px-4 py-4 text-base ${dark ? "bg-cream-100/10 text-cream-50" : "bg-white text-navy-900"}`}
      >
        <span aria-hidden="true" className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-gold-500 text-sm font-bold text-navy-950">
          ✓
        </span>
        You&apos;re on the list — we&apos;ll email you when it&apos;s ready.
      </p>
    );
  }

  return (
    <form ref={formRef} onSubmit={onSubmit} className="relative">
      <div className="flex flex-col gap-3 sm:flex-row">
        <label htmlFor={id} className="sr-only">
          Email address
        </label>
        <input
          id={id}
          type="email"
          name="email"
          required
          maxLength={254}
          autoComplete="email"
          inputMode="email"
          placeholder="you@example.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          disabled={loading}
          aria-invalid={status === "error" || undefined}
          aria-describedby={status === "error" ? `${id}-error` : undefined}
          className={`h-14 w-full flex-1 rounded-xl border-2 px-4 text-base focus:border-gold-500 focus:outline-none disabled:opacity-70 ${
            dark
              ? "border-cream-100/20 bg-navy-900 text-cream-50 placeholder:text-cream-300/60"
              : "border-navy-900/15 bg-white text-navy-900 placeholder:text-navy-700/60"
          }`}
        />

        {/* Honeypot: hidden from people and screen readers; bots that fill every field get flagged. */}
        <div aria-hidden="true" className="absolute -left-[9999px] h-px w-px overflow-hidden">
          <label htmlFor={`${id}-website`}>Website</label>
          <input ref={honeypotRef} id={`${id}-website`} type="text" name="website" tabIndex={-1} autoComplete="off" defaultValue="" />
        </div>

        <button
          type="submit"
          disabled={loading}
          aria-busy={loading}
          className="inline-flex h-14 shrink-0 items-center justify-center gap-2 rounded-xl bg-gold-500 px-6 text-base font-semibold text-navy-950 transition hover:bg-gold-400 active:translate-y-px disabled:cursor-wait disabled:opacity-80"
        >
          {loading && (
            <svg aria-hidden="true" viewBox="0 0 24 24" className="h-5 w-5 animate-spin" fill="none">
              <circle cx="12" cy="12" r="9" stroke="currentColor" strokeOpacity="0.25" strokeWidth="3" />
              <path d="M21 12a9 9 0 0 0-9-9" stroke="currentColor" strokeWidth="3" strokeLinecap="round" />
            </svg>
          )}
          {loading ? "Signing you up…" : buttonLabel}
        </button>
      </div>

      {status === "error" && (
        <div
          id={`${id}-error`}
          role="alert"
          className={`mt-3 flex flex-wrap items-center gap-x-3 gap-y-1 rounded-xl px-4 py-3 text-[15px] ${
            dark ? "bg-red-400/15 text-cream-50" : "bg-red-50 text-red-900"
          }`}
        >
          <span>{error}</span>
          <button
            type="button"
            onClick={() => formRef.current?.requestSubmit()}
            className="inline-flex min-h-11 items-center font-semibold underline underline-offset-2"
          >
            Try again
          </button>
        </div>
      )}
    </form>
  );
}
