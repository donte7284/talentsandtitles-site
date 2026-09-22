import Link from "next/link";
import { site } from "@/lib/site";
import { Monogram } from "./SiteHeader";

export function SiteFooter() {
  const year = new Date().getFullYear();
  return (
    <footer className="bg-navy-950 text-cream-200">
      <div className="mx-auto max-w-5xl px-4 py-12 sm:px-6">
        <div className="flex items-center gap-2.5">
          <Monogram className="h-9 w-11 text-[15px]" />
          <span className="font-serif text-lg font-semibold text-cream-50">Talents &amp; Titles</span>
        </div>
        <p className="mt-3 max-w-md text-sm text-cream-300">{site.tagline}.</p>

        <nav aria-label="Footer" className="mt-6 flex flex-wrap gap-x-2 gap-y-1 text-sm">
          <Link href="/#find-your-state" className="inline-flex min-h-11 items-center pr-4 hover:text-gold-400">
            All 50 states
          </Link>
          <Link href="/#faq" className="inline-flex min-h-11 items-center pr-4 hover:text-gold-400">
            FAQ
          </Link>
          <Link href="/disclaimer" className="inline-flex min-h-11 items-center pr-4 hover:text-gold-400">
            Legal disclaimer
          </Link>
        </nav>

        <p className="mt-6 border-t border-cream-100/10 pt-6 text-xs leading-relaxed text-cream-300">
          <strong className="font-semibold text-cream-100">Disclaimer:</strong> {site.disclaimerShort}{" "}
          <Link href="/disclaimer" className="underline underline-offset-2 hover:text-gold-400">
            Read the full disclaimer
          </Link>
          .
        </p>
        <p className="mt-4 text-xs text-cream-300/70">
          © {year} {site.name}. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
