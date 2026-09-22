"use client";

import { useId, useState } from "react";

type Props = {
  /** Set on state pages so you know which pack the subscriber is waiting for. */
  stateName?: string;
  buttonLabel?: string;
  tone?: "light" | "dark";
};

export function NotifyForm({ stateName, buttonLabel = "Notify me", tone = "light" }: Props) {
  const id = useId();
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    // TODO: Wire up your email provider here (ConvertKit/Kit, Mailchimp, Beehiiv, Gumroad, etc.).
    // Send `email` and `stateName` (undefined on the home page) to your provider's API or
    // embed endpoint, then show the confirmation below only on success.
    setSubmitted(true);
  }

  const dark = tone === "dark";

  if (submitted) {
    return (
      <p
        role="status"
        className={`rounded-xl px-4 py-4 text-base ${dark ? "bg-cream-100/10 text-cream-50" : "bg-white text-navy-900"}`}
      >
        Thanks! We&apos;ll email you{stateName ? ` as soon as the ${stateName} pack is live` : " when there are updates"}.
      </p>
    );
  }

  return (
    <form onSubmit={onSubmit} className="flex flex-col gap-3 sm:flex-row">
      <label htmlFor={id} className="sr-only">
        Email address
      </label>
      <input
        id={id}
        type="email"
        required
        autoComplete="email"
        inputMode="email"
        placeholder="you@example.com"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className={`h-14 w-full flex-1 rounded-xl border-2 px-4 text-base focus:border-gold-500 focus:outline-none ${
          dark
            ? "border-cream-100/20 bg-navy-900 text-cream-50 placeholder:text-cream-300/60"
            : "border-navy-900/15 bg-white text-navy-900 placeholder:text-navy-700/60"
        }`}
      />
      {stateName && <input type="hidden" name="state" value={stateName} />}
      <button
        type="submit"
        className="h-14 shrink-0 rounded-xl bg-gold-500 px-6 text-base font-semibold text-navy-950 transition hover:bg-gold-400 active:translate-y-px"
      >
        {buttonLabel}
      </button>
    </form>
  );
}
