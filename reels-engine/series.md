# Parables for Builders: series bible

Everything a fresh production session needs. Read this first, then `AGENTS.md` at the repo root.

## The series
- Instagram and Facebook Reels for Donte (@talentsandtitles). Scripture stories (Bible and Book of Mormon) told in about 25-40 seconds for people building something.
- Planning, review and scheduling happen in a separate Cowork chat; Donte relays between the two. The production session's job ends at a public video link plus a caption draft.
- **Look (from No. 8, Oct 28 2026; Donte: "this is a great direction"):** cinematic and premium, not flat. Deep navy sky `#0f1f3a` with falling light beams, vignette and film grain; objects drawn as real materials (metallic brass that catches a moving glint, chainmail rings, polished stone, leather, wood, steel, glass, water) with shading and soft shadows; a slow camera push in every shot. Gold `#c9a24a` / `#e3bb5c` for labels and highlights, cream text `#f4ecd8`, muted red `#d9735a` for loss/warning strikes. Fonts: Lora (serif) and Inter. Header "Parable No. N" and @talentsandtitles in the top safe zone. Ends on the textured cream page `#f3ead7` with the turn, the highlighted punchline, the question, the reference and a boxed "Send this to..." line. Built with HyperFrames in `hf/` (see "HyperFrames engine" below); the old flat line-art engine (`base.py`, `epNN_*.py`) is retired for new episodes.
- **Banned (looks cheap):** flat thin line drawings on an empty background, glowing orbs, lens flares, neon gradients, floating particles, emoji or sparkle icons, stock people, more than two typefaces, captions in Instagram's bottom 300 px, static frames.
- **Objects and symbols only, no drawn people.** Short Inter caps labels (FUNDS, THE PLAN, NO TOOLS, "5 FULL · NO JARS LEFT") are part of the visual language.
- **Episode shape:** the hook (first spoken line, present tense, says what the story is about and why it's strange: Kallaway's rule, the same idea shown three ways in the first second: the spoken line, the big hook card text and the visual), the story in three beats, the turn (one line for a builder today, shown on the cream page), then a question and a spoken "Send this to..." line. The hook card text must say the same thing as the first spoken line.
- **Timing follows the voice.** Every drawing beat lands on the word it illustrates; the cream page wipes up as the punchline starts; caption words appear as they are spoken.

## Rules
- Never publish to `main` or schedule anything in Metricool without Donte's reply approving it in the same session. Reading Metricool is always fine. Never message anyone on his behalf.
- Do not touch the website's pages, components, config or dependencies. Only add files under `reels-engine/` and `public/reels/`.
- Send every finished video in the chat for review before it goes to `main`. Once Donte approves, pushing it to `public/reels/` on `main` is fine (commit only the reel files and `reels-engine/`; never other site files).
- Check every scripture detail against the text before it goes on screen or into a script: `python verse.py "2 Kings 4:1-7"`.
- The voiced wording is the source of truth. Donte may reword lines; keep `narration/epNN_*.txt` in step.
- Never print, request or look for the ElevenLabs API key; the environment adds it to requests to api.elevenlabs.io.
- Develop on the `claude/` working branch you are given; `main` gets only approved reels and `reels-engine/` updates.
- `src/app/globals.css` has `@source not "../../reels-engine";` so Tailwind does not scan this folder. Keep it; without it the site's CSS picks up stray class names from these files.

## Voice
- **ElevenLabs Instant Voice Clone of Donte, voice ID `RZj1s99qJKmkDAEw69aI`.** The clone is the voice for the whole series, including episodes 1-3.
- Model `eleven_multilingual_v2`, text-to-speech "with timestamps". The account is on the Starter tier: `mp3_44100_128` works, 192 kbps does not.
- **Pace:** run `tts.py` with speed `0.92` (default 1.0 reads too fast, about 200 words a minute; 0.92 gives about 165). Mark dramatic pauses in the narration with `<break time="0.8s" />`, e.g. before a one-word answer and before the punchline; `tts.py` keeps them out of the word timings. A new take changes the whole read, not just the edited line.
- Do not create or edit voices through the API.

## How to make an episode
1. Pick the next story from the backlog; check the references with `verse.py`; write the narration (about 75-95 words, hook first) to `narration/epNN_name.txt`. Donte approves the script in the Cowork chat.
2. Clone narration with word timestamps:
   `python tts.py RZj1s99qJKmkDAEw69aI narration/epNN_name.txt work/epNN.wav work/epNN.stt.json 0.92`
3. Write `hf/epNN_name.html` modelled on `hf/ep08_david_stones.html` (see "HyperFrames engine").
4. `python hf/build.py epNN_name work/epNN.wav work/epNN.stt.json out/parable-NN-name.mp4`. Check frames, send it for review.
5. After approval: put it at `public/reels/parable-NN-name.mp4` on `main` (merge the working branch, or a worktree from `origin/main`), push, and wait for the Vercel status on the commit to read "Deployment has completed". The link is `https://talentsandtitles.vercel.app/reels/parable-NN-name.mp4`. This environment cannot open vercel.app itself; check the status with `curl https://api.github.com/repos/donte7284/talentsandtitles-site/commits/<sha>/status`.

## HyperFrames engine (`hf/`)
- **Setup once per container:** `bash hf/setup.sh` (npm install of the pinned HyperFrames CLI, GSAP and the Lora/Inter fonts; finds a headless Chrome: the environment's Playwright Chromium, else the one inside the `@sparticuz/chromium` npm package; writes its path to `hf/.chrome`). Needs ffmpeg.
- **Shared look:** `hf/template.html` (layers, shared materials: brass, stone, leather, wood, steel, clay, glass, water, barley, rock), `hf/kit.css`, `hf/kit.js` (atmosphere, hook card, word-by-word captions, cream ending, camera, `K.at`, `K.show`, `K.hide`, `K.draw`). Change these only to change every episode.
- **An episode** is one file `hf/epNN_slug.html` with four parts after marker comments: `@config` (JSON: `no`, `hook_html`, `turn_at`, `turn_html`, `turn_size`, `turn_hl`, `question_at`, `question`, `ref`, `send`, optional `theme` colour overrides), `@css`, `@html` (the objects, start hidden with `opacity:0` in `@css`), `@js` (`K.run(function(tl, K){ ... })`).
- **Cue every beat to the voice** with `K.at("spoken words")` (first word's start; `{from: t}` for a later occurrence, `K.end(...)` for a word's end). Never hard-code seconds for story beats. `K.show(tl, sel, t, {y:40})` / `K.hide(...)` move objects relative to where they sit.
- **Determinism:** no `Math.random`, no `Date`, no network; GSAP staggers must not use `from:"random"`. Lay out generated objects with fixed formulas.
- **Captions** come from the word timings automatically: one phrase at a time at y 1330, the spoken word in gold, gone when the cream page starts (`turn_at`). Labels sit at y 470; objects live between y 560 and 1300.
- **Before rendering, look:** `python hf/build.py epNN_slug work/epNN.wav work/epNN.stt.json x.mp4 --snap 1,4,8,12,...` writes a contact sheet. For layout work before a voice exists, `python hf/fake_stt.py narration/epNN_slug.txt work/epNN_fake.wav work/epNN_fake.stt.json` gives silent audio and estimated timings (never ship a fake-timed render).
- **Render:** `python hf/build.py epNN_slug work/epNN.wav work/epNN.stt.json out/parable-NN-slug.mp4` (lints first and stops on errors; cleans the voice to -14 LUFS like `episode.py`).

## Weekly run
Follow this exactly when Donte asks for the weekly run. It needs no other context.

**a. Find this run's slots.** Read this file. In Metricool (brand 6944613, timezone America/Los_Angeles) call getScheduledPosts from today to 60 days ahead and find the last scheduled parable post (text contains `#ParablesForBuilders` or a "(Book C:V)" reference). The next four open Mon/Wed/Fri/Sun 10:00 AM Pacific slots after it are this run's slots. If no parable post is scheduled, start from the first slot after now. Skip any slot that already holds a post.

**b. Write four narrations.** Narrations open with the hook (see Episode shape). Take the next four stories from the backlog in order, keeping about one in four from the Book of Mormon (if the next four have none, swap the fourth for the next Book of Mormon story). Number them on from the episode log. Write each narration in the series format (the hook in present tense, three beats, the turn, a question, "Send this to someone who...") at about 75-95 words, into `narration/epNN_slug.txt`. Check every detail with `python verse.py "<reference>"`. Nothing goes in that the text doesn't support: no invented numbers, names, dialogue or order of events. Quote KJV wording where you quote.

**c. Voice, build, render.** Run `bash hf/setup.sh` once. For each: `python tts.py RZj1s99qJKmkDAEw69aI narration/epNN_slug.txt work/epNN.wav work/epNN.stt.json 0.92`. Write `hf/epNN_slug.html` in the series look (real materials, depth and light, short caps labels, objects and symbols only, no people), with the hook card matching the first spoken line and every beat cued with `K.at(...)`. Render with `python hf/build.py epNN_slug work/epNN.wav work/epNN.stt.json out/parable-NN-slug.mp4`.

**d. Check frames.** Pull about twelve frames from each video (`ffmpeg ... select=...,tile=6x2`, or `build.py --snap`) and look at them: the hook card is up in the first second and says what the voice says; fonts are Lora and Inter (not a fallback); every beat shows the thing being said; no empty or static stretch longer than about 2 s; captions fit inside the frame above the bottom 300 px and never overlap a label or object; the reference is right; the cream page covers the navy completely at the end. Fix and re-render anything wrong.

**e. Save the work.** Copy the four videos to `public/reels/parable-NN-slug.mp4`, then commit them with the narrations and episode scripts to the `claude/` working branch and push it. Not `main`. This keeps everything if the session resets.

**f. Ask, then stop.** In the session, post: the four videos (send the files), each narration, each Instagram caption and Facebook caption, and the proposed slot for each. Ask Donte to approve. Stop and wait.

**g. Only after Donte replies in that session approving it:**
1. Merge the working branch into `main` (only `public/reels/` and `reels-engine/` change) and push. Wait until the Vercel status on the merge commit reads "Deployment has completed" (`curl https://api.github.com/repos/donte7284/talentsandtitles-site/commits/<sha>/status`).
2. For each episode create two Metricool posts with createScheduledPost, `blogId` 6944613, at its slot (`publicationDate` {dateTime "YYYY-MM-DDT10:00:00", timezone "America/Los_Angeles"}), `autoPublish` true, `media` [the public link `https://talentsandtitles.vercel.app/reels/parable-NN-slug.mp4`]:
   - Instagram: providers [{network: instagram}], `instagramData` {type: "REEL", showReelOnFeed: true, isAiGenerated: true}, text = caption + blank line + the 5 hashtags.
   - Facebook: providers [{network: facebook}], `facebookData` {type: "REEL"}, text = the same caption with no hashtags.
3. Read them back with getScheduledPosts and check date, time, network, type, AI flag, text and media for each.
4. Move the four stories from the backlog to the episode log (with file names and slots), commit and push.
5. Report: links, slots, anything that went wrong.

Only an approval of the posted batch counts; a change request means revise, re-post, and ask again.

**h. Never publish or schedule without Donte's reply in that session.** If he doesn't reply, do nothing further.

## Episode log
| No. | Title | Reference on screen | Public file | Length | Metricool (IG + FB) |
|---|---|---|---|---|---|
| 1 | The widow's oil | 2 KINGS 4 : 1–7 | `public/reels/parable-01-widows-oil.mp4` | 35.8 s | Mon 12 Oct 2026, 10:00 PT |
| 2 | The unfinished tower | LUKE 14 : 28–30 | `public/reels/parable-02-tower.mp4` | 25.2 s | Wed 14 Oct 2026, 10:00 PT |
| 3 | Nephi's ship | 1 NEPHI 17 : 8–18 | `public/reels/parable-03-nephis-ship.mp4` | 28.4 s | Fri 16 Oct 2026, 10:00 PT |
| 4 | Joseph's grain | GENESIS 41 : 47–57 | `public/reels/parable-04-joseph-grain.mp4` | 29.8 s | Wed 21 Oct 2026, 10:00 PT |
| 5 | The wise and foolish builders | MATTHEW 7 : 24–27 | `public/reels/parable-05-wise-builders.mp4` | 28.8 s | Fri 23 Oct 2026, 10:00 PT |
| 6 | Gideon's 300 | JUDGES 7 : 2–8 | `public/reels/parable-06-gideon-300.mp4` | 27.9 s | Sun 25 Oct 2026, 10:00 PT |
| 7 | Nephi's broken bow | 1 NEPHI 16 : 18–32 | `public/reels/parable-07-nephi-bow.mp4` | 34.7 s | Mon 26 Oct 2026, 10:00 PT |

Notes:
- No. 1 originally said Elisha "asks just one question"; 2 Kings 4:2 has him ask "What shall I do for thee? tell me, what hast thou in the house?" Changed to "The prophet asks her: what do you have in your house?" before it posted: re-voiced at speed 0.92 with pauses before "Nothing" and the punchline, `public/reels/parable-01-widows-oil.mp4` replaced, and both Oct 12 Metricool posts updated to the new video (media link `...parable-01-widows-oil.mp4?v=2`).
- No. 3 follows the text's order: ore question (17:9), tools made (17:16), "Our brother is a fool" (17:17).
- No. 4-7 come from the weekly run on branch `claude/busy-bardeen-rabemw` (Oct 17). An earlier run of the same four stories on `claude/busy-bardeen-aioc2z` (Oct 10) was not used. The Oct 18 slot had passed, so they went out Wed/Fri/Sun/Mon Oct 21-26.

## Story backlog
Roughly one Book of Mormon story in every four. References checked against `scripture/`.

| Story | Reference | The builder's turn (draft angle) |
|---|---|---|
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
