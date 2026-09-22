import { ImageResponse } from "next/og";
import { readFile } from "node:fs/promises";
import { join } from "node:path";

// Heading serif, bundled so share previews and icons match the site typography.
export async function brandFonts() {
  const data = await readFile(join(process.cwd(), "src/assets/SourceSerif4-SemiBold.ttf"));
  return [{ name: "Source Serif", data, weight: 600 as const, style: "normal" as const }];
}

export const ogSize = { width: 1200, height: 630 };

const NAVY = "#13213c";
const CREAM = "#f7f1e5";
const GOLD = "#d4a954";

export async function renderOgImage({ eyebrow, title, subtitle }: { eyebrow: string; title: string; subtitle: string }) {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          background: NAVY,
          color: CREAM,
          padding: "64px 72px",
          fontFamily: "Source Serif",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              width: 96,
              height: 80,
              borderRadius: 12,
              border: `3px solid ${GOLD}`,
              fontSize: 40,
              fontWeight: 600,
            }}
          >
            T<span style={{ color: GOLD }}>&amp;</span>T
          </div>
          <div style={{ fontSize: 36, fontWeight: 600 }}>Talents &amp; Titles</div>
        </div>

        <div style={{ display: "flex", flexDirection: "column" }}>
          <div style={{ fontSize: 26, letterSpacing: 4, color: GOLD, textTransform: "uppercase", fontFamily: "sans-serif" }}>
            {eyebrow}
          </div>
          <div style={{ fontSize: 76, fontWeight: 600, lineHeight: 1.05, marginTop: 16, maxWidth: 1000 }}>{title}</div>
          <div style={{ fontSize: 30, marginTop: 24, color: "#dccdb0", fontFamily: "sans-serif", maxWidth: 1000 }}>
            {subtitle}
          </div>
        </div>

        <div style={{ display: "flex", height: 8, width: 160, background: GOLD, borderRadius: 4 }} />
      </div>
    ),
    { ...ogSize, fonts: await brandFonts() },
  );
}
