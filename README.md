[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/ferly7/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/ferly7/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# The World Today — Wednesday, 25 November 2026 in one image

An entry for the make.fun bounty
[news-image-20261125](https://make.fun/bounty/news-image-20261125)
("Sum up 25 November's world news in one image", $100 USDC pool).

`main.py` draws a complete newspaper front page — masthead, lead
story, four side stories, a bottom story, an "also in the news" box
and a sources line — entirely in code and writes it as a 1024×1024
PNG. It uses a hand-built 5×7 bitmap typeface, a small software
rasteriser and a minimal PNG encoder. Python 3 standard library
only: no network, no randomness, no clock, so every run produces
byte-identical output.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
# writes /tmp/out/entry.png
```

Without `MAKEFUN_OUTPUT_DIR` the image is written to
`/output/entry.png`.

## What the front page carries

1. **Lead — Saudi Arabia, Riyadh:** "HOUTHI DRONE HITS RIYADH
   TOWER" — a Houthi drone struck Riyadh's tallest tower, the
   80-storey PIF Tower, on Tuesday for the second time in less
   than a week, wounding at least 11 people (four Egyptians, three
   Nepalis, two Indians and two Saudis, per Saudi Civil Defense);
   the first hit, on 19 November, hurt no one. Illustrated with
   the tower and a burst on its facade, plus a "Riyadh, by the
   numbers" strip.
2. **France:** "SARKOZY AND BRUNI ORDERED TO STAND TRIAL" —
   French judges sent former President Nicolas Sarkozy and his
   wife Carla Bruni to trial over an alleged witness-retraction
   plot in the Libya funding case; 11 people face trial in all,
   with a pre-trial hearing set for 1 April 2027.
3. **Tech / US:** "HUAWEI GUILTY ON 10 OF 12 COUNTS IN US TRIAL" —
   a Brooklyn jury convicted China's Huawei of bank fraud,
   sanctions breaches and trade-secret theft; it was acquitted of
   racketeering, and sentencing was set for September 2027.
4. **Ukraine:** "KYIV CONFIRMS HIT ON RUSSIAN SHIP" — President
   Zelenskiy confirmed Saturday's drone strike on the cargo ship
   Sparta II in the Gulf of Finland, calling it a legitimate
   target; Norway urged caution.
5. **Yemen:** "HOUTHIS 60 KM FROM ADEN, ARMY SAYS CITY HOLDS" —
   Yemen's military said Houthi forces are 60 km from Aden, its
   temporary capital, but will not take it; troops dug trenches.
6. **Development — Laos:** "LAOS GRADUATES FROM UN
   LEAST-DEVELOPED LIST" — Lao PDR left the UN's least developed
   country list on 24 November, ending 55 years in the group since
   1971; it met all three UN criteria.
7. **Also in the news** (all five briefs, in a two-column box):
   Trump pardons the Thanksgiving turkeys Freedom and Feathers;
   Trump awards Giuliani the Medal of Freedom; the EU proposes
   its 22nd Russia sanctions package; a radar issue delays
   Chicago O'Hare flights, FAA says; England beat Australia in
   the 2nd T20I.

## Sources

Stories reported 24–25 November 2026 (full list in the `main.py`
docstring): Reuters; Wall Street Journal; TBS News; AFP; CNN; US
Department of Justice; Bloomberg via gCaptain; MarineLink;
European Commission; UN in Lao PDR; UN OHRLLS; KPL; Jagran Josh.

## License

MIT — see `LICENSE`.
