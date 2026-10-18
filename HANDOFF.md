# Minor issues and mismatches — detailed checklist

Date: 2026-10-18
Mode: read-only verification. No kernel/KernelSU source was modified.
Companion to `reports/04-final-report.md`. This file contains **only** the minor findings, with the
exact evidence needed to check each one by hand.

Status legend:
- **LATENT** — real mismatch, harmless with the current code, can break after an upstream update.
- **HYGIENE** — repo/config cleanliness, no functional effect today.
- **COSMETIC** — display/comment-only difference.
- **ADAPTATION** — deliberate and correct for this 4.14 tree; do not "fix" to match upstream.

Priority order: #1 is the only one worth acting on soon; #2–#7 are optional; §C items are not defects.

---

## Summary table

| # | Item | Class | Functional impact today | Needs approval |
|---|---|---|---|---|
| 1 | `ksu_handle_sys_read` arity drift | LATENT | None (arm64, body ignores extra args) | No (source edit, but low risk) |
| 2 | `dispatch.c` implicit declarations | LATENT/STYLE | None (all handlers return `void`) | No (BakaSU-side) |
| 3 | Dead `susfs_set_*_sid()` declarations | HYGIENE | None (never referenced) | No (BakaSU-side) |
| 4 | Stale `.rej` / `.orig` files | HYGIENE | None (all hunks already applied) | **Yes** (deletion) |
| 5 | KernelSU submodule pointer mismatch | HYGIENE | None now; rollback risk later | Yes (pin change) |
| 6 | KernelSU remote URL mismatch | HYGIENE | None | Yes (config change) |
| 7 | Four dead defconfig symbols | HYGIENE | None (silently dropped) | **Yes** (defconfig) |
| 8 | Inline-hook script non-idempotent | HYGIENE/WARNING | None (never run it on this tree) | No (documentation) |

---

## 1. `ksu_handle_sys_read` argument-count drift — LATENT

**Locations**

- Kernel declaration: `fs/read_write.c:600`
  ```c
  extern __attribute__((cold)) int ksu_handle_sys_read(unsigned int fd);
  ```
- Kernel call: `fs/read_write.c:610`
  ```c
  if (static_branch_unlikely(&ksu_is_init_rc_hook_enabled))
      ksu_handle_sys_read(fd);
  ```
- BakaSU definition: `KernelSU/kernel/runtime/ksud_integration.c:770`
  ```c
  int ksu_handle_sys_read(unsigned int fd, char __user **buf_ptr, size_t *count_ptr)
  {
  #ifdef CONFIG_KSU_MANUAL_HOOK_AUTO_INITRC_HOOK
      return 0; // dummy hook here
  #else
      ksu_handle_sys_read_fd(fd);
      return 0;
  #endif
  }
  ```
- Body only uses `fd`: `ksu_handle_sys_read_fd()` at `ksud_integration.c:757-769`.

**Why it works today:** on AArch64 the two missing arguments are simply garbage in `x1`/`x2`; the
callee never reads them. The call is also guarded by `ksu_is_init_rc_hook_enabled`, so it only runs
when the init-rc hook is enabled.

**Risk:** if a future BakaSU starts dereferencing `buf_ptr`/`count_ptr` at this call site, it is
undefined behaviour. `CONFIG_KSU_MANUAL_HOOK_AUTO_INITRC_HOOK` is not set here (checked in
`.config`), so the non-dummy branch is the one compiled.

**Suggested action:** align the kernel prototype/call with the 3-argument form and pass `&buf`,
`&count` from `SYSCALL_DEFINE3(read, ...)`; or intentionally keep the 1-arg shim and document it.
Do not change until the next BakaSU update is planned.

**Verify command**

```bash
grep -n "ksu_handle_sys_read" fs/read_write.c KernelSU/kernel/runtime/ksud_integration.c
sed -n '755,782p' KernelSU/kernel/runtime/ksud_integration.c
```

---

## 2. `supercall/dispatch.c` uses implicit declarations — LATENT / STYLE

**Location:** `KernelSU/kernel/supercall/dispatch.c:9`

```c
#include <linux/susfs_def.h>
```

It does **not** include `<linux/susfs.h>`, which is where the handlers are declared
(`include/linux/susfs.h:191-238`).

**Evidence:** 16 call sites in `dispatch.c` have no visible prototype:

| Line | Call |
|---:|---|
| 175 | `susfs_start_sdcard_monitor_fn()` |
| 1013 | `susfs_add_sus_path(arg)` |
| 1017 | `susfs_add_sus_path_loop(arg)` |
| 1023 | `susfs_set_hide_sus_mnts_for_non_su_procs(arg)` |
| 1029 | `susfs_add_sus_kstat(arg)` |
| 1033 | `susfs_update_sus_kstat(arg)` |
| 1037 | `susfs_add_sus_kstat(arg)` |
| 1043 | `susfs_set_uname(arg)` |
| 1049 | `susfs_enable_log(arg)` |
| 1055 | `susfs_set_cmdline_or_bootconfig(arg)` |
| 1061 | `susfs_add_open_redirect(arg)` |
| 1067 | `susfs_add_sus_map(arg)` |
| 1072 | `susfs_set_avc_log_spoofing(arg)` |
| 1076 | `susfs_get_enabled_features(arg)` |
| 1080 | `susfs_show_variant(arg)` |
| 1084 | `susfs_show_version(arg)` |

(Note: the Phase 3 report said "15"; the sdcard-monitor call at line 175 is a 16th implicit
declaration. Same class, corrected count.)

`susfs_is_current_proc_umounted()` at `dispatch.c:541` is **not** affected — it is a `static inline`
in `include/linux/susfs_def.h`.

**Impact:** none today. With `-Wno-implicit-function-declaration` (visible in
`KernelSU/kernel/supercall/.supercall.o.cmd`) and `KCFLAGS=-Wno-error`, this compiles. All handlers
are `void`, so the implicit `int` return assumption is harmless.

**Suggested action:** add `#include <linux/susfs.h>` to `dispatch.c` upstream. Not a kernel-side
integration defect.

**Verify command**

```bash
grep -n "#include <linux/susfs" KernelSU/kernel/supercall/dispatch.c
grep -n "susfs_[a-z_]*(" KernelSU/kernel/supercall/dispatch.c
```

---

## 3. Dead `susfs_set_*_sid()` declarations — HYGIENE

**Location:** `KernelSU/kernel/selinux/selinux.h:60,62,64`

```c
void susfs_set_ksu_sid(void);
void susfs_set_init_sid(void);
void susfs_set_priv_app_sid(void);
```

**Evidence:** a tree-wide grep for definitions/callers finds only these three declaration lines:

```bash
grep -rn "susfs_set_ksu_sid\|susfs_set_init_sid\|susfs_set_priv_app_sid" KernelSU/kernel fs/ include/
# -> only selinux.h:60,62,64
```

The SIDs are assigned directly in `cache_sid()` (`KernelSU/kernel/selinux/selinux.c:181-189`).

**Impact:** none — no link error because nothing references the symbols.

**Suggested action:** remove upstream, or leave. No kernel change needed.

---

## 4. Stale `.rej` / `.orig` files — HYGIENE (deletion needs approval)

17 files outside `KernelSU/` and `toolchains/`:

`.rej` (6):
```
fs/namespace.c.rej
fs/notify/fdinfo.c.rej
fs/proc/task_mmu.c.rej
fs/readdir.c.rej
kernel/kallsyms.c.rej
security/selinux/avc.c.rej
```

`.orig` (11):
```
fs/namei.c.orig
fs/namespace.c.orig
fs/notify/fdinfo.c.orig
fs/proc/base.c.orig
fs/proc/task_mmu.c.orig
fs/readdir.c.orig
fs/super.c.orig
kernel/kallsyms.c.orig
kernel/sys.c.orig
mm/memory.c.orig
security/selinux/avc.c.orig
```

**Status:** every rejected hunk in every `.rej` was checked by hand during Phase 2 and **is already
applied** (including the `bypass_orig_flow` label in `avc.c`). These are leftovers from the original
patching, not pending work.

**Impact:** none on the build (they are not compiled). They only confuse future diffs/searches.

**Suggested action:** delete after your approval. Per hard rule 7, no files are deleted without
asking.

**Verify command**

```bash
find . -path ./KernelSU -prune -o -path ./toolchains -prune -o \( -name '*.rej' -o -name '*.orig' \) -print | sort
```

---

## 5. KernelSU submodule pointer mismatch — HYGIENE

| View | Commit | Date |
|---|---|---|
| Superproject index (`git ls-tree HEAD KernelSU`) | `5b76b884c75f729a220bb317aa4a4fc78f0e0e9c` | 2026-10-09 |
| Actual KernelSU worktree (`git -C KernelSU rev-parse HEAD`) | `f308ed0936bdd31163cb53da3f42bc7a698f5512` | 2026-10-17 |

**Impact:** the build uses the worktree (`f308ed09`), which is what Phase 3 audited. But a future
`git submodule update` (or a fresh clone at the recorded commit) would silently roll BakaSU back to
`5b76b884`, changing behaviour without any source edit in this repo.

**Suggested action:** deliberately pin `f308ed09` in the superproject index (requires your
approval; this is a submodule pointer change).

**Verify command**

```bash
git ls-tree HEAD KernelSU
git -C KernelSU rev-parse HEAD
```

---

## 6. KernelSU remote URL mismatch — HYGIENE / UNVERIFIED

- `.gitmodules:3` records `https://github.com/Baka-SU/BakaSU`
- Actual `git -C KernelSU remote get-url origin` returns `https://github.com/ReSukiSU/ReSukiSU`

Both projects are related (BakaSU is a ReSukiSU-based fork), but which repository is authoritative
for this build was **not verified**. The checked-out branch is `sync-susfs` and HEAD `f308ed09` was
audited as-is.

**Impact:** none at build time. It matters for reproducibility and for "update upstream" decisions.

**Suggested action:** decide which URL is authoritative, then align `.gitmodules` and the actual
remote (requires your approval).

**Verify command**

```bash
git -C KernelSU remote get-url origin
grep -n -A2 "KernelSU" .gitmodules
```

---

## 7. Four dead defconfig symbols — HYGIENE (defconfig change needs approval)

**Location:** `arch/arm64/configs/exynos9610-m21dd_defconfig:5878-5881`

```
CONFIG_KSU_SUSFS_TRY_UMOUNT=y
CONFIG_KSU_SUSFS_AUTO_ADD_SUS_KSU_DEFAULT_MOUNT=y
CONFIG_KSU_SUSFS_AUTO_ADD_SUS_BIND_MOUNT=y
CONFIG_KSU_SUSFS_AUTO_ADD_TRY_UMOUNT_FOR_BIND_MOUNT=y
```

**Evidence:** none of these symbols exists in the current BakaSU/susfs Kconfig, and neither the
kernel nor KernelSU references them. Kconfig silently drops them from `.config`; they have no
functional effect.

**Suggested action:** remove for clarity — **only with your approval** (hard rule 7: no defconfig
changes without asking).

**Verify command**

```bash
grep -n "KSU_SUSFS_TRY_UMOUNT\|AUTO_ADD_SUS_KSU_DEFAULT_MOUNT\|AUTO_ADD_SUS_BIND_MOUNT\|AUTO_ADD_TRY_UMOUNT_FOR_BIND_MOUNT" arch/arm64/configs/exynos9610-m21dd_defconfig
grep -n "KSU_SUSFS_TRY_UMOUNT\|AUTO_ADD_SUS_KSU_DEFAULT_MOUNT" .config
# second command should print nothing
```

---

## 8. Inline-hook script is not idempotent — WARNING

`Patches/susfs_inline_hook_patches.sh` (Jack `mainline`, last changed `466c4a9`) skips any target
file already containing `ksu_handle`:

```bash
if grep -q "ksu_handle" "$i"; then
    continue
fi
```

Every target file in this tree already contains `ksu_handle`, so **re-running the script would
silently do nothing**. It must never be used as an update mechanism on this tree; port later inline
hooks by hand (hard rule 3).

**Impact:** none as long as the script is not run. This is a process warning, not a code defect.

---

# Part B — Cosmetic / correct adaptations (do not "fix")

These look like differences from Jack's upstream but are correct for this tree.

## B1. `fs/notify/fdinfo.c` ignored-mask printing — COSMETIC

- This tree (`fs/notify/fdinfo.c:123,153,170,200,209`):
  ```c
  seq_printf(m, "... ignored_mask:%x ", ..., mask, mark->ignored_mask);
  ```
- Jack's 4.14 patch:
  ```c
  seq_printf(m, "... ignored_mask:0 ", ..., inotify_mark_user_mask(mark));
  ```
- `inotify_mark_user_mask()` exists **nowhere** in this tree or KernelSU, is not defined by any
  Jack hunk, and vanilla 4.14.113 uses `mask, mark->ignored_mask`. Applying Jack's text would not
  compile. Only cosmetics differ; the ino/dev spoofing is intact.

## B2. `include/linux/susfs_def.h:4` — ADAPTATION

```c
#include <linux/bitops.h>   /* project */
/* Jack: #include <linux/bits.h> */
```

`include/linux/bits.h` does not exist in 4.14. Required adaptation. If a future Jack patch rewrites
this include, adapt it again rather than copying verbatim.

## B3. `fs/susfs.c` two commented-out lines — COSMETIC

The project has 1560 lines vs 1558 upstream; the extra two are commented-out
`statfs_by_dentry(...)` calls; the live code calls `statfs_by_dentry_wrapper(...)`.

## B4. `fs/susfs.c:1552` stray trailing backslash — COSMETIC

```c
void susfs_init(void) {\
        SUSFS_LOGI("Initializing susfs_extra_works\n");
```

Present verbatim in Jack's upstream patch; joins the lines and compiles fine. Not a local edit.

## B5. `fs/namei.c` comments — COSMETIC

- `bool is_fuse = ...; // Move here` (local explanatory comment).
- One comment reads "from being created" where Jack has the "from from" typo.

---

# Part C — Candidate issues checked and cleared (not defects)

## C1. `ksu_handle_rename` reachability — CLEARED

No direct call site exists in `fs/`, `security/`, or `kernel/`, which initially looks like a missing
manual hook. It is in fact wired:

- `KernelSU/kernel/Kbuild:209-212` compiles `hook/lsm_hooks.o` for kernel version < 6.8.
- `lsm_hooks.c` registers `LSM_HOOK_INIT(inode_rename, ksu_inode_rename)`, which calls
  `ksu_handle_rename()` (`lsm_hooks.c:63-69, 108-110`).
- `ksu_lsm_hook_built_in_init()` is called from the `CONFIG_KSU_SUSFS` branch in
  `KernelSU/kernel/core/init.c:118-121`.
- `security_add_hooks()` exists in this tree at `security/security.c:162` (4.14 >= 4.11, so the
  name argument form is used).
- `ksu_handle_rename` is present in `System.map`.

**Conclusion:** rename tracking works on this kernel via the LSM hook.

## C2. `ksu_handle_setuid` reachability — CLEARED

- `kernel/sys.c:611` calls `ksu_handle_setresuid(ruid, euid, suid)`.
- `KernelSU/kernel/hook/setuid_hook.c:181-188` implements it and calls `ksu_handle_setuid()`.
- `CONFIG_KSU_MANUAL_HOOK_AUTO_SETUID_HOOK` is not set, so the real path is compiled.
- `syscall_event_bridge.o` is **not** compiled (tracepoint hook off), but that path is only needed
  for `CONFIG_KSU_TRACEPOINT_HOOK`.

## C3. `RKP_NS_PROT` branch — NOT APPLICABLE

`fs/namespace.c` has a separate `CONFIG_RKP_NS_PROT` path that calls `rkp_assign_mnt_flags()` and
does not carry the susfs unshared flag. `CONFIG_RKP_NS_PROT` is **not present** in `.config` or the
defconfig, so that branch is dead code here. If it were ever enabled, `118ac2b`'s replacement would
not cover it — re-audit then.

---

# Verification batch

Run from `/root/m21_susfs`:

```bash
# 1
grep -n "ksu_handle_sys_read" fs/read_write.c KernelSU/kernel/runtime/ksud_integration.c
# 2
grep -n "#include <linux/susfs" KernelSU/kernel/supercall/dispatch.c
grep -n "susfs_[a-z_]*(" KernelSU/kernel/supercall/dispatch.c
# 3
grep -rn "susfs_set_ksu_sid\|susfs_set_init_sid\|susfs_set_priv_app_sid" KernelSU/kernel fs/ include/
# 4
find . -path ./KernelSU -prune -o -path ./toolchains -prune -o \( -name '*.rej' -o -name '*.orig' \) -print | sort
# 5
git ls-tree HEAD KernelSU; git -C KernelSU rev-parse HEAD
# 6
git -C KernelSU remote get-url origin; grep -n -A2 "KernelSU" .gitmodules
# 7
grep -n "KSU_SUSFS_TRY_UMOUNT\|AUTO_ADD_SUS_KSU_DEFAULT_MOUNT\|AUTO_ADD_SUS_BIND_MOUNT\|AUTO_ADD_TRY_UMOUNT_FOR_BIND_MOUNT" arch/arm64/configs/exynos9610-m21dd_defconfig
```

No source file was modified to produce this document.
