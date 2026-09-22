import { renderOgImage, ogSize } from "@/lib/og";

export const alt = "Talents & Titles — State-specific landlord forms, updated for current law";
export const size = ogSize;
export const contentType = "image/png";

export default function Image() {
  return renderOgImage({
    eyebrow: "All 50 states",
    title: "State-specific landlord forms, updated for current law",
    subtitle: "Notices, checklists & forms · Deposit tracker · Calculator",
  });
}
