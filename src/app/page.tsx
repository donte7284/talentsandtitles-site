import Link from "next/link";
import { states, PACK_CONTENTS } from "@/data/states";
import { StatePicker } from "@/components/StatePicker";
import { PackContents } from "@/components/PackContents";
import { NotifyForm } from "@/components/NotifyForm";
import { Faq, type FaqItem } from "@/components/Faq";
import { Section } from "@/components/Section";

const faqs: FaqItem[] = [
  {
    q: "Who are these packs for?",
    a: "Self-managing landlords — people who own one or a handful of rentals and handle leasing, notices and deposits themselves, without a property manager.",
  },
  {
    q: "How are these different from free templates online?",
    a: "Generic templates are written to work \"everywhere,\" which usually means they miss state rules on security deposit limits and return deadlines, notice periods, required disclosures and entry notice. Each of our packs is researched against that state's current landlord-tenant statutes.",
  },
  {
    q: "What format are the files in?",
    a: `${PACK_CONTENTS.wordDocuments.length} editable Word (.docx) documents that open in Microsoft Word or Google Docs, an Excel (.xlsx) security deposit tracker, and an HTML calculator that opens in any web browser, works offline, and never sends your data anywhere.`,
  },
  {
    q: "Does the pack include a lease?",
    a: "No. The pack is built to work alongside the lease you already use. It covers everything around it: inspections, deposits, notices, screening, and a State Disclosure Addendum you attach to every new lease and renewal.",
  },
  {
    q: "How do I get my files after I buy?",
    a: "Checkout is handled by Gumroad or Etsy. Your download link arrives instantly by email and stays in your Gumroad library or Etsy purchases.",
  },
  {
    q: "What if my state's law changes?",
    a: "Landlord-tenant law changes often. Join the email list and we'll let you know when your state's pack is updated.",
  },
  {
    q: "Is this legal advice?",
    a: "No. Talents & Titles is not a law firm. The forms are templates for informational purposes. For advice about your specific situation, consult a licensed attorney in your state.",
  },
];

const whyOurs = [
  {
    title: "Built from your state's statutes",
    body: "Every pack is researched against the state's current landlord-tenant code — not a one-size-fits-all template with the state name swapped in.",
  },
  {
    title: "The rules that trip landlords up",
    body: "Deposit caps and return deadlines, notice periods, entry notice and required disclosures are the details generic forms get wrong.",
  },
  {
    title: "Updated for current law",
    body: "Packs are reviewed as laws change, so you're not working from a form written years ago.",
  },
  {
    title: "Everything in one download",
    body: "Checklists, notices, deposit forms, a plain-English rulebook, a tracker and a calculator. Everything you need alongside your own lease, not scattered across bookmarks.",
  },
];

export default function Home() {
  const pickerStates = states.map(({ name, slug, abbreviation }) => ({ name, slug, abbreviation }));

  return (
    <>
      {/* Hero + state picker */}
      <section className="relative overflow-hidden bg-navy-900 text-cream-50">
        <div
          aria-hidden="true"
          className="pointer-events-none absolute inset-0 opacity-[0.07]"
          style={{
            backgroundImage:
              "repeating-linear-gradient(0deg, #f7f1e5 0 1px, transparent 1px 32px), repeating-linear-gradient(90deg, #f7f1e5 0 1px, transparent 1px 32px)",
          }}
        />
        <div className="relative mx-auto max-w-5xl px-4 pt-12 pb-14 sm:px-6 sm:pt-20 sm:pb-20">
          <p className="inline-flex items-center gap-2 rounded-full border border-gold-400/40 px-3 py-1 text-xs font-semibold tracking-[0.14em] text-gold-400 uppercase">
            For self-managing landlords · All 50 states
          </p>
          <h1 className="mt-5 max-w-3xl font-serif text-4xl leading-[1.08] font-semibold tracking-tight text-balance sm:text-6xl">
            State-specific landlord forms, <span className="text-gold-400 italic">updated for current law</span>
          </h1>
          <p className="mt-5 max-w-xl text-lg leading-relaxed text-cream-200">
            Notices, checklists and deposit forms written for your state, plus a deposit tracker and calculator. Built
            to work alongside your own lease. One download, ready to use.
          </p>

          <div id="find-your-state" className="mt-8 max-w-xl scroll-mt-24 rounded-2xl bg-cream-100 p-4 text-navy-900 shadow-2xl sm:p-5">
            <p className="mb-3 font-serif text-lg font-semibold">Find your state&apos;s pack</p>
            <StatePicker states={pickerStates} />
          </div>

          <ul className="mt-8 flex flex-wrap gap-x-6 gap-y-2 text-sm text-cream-200">
            <li>✓ {PACK_CONTENTS.wordDocuments.length} editable Word documents</li>
            <li>✓ Excel tracker</li>
            <li>✓ Interactive calculator</li>
            <li>✓ Instant download</li>
          </ul>
        </div>
      </section>

      <Section
        id="whats-inside"
        eyebrow="What's in every pack"
        title="12 files for every stage of a tenancy"
        intro="Each state pack follows the same structure, customized to that state's rules, and built to work alongside the lease you already use."
      >
        <PackContents />
      </Section>

      <Section
        id="why-ours"
        eyebrow="Why ours"
        title="Researched against each state's current statutes — not generic templates"
        className="bg-cream-50"
      >
        <div className="grid gap-4 sm:grid-cols-2">
          {whyOurs.map((item, i) => (
            <div key={item.title} className="rounded-2xl border border-navy-900/10 bg-white p-5 sm:p-6">
              <span className="font-serif text-2xl font-semibold text-gold-500">0{i + 1}</span>
              <h3 className="mt-2 font-serif text-xl font-semibold">{item.title}</h3>
              <p className="mt-2 text-[15px] leading-relaxed text-navy-800">{item.body}</p>
            </div>
          ))}
        </div>
      </Section>

      <Section id="all-states" eyebrow="Browse" title="All 50 states">
        <ul className="grid grid-cols-2 gap-2 sm:grid-cols-3 lg:grid-cols-4">
          {states.map((s) => (
            <li key={s.slug}>
              <Link
                href={`/landlord-forms/${s.slug}`}
                className="flex min-h-12 items-center justify-between rounded-lg border border-navy-900/10 bg-white px-3 text-[15px] transition hover:border-gold-500 hover:bg-cream-50"
              >
                <span>{s.name}</span>
                <span className="text-xs font-semibold text-navy-700/50">{s.abbreviation}</span>
              </Link>
            </li>
          ))}
        </ul>
      </Section>

      {/* Email signup */}
      <section id="notify" className="scroll-mt-20 bg-navy-900 py-14 text-cream-50 sm:py-20">
        <div className="mx-auto max-w-5xl px-4 sm:px-6">
          <p className="text-xs font-semibold tracking-[0.16em] text-gold-400 uppercase">Stay current</p>
          <h2 className="mt-2 max-w-2xl font-serif text-3xl leading-tight font-semibold tracking-tight text-balance sm:text-4xl">
            Get notified when laws change or new state packs launch
          </h2>
          <p className="mt-3 max-w-xl text-base text-cream-200 sm:text-lg">
            Occasional emails only. Unsubscribe anytime.
          </p>
          <div className="mt-8 max-w-xl">
            <NotifyForm tone="dark" buttonLabel="Sign me up" />
          </div>
        </div>
      </section>

      <Section id="faq" eyebrow="FAQ" title="Questions landlords ask">
        <Faq items={faqs} />
      </Section>
    </>
  );
}
