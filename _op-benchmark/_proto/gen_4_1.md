### 4.1 (GENERATED from bench_4_1.jsonl) — Add / Subtract

**P-gen — d128 (ns/op).**

| port | add SQ | add NQ | add MQ | add OQ | add FQ | sub SQ | sub NQ | sub MQ | sub OQ | sub FQ |
|------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| c     | 2.21 | 3.88 | 9.93 | 11.74 | 6.53 | 1.66 | 4.03 | 10.87 | 12.08 | 6.84 |
| rust  | 3.08 | 4.57 | 13.50 | 10.59 | 7.56 | 1.87 | 4.68 | 13.96 | 10.68 | 6.83 |
| zig   | 3.00 | 5.97 | 11.78 | 12.96 | 7.83 | 1.79 | 5.71 | 12.34 | 12.60 | 7.68 |
| swift | 4.70 | 5.95 | 15.41 | 17.89 | 13.41 | 2.95 | 5.41 | 15.09 | 18.67 | 13.56 |
| csharp| 2.18 | 7.02 | 17.56 | 18.96 | 11.93 | 1.47 | 9.79 | 11.95 | 20.14 | 9.19 |
| go    | 4.49 | 9.77 | 21.64 | 33.38 | 20.12 | 2.98 | 9.75 | 21.04 | 33.18 | 19.49 |
| java‡ | 5.45 | 6.78 | 12.00 | 19.97 | 14.30 | 4.49 | 7.34 | 12.40 | 20.12 | 14.66 |
| kotlin‡| 6.08 | 7.06 | 13.37 | 23.60 | 15.57 | 4.65 | 7.32 | 13.67 | 24.24 | 14.94 |

**P-max — d128 (ns/op):**

| port | add SQ | add OQ | add FQ | sub SQ | sub OQ | sub FQ |
|------|-------:|-------:|-------:|-------:|-------:|-------:|
| c     | 3.53 | 18.19 | 7.28 | 3.24 | 17.92 | 7.07 |
| rust  | 5.11 | 12.79 | 6.44 | 3.87 | 12.82 | 6.64 |
| zig   | 4.01 | 16.47 | 8.55 | 3.73 | 15.78 | 7.19 |
| swift | 6.46 | 22.50 | 13.35 | 4.63 | 22.36 | 11.97 |
| csharp| 6.02 | 23.17 | 9.13 | 3.68 | 24.72 | 6.83 |
| go    | 7.15 | 42.48 | 18.89 | 5.97 | 42.99 | 18.72 |
| java‡ | 6.74 | 19.88 | 16.29 | 6.41 | 20.02 | 15.86 |
| kotlin‡| 7.27 | 21.00 | 11.21 | 7.02 | 21.27 | 11.56 |

**Relational — d128 vs peers** (ratio = peer/ours, computed; missing peer ⇒ `-`):

| port | op | cat | profile | arch | mode | ours | alt | alt ns | ratio | run | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c | add | SQ | P-gen | arm64 | thru | 2.21 | libbid | 8.43 | **3.81×** | Rprof |  |
| c | add | NQ | P-gen | arm64 | thru | 3.88 | libbid | 8.38 | **2.16×** | Rprof |  |
| c | add | MQ | P-gen | arm64 | thru | 9.93 | libbid | 8.58 | **0.86×** | Rprof |  |
| c | add | OQ | P-gen | arm64 | thru | 11.74 | libbid | 13.75 | **1.17×** | Rc |  |
| c | add | FQ | P-gen | arm64 | thru | 6.53 | libbid | 10.36 | **1.59×** | Rc |  |
| c | sub | SQ | P-gen | arm64 | thru | 1.66 | libbid | 9.89 | **5.96×** | Rprof |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.03 | libbid | 11.66 | **2.89×** | Rprof |  |
| c | sub | MQ | P-gen | arm64 | thru | 10.87 | libbid | 10.39 | **0.96×** | Rprof |  |
| c | sub | OQ | P-gen | arm64 | thru | 12.08 | libbid | 14.86 | **1.23×** | Rc |  |
| c | sub | FQ | P-gen | arm64 | thru | 6.84 | libbid | 12.30 | **1.80×** | Rc |  |
| rust | add | SQ | P-gen | arm64 | thru | 3.08 | libbid | 8.43 | **2.74×** | Rprof |  |
| rust | add | NQ | P-gen | arm64 | thru | 4.57 | libbid | 8.38 | **1.83×** | Rprof |  |
| rust | add | MQ | P-gen | arm64 | thru | 13.50 | libbid | 8.58 | **0.64×** | Rprof |  |
| rust | add | OQ | P-gen | arm64 | thru | 10.59 | libbid | 13.75 | **1.30×** | Rc |  |
| rust | add | FQ | P-gen | arm64 | thru | 7.56 | libbid | 10.36 | **1.37×** | Rc |  |
| rust | sub | SQ | P-gen | arm64 | thru | 1.87 | libbid | 9.89 | **5.29×** | Rprof |  |
| rust | sub | NQ | P-gen | arm64 | thru | 4.68 | libbid | 11.66 | **2.49×** | Rprof |  |
| rust | sub | MQ | P-gen | arm64 | thru | 13.96 | libbid | 10.39 | **0.74×** | Rprof |  |
| rust | sub | OQ | P-gen | arm64 | thru | 10.68 | libbid | 14.86 | **1.39×** | Rc |  |
| rust | sub | FQ | P-gen | arm64 | thru | 6.83 | libbid | 12.30 | **1.80×** | Rc |  |
| zig | add | SQ | P-gen | arm64 | thru | 3.00 | libbid | 8.43 | **2.81×** | Rprof |  |
| zig | add | NQ | P-gen | arm64 | thru | 5.97 | libbid | 8.38 | **1.40×** | Rprof |  |
| zig | add | MQ | P-gen | arm64 | thru | 11.78 | libbid | 8.58 | **0.73×** | Rprof |  |
| zig | add | OQ | P-gen | arm64 | thru | 12.96 | libbid | 13.75 | **1.06×** | Rc |  |
| zig | add | FQ | P-gen | arm64 | thru | 7.83 | libbid | 10.36 | **1.32×** | Rc |  |
| zig | sub | SQ | P-gen | arm64 | thru | 1.79 | libbid | 9.89 | **5.53×** | Rprof |  |
| zig | sub | NQ | P-gen | arm64 | thru | 5.71 | libbid | 11.66 | **2.04×** | Rprof |  |
| zig | sub | MQ | P-gen | arm64 | thru | 12.34 | libbid | 10.39 | **0.84×** | Rprof |  |
| zig | sub | OQ | P-gen | arm64 | thru | 12.60 | libbid | 14.86 | **1.18×** | Rc |  |
| zig | sub | FQ | P-gen | arm64 | thru | 7.68 | libbid | 12.30 | **1.60×** | Rc |  |
| swift | add | SQ | P-gen | arm64 | thru | 4.70 | libbid | 8.43 | **1.79×** | Rprof |  |
| swift | add | NQ | P-gen | arm64 | thru | 5.95 | libbid | 8.38 | **1.41×** | Rprof |  |
| swift | add | MQ | P-gen | arm64 | thru | 15.41 | libbid | 8.58 | **0.56×** | Rprof |  |
| swift | add | OQ | P-gen | arm64 | thru | 17.89 | libbid | 13.75 | **0.77×** | Rc |  |
| swift | add | FQ | P-gen | arm64 | thru | 13.41 | libbid | 10.36 | **0.77×** | Rc |  |
| swift | sub | SQ | P-gen | arm64 | thru | 2.95 | libbid | 9.89 | **3.35×** | Rprof |  |
| swift | sub | NQ | P-gen | arm64 | thru | 5.41 | libbid | 11.66 | **2.16×** | Rprof |  |
| swift | sub | MQ | P-gen | arm64 | thru | 15.09 | libbid | 10.39 | **0.69×** | Rprof |  |
| swift | sub | OQ | P-gen | arm64 | thru | 18.67 | libbid | 14.86 | **0.80×** | Rc |  |
| swift | sub | FQ | P-gen | arm64 | thru | 13.56 | libbid | 12.30 | **0.91×** | Rc |  |
| csharp | add | SQ | P-gen | arm64 | thru | 2.18 | libbid | 8.43 | **3.87×** | Rprof |  |
| csharp | add | NQ | P-gen | arm64 | thru | 7.02 | libbid | 8.38 | **1.19×** | Rprof |  |
| csharp | add | MQ | P-gen | arm64 | thru | 17.56 | libbid | 8.58 | **0.49×** | Rprof |  |
| csharp | add | OQ | P-gen | arm64 | thru | 18.96 | libbid | 13.75 | **0.73×** | Rc |  |
| csharp | add | FQ | P-gen | arm64 | thru | 11.93 | libbid | 10.36 | **0.87×** | Rc |  |
| csharp | sub | SQ | P-gen | arm64 | thru | 1.47 | libbid | 9.89 | **6.73×** | Rprof |  |
| csharp | sub | NQ | P-gen | arm64 | thru | 9.79 | libbid | 11.66 | **1.19×** | Rprof |  |
| csharp | sub | MQ | P-gen | arm64 | thru | 11.95 | libbid | 10.39 | **0.87×** | Rprof |  |
| csharp | sub | OQ | P-gen | arm64 | thru | 20.14 | libbid | 14.86 | **0.74×** | Rc |  |
| csharp | sub | FQ | P-gen | arm64 | thru | 9.19 | libbid | 12.30 | **1.34×** | Rc |  |
| go | add | SQ | P-gen | arm64 | thru | 4.49 | libbid | 8.43 | **1.88×** | Rprof |  |
| go | add | NQ | P-gen | arm64 | thru | 9.77 | libbid | 8.38 | **0.86×** | Rprof |  |
| go | add | MQ | P-gen | arm64 | thru | 21.64 | libbid | 8.58 | **0.40×** | Rprof |  |
| go | add | OQ | P-gen | arm64 | thru | 33.38 | libbid | 13.75 | **0.41×** | Rc |  |
| go | add | FQ | P-gen | arm64 | thru | 20.12 | libbid | 10.36 | **0.51×** | Rc |  |
| go | sub | SQ | P-gen | arm64 | thru | 2.98 | libbid | 9.89 | **3.32×** | Rprof |  |
| go | sub | NQ | P-gen | arm64 | thru | 9.75 | libbid | 11.66 | **1.20×** | Rprof |  |
| go | sub | MQ | P-gen | arm64 | thru | 21.04 | libbid | 10.39 | **0.49×** | Rprof |  |
| go | sub | OQ | P-gen | arm64 | thru | 33.18 | libbid | 14.86 | **0.45×** | Rc |  |
| go | sub | FQ | P-gen | arm64 | thru | 19.49 | libbid | 12.30 | **0.63×** | Rc |  |
| c | add | SQ | P-gen | arm64 | thru | 2.21 | libdecquad | 19.96 | **9.03×** | Rprof |  |
| c | add | NQ | P-gen | arm64 | thru | 3.88 | libdecquad | 29.66 | **7.64×** | Rprof |  |
| c | add | MQ | P-gen | arm64 | thru | 9.93 | libdecquad | 28.18 | **2.84×** | Rprof |  |
| c | add | OQ | P-gen | arm64 | thru | 11.74 | libdecquad | 34.53 | **2.94×** | Rc |  |
| c | add | FQ | P-gen | arm64 | thru | 6.53 | libdecquad | 26.32 | **4.03×** | Rc |  |
| c | sub | SQ | P-gen | arm64 | thru | 1.66 | libdecquad | 22.17 | **13.36×** | Rprof |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.03 | libdecquad | 33.85 | **8.40×** | Rprof |  |
| c | sub | MQ | P-gen | arm64 | thru | 10.87 | libdecquad | 30.13 | **2.77×** | Rprof |  |
| c | sub | OQ | P-gen | arm64 | thru | 12.08 | libdecquad | 36.84 | **3.05×** | Rc |  |
| c | sub | FQ | P-gen | arm64 | thru | 6.84 | libdecquad | 29.97 | **4.38×** | Rc |  |
| c | add | SQ | P-gen | arm64 | thru | 2.21 | libmpdecimal | 12.48 | **5.65×** | Rprof |  |
| c | add | NQ | P-gen | arm64 | thru | 3.88 | libmpdecimal | 26.76 | **6.90×** | Rprof |  |
| c | add | MQ | P-gen | arm64 | thru | 9.93 | libmpdecimal | 26.75 | **2.69×** | Rprof |  |
| c | add | OQ | P-gen | arm64 | thru | 11.74 | libmpdecimal | 44.67 | **3.80×** | Rc |  |
| c | add | FQ | P-gen | arm64 | thru | 6.53 | libmpdecimal | 39.16 | **6.00×** | Rc |  |
| c | sub | SQ | P-gen | arm64 | thru | 1.66 | libmpdecimal | 14.31 | **8.62×** | Rprof |  |
| c | sub | NQ | P-gen | arm64 | thru | 4.03 | libmpdecimal | 21.22 | **5.27×** | Rprof |  |
| c | sub | MQ | P-gen | arm64 | thru | 10.87 | libmpdecimal | 20.51 | **1.89×** | Rprof |  |
| c | sub | OQ | P-gen | arm64 | thru | 12.08 | libmpdecimal | 44.55 | **3.69×** | Rc |  |
| c | sub | FQ | P-gen | arm64 | thru | 6.84 | libmpdecimal | 39.13 | **5.72×** | Rc |  |
| rust | add | SQ | P-gen | arm64 | thru | 3.08 | rust_decimal | 4.03 | **1.31×** | Rprof | compact idiom peer |
| rust | add | NQ | P-gen | arm64 | thru | 4.57 | rust_decimal | 5.26 | **1.15×** | Rprof | compact idiom peer |
| rust | add | MQ | P-gen | arm64 | thru | 13.50 | rust_decimal | 5.31 | **0.39×** | Rprof | compact idiom peer |
| rust | sub | SQ | P-gen | arm64 | thru | 1.87 | rust_decimal | 3.29 | **1.76×** | Rprof | compact idiom peer |
| rust | sub | NQ | P-gen | arm64 | thru | 4.68 | rust_decimal | 5.12 | **1.09×** | Rprof | compact idiom peer |
| rust | sub | MQ | P-gen | arm64 | thru | 13.96 | rust_decimal | 5.42 | **0.39×** | Rprof | compact idiom peer |
