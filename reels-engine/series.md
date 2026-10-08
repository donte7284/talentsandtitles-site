# Parables for Builders: series bible

Everything a fresh production session needs. Read this first, then `AGENTS.md` at the repo root.

## The series
- Instagram and Facebook Reels for Donte (@talentsandtitles). Scripture stories (Bible and Book of Mormon) told in about 25-40 seconds for people building something.
- Planning, review and scheduling happen in a separate Cowork chat; Donte relays between the two. The production session's job ends at a public video link plus a caption draft.
- **Look:** gold line drawings on navy `#0f1f3a` that act out the story with fluid motion, full frame 1080x1920. Then a cream page `#f3ead7` wipes up with the highlighted punchline and the scripture reference. Gold `#c9a24a`, bright gold `#e3bb5c`, cream text `#f4ecd8`, muted red `#d9735a` for loss/warning. Fonts: Lora (serif) and Inter. Header "Parable No. N", watermark @talentsandtitles.
- **Objects and symbols only, no drawn people.** Short Inter caps labels (FUNDS, THE PLAN, NO TOOLS, "5 FULL · NO JARS LEFT") are part of the visual language.
- **Episode shape:** cold open (0-3 s, present tense), the story in three beats, the turn (one line for a builder today, shown on the cream page), then a question and a spoken "Send this to..." line.
- **Timing follows the voice.** Every drawing beat lands on the word it illustrates; the cream page wipes up as the punchline starts; caption words appear as they are spoken.

## Rules
- Do not post, schedule or message anything on Donte's behalf. Reading Metricool is fine; scheduling is done from the Cowork chat.
- Do not touch the website's pages, components, config or dependencies. Only add files under `reels-engine/` and `public/reels/`.
- Send every finished video in the chat for review before it is pushed. Once Donte approves an episode, pushing it to `public/reels/` on `main` is approved (commit only the video files; nothing else on the site).
- Check every scripture detail against the text before it goes on screen or into a script: `python verse.py "2 Kings 4:1-7"`.
- The voiced wording is the source of truth. Donte may reword lines; keep `narration/epNN_*.txt` in step.
- Never print, request or look for the ElevenLabs API key; the environment adds it to requests to api.elevenlabs.io.
- Develop on the working branch you are given; `main` gets only approved reels (and `reels-engine/` once Donte approves that merge).

## Voice
- **ElevenLabs Instant Voice Clone of Donte, voice ID `RZj1s99qJKmkDAEw69aI`.** The clone is the voice for the whole series, including episodes 1-3.
- Model `eleven_multilingual_v2`, text-to-speech "with timestamps". The account is on the Starter tier: `mp3_44100_128` works, 192 kbps does not.
- Do not create or edit voices through the API.

## How to make an episode
1. Pick the next story from the backlog; check the references with `verse.py`; write the narration (about 75-95 words) to `narration/epNN_name.txt`. Donte approves the script in the Cowork chat.
2. Clone narration with word timestamps:
   `python tts.py RZj1s99qJKmkDAEw69aI narration/epNN_name.txt work/epNN.wav work/epNN.stt.json`
3. Write `epNN_name.py` modelled on `ep02_tower.py`: a scene (SVG drawing code for `base.py`), cue times read with `v.at("spoken phrase")`, the caption words, and the cream-page lines and reference. `episode.py` does the rest (silence fix, audio clean-up to -14 LUFS, render, mux).
4. `python epNN_name.py work/epNN.wav work/epNN.stt.json out/parable-NN-name.mp4` (about 2.5 s of render time per second of video). Check frames, send it for review.
5. After approval: copy it to `public/reels/parable-NN-name.mp4` on `main` (a worktree from `origin/main`, commit only that file), push, and wait for the Vercel status on the commit to read "Deployment has completed". The link is `https://talentsandtitles.vercel.app/reels/parable-NN-name.mp4`. This environment cannot open vercel.app itself; check the status with `curl https://api.github.com/repos/donte7284/talentsandtitles-site/commits/<sha>/status`.

Files: `base.py` (page template), `render.py` (Playwright frames to H.264), `episode.py` (shared voice/cue/render steps), `tts.py` (clone narration), `verse.py` + `scripture/` (source texts), `scenes.py` (the original silent tests), `ep01_widow.py`, `ep02_tower.py`, `ep03_nephi.py`. Generated HTML, frames, `out/` and `work/` are gitignored. The environment's setup script installs Python Playwright and the Lora font.

## Episode log
| No. | Title | Reference on screen | Public file | Length | Metricool (IG + FB) |
|---|---|---|---|---|---|
| 1 | The widow's oil | 2 KINGS 4 : 1–7 | `public/reels/parable-01-widows-oil.mp4` | 34.5 s | Mon 12 Oct 2026, 10:00 PT |
| 2 | The unfinished tower | LUKE 14 : 28–30 | `public/reels/parable-02-tower.mp4` | 25.2 s | Wed 14 Oct 2026, 10:00 PT |
| 3 | Nephi's ship | 1 NEPHI 17 : 8–18 | `public/reels/parable-03-nephis-ship.mp4` | 28.4 s | Fri 16 Oct 2026, 10:00 PT |

Notes:
- No. 1 says Elisha "asks just one question"; 2 Kings 4:2 has him ask "What shall I do for thee? tell me, what hast thou in the house?" Fine as a summary, but avoid the "just one" framing in future scripts.
- No. 3 follows the text's order: ore question (17:9), tools made (17:16), "Our brother is a fool" (17:17).

## Story backlog
Roughly one Book of Mormon story in every four. References checked against `scripture/`.

| Story | Reference | The builder's turn (draft angle) |
|---|---|---|
| Joseph's grain | Genesis 41:47-57 | Store up in the good years; the famine finds out who planned. |
| Wise and foolish builders | Matthew 7:24-27 | Same storm, same house; the difference was the foundation nobody sees. |
| Gideon's 300 | Judges 7:2-8 | 32,000 cut to 300; the smaller team won. |
| **Nephi's broken bow** (BoM) | 1 Nephi 16:18-32 | The tool broke; he made a new one from what he had and asked where to go. |
| David's five stones | 1 Samuel 17:38-50 | He left Saul's armour and used the tools he'd practised with. |
| Ruth gleaning | Ruth 2:1-17 | She showed up to the edge of someone else's field and worked it. |
| Manna | Exodus 16:14-21 | Enough for today; hoarding it went bad overnight. |
| **The brother of Jared's stones** (BoM) | Ether 3:1-6 | He did the work he could (sixteen stones) and asked for the rest. |
| The ant | Proverbs 6:6-8 | No overseer, no boss; she works in summer for the winter. |
| Noah | Genesis 6:13-22 | He built for rain nobody had seen. |
| The unjust steward | Luke 16:1-9 | Even the dishonest manager planned ahead; "wiser in their generation". |
| **Captain Moroni's fortifications** (BoM) | Alma 48:7-10; 49:1-9 | Prepared before the attack; the enemy was astonished. |
| The mustard seed | Matthew 13:31-32 | The least of all seeds becomes the tree. |
| The ten virgins | Matthew 25:1-13 | Five brought extra oil; preparation can't be borrowed at midnight. |
| **Small and simple things** (BoM) | Alma 37:6-7 | Great things come by small means. |

Add new ideas at the bottom; mark a story done by moving it to the episode log.

## Captions
- 1-3 lines, include the scripture reference, e.g. `(Luke 14:28–30)`. End on the episode's question.
- Instagram: at most 5 hashtags. In use: `#ParablesForBuilders #Bible` (or `#BookOfMormon`) `#faith #faithandwork #christianentrepreneur`.
- Facebook: the same text with no hashtags.
- No "link in bio".

## Metricool
- Brand **6944613** ("talentsandtitles"), timezone America/Los_Angeles, Instagram `talentsandtitles` and the Facebook page.
- Posting slots: **Monday, Wednesday, Friday, Sunday at 10:00 AM Pacific.** Each episode is two posts: an Instagram Reel (shown on feed, marked AI-generated) and a Facebook Reel.
- Metricool keeps its own copy of the video, so old files in `public/reels/` can be deleted later.
