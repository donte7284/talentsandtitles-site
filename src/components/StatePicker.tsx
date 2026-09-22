"use client";

import { useId, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";

type Option = { name: string; slug: string; abbreviation: string };

export function StatePicker({ states }: { states: Option[] }) {
  const router = useRouter();
  const listId = useId();
  const inputRef = useRef<HTMLInputElement>(null);
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState(0);

  const matches = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return states;
    // Exact abbreviation first ("TX"), then names that start with the query, then contains.
    const abbr = states.filter((s) => s.abbreviation.toLowerCase() === q);
    const starts = states.filter((s) => s.name.toLowerCase().startsWith(q) && !abbr.includes(s));
    const contains = states.filter(
      (s) => s.name.toLowerCase().includes(q) && !starts.includes(s) && !abbr.includes(s),
    );
    return [...abbr, ...starts, ...contains];
  }, [query, states]);

  function go(slug: string) {
    setOpen(false);
    router.push(`/landlord-forms/${slug}`);
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setOpen(true);
      setActive((i) => Math.min(i + 1, matches.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActive((i) => Math.max(i - 1, 0));
    } else if (e.key === "Enter") {
      e.preventDefault();
      const pick = matches[active] ?? matches[0];
      if (pick) go(pick.slug);
    } else if (e.key === "Escape") {
      setOpen(false);
    }
  }

  return (
    <div className="space-y-3">
      <div className="relative">
        <label htmlFor={`${listId}-input`} className="sr-only">
          Search for your state
        </label>
        <svg
          aria-hidden="true"
          viewBox="0 0 20 20"
          className="pointer-events-none absolute top-1/2 left-4 h-5 w-5 -translate-y-1/2 text-navy-700"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <circle cx="9" cy="9" r="6" />
          <path d="m14 14 4 4" strokeLinecap="round" />
        </svg>
        <input
          ref={inputRef}
          id={`${listId}-input`}
          type="text"
          inputMode="search"
          autoComplete="off"
          enterKeyHint="go"
          placeholder="Type your state (e.g. Texas or TX)"
          role="combobox"
          aria-expanded={open}
          aria-controls={listId}
          aria-autocomplete="list"
          aria-activedescendant={open && matches[active] ? `${listId}-${matches[active].slug}` : undefined}
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setActive(0);
            setOpen(true);
          }}
          onFocus={() => setOpen(true)}
          onBlur={() => setTimeout(() => setOpen(false), 150)}
          onKeyDown={onKeyDown}
          className="h-14 w-full rounded-xl border-2 border-navy-900/15 bg-white pr-4 pl-12 text-base text-navy-900 shadow-sm placeholder:text-navy-700/60 focus:border-gold-500 focus:outline-none"
        />
        {open && (
          <ul
            id={listId}
            role="listbox"
            className="absolute z-20 mt-2 max-h-72 w-full overflow-y-auto overscroll-contain rounded-xl border border-navy-900/10 bg-white py-1 shadow-xl"
          >
            {matches.length === 0 ? (
              <li className="px-4 py-3 text-sm text-navy-700">No state matches “{query}”.</li>
            ) : (
              matches.map((s, i) => (
                <li
                  key={s.slug}
                  id={`${listId}-${s.slug}`}
                  role="option"
                  aria-selected={i === active}
                  onMouseDown={(e) => e.preventDefault()}
                  onClick={() => go(s.slug)}
                  onMouseEnter={() => setActive(i)}
                  className={`flex min-h-12 cursor-pointer items-center justify-between px-4 text-base ${
                    i === active ? "bg-cream-100" : ""
                  }`}
                >
                  <span>{s.name}</span>
                  <span className="text-xs font-semibold tracking-wider text-navy-700/60">{s.abbreviation}</span>
                </li>
              ))
            )}
          </ul>
        )}
      </div>

      <div className="relative">
        <label htmlFor={`${listId}-select`} className="sr-only">
          Or select your state from a list
        </label>
        <select
          id={`${listId}-select`}
          defaultValue=""
          onChange={(e) => e.target.value && go(e.target.value)}
          className="h-14 w-full appearance-none rounded-xl border-2 border-navy-900/15 bg-cream-50 px-4 text-base text-navy-900 focus:border-gold-500 focus:outline-none"
        >
          <option value="" disabled>
            …or pick from the list
          </option>
          {states.map((s) => (
            <option key={s.slug} value={s.slug}>
              {s.name}
            </option>
          ))}
        </select>
        <svg
          aria-hidden="true"
          viewBox="0 0 20 20"
          className="pointer-events-none absolute top-1/2 right-4 h-5 w-5 -translate-y-1/2 text-navy-700"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <path d="m5 8 5 5 5-5" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </div>
    </div>
  );
}
