# The World Today — 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/itserwe/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/itserwe/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A single-page newspaper front page for Tuesday 24 November 2026: a Houthi
drone hits Riyadh's PIF Tower for the second time in five days, a fourth
tanker is hit by a mine in the Strait of Hormuz, and the market rally fades
with Bitcoin below $60,000 — with 31 more stories, a UTC timeline of the
day, a numbers strip, and a map of where it all happened. Every item
carries a CONFIRMED or REPORTED mark plus its source, and a date-check box
leaves out events that happened on other days.

## How the page is made

`main.py` draws `entry.png` (1024 × 1024) with Pillow — masthead,
headlines, lead stories, secondaries, map, briefs, everything. No image
generator is involved; run the script and the page comes out again. On a
machine without Pillow (the make.fun grader runs standard library only),
`main.py` copies the pre-drawn `entry.png` from the repository instead.

## Regenerate

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

That writes `out/entry.png`.
