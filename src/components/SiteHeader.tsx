import Link from "next/link";

export function Monogram({ className = "" }: { className?: string }) {
  return (
    <span
      aria-hidden="true"
      className={`inline-flex items-center justify-center rounded-md bg-navy-900 font-serif font-semibold text-cream-100 ring-1 ring-gold-500/60 ${className}`}
    >
      T<span className="text-gold-400">&amp;</span>T
    </span>
  );
}

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-30 border-b border-navy-900/10 bg-cream-100/90 backdrop-blur supports-[backdrop-filter]:bg-cream-100/75">
      <div className="mx-auto flex h-16 max-w-5xl items-center justify-between px-4 sm:px-6">
        <Link href="/" className="flex min-h-11 items-center gap-2.5" aria-label="Talents & Titles home">
          <Monogram className="h-9 w-11 text-[15px]" />
          <span className="font-serif text-lg font-semibold tracking-tight">Talents &amp; Titles</span>
        </Link>
        <Link
          href="/#find-your-state"
          className="inline-flex min-h-11 items-center rounded-full bg-navy-900 px-4 text-sm font-semibold text-cream-100 transition hover:bg-navy-800"
        >
          Find your state
        </Link>
      </div>
    </header>
  );
}
