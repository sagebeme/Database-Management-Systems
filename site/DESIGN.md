---
name: The Ledger
colors:
  canvas: "#EEF4F7"        # ledger paper with a sky tint
  canvas-soft: "#DDEAF1"   # a band: the next folio
  raised: "#FBFDFE"        # the sheet a lesson is printed on, the query box
  ink: "#0F2230"           # navy ledger ink
  ink-mute: "#45596A"      # pencil notes
  rule: "#B5CCD9"          # the printed ruling
  rule-strong: "#7FA3B8"   # column heads, the money column
  field: "#5BC0EB"         # SKY: the colour field (masthead and hero band)
  sky: "#1A87BD"           # SKY as large type: folio numerals, the day number
  link: "#0A6699"          # SKY, deep enough for text: links, the mysql> prompt, focus
  hot: "#B81B66"           # HOT PINK: stamps, the total rule, the one action
  hot-press: "#97134F"
  lime: "#B5E33B"          # LIME: the highlighter, the slab behind the query box, terminal success
  on-lime: "#0F2230"       # text on lime, both themes
  term: "#0E1F2B"          # terminal panels and the footer band (ink #E6EFF4)
  term-hot: "#FF5FA8"      # FAILED in a terminal
dark:
  canvas: "#0D1A23"
  canvas-soft: "#12232F"
  raised: "#182C3A"
  ink: "#E6EFF4"
  ink-mute: "#9EB4C3"
  rule: "#26394A"
  rule-strong: "#3D5568"
  field: "#123F58"
  sky: "#4CC3F5"
  link: "#74CEF7"
  hot: "#FF5FA8"
  hot-press: "#FF85BD"
  lime: "#C6EE52"
  term: "#07121A"
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
  button-primary: { fill: "{colors.hot}", text: "{colors.raised}", rounded: "{rounded.button}", hover: "{colors.hot-press}", focus: "3px outline {colors.link}, 2px offset" }
  link: { text: "{colors.link}", underline: "1px, 3px offset" }
  stamp: { border: "3px double {colors.hot}", text: "{colors.hot}", rotate: "-4deg", rounded: "{rounded.stamp}" }
  ledger-row: { border-bottom: "1px solid {colors.rule}", figures: "{typography.figures}" }
---

# The Ledger: the course site's design system

## Overview

Before databases were software, Kenyan businesses kept them in ledgers: the duka's credit book, the SACCO's members' passbook, the chama's contributions book. Ruled columns, a row per entry, totals carried forward to the next folio, and a rubber stamp when something was posted. This course turns those into tables, so the site *is* one: a columnar ledger, printed in the loud colours of the 80s and 90s, in which the hundred days are entries, phases are folios, and finishing a day stamps it.

**The idea, in one sentence:** on this site, the ledger book that ran every duka and SACCO becomes the course's table of contents, and the course's own data answers real SQL typed into it.

Competitor test: a generic SQL course could print a table, but not this book, these stamps, or these names.

### Key characteristics (the signature moves)

1. **The page is ruled paper.** Rows sit on ruling lines (`rule`), column heads on a heavier one (`rule-strong`), and the right-hand figures column is set off by a double vertical rule, as in a cash book. No cards, no boxes: hierarchy comes from the ruling and the band tone.
2. **Colour like the 80s and 90s, not the 2020s.** A triad: sky blue, hot pink, lime, all at full voice, the colours of a 1990 matatu, a Kasuku exercise book cover, a shell suit. Sky is the field: the masthead and the hero are a flat block of it. Hot pink has three jobs only: the DONE stamp, the double rule under a folio's total, and the one primary action. Lime is the highlighter: the slab behind the query box, the marker on a posted day and on a total, success in a terminal. Colour never carries meaning alone: a stamp always says DONE and its date.
3. **The stamp.** Marking a day done lands a rotated double-bordered stamp with the date, the one animation on the site (it explains a state change). It is slightly uneven: a grain mask breaks its ink.
4. **Real SQL is the product shot.** The hero is a working query box over the course's own data (`days`, `phases`), answering in the mysql client's box-drawn tables. Monospace appears only for real code and real query output.
5. **One serif, regular weight.** Source Serif 4 at 400 everywhere; size and spacing make hierarchy. Every number uses tabular lining figures so ledger columns align.

## Colors

A triadic harmony, sky blue (hue 199°), hot pink (332°) and lime (76°), kept loud on purpose: the brief is the saturated colour of the 80s and 90s, not today's greige. Loud colours stay legible because the rest is quiet: everything else is a sky-tinted neutral (paper, ink, ruling), so about 60% neutral paper, 30% sky (the field, numerals, links), 10% hot pink and lime together.

| Token | Light | Dark | Job | Contrast |
|---|---|---|---|---|
| canvas | #EEF4F7 | #0D1A23 | the page | |
| canvas-soft | #DDEAF1 | #12232F | alternate folio bands | |
| raised | #FBFDFE | #182C3A | the lesson sheet, the query box | |
| ink | #0F2230 | #E6EFF4 | running text | 14.7 / 15.2 on canvas; 7.9 / 9.6 on field |
| ink-mute | #45596A | #9EB4C3 | notes, column heads (never on the field) | 6.6 / 8.2 |
| field | #5BC0EB | #123F58 | masthead and hero colour block | |
| sky | #1A87BD | #4CC3F5 | large numerals only | 3.6 / 8.8 (large text) |
| link | #0A6699 | #74CEF7 | links, prompt, focus ring | 5.6 / 10.0 |
| hot | #B81B66 | #FF5FA8 | stamp, total rule, primary action | 5.6 / 6.3; button text 6.1 / 6.3 |
| lime | #B5E33B | #C6EE52 | highlighter and slab; text on it is always on-lime #0F2230 | 10.9 |
| term | #0E1F2B | #07121A | terminals, footer band; lime and term-hot inside | 11.2 / 6.7 |

The dark theme is the same book under a lamp: navy paper, the field drops to a deep sky so it doesn't glare, and the accents brighten.

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
- A folio: phase number and title in a narrow left column, the ledger rows in a wide right one; its total line ("carried forward: 9 of 14") under a hot-pink double rule; a posted day gets a lime highlighter on its number.
- The lesson page: a left margin column (the day number large, the phase, the checklist of files, the stamp action, the commands) and the README on a raised sheet to its right. On phones the margin column comes first, then the sheet.

## Elevation and depth

Tone steps only (canvas → canvas-soft → raised). No soft shadows. The query box alone has a hard, flat lime slab offset behind it (10px, no blur): a printed colour block, not a shadow. A faint paper grain (SVG noise at about 4% opacity) on the canvas gives the paper tooth.

## Shapes

Square corners everywhere. The stamp alone has a 3px radius. Buttons are flat rectangles.

## Components

- **Primary button**: hot-pink fill, raised-colour text, square. One per view ("Start Day 1" / "Continue Day 37" on home; "Mark day done" on a lesson). Hover darkens to hot-press, focus shows a 3px link-blue outline.
- **Secondary action**: a text link in link blue with an underline.
- **Ledger row**: day number (tabular), project title (link), what it teaches (mute, hidden on phones), status column (stamp or empty).
- **Extras rows** (checkpoints, drills, worked examples) sit between the days they follow, indented, in italic, with no day number: in the book but outside the count.
- **Query box**: raised sheet on the sky field with the lime slab behind it, `mysql>` prompt in link blue, input in mono, results as box-drawn text in a scrollable `pre`; example queries as plain links underneath. Errors answer the way MySQL does (`ERROR 1064 ...`). Without JavaScript it simply isn't shown; the ledger below has everything.
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

- Do keep hot pink for the stamp, the total rule and one action, and lime for highlighting. Don't colour a heading or a paragraph pink or lime.
- Do let the sky field be a flat block of colour. Don't fade it into a gradient.
- Do set every number in tabular figures. Don't mix figure styles in a column.
- Do use mono for SQL and terminal output. Don't use it for labels or decoration.
- Don't add cards, shadows, gradients, pills or icons in tinted squares. The ruling is the structure.
- Don't invent proof: every figure on the site (days, tests, databases) comes from the repository.

## Known gaps

- Progress is per browser (localStorage). There's no import from the test runner yet.
- README links to files that aren't Markdown (SQL, Python) open on GitHub, not on the site.
