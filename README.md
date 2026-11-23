# chess-fast

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/sxlty24/chess-fast/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/sxlty24/chess-fast/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A chess engine in under 4,096 bytes of Python 3.13 (standard library only) for the make.fun tiny-chess gauntlet. It plays each game through the env at MAKEFUN_ENV_URL: a 0x88 mailbox board, iterative-deepening alpha-beta with a transposition table, killer/history move ordering, null-move pruning, late-move reductions and quiescence search, tuned piece-square tables, under a fixed node budget (no clock). Local practice gauntlet: 5 wins + 1 draw, 0 losses (Elo ~1809).

## Run it

```sh
MAKEFUN_ENV_URL=http://127.0.0.1:8800 python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=s0vht5xe&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>
