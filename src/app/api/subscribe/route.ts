import { states } from "@/data/states";

// Server-only: these are read at request time and never sent to the browser.
const WEBHOOK_URL = process.env.N8N_SIGNUP_WEBHOOK_URL;
const WEBHOOK_KEY = process.env.SIGNUP_WEBHOOK_KEY;

const TIMEOUT_MS = 10_000;
const MAX = { email: 254, state: 40, sourcePage: 200, website: 200 };
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const STATE_NAMES = new Set(states.map((s) => s.name));

function fail(status: number, error: string) {
  return Response.json({ ok: false, error }, { status });
}

function str(value: unknown, max: number): string {
  return typeof value === "string" ? value.trim().slice(0, max) : "";
}

export async function POST(request: Request) {
  if (!WEBHOOK_URL || !WEBHOOK_KEY) {
    console.error("[subscribe] N8N_SIGNUP_WEBHOOK_URL or SIGNUP_WEBHOOK_KEY is not set");
    return fail(500, "Signups are temporarily unavailable. Please try again later.");
  }

  let body: Record<string, unknown>;
  try {
    const parsed = await request.json();
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) throw new Error("not an object");
    body = parsed;
  } catch {
    return fail(400, "Something went wrong sending your signup. Please try again.");
  }

  const rawEmail = typeof body.email === "string" ? body.email.trim() : "";
  if (rawEmail.length > MAX.email || !EMAIL_RE.test(rawEmail)) {
    return fail(400, "Please enter a valid email address.");
  }

  const email = rawEmail.toLowerCase();
  const stateInput = str(body.state, MAX.state);
  const state = STATE_NAMES.has(stateInput) ? stateInput : "";
  const pageInput = str(body.sourcePage, MAX.sourcePage);
  const sourcePage = pageInput.startsWith("/") ? pageInput : "";
  const website = str(body.website, MAX.website);

  try {
    const res = await fetch(WEBHOOK_URL, {
      method: "POST",
      headers: { "content-type": "application/json", "x-signup-key": WEBHOOK_KEY },
      body: JSON.stringify({ email, state, sourcePage, website }),
      signal: AbortSignal.timeout(TIMEOUT_MS),
      cache: "no-store",
    });
    if (!res.ok) {
      console.error(`[subscribe] webhook responded ${res.status}`);
      return fail(502, "We couldn't add you to the list just now. Please try again.");
    }
  } catch (err) {
    const timedOut = err instanceof DOMException && err.name === "TimeoutError";
    console.error(`[subscribe] webhook ${timedOut ? "timed out" : "request failed"}`, err);
    return fail(504, "That took too long. Please try again in a moment.");
  }

  return Response.json({ ok: true });
}
