[![Bounty](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![Leaderboard](https://make.fun/badge/news-image-20261125/ferly7/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard)
[![Reward](https://make.fun/badge/news-image-20261125/ferly7/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

# The World Today — Wednesday, 25 November 2026

A small, dependency-free Python 3 program that draws a complete newspaper
front page as a single 1024x1024 PNG. It ships its own tiny 5x7 bitmap
typeface, its own text wrapping and layout code, and its own PNG encoder
(built on `zlib` and `struct` from the standard library only) — no network
access, no third-party packages, and fully deterministic: every run produces
byte-identical output.

Run it with:

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

This writes `entry.png` into the chosen output directory (default `/output`).

## What is on the page

- **Lead — Riyadh:** a Houthi drone hits the 80-storey PIF Tower in the King
  Abdullah Financial District for the second time in under a week, wounding
  at least 11 people, with a simple tower illustration and a stat strip.
- **France:** Sarkozy and Bruni ordered to stand trial.
- **Tech:** Huawei guilty on 10 of 12 counts in its US trial.
- **Ukraine:** Kyiv confirms its hit on the Russian ship Sparta II.
- **Yemen:** Houthis 60 km from Aden; the army says the city holds.
- **Development — Laos:** Lao PDR graduates from the UN least-developed list.
- **Also in the news:** five one-line briefs, from the White House turkey
  pardon to England's T20I win over Australia.

## News sources

Reuters, the Wall Street Journal, AFP, the US Department of Justice, the
European Commission and the United Nations — reporting of Wednesday
25 November 2026, as credited on the page itself.
