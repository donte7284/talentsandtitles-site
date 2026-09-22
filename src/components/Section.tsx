export function Section({
  id,
  eyebrow,
  title,
  intro,
  children,
  className = "",
}: {
  id?: string;
  eyebrow?: string;
  title: string;
  intro?: string;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <section id={id} className={`scroll-mt-20 py-14 sm:py-20 ${className}`}>
      <div className="mx-auto max-w-5xl px-4 sm:px-6">
        {eyebrow && <p className="text-xs font-semibold tracking-[0.16em] text-gold-600 uppercase">{eyebrow}</p>}
        <h2 className="mt-2 font-serif text-3xl leading-tight font-semibold tracking-tight text-balance sm:text-4xl">
          {title}
        </h2>
        {intro && <p className="mt-3 max-w-2xl text-base leading-relaxed text-navy-800 sm:text-lg">{intro}</p>}
        <div className="mt-8">{children}</div>
      </div>
    </section>
  );
}
