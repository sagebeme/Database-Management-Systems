---
name: The Ledger
colors:
  canvas: "#E8EDE4"        # columnar ledger paper, pale green-grey
  canvas-soft: "#DCE4D8"   # a band: the next folio
  raised: "#F4F6F0"        # the sheet a lesson is printed on
  ink: "#16231C"           # green-black ledger ink
  ink-mute: "#4A5B51"      # pencil notes
  rule: "#B6C7B9"          # the printed ruling
  rule-strong: "#8FA897"   # column heads, the money column
  red: "#A12E27"           # red ink: stamps, totals, the one action
  red-press: "#86241F"
  green: "#2F5D46"         # links and the query prompt
  term: "#16231C"          # command and terminal panels (dark: #0A100D, ink #E2EADF)
dark:
  canvas: "#111916"
  canvas-soft: "#17211C"
  raised: "#1C2822"
  ink: "#E2EADF"
  ink-mute: "#A1B2A6"
  rule: "#2D3C34"
  rule-strong: "#46594E"
  red: "#E26A5F"
  red-press: "#EB8379"
  green: "#8CC2A2"
typography:
  display-xl: { family: "Source Serif 4", size: "clamp(3rem, 8vw, 6.75rem)", weight: 400, line-height: 0.95, letter-spacing: "-0.03em" }
  heading-lg: { family: "Source Serif 4", size: "clamp(2rem, 4vw, 3rem)", weight: 400, line-height: 1.05, letter-spacing: "-0.02em" }
  heading-md: { family: "Source Serif 4", size: "1.375rem", weight: 600, line-height: 1.2, letter-spacing: "-0.01em" }
  body-md: { family: "Source Serif 4", size: "1.125rem", weight: 400, line-height: 1.55 }
  body-sm: { family: "Source Serif 4", size: "0.95rem", weight: 400, line-height: 1.45 }
  figures: { family: "Source Serif 4", font-feature-settings: "'tnum' 1, 'lnum' 1" }
  code: { family: "IBM Plex Mono", size: "0.875rem", weight: 400, line-height: 1.5 }
rounded: { none: 0, stamp: 3px, button: 0 }
spacing: { unit: 8px, gutter: "clamp(16px, 4vw, 32px)", section: "clamp(96px, 14vw, 200px)" }
motion:
  duration-fast: 120ms
  duration-base: 200ms
  ease-out: "cubic-bezier(0.2, 0.8, 0.2, 1)"
  ease-in: "cubic-bezier(0.4, 0, 1, 1)"
components:
  button-primary: { fill: "{colors.red}", text: "{colors.raised}", rounded: "{rounded.button}", hover: "{colors.red-press}", focus: "3px outline {colors.green}, 2px offset" }
  link: { text: "{colors.green}", underline: "1px, 3px offset" }
  stamp: { border: "3px double {colors.red}", text: "{colors.red}", rotate: "-4deg", rounded: "{rounded.stamp}" }
  ledger-row: { border-bottom: "1px solid {colors.rule}", figures: "{typography.figures}" }
---

# The Ledger: the course site's design system

## Overview

Before databases were software, Kenyan businesses kept them in ledgers: the duka's credit book, the SACCO's members' passbook, the chama's contributions book. Ruled columns, a row per entry, totals carried forward to the next folio, and a rubber stamp when something was posted. This course turns those into tables, so the site *is* one: a green columnar ledger in which the hundred days are entries, phases are folios, and finishing a day stamps it.

**The idea, in one sentence:** on this site, the ledger book that ran every duka and SACCO becomes the course's table of contents, and the course's own data answers real SQL typed into it.

Competitor test: a generic SQL course could print a table, but not this book, these stamps, or these names.

### Key characteristics (the signature moves)

1. **The page is ruled paper.** Rows sit on ruling lines (`rule`), column heads on a heavier one (`rule-strong`), and the right-hand figures column is set off by a double vertical rule, as in a cash book. No cards, no boxes: hierarchy comes from the ruling and the band tone.
2. **Red ink has three jobs only:** the DONE stamp, the double rule under a folio's total, and the one primary action per view. Nothing else is red. Red never carries meaning alone: a stamp always says DONE and its date.
3. **The stamp.** Marking a day done lands a rotated double-bordered stamp with the date, the one animation on the site (it explains a state change). It is slightly uneven: a grain mask breaks its ink.
4. **Real SQL is the product shot.** The hero is a working query box over the course's own data (`days`, `phases`), answering in the mysql client's box-drawn tables. Monospace appears only for real code and real query output.
5. **One serif, regular weight.** Source Serif 4 at 400 everywhere; size and spacing make hierarchy. Every number uses tabular lining figures so ledger columns align.

## Colors

Complementary harmony, heavily muted: a dominant grey-green (hue ≈ 100–150°, saturation under 20%) for paper, ink and ruling, and its complement, ledger red (hue ≈ 4°), kept to under 5% of any screen. 60% paper, 30% ink and ruling, 10% red and green links together.

| Token | Light | Dark | Job | Contrast on canvas |
|---|---|---|---|---|
| canvas | #E8EDE4 | #111916 | the page | |
| canvas-soft | #DCE4D8 | #17211C | alternate bands (folios) | |
| raised | #F4F6F0 | #1C2822 | the lesson sheet, the query box | |
| ink | #16231C | #E2EADF | all running text | 13.7 / 14.5 |
| ink-mute | #4A5B51 | #A1B2A6 | secondary notes, column heads | 6.1 / 8.0 |
| rule, rule-strong | #B6C7B9, #8FA897 | #2D3C34, #46594E | ruling | 1.5 (decorative) |
| red | #A12E27 | #E26A5F | stamp, total rule, primary action | 6.0 / 5.5 |
| green | #2F5D46 | #8CC2A2 | links, the `mysql>` prompt, focus ring | 6.4 / 8.8 |

The dark theme is the same ledger under a lamp at night: ink-green paper, pale ink. It follows `prefers-color-scheme` and can be set by the toggle, which is remembered.

## Typography

| Role | Size | Use |
|---|---|---|
| display-xl | 48–108px, 400, -3% | the course title, the day number on a lesson |
| heading-lg | 32–48px, 400, -2% | folio (phase) titles, lesson title |
| heading-md | 22px, 600 | headings inside a README |
| body-md | 18px, 1.55 | everything you read |
| body-sm | 15px | ledger rows, notes |
| code | 14px Plex Mono | SQL, commands, query output only |

No eyebrows, no tracked uppercase labels (the stamp is an object, not a label), no accent words in headlines.

## Layout

- Container 1200px, outer gutter 16–32px, equal on both sides at every width.
- The home page: a hero (title and lede left, the query box right, overlapping the column edge slightly so the composition isn't mirrored), then eight folios, then how a day works, then setting up, then the footer, where the course name returns at full width.
- A folio: phase number and title in a narrow left column, the ledger rows in a wide right one; its total line ("carried forward: 9 of 14") under a red double rule.
- The lesson page: a left margin column (the day number large, the phase, the checklist of files, the stamp action, the commands) and the README on a raised sheet to its right. On phones the margin column comes first, then the sheet.

## Elevation and depth

Tone steps only (canvas → canvas-soft → raised). No resting shadows. A faint paper grain (SVG noise at about 4% opacity) on the canvas gives the paper tooth.

## Shapes

Square corners everywhere. The stamp alone has a 3px radius. Buttons are flat rectangles.

## Components

- **Primary button**: red fill, raised-colour text, square. One per view ("Start Day 1" / "Continue Day 37" on home; "Mark day done" on a lesson). Hover darkens to red-press, focus shows a 3px green outline.
- **Secondary action**: a text link in green with an underline.
- **Ledger row**: day number (tabular), project title (link), what it teaches (mute, hidden on phones), status column (stamp or empty).
- **Extras rows** (checkpoints, drills, worked examples) sit between the days they follow, indented, in italic, with no day number: in the book but outside the count.
- **Query box**: raised sheet, `mysql>` prompt in green, input in mono, results as box-drawn text in a scrollable `pre`; example queries as plain links underneath. Errors answer the way MySQL does (`ERROR 1064 ...`). Without JavaScript it simply isn't shown; the ledger below has everything.
- **States**: links underline thicker on hover; checkboxes are native and large (24px); focus-visible on everything interactive; empty query results print `Empty set`.

## Motion

Quiet by default. The home page arrives once: the title, then the lede, then the query box rise 20px into place (520ms ease-out, 80ms apart), in CSS, so nothing stays hidden if a script fails. After that, one move, explaining a change: the stamp lands (scale 1.3 → 1, opacity 0 → 1, 200ms ease-out) when a day is marked done. Query results appear without animation, and lesson pages don't move. `prefers-reduced-motion` turns all of it into instant changes.

## Responsive behaviour

| Width | Change |
|---|---|
| ≥ 1000px | hero in two columns; folio label column beside the rows; lesson margin column beside the sheet |
| 640–999px | hero stacks (title, then the query box); folio label above its rows |
| < 640px | ledger rows drop the "teaches" column; touch targets 44px; query output scrolls sideways inside its box, never the page |

## Do's and don'ts

- Do keep red for the stamp, the total rule and one action. Don't colour a heading, an icon or a background red.
- Do set every number in tabular figures. Don't mix figure styles in a column.
- Do use mono for SQL and terminal output. Don't use it for labels or decoration.
- Don't add cards, shadows, gradients, pills or icons in tinted squares. The ruling is the structure.
- Don't invent proof: every figure on the site (days, tests, databases) comes from the repository.

## Known gaps

- Progress is per browser (localStorage). There's no import from the test runner yet.
- README links to files that aren't Markdown (SQL, Python) open on GitHub, not on the site.
