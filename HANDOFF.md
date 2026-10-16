# Kontho decompile -- handoff / resume note

Written at the moment the user interrupted. Everything below is accurate as of that point.

---

## 0. Status in one paragraph

Stock `pycdc` cannot decompile Python 3.13 at all. A from-source build of `pycdc` has been taught
3.13's bytecode through a ~1400-line patch script, and it now decompiles the whole app
(`Kontho.pyc`, 12,379 output lines) with **no fatal errors**. The last big structural gap --
`with` statements in 3.11+ code -- was fixed and **compiled successfully** just before this note
was written; `with` clauses now come out correct. What remains inside the decompiled file is a
small number of parse failures (5 functions at last count, probably fewer now) caused by
`with`-body regions that the CPython compiler truncates around nested `try` statements.

---

## 1. The goal

The user extracted a Windows installer (`innoextract`), then the app inside it
(`pyinstxtractor-ng`), and wants the Python source of `Kontho.pyc` recovered, properly structured,
so that it **runs and shows its GUI**.

Decisions the user already made:

* Method: **pycdc draft + manual verification against the bytecode**.
* Order: **get it running first, then refine**.

---

## 2. Layout / paths

Everything is relative to the working directory unless absolute.

| What | Path |
|---|---|
| Repo root (untouched originals) | `C:/Users/Nafis/Desktop/kontho` |
| **Working directory** | `C:/Users/Nafis/Desktop/kontho/_work` |
| **Source of truth: the app bytecode** | `C:/Users/Nafis/Desktop/kontho/Kontho.exe_extracted/Kontho.pyc` |
| Extracted exe contents (14 entries) | `C:/Users/Nafis/Desktop/kontho/Kontho.exe_extracted/` |
| Bundled CPython 3.13.5 (for `dis`/`marshal`) | `_work/tools/py313/python.exe` |
| pycdc checkout (git) | `_work/tools/pycdc` |
| pycdc build dir (Ninja) | `_work/tools/pycdc/build-msvc` |
| **Built decompiler** | `_work/tools/pycdc/build-msvc/pycdc.exe` |
| Raw decompile output | `_work/pycdc_raw.py` |
| Decompiler stderr (warnings) | `_work/pycdc_err.txt` |
| Micro test corpus | `_work/t/micro/` |
| The **central artifact** | `_work/scripts/patch_pycdc.py` |

`Kontho.exe_extracted` contains only 14 entries: `Kontho.pyc`, `PYZ-00.pyz`,
`PYZ-00.pyz_extracted/`, five `pyi_rth_*.pyc` hooks, `pyiboot01_bootstrap.pyc`,
`pyimod01..04_*.pyc`, and `struct.pyc`. **`Kontho.pyc` is the entire application** -- there is no
tree of local modules to decompile. `PYZ-00.pyz_extracted` holds the bundled stdlib / PyQt5.

---

## 3. Toolchain and the build

* Compiler: MSVC, VS 18 BuildTools.
* `vcvars64.bat`: `C:/Program Files (x86)/Microsoft Visual Studio/18/BuildTools/VC/Auxiliary/Build/vcvars64.bat`
* Generator: Ninja, already configured in `tools/pycdc/build-msvc`.
* Bundled Python: `tools/py313/python.exe` (3.13.5). Use `-I` for every invocation.
* pycdc revision: `b428976` ("Merge pull request #599 from daiche330-png/wip/python311-exception-opcodes-20260405").

### Rebuild command (verified working, PowerShell)

```powershell
Set-Location C:\Users\Nafis\Desktop\kontho\_work\tools\pycdc
cmd /c '"C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul && cmake --build build-msvc'
```

**Gotcha:** without `vcvars64` the build fails immediately with
`fatal error C1083: Cannot open include file: 'cstring'` (and the same for `typeinfo`). That is a
missing-environment error, **not** a source error -- do not go hunting in the code.
A `'vswhere.exe' is not recognized` line printed by `vcvars64.bat` is harmless noise.

### Patch generation rule (important)

`tools/pycdc/ASTree.cpp` and `tools/pycdc/ASTNode.h` are **generated**: `patch_pycdc.py` applies
exact-string replacements to the *pristine* files, so they must be reverted first, every time:

```bash
cd /c/Users/Nafis/Desktop/kontho/_work
git -C tools/pycdc checkout -- ASTree.cpp ASTNode.h
./tools/py313/python.exe -I scripts/patch_pycdc.py
# optional, debug only -- adds PYCDC_TRACE instrumentation, not for release builds:
./tools/py313/python.exe -I scripts/trace_pycdc.py
# then rebuild (see above)
```

`git status` in `tools/pycdc` normally shows `M ASTNode.h`, `M ASTree.cpp`, `?? build-msvc/`.

---

## 4. The pipeline scripts (`_work/scripts/`)

| Script | Purpose |
|---|---|
| `patch_pycdc.py` | **The whole patch.** Sections 1e..1s, applied in order to pristine `ASTree.cpp` / `ASTNode.h`. ~1400 lines. Every section asserts its anchor is found exactly once, so a failure here means the pristine file changed (wrong revision) -- not a logic bug. |
| `trace_pycdc.py` | Inserts an env-gated trace into the *already patched* `ASTree.cpp`. Run with `PYCDC_TRACE=1` to get `TR <event> pos=.. a=.. b=.. blk=.. end=.. blocks=.. hist=..` on stderr. Events: `loop`, `push-home`, `entry`, `region`, `try-close`, `exc-close`, `adopt`. **Must not be applied for a release build.** |
| `check.py` | `python -I scripts/check.py pycdc_raw.py bad` -- splits the decompiled file into top-level blocks and reports which ones fail `ast.parse`. This is the regression metric. |
| `disco.py` | `python -I scripts/disco.py <file.pyc> [qualname-substring]` -- disassembles matching code objects **with the exception table**. Outputs the *resolved* jump targets (`argval`), not raw operands. |
| `gaps.py` | For every depth-0 region, prints `[start,end) -> target` plus the opnames just after the region end. |
| `extract.py` | `python -I scripts/extract.py <file.pyc> <qualname-substring> <out.pyc>` -- writes a pyc whose top-level code object is the matching nested function, so one function can be decompiled/traced alone. This is the main debugging loop. |
| others | `disq.py`, `dec1.py`, `moddis.py`, `load_pyc.py`, `exctab.py`, `opcodes.py`, `gen313.py`, `runtest.py`, `linecheck.py`, `inventory.py` -- assorted helpers from earlier phases; not on the critical path. |

### The main debug loop

```bash
cd /c/Users/Nafis/Desktop/kontho/_work
PYC="C:/Users/Nafis/Desktop/kontho/Kontho.exe_extracted/Kontho.pyc"

# whole module
./tools/pycdc/build-msvc/pycdc.exe "$PYC" > pycdc_raw.py 2> pycdc_err.txt
./tools/py313/python.exe -I scripts/check.py pycdc_raw.py bad

# one function, with trace
./tools/py313/python.exe -I scripts/extract.py "$PYC" "<qualname>" _work_x.pyc
PYCDC_TRACE=1 ./tools/pycdc/build-msvc/pycdc.exe _work_x.pyc > x.py 2> x.tr
```

---

## 5. What is DONE

1. **Recon of the whole extraction** -- Inno -> PyInstaller onedir -> PYZ; the app is one module.
2. **pycdc built from source** and reproducibly patched.
3. **Python 3.13 support in the decompiler** (`patch_pycdc.py`), covering:
   * the 3.13 exception-table varint format and `lasti`/depth decoding;
   * handler **islands** (out-of-line handler bodies, `PUSH_EXC_INFO` discriminator);
   * multi-region `try`s (same depth+target spread over several entries);
   * multi-clause handlers (non-match jump + `starts_clause` + container append);
   * the 3.12+ relative-jump offset bug (operand is relative to the end of the instruction
     *including inline caches*), fixed by `jump_caches()`;
   * trimmed `RETURN_CONST`/`RETURN_VALUE` tails at the end of a region;
   * the `else_pop` sweep over-popping a `try`/container pair (section 1r);
   * **`with` statements for 3.11+** (section 1s -- `BEFORE_WITH`, `WITH_EXCEPT_START`, the
     cleanup island), which is the newest and was compiled successfully.
4. Whole-module decompile: **12,379 lines, no fatal opcode aborts.**
5. `with` statements now render correctly, e.g.:

```python
            with QMutexLocker(mutex):
                self.ownList = secondDicPKL.get_values_by_value_prefix(self.rawWord[0])
```

   (Previously this produced `try: QMutexLocker(mutex) ... except: with None: if not None: pass`.)

---

## 6. What was IN FLIGHT at the interruption

* `scripts/patch_pycdc.py` **section 1s** (3.11+ `with`) is written and **compiles**; the rebuild
  succeeded and the extracted test function `spell_check_thread.suggest_from_lacoal_second_lang`
  (`_work/sl.py`) now has correct `with` blocks.
* That same function still has **residual defects**, which is the immediate next thing to work on
  (see section 8, item 1). It is the only fully analysed example; the other 4 failing functions
  are presumably the same class.

---

## 7. How to resume -- copy/paste

```bash
# 1. regenerate + rebuild the decompiler
cd /c/Users/Nafis/Desktop/kontho/_work
git -C tools/pycdc checkout -- ASTree.cpp ASTNode.h
./tools/py313/python.exe -I scripts/patch_pycdc.py
#    (add trace_pycdc.py only if you want PYCDC_TRACE)
```
```powershell
# 2. rebuild
Set-Location C:\Users\Nafis\Desktop\kontho\_work\tools\pycdc
cmd /c '"C:\Program Files (x86)\Microsoft Visual Studio\18\BuildTools\VC\Auxiliary\Build\vcvars64.bat" >nul && cmake --build build-msvc'
```
```bash
# 3. re-measure
cd /c/Users/Nafis/Desktop/kontho/_work
PYC="C:/Users/Nafis/Desktop/kontho/Kontho.exe_extracted/Kontho.pyc"
./tools/pycdc/build-msvc/pycdc.exe "$PYC" > pycdc_raw.py 2> pycdc_err.txt
./tools/py313/python.exe -I scripts/check.py pycdc_raw.py bad
grep -c . pycdc_raw.py
```

---

## 8. What is LEFT

### 8.1 Fix the remaining parse failures (immediate)

Last measured: **5** failing top-level blocks -- `SpeechThread`, `spell_check_thread`,
`listViewClass`, `Ui`, `excepthook`. (Re-measure: section 1s should have removed some.)

**Root cause of at least one, fully analysed:**

`with` bodies whose region the compiler truncates because something inside them needs its own
`try`. Worked example -- `spell_check_thread.suggest_from_lacoal_second_lang`, the `with` at
`L1640`:

```
   980  LOAD_GLOBAL 'mutex'
   990  CALL 1
   998  BEFORE_WITH
  1000  POP_TOP              <- region [1000,1002) -> 1616  (only 2 bytes!)
  1002  NOP                  <- L1641, the `try` statement
  1004  ... 1072             <- region [1004,1082) -> 1554   (the nested try)
  1082  LOAD_CONST None      <- the with's own exit call ...
  1084  LOAD_CONST None
  1086  LOAD_CONST None
  1088  CALL 2
  1096  POP_TOP              <- ... ends here
  1098  <continuation>
```

The `with`'s body region is `[1000,1002)` only, because the nested `try` took over `[1004,1082)`.
So the current code sets the block's `end` to `1002`, closes the `with` after the `POP_TOP`, and
emits `with QMutexLocker(mutex): pass` followed by the `try` **dedented out of the `with`**.
Output today:

```python
                    with QMutexLocker(mutex):
                        pass

                    try:
                        self.ownList = secondDicPKL.search_by_main_word_prefix_withOutLimit(self.word[0])
                    except Exception:
                        self.ownList = []

                    None(None, None)          <- junk: the swallowed exit call
```

**Fix direction (recommended):** stop relying on the region end for the body. Instead:

1. the exit call is a fixed shape -- `LOAD_CONST, LOAD_CONST, LOAD_CONST, CALL, CACHE*,
   POP_TOP` -- and is essentially unique in real code (`f(None, None, None)` would be `CALL 3`,
   after a `LOAD f`);
2. scan forward from the instruction after `BEFORE_WITH` for the **first** match, giving
   `exit_start`/`exit_end`;
3. set the `with` block's `end` to `exit_start`, push `(exit_start, exit_end)` onto `with_exits`
   (already implemented), and the existing loop-head skip does the rest.

**Alternative (also viable, one unknown):** resolve the cleanup island's terminating
`JUMP_BACKWARD_NO_INTERRUPT` target, which *is* the continuation offset (the end of the exit
call). Resolved targets observed: island@1482 -> 352, island@1518 -> 738, island@1616 -> 1098 --
each exactly the first instruction after the corresponding `with`'s exit call. **Open question:**
the arithmetic to get those numbers from the raw operand bytes was *not* pinned down. `dis` reports
`arg=580, argval=352` at offset 1510 with `EXTENDED_ARG 2` at 1508, and neither
`(1510+2) - (2<<8|580)` nor any obvious variant yields 352. Resolve this in Python with
`dis.get_instructions` + raw `co_code` bytes before relying on it. The forward-scan option above
sidesteps the question entirely.

### 8.2 Remaining cosmetic / correctness warnings in the output

Measured on the previous full run (counts will have moved):

* 23x `block stack is not empty`
* 22x `Stack history is not empty`
* 17x `function annotations dropped`
* 6x `Wrong block type N for END_FOR`
* 2x `unhandled CALL_INTRINSIC_1 id 3`
* 2x `DICT_UPDATE rendered as .update()` (rendered as an explicit `.update()` call on purpose;
  should become `{**a, **b}`)
* 1x `Unsupported argument found for LIST_EXTEND`

### 8.3 3.13 compiler artifacts to strip (post-processing pass)

* `__firstlineno__ = ...`
* `__static_attributes__ = ...`
* `__classcell__ = __class__` and the trailing `return __class__`
* `e = None; del e` pairs -> fold back into `except E as e:`
* `except E:` + leading `X = None` + trailing `del X` -> `except E as X:`
* `LOAD_CONST False/True` sometimes renders as `None` (a `PycBool` issue). Concrete example:
  `self.busy = None` in `check_word` should be `self.busy = False`.

### 8.4 Make it run (the user's actual goal)

* Import the recovered module with the bundled runtime from `Kontho.exe_extracted`.
* Bootstrap before Qt loads:
  * `os.add_dll_directory` for `_internal`, `_internal/PyQt5`, `_internal/PyQt5/Qt5/bin`,
    `_internal/pywin32_system32`;
  * set `QT_QPA_PLATFORM_PLUGIN_PATH`.
* Expect *runtime* errors from subtly-wrong decompiled spots; fix as they appear.

### 8.5 Manual verification against the bytecode

The long tail, and what the user originally asked for. A 12k-line file can parse and even run
while still being subtly wrong. Not started.

### 8.6 Housekeeping

* Delete `scripts/_mid.txt` if still present.
* Remove the temporary tracing before any "release" build (`trace_pycdc.py` is opt-in, but note it
  in whatever build instructions get handed over).

---

## 9. Hard-won technical notes

These cost most of the elapsed time. They are the reason not to start over.

### Python 3.13 bytecode facts

* Magic `3571`, 16-byte pyc header, 2 bytes per instruction.
* Exception-table entries: varints `start`, `length`, `target`, `dl`. Each encoded with a 0x40
  continuation bit, values shifted left by 1; `depth = dl >> 1`, `lasti = dl & 1`.
* Inline caches in 3.13: `POP_JUMP_IF_FALSE/TRUE` = 1, `FOR_ITER` = 1, `JUMP_BACKWARD` = 1,
  `LOAD_GLOBAL` = 4. `JUMP_BACKWARD_NO_INTERRUPT` = 0.
* From 3.12 on, a jump operand is relative to the end of the instruction **including its caches**.
  Upstream pycdc adds it to the offset just past the opcode, so every target lands one cache short.
* Handler islands: each handler body is emitted out of line and starts with `PUSH_EXC_INFO`.
  Cleanup islands start with `COPY`/`POP_EXCEPT`/`RERAISE` instead -- that is the discriminator.
* A `with` in 3.11+ uses the exception table too: its island starts
  `PUSH_EXC_INFO; WITH_EXCEPT_START`. **No `try` handler ever starts that way.** This is the
  test for "is this island a `with` cleanup?".
* `BEFORE_WITH` leaves `__exit__` and the result of `__enter__` on the stack. `with X:` follows it
  with a `POP_TOP`; `with X as y:` follows it with a `STORE_FAST`, which pristine pycdc already
  handles via the `BLK_WITH && !inited` path.
* The `with` body's region ends where the exit call begins, and the exit call is
  `LOAD_CONST None; LOAD_CONST None; LOAD_CONST None; CALL 2; <caches>; POP_TOP`.
* One `try` compiles to several depth-0 regions with the same target as soon as anything inside
  needs a `try` of its own -- so a `try` must span *all* of them.
* The compiler leaves terminal, non-raising instructions (`RETURN_CONST`, `RETURN_VALUE`) out of a
  region, so a region can end before the `try` really ends.

### pycdc internals that matter

* pycdc's own `pos` variable is the offset **after** the instruction just fetched (i.e. of the
  *next* instruction). At the loop head, before `bc_next`, it is the current instruction's offset.
  `curpos` is the current instruction's offset inside a `case`.
* Main loop order: loop head (advance entries, island/home push, region starts) -> TRY close ->
  EXCEPT close -> `curpos = pos; bc_next(...)` -> `else_pop` sweep -> `switch (opcode)`.
* `source` is a `PycBuffer` over the raw code bytes; it has **no `seek`**, but bytes can be consumed
  with `source.getByte()`. To skip instructions safely, call `bc_next` in a loop passing the
  current offset, i.e. the idiom used by section 1s:
  ```cpp
  while (pos < stop && !source.atEof()) {
      int walk_op, walk_arg, walk_at = pos;
      bc_next(source, mod, walk_op, walk_arg, walk_at);
      pos = walk_at;
  }
  ```
* `ASTBlock::BlkType`: `BLK_MAIN=0, BLK_IF=1, BLK_ELSE=2, BLK_ELIF=3, BLK_TRY=4, BLK_CONTAINER=5,
  BLK_EXCEPT=6, BLK_FINALLY=7, BLK_WHILE=8, BLK_FOR=9, BLK_WITH=10`.
* Opcode constants live in `tools/pycdc/bytecode_ops.inl`; `OPCODE(x)` -> `x`, `OPCODE_A(x)` ->
  `x_A`. So: `Pyc::CALL_A`, `Pyc::CACHE`, `Pyc::LOAD_CONST_A`, `Pyc::COPY_A`, `Pyc::RERAISE_A`,
  `Pyc::RERAISE`, `Pyc::PUSH_EXC_INFO`, `Pyc::WITH_EXCEPT_START`, `Pyc::BEFORE_WITH`,
  `Pyc::JUMP_BACKWARD_NO_INTERRUPT_A`.
* `ASTWithBlock(end)`; `setExpr()` calls `init()`; printing uses `expr()`/`var()`. `inited()` is
  what makes the `POP_TOP` / `STORE_FAST` handlers fill in the expression.
* `disco.py` prints **resolved jump targets** (dis `argval`), not raw operands -- do not confuse
  these with the bytes in `co_code`.
