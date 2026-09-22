/**
 * ─────────────────────────────────────────────────────────────────────────
 *  THIS IS THE ONLY FILE YOU NEED TO EDIT.
 * ─────────────────────────────────────────────────────────────────────────
 *
 *  For each state:
 *    gumroadUrl  – paste the full Gumroad product link, e.g.
 *                  "https://talentsandtitles.gumroad.com/l/texas"
 *    etsyUrl     – paste the full Etsy listing link.
 *    highlights  – short bullet points shown on that state's page, e.g.
 *                  ["Security deposit returned within 30 days (Tex. Prop. Code § 92.103)"]
 *
 *  If BOTH links are null, the state page shows "Coming soon — get notified"
 *  instead of buy buttons. If only one link is set, only that button shows.
 *
 *  After editing, commit and push — Vercel redeploys automatically.
 */

/** Year shown in page titles, e.g. "Texas Landlord Forms Pack (2026)". */
export const PACK_YEAR = 2026;

/**
 * What's in every pack (12 files). Shown on the home page and on every state page.
 * `detail` is optional — leave it out for a one-line item.
 */
export const PACK_CONTENTS = {
  wordDocuments: [
    { title: "Move-In Inspection Checklist" },
    {
      title: "Move-Out Inspection Checklist",
      detail: "Captures the forwarding address that starts the deposit-return clock",
    },
    {
      title: "Security Deposit Documentation",
      detail: "Deposit receipt, itemized deduction statement, full-refund letter",
    },
    {
      title: "Late Rent & Termination Notices",
      detail: "Your state's required notice forms, plus a delivery certificate and day-count guide",
    },
    { title: "Lease Violation Notice" },
    {
      title: "Notice of Intent to Enter",
      detail: "Plus an entry log and a model lease clause",
    },
    {
      title: "Tenant Screening Checklist",
      detail: "Plus the state's required screening notice",
    },
    {
      title: "Plain-English Landlord Rulebook",
      detail: "8 sections, every rule cited to state statute, quick-reference deadline table",
    },
    {
      title: "State Disclosure Addendum",
      detail: "Attach to every new lease and renewal",
    },
    { title: "Legal Disclaimer & How to Use This Pack" },
  ] as { title: string; detail?: string }[],
  excel: {
    title: "Security Deposit Tracker",
    description: "Deadline math, status colors, deduction worksheet.",
  },
  calculator: {
    title: "Deposit Calculator & Deadline Tracker",
    description: "Opens in any browser, works offline, nothing leaves your computer.",
  },
};

export type State = {
  name: string;
  slug: string;
  abbreviation: string;
  gumroadUrl: string | null;
  etsyUrl: string | null;
  highlights: string[];
};

export const states: State[] = [
  {
    name: "Alabama",
    slug: "alabama",
    abbreviation: "AL",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Alaska",
    slug: "alaska",
    abbreviation: "AK",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Arizona",
    slug: "arizona",
    abbreviation: "AZ",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Arkansas",
    slug: "arkansas",
    abbreviation: "AR",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "California",
    slug: "california",
    abbreviation: "CA",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Colorado",
    slug: "colorado",
    abbreviation: "CO",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Connecticut",
    slug: "connecticut",
    abbreviation: "CT",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Delaware",
    slug: "delaware",
    abbreviation: "DE",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Florida",
    slug: "florida",
    abbreviation: "FL",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Georgia",
    slug: "georgia",
    abbreviation: "GA",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Hawaii",
    slug: "hawaii",
    abbreviation: "HI",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Idaho",
    slug: "idaho",
    abbreviation: "ID",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Illinois",
    slug: "illinois",
    abbreviation: "IL",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Indiana",
    slug: "indiana",
    abbreviation: "IN",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Iowa",
    slug: "iowa",
    abbreviation: "IA",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Kansas",
    slug: "kansas",
    abbreviation: "KS",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Kentucky",
    slug: "kentucky",
    abbreviation: "KY",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Louisiana",
    slug: "louisiana",
    abbreviation: "LA",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Maine",
    slug: "maine",
    abbreviation: "ME",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Maryland",
    slug: "maryland",
    abbreviation: "MD",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Massachusetts",
    slug: "massachusetts",
    abbreviation: "MA",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Michigan",
    slug: "michigan",
    abbreviation: "MI",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Minnesota",
    slug: "minnesota",
    abbreviation: "MN",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Mississippi",
    slug: "mississippi",
    abbreviation: "MS",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Missouri",
    slug: "missouri",
    abbreviation: "MO",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Montana",
    slug: "montana",
    abbreviation: "MT",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Nebraska",
    slug: "nebraska",
    abbreviation: "NE",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Nevada",
    slug: "nevada",
    abbreviation: "NV",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "New Hampshire",
    slug: "new-hampshire",
    abbreviation: "NH",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "New Jersey",
    slug: "new-jersey",
    abbreviation: "NJ",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "New Mexico",
    slug: "new-mexico",
    abbreviation: "NM",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "New York",
    slug: "new-york",
    abbreviation: "NY",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "North Carolina",
    slug: "north-carolina",
    abbreviation: "NC",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "North Dakota",
    slug: "north-dakota",
    abbreviation: "ND",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Ohio",
    slug: "ohio",
    abbreviation: "OH",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Oklahoma",
    slug: "oklahoma",
    abbreviation: "OK",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Oregon",
    slug: "oregon",
    abbreviation: "OR",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Pennsylvania",
    slug: "pennsylvania",
    abbreviation: "PA",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Rhode Island",
    slug: "rhode-island",
    abbreviation: "RI",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "South Carolina",
    slug: "south-carolina",
    abbreviation: "SC",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "South Dakota",
    slug: "south-dakota",
    abbreviation: "SD",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Tennessee",
    slug: "tennessee",
    abbreviation: "TN",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Texas",
    slug: "texas",
    abbreviation: "TX",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Utah",
    slug: "utah",
    abbreviation: "UT",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Vermont",
    slug: "vermont",
    abbreviation: "VT",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Virginia",
    slug: "virginia",
    abbreviation: "VA",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Washington",
    slug: "washington",
    abbreviation: "WA",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "West Virginia",
    slug: "west-virginia",
    abbreviation: "WV",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Wisconsin",
    slug: "wisconsin",
    abbreviation: "WI",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
  {
    name: "Wyoming",
    slug: "wyoming",
    abbreviation: "WY",
    gumroadUrl: null,
    etsyUrl: null,
    highlights: [],
  },
];

export function getStateBySlug(slug: string): State | undefined {
  return states.find((s) => s.slug === slug);
}
