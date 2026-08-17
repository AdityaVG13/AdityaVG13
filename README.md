<div align="center">

<a href="https://github.com/AdityaVG13">
  <img src="assets/profile-banner.gif" alt="AdityaG: emath compiles mathematics to verified Rust. ZeroStack hub with TokenZero, GraphZero, and FSZero." width="100%" />
</a>

<p>
  <a href="https://github.com/AdityaVG13"><img src="https://img.shields.io/badge/GitHub-AdityaVG13-2b3038?style=flat-square&logo=github&labelColor=3d4450&color=552583" alt="GitHub"></a>
  <a href="https://x.com/adityavg13"><img src="https://img.shields.io/badge/X-@adityavg13-2b3038?style=flat-square&logo=x&labelColor=3d4450&color=94a3b8" alt="X"></a>
  <a href="https://ko-fi.com/adityavg13"><img src="https://img.shields.io/badge/Ko--fi-adityavg13-2b3038?style=flat-square&logo=kofi&logoColor=white&labelColor=3d4450&color=fdb927" alt="Ko-fi"></a>
  <a href="https://beacons.ai/adityavg13"><img src="https://img.shields.io/badge/beacons-adityavg13-2b3038?style=flat-square&labelColor=3d4450&color=552583" alt="beacons"></a>
</p>

</div>

I write systems that turn intent into something you can run, inspect, and prove. [emath](https://github.com/AdityaVG13/emath) compiles mathematics into Rust. [ZeroStack](https://github.com/AdityaVG13/zerostack) keeps agent tool output out of the model until it is needed, then returns the original bytes.

## Selected work

### 1. [emath](https://github.com/AdityaVG13/emath)

Write the mathematics you mean. emath compiles it into inspectable Rust.

A `.emath` program can describe formulas, tensors, constraints, and goals. The compiler runs a deterministic pipeline (source, typed IR, resolution, generated Rust, Cargo artifact) and will not admit a result that fails `emath check` and `emath build --verify`.

`Rust` · `compiler` · `math`

### 2. [ZeroStack](https://github.com/AdityaVG13/zerostack) (hub)

Context infrastructure for coding agents. Three engines, one composition host, typed recoverable refs.

TokenZero, GraphZero, and FSZero stay independent. ZeroStack defines the shared contracts and runs them in one process (`zsx`) so agents keep evidence without stuffing every intermediate byte into the model.

| Engine | Role |
| :--- | :--- |
| [TokenZero](https://github.com/AdityaVG13/tokenzero) | Compact, deduplicate, and selectively expand tool output (`tz://`). Recovery-aware: savings are counted after the original bytes can be restored, not after they are thrown away. |
| [GraphZero](https://github.com/AdityaVG13/graphzero) | Code graph for orientation, callers, blast radius, and decision memory (`gz://`). Public shortly. |
| [FSZero](https://github.com/AdityaVG13/fszero) | Executable filesystem: live tree, search, controlled mutation, undo (`fz://`). Public shortly. |

`Rust` · `RACC` · `CodeMode`

### 3. [ast-sgrep](https://github.com/AdityaVG13/ast-sgrep)

Hybrid lexical and AST graph search. ripgrep finds strings. ast-grep finds shapes. ast-sgrep finds intent.

Local-first, 13 languages, no cloud embedding client. Ships as a standalone CLI and as a Pi package (`pi install npm:pi-ast-sgrep`).

`Rust` · `code search` · `Pi`

### 4. [Model Switchboard](https://github.com/AdityaVG13/Model-Switchboard)

Mac menu bar for local LLM runtimes. One click activates a profile and stops everything else. A profile is green only after a real `/v1/models` probe (or your custom HTTP check) succeeds.

llama.cpp, MLX, Ollama, vLLM, and the rest sit behind one OpenAI-compatible endpoint. SwiftUI, not Electron.

`Swift` · `macOS` · `local inference`

### 5. [Cortex](https://github.com/AdityaVG13/cortex)

Persistent shared memory for coding agents. Local-first Rust daemon with HTTP, MCP, and a desktop control center. One memory, every tool. Data stays on the machine.

`Rust` · `MCP` · `agent memory`

## Also shipping

| Project | What it is |
| :--- | :--- |
| [pi-stack](https://github.com/AdityaVG13/pi-stack) | Pi packages: papercuts friction log, deferred context engine. |
| [TweetKB](https://github.com/AdityaVG13/TweetKB) | Private X bookmark knowledge base. Local SQLite, terminal-first, export to notes. |
| [TwitterArticles](https://github.com/AdityaVG13/TwitterArticles) | Save X articles and long-form posts to Markdown, PDF, or DOCX on your machine. |
| [outfit-skills](https://github.com/AdityaVG13/outfit-skills) | Proof-first agent skill packs. Each racket is a full protocol, not a prompt file. |
| [grokplan](https://github.com/AdityaVG13/grokplan) | Adversarial planning. Tracker rows have to resist weak execution, not only look complete. |

<div align="center">

<a href="https://github.com/AdityaVG13"><img src="https://img.shields.io/badge/GitHub-AdityaVG13-2b3038?style=flat-square&logo=github&labelColor=3d4450&color=552583" alt="GitHub"></a>
<a href="https://x.com/adityavg13"><img src="https://img.shields.io/badge/X-@adityavg13-2b3038?style=flat-square&logo=x&labelColor=3d4450&color=94a3b8" alt="X"></a>
<a href="https://ko-fi.com/adityavg13"><img src="https://img.shields.io/badge/Ko--fi-adityavg13-2b3038?style=flat-square&logo=kofi&logoColor=white&labelColor=3d4450&color=fdb927" alt="Ko-fi"></a>

</div>
