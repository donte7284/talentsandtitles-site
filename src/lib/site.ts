// On Vercel, the production domain is picked up automatically.
// Set NEXT_PUBLIC_SITE_URL in Vercel to override it (e.g. once you add a custom domain).
function resolveSiteUrl(): string {
  if (process.env.NEXT_PUBLIC_SITE_URL) return process.env.NEXT_PUBLIC_SITE_URL.replace(/\/$/, "");
  if (process.env.VERCEL_PROJECT_PRODUCTION_URL) return `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}`;
  return "http://localhost:3000";
}

export const site = {
  name: "Talents & Titles",
  url: resolveSiteUrl(),
  tagline: "State-specific landlord forms, updated for current law",
  description:
    "Landlord document packs for all 50 states: notices, checklists, deposit forms, a security deposit tracker and calculator — researched against each state's current landlord-tenant statutes.",
  disclaimerShort:
    "Talents & Titles is not a law firm and does not provide legal advice. Forms are templates for informational purposes; consult a licensed attorney in your state.",
};
