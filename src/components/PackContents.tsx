import { PACK_CONTENTS } from "@/data/states";

function DocIcon() {
  return (
    <svg aria-hidden="true" viewBox="0 0 24 24" className="mt-0.5 h-5 w-5 shrink-0 text-gold-600" fill="none" stroke="currentColor" strokeWidth="1.8">
      <path d="M7 3h7l5 5v13H7z" strokeLinejoin="round" />
      <path d="M14 3v5h5M10 13h6M10 17h6" strokeLinecap="round" />
    </svg>
  );
}

export function PackContents({ stateName }: { stateName?: string }) {
  const { wordDocuments, excel, calculator } = PACK_CONTENTS;
  return (
    <div className="grid gap-4 md:grid-cols-5">
      <div className="rounded-2xl border border-navy-900/10 bg-white p-5 sm:p-6 md:col-span-3">
        <p className="text-xs font-semibold tracking-[0.14em] text-gold-600 uppercase">
          {wordDocuments.length} Word documents
        </p>
        <h3 className="mt-1 font-serif text-xl font-semibold">
          {stateName ? `${stateName} notices, checklists & forms` : "Notices, checklists & forms"}
        </h3>
        <ol className="mt-4 space-y-3">
          {wordDocuments.map((doc) => (
            <li key={doc.title} className="flex gap-3 text-[15px] leading-snug">
              <DocIcon />
              <span>
                <span className="font-medium">{doc.title}</span>
                {doc.detail && <span className="mt-0.5 block text-sm text-navy-700">{doc.detail}</span>}
              </span>
            </li>
          ))}
        </ol>
        <p className="mt-5 border-t border-navy-900/10 pt-4 text-sm text-navy-700">
          Editable files that open in Microsoft Word or Google Docs. Built to work alongside your own lease.
        </p>
      </div>

      <div className="flex flex-col gap-4 md:col-span-2">
        <div className="rounded-2xl border border-navy-900/10 bg-white p-5 sm:p-6">
          <p className="text-xs font-semibold tracking-[0.14em] text-gold-600 uppercase">Excel tracker</p>
          <h3 className="mt-1 font-serif text-xl font-semibold">{excel.title}</h3>
          <p className="mt-2 text-[15px] text-navy-700">{excel.description}</p>
        </div>
        <div className="rounded-2xl bg-navy-900 p-5 text-cream-100 sm:p-6">
          <p className="text-xs font-semibold tracking-[0.14em] text-gold-400 uppercase">Interactive calculator</p>
          <h3 className="mt-1 font-serif text-xl font-semibold text-cream-50">{calculator.title}</h3>
          <p className="mt-2 text-[15px] text-cream-200">{calculator.description}</p>
        </div>
      </div>
    </div>
  );
}
