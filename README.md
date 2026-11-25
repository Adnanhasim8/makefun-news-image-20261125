[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Adnanhasim8/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Adnanhasim8/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# Wednesday 25 November 2026 in one picture

A front page summing up the world news of Wednesday 25 November 2026: 18 dated
stories across 7 regions — Ukraine's confirmed strike on a Russian ship in the
Gulf of Finland, the Gaza strike, the Houthi attack on Riyadh, China's
Shenzhou-24 carrying the first Pakistani into orbit, the AI stock slide and
planned new tariffs, and more. See `NEWS.md` for the stories and their sources.

## How to run

```sh
python3 main.py
```

This writes a 1024×1024 PNG (at most 1 MiB, byte-identical on every run) to
`/output/entry.png` (`MAKEFUN_OUTPUT_DIR` overrides the output directory).
Python 3.13 standard library only — no network, no dependencies. The program
draws the whole front page itself, including its own PNG encoder and bitmap
font, and asserts the output is a valid 1024×1024 PNG under 1 MiB.
