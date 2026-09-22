import { renderOgImage, ogSize } from "@/lib/og";
import { states, getStateBySlug, PACK_YEAR } from "@/data/states";

export const alt = "State landlord forms pack by Talents & Titles";
export const size = ogSize;
export const contentType = "image/png";

export function generateStaticParams() {
  return states.map((s) => ({ slug: s.slug }));
}

export default async function Image({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const state = getStateBySlug(slug);
  const name = state?.name ?? "Your State";
  return renderOgImage({
    eyebrow: `${PACK_YEAR} edition`,
    title: `${name} Landlord Forms Pack`,
    subtitle: "Notices, checklists & forms · Deposit tracker · Calculator",
  });
}
