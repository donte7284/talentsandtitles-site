import type { MetadataRoute } from "next";
import { states } from "@/data/states";
import { site } from "@/lib/site";

export default function sitemap(): MetadataRoute.Sitemap {
  const lastModified = new Date();
  return [
    { url: site.url, lastModified, changeFrequency: "weekly", priority: 1 },
    ...states.map((s) => ({
      url: `${site.url}/landlord-forms/${s.slug}`,
      lastModified,
      changeFrequency: "monthly" as const,
      priority: 0.8,
    })),
    { url: `${site.url}/disclaimer`, lastModified, changeFrequency: "yearly", priority: 0.2 },
  ];
}
