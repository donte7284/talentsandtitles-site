export type FaqItem = { q: string; a: string };

export function Faq({ items }: { items: FaqItem[] }) {
  return (
    <div className="divide-y divide-navy-900/10 rounded-2xl border border-navy-900/10 bg-white">
      {items.map((item) => (
        <details key={item.q} className="group px-5 sm:px-6">
          <summary className="flex min-h-16 cursor-pointer list-none items-center justify-between gap-4 py-4 font-serif text-lg font-semibold [&::-webkit-details-marker]:hidden">
            {item.q}
            <span
              aria-hidden="true"
              className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-cream-100 text-xl leading-none text-navy-900 transition group-open:rotate-45"
            >
              +
            </span>
          </summary>
          <p className="pb-5 text-[15px] leading-relaxed text-navy-800">{item.a}</p>
        </details>
      ))}
    </div>
  );
}
