import { ImageResponse } from "next/og";
import { brandFonts } from "@/lib/og";

export const size = { width: 180, height: 180 };
export const contentType = "image/png";

export default async function AppleIcon() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          background: "#13213c",
          color: "#f7f1e5",
          fontSize: 72,
          fontWeight: 600,
          fontFamily: "Source Serif",
        }}
      >
        T<span style={{ color: "#d4a954" }}>&amp;</span>T
      </div>
    ),
    { ...size, fonts: await brandFonts() },
  );
}
