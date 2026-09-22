import type { Metadata } from "next";
import { site } from "@/lib/site";

export const metadata: Metadata = {
  title: "Legal Disclaimer",
  description: "Talents & Titles is not a law firm and does not provide legal advice.",
  alternates: { canonical: "/disclaimer" },
};

export default function DisclaimerPage() {
  return (
    <div className="mx-auto max-w-2xl px-4 py-14 sm:px-6 sm:py-20">
      <p className="text-xs font-semibold tracking-[0.16em] text-gold-600 uppercase">Legal</p>
      <h1 className="mt-2 font-serif text-4xl font-semibold tracking-tight">Disclaimer</h1>

      <p className="mt-8 rounded-2xl border-l-4 border-gold-500 bg-white p-5 font-serif text-xl leading-relaxed sm:p-6">
        {site.disclaimerShort}
      </p>

      <div className="mt-8 space-y-4 text-base leading-relaxed text-navy-800">
        <p>
          Talents &amp; Titles products are document templates and tools. Purchasing or using them does not create an
          attorney-client relationship.
        </p>
        <p>
          While each pack is researched against the state&apos;s landlord-tenant statutes, laws change and may be
          affected by court decisions and local (city or county) ordinances. We make no guarantee that any form is
          complete, current, or suitable for your specific situation.
        </p>
        <p>
          You are responsible for reviewing each document before use. For advice about your rights and obligations,
          consult a licensed attorney in your state.
        </p>
      </div>
    </div>
  );
}
