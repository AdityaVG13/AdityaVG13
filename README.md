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

<p><b>Systems engineer building developer tools and AI-agent infrastructure in Rust and Swift.</b><br>
<sub>compilers · code search · context and memory for coding agents · local LLM tooling</sub></p>

</div>

I write systems that turn intent into something you can run, inspect, and prove. [emath](https://github.com/AdityaVG13/emath) compiles mathematics into Rust. [ZeroStack](https://github.com/AdityaVG13/zerostack) keeps agent tool output out of the model until it is needed, then returns the original bytes. Everything I ship is local-first, measured, and honest about its tradeoffs.

<table>
  <tr>
    <td align="center" width="25%"><h3>96–98%</h3><sub>fewer tokens on large source reads in <a href="https://github.com/AdityaVG13/tokenzero">TokenZero</a>, with byte-exact recovery</sub></td>
    <td align="center" width="25%"><h3>.297 → .719</h3><sub>MRR@10 on RepoQA-600 for natural-language search in <a href="https://github.com/AdityaVG13/ast-sgrep">ast-sgrep</a></sub></td>
    <td align="center" width="25%"><h3>35+</h3><sub>local LLM runtimes behind one menu-bar contract in <a href="https://github.com/AdityaVG13/Model-Switchboard">Model Switchboard</a></sub></td>
    <td align="center" width="25%"><h3>15</h3><sub>languages indexed by ast-sgrep, fully offline, no API key</sub></td>
  </tr>
</table>

<p align="center">
  <img src="https://img.shields.io/badge/Rust-2b3038?style=flat-square&logo=rust&logoColor=white" alt="Rust">
  <img src="https://img.shields.io/badge/Swift-2b3038?style=flat-square&logo=swift&logoColor=F05138" alt="Swift">
  <img src="https://img.shields.io/badge/SwiftUI-2b3038?style=flat-square&logo=swift&logoColor=white" alt="SwiftUI">
  <img src="https://img.shields.io/badge/TypeScript-2b3038?style=flat-square&logo=typescript&logoColor=3178C6" alt="TypeScript">
  <img src="https://img.shields.io/badge/Python-2b3038?style=flat-square&logo=python&logoColor=FFD43B" alt="Python">
  <img src="https://img.shields.io/badge/C++-2b3038?style=flat-square&logo=cplusplus&logoColor=00599C" alt="C++">
  <img src="https://img.shields.io/badge/Lean-2b3038?style=flat-square&logoColor=white" alt="Lean">
  <img src="https://img.shields.io/badge/SQLite-2b3038?style=flat-square&logo=sqlite&logoColor=74C0FC" alt="SQLite">
  <img src="https://img.shields.io/badge/MCP-2b3038?style=flat-square&logoColor=white" alt="MCP">
</p>

## Selected work

### [emath](https://github.com/AdityaVG13/emath)

A programming language for mathematics that computes. Write definitions the way you would on a whiteboard; get back an exact answer, a trajectory, a standalone Rust crate, or a clear reason it cannot compute yet.

- Exact by default: unbounded integers and exact rationals, so `1/10 + 2/10 == 3/10`.
- `emath compare` runs one function in exact rationals, IEEE floats, intervals, and affine forms and shows where the answers part.
- Small Rust core (parser, type checker, typed IR, reference VM, Rust code generator). The math library itself is written in emath.

`Rust` · `compiler` · `language design` · `numerics`

### [ZeroStack](https://github.com/AdityaVG13/zerostack) (hub)

Context infrastructure for coding agents. Three engines, one composition host, typed recoverable refs.

TokenZero, GraphZero, and FSZero stay independent. ZeroStack defines the shared contracts and runs them in one process (`zsx`) so agents keep evidence without stuffing every intermediate byte into the model.

| Engine | Role |
| :--- | :--- |
| [TokenZero](https://github.com/AdityaVG13/tokenzero) | Recovery-Aware Context Compression (RACC) for reads, search hits, and shell output (`tz://`). Savings are counted only after recovered bytes are subtracted. Crash-safe local store; Windows, Linux, and macOS releases. |
| [GraphZero](https://github.com/AdityaVG13/graphzero) | Code graph for orientation, callers, blast radius, and decision memory (`gz://`). Public shortly. |
| [FSZero](https://github.com/AdityaVG13/fszero) | Executable filesystem: live tree, search, controlled mutation, undo (`fz://`). Public shortly. |

`Rust` · `RACC` · `CodeMode` · `agents`

### [ast-sgrep](https://github.com/AdityaVG13/ast-sgrep) <img src="https://img.shields.io/github/stars/AdityaVG13/ast-sgrep?style=flat-square&label=%E2%98%85&labelColor=3d4450&color=552583" alt="stars">

Hybrid lexical, AST, call-graph, and semantic code search. ripgrep finds strings. ast-grep finds shapes. ast-sgrep finds intent.

- Persistent index of symbols, caller/callee edges, imports, full-text, and symbol-level vectors; one ranked list for `defs:`, `callers:`, `pattern:`, and plain English.
- Embedding engine compiled into the binary: offline, deterministic, no model download. Lifted RepoQA-600 MRR@10 from .297 to .719.
- Ships as a CLI, an MCP server, a Pi package (`pi install npm:pi-ast-sgrep`), and native Hermes agent tools. v2.7.0.

`Rust` · `code search` · `embeddings` · `MCP`

### [Model Switchboard](https://github.com/AdityaVG13/Model-Switchboard) <img src="https://img.shields.io/github/stars/AdityaVG13/Model-Switchboard?style=flat-square&label=%E2%98%85&labelColor=3d4450&color=552583" alt="stars">

Mac menu bar for local LLM runtimes. One click activates a profile and stops everything else. A profile is green only after a real `/v1/models` probe (or your custom HTTP check) succeeds.

- llama.cpp, MLX, Ollama, vLLM, SGLang, TGI, and 35+ others behind one OpenAI-compatible endpoint, with auto-restart on crash.
- Built-in benchmarks (TTFT at 1k/4k/8k context, decode tok/s) and remote Linux gateways over SSH or Tailscale.
- Native SwiftUI, signed DMG, scriptable `model-switchboardctl` CLI. Not Electron.

`Swift` · `SwiftUI` · `macOS` · `local inference`

### [Cortex](https://github.com/AdityaVG13/cortex) <img src="https://img.shields.io/github/stars/AdityaVG13/cortex?style=flat-square&label=%E2%98%85&labelColor=3d4450&color=552583" alt="stars">

Private, persistent memory for coding agents. One local Rust memory kernel shared by Claude Code, Codex, and any MCP client, so your tools stop starting from scratch. Data never leaves the machine.

`Rust` · `MCP` · `agent memory`

## Also shipping

| Project | What it is |
| :--- | :--- |
| [Continuum](https://github.com/AdityaVG13/Continuum) | Owner-gated control plane for the router you physically own. Every effect is receipted and reversible. |
| [pi-stack](https://github.com/AdityaVG13/pi-stack) | Pi packages: papercuts friction log, deferred context engine. |
| [gpr](https://github.com/AdityaVG13/gpr) | Goal-driven PRD ratchet: an agent loop that only marks work done when real artifacts pass real checks. |
| [TweetKB](https://github.com/AdityaVG13/TweetKB) | Private X bookmark knowledge base. Local SQLite, terminal-first, export to notes. |
| [TwitterArticles](https://github.com/AdityaVG13/TwitterArticles) | Chrome extension that saves X articles and long-form posts to Markdown, PDF, or DOCX. |
| [outfit-skills](https://github.com/AdityaVG13/outfit-skills) | Proof-first agent skill packs. Each racket is a full protocol, not a prompt file. |
| [grokplan](https://github.com/AdityaVG13/grokplan) | Adversarial planning. Tracker rows have to resist weak execution, not only look complete. |

<div align="center">
<br>
<sub>If any of this overlaps with what your team is building, I'd like to hear about it. Reach me on <a href="https://x.com/adityavg13">X</a>.</sub>
</div>
