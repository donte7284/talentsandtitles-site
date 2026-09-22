import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { states, getStateBySlug, PACK_CONTENTS, PACK_YEAR, type State } from "@/data/states";
import { PackContents } from "@/components/PackContents";
import { NotifyForm } from "@/components/NotifyForm";
import { site } from "@/lib/site";

// Only the 50 states exist; anything else is a 404.
export const dynamicParams = false;

export function generateStaticParams() {
  return states.map((s) => ({ slug: s.slug }));
}

export async function generateMetadata({ params }: PageProps<"/landlord-forms/[slug]">): Promise<Metadata> {
  const { slug } = await params;
  const state = getStateBySlug(slug);
  if (!state) return {};

  const title = `${state.name} Landlord Forms Pack (${PACK_YEAR})`;
  const description = `${state.name} landlord notices, inspection checklists and deposit forms, plus a security deposit tracker and calculator — researched against current ${state.name} landlord-tenant law. Instant download.`;
  const path = `/landlord-forms/${state.slug}`;

  return {
    title: { absolute: `${title} | ${site.name}` },
    description,
    alternates: { canonical: path },
    openGraph: { type: "website", siteName: site.name, title, description, url: path },
    twitter: { card: "summary_large_image", title, description },
  };
}

function BuyButtons({ state }: { state: State }) {
  const { gumroadUrl, etsyUrl } = state;

  if (!gumroadUrl && !etsyUrl) {
    return (
      <div className="rounded-2xl border-2 border-dashed border-gold-500/60 bg-cream-50 p-5 sm:p-6">
        <p className="inline-flex items-center gap-2 rounded-full bg-gold-500/15 px-3 py-1 text-xs font-semibold tracking-[0.14em] text-gold-600 uppercase">
          Coming soon
        </p>
        <h2 className="mt-3 font-serif text-2xl font-semibold">Get notified when the {state.name} pack launches</h2>
        <p className="mt-2 text-[15px] text-navy-800">Drop your email and we&apos;ll send you the link the day it&apos;s live.</p>
        <div className="mt-5">
          <NotifyForm stateName={state.name} buttonLabel="Get notified" />
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {gumroadUrl && (
        <a
          href={gumroadUrl}
          target="_blank"
          rel="noopener"
          className="flex min-h-16 w-full items-center justify-center gap-2 rounded-xl bg-gold-500 px-6 text-lg font-semibold text-navy-950 shadow-lg shadow-gold-600/20 transition hover:bg-gold-400 active:translate-y-px"
        >
          Buy on Gumroad
          <span aria-hidden="true">→</span>
        </a>
      )}
      {etsyUrl && (
        <a
          href={etsyUrl}
          target="_blank"
          rel="noopener"
          className={
            gumroadUrl
              ? "flex min-h-14 w-full items-center justify-center rounded-xl border-2 border-navy-900/20 bg-white px-6 text-base font-semibold text-navy-900 transition hover:border-navy-900"
              : "flex min-h-16 w-full items-center justify-center gap-2 rounded-xl bg-gold-500 px-6 text-lg font-semibold text-navy-950 shadow-lg shadow-gold-600/20 transition hover:bg-gold-400"
          }
        >
          {gumroadUrl ? "Also on Etsy" : "Buy on Etsy →"}
        </a>
      )}
      <p className="pt-1 text-center text-sm text-navy-700">Instant download · Secure checkout</p>
    </div>
  );
}

export default async function StatePage({ params }: PageProps<"/landlord-forms/[slug]">) {
  const { slug } = await params;
  const state = getStateBySlug(slug);
  if (!state) notFound();

  const docCount = PACK_CONTENTS.wordDocuments.length;

  return (
    <>
      <section className="bg-navy-900 text-cream-50">
        <div className="mx-auto max-w-5xl px-4 pt-6 pb-10 sm:px-6 sm:pt-10 sm:pb-14">
          <nav aria-label="Breadcrumb" className="text-sm text-cream-300">
            <Link href="/#find-your-state" className="inline-flex min-h-11 items-center hover:text-gold-400">
              ← All states
            </Link>
          </nav>
          <p className="mt-2 text-xs font-semibold tracking-[0.16em] text-gold-400 uppercase">
            {state.abbreviation} · {PACK_YEAR} edition
          </p>
          <h1 className="mt-2 font-serif text-4xl leading-[1.08] font-semibold tracking-tight text-balance sm:text-5xl">
            {state.name} Landlord Forms Pack
          </h1>
          <p className="mt-4 max-w-2xl text-lg leading-relaxed text-cream-200">
            {docCount} Word documents, an Excel deposit tracker and an interactive calculator — researched
            against current {state.name} landlord-tenant law.
          </p>
        </div>
      </section>

      <div className="mx-auto max-w-5xl px-4 sm:px-6">
        <div className="-mt-6 max-w-xl rounded-2xl bg-cream-100 sm:-mt-8">
          <div className="rounded-2xl border border-navy-900/10 bg-white p-4 shadow-xl sm:p-5">
            <BuyButtons state={state} />
          </div>
        </div>

        {state.highlights.length > 0 && (
          <section className="mt-12">
            <p className="text-xs font-semibold tracking-[0.16em] text-gold-600 uppercase">{state.name} highlights</p>
            <h2 className="mt-2 font-serif text-3xl font-semibold tracking-tight">Built around {state.name}&apos;s rules</h2>
            <ul className="mt-6 space-y-3">
              {state.highlights.map((h) => (
                <li key={h} className="flex gap-3 rounded-xl border border-navy-900/10 bg-white p-4 text-[15px] leading-snug">
                  <span aria-hidden="true" className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-gold-500 text-xs font-bold text-navy-950">
                    ✓
                  </span>
                  <span>{h}</span>
                </li>
              ))}
            </ul>
          </section>
        )}

        <section className="mt-12">
          <p className="text-xs font-semibold tracking-[0.16em] text-gold-600 uppercase">What&apos;s in the pack</p>
          <h2 className="mt-2 font-serif text-3xl font-semibold tracking-tight">Everything in one download</h2>
          <div className="mt-6">
            <PackContents stateName={state.name} />
          </div>
        </section>

        {(state.gumroadUrl || state.etsyUrl) && (
          <div className="mt-10 max-w-xl">
            <BuyButtons state={state} />
          </div>
        )}

        <aside aria-label="Disclaimer" className="mt-12 mb-16 rounded-2xl bg-cream-200/60 p-5 text-sm leading-relaxed text-navy-800 sm:p-6">
          <p className="font-semibold text-navy-900">Disclaimer</p>
          <p className="mt-1">
            {site.disclaimerShort} Laws change, and how they apply depends on your facts and local (city/county)
            ordinances.{" "}
            <Link href="/disclaimer" className="font-medium underline underline-offset-2">
              Full disclaimer
            </Link>
            .
          </p>
        </aside>
      </div>
    </>
  );
}
