# Repository Status — os-2026-PlesuDinu

Student: Pleșu Dinu, FAF-241. Course: Operating Systems, UTM, 2026-2027.
Last updated: 27.10.2026.

## What is done

Every lab folder now contains its report (docx built from the official UTM
template) and the code for that lab. No template placeholders remain in any
report; every figure in the reports is a real capture from my own machine
(Linux VM) or from a real xv6/QEMU session.

| Lab | Topic | Report | Code | Notes |
|-----|-------|--------|------|-------|
| Lab1 | The OS as a Resource Manager | Lab1_PlesuDinu_FAF-241.docx (12 figures) | report.md | Outputs recorded on the VirtualBox Ubuntu VM |
| Lab2 | Shell basics | Lab2_PlesuDinu_FAF-241.docx | sleep.c etc. | Verified: sleep.c uses pause(), compiles on current xv6 |
| Lab3 | Shell, pipes, text filters | Lab3_PlesuDinu_FAF-241.docx (28 figures) | oneliners.sh, report.sh | bash oneliners.sh runs; report.sh exits 1 for a missing log |
| Lab4 | Arguments in C (xv6 + Linux) | Lab4_PlesuDinu_FAF-241.docx (9 figures) | args.c, args_linux.c | |
| Lab5 (+6) | File system fundamentals | Lab5_PlesuDinu_FAF-241.docx (11 figures) | exercises.sh | Covers Lab 5 |
| Lab6 | Inside the xv6 File System | Lab6_PlesuDinu_FAF-241.docx (8 figures) | mystat.c, find.c, Makefile (UPROGS: $U/_mystat, $U/_find) | Built and booted in QEMU on 26-27.10: mystat, hard-link counts, DIRSIZ truncation and find all captured live |
| Lab7 | Three small Linux programs | Lab7_PlesuDinu_FAF-241.docx (5 figures) | run.c, redirect.c, pipeline.c, zombie.c | |
| Lab8 | Same calls in xv6 | Lab8_PlesuDinu_FAF-241.docx (3 figures) | pingpong.c, run.c | |

Verification performed:

- xv6 tree (`~/xv6-riscv`, same Makefile as Lab6/Makefile) builds clean:
  `make CPUS=1` exit 0, `make fs.img` prints
  `nmeta 47 (boot, super, log blocks 31, inode blocks 13, bitmap blocks 1) blocks 1953 total 2000`.
- Lab 6 was run live in QEMU (sessions saved in Lab6/captures/): ls with
  name/type/inode/size, `mystat README . console`, hard links (`ln`/`rm`
  changing only the link count), `averyveryverylongname` truncated to
  DIRSIZ = 14, and `find . r2` / `find a b` on a fresh disk.
- Lab 3 scripts re-run in a real pty; Part 2 figures re-captured after fixing
  a wrong-directory bug.
- Placeholder scan of all docx: 0 hits for every lab.

## What was changed in this round

1. Lab1 report docx created from report.md (real VM outputs turned into
   captioned figures).
2. Lab6 report docx created: dedicated Lab 6 report (the Lab5 docx keeps its
   "No. 5 and 6" section; the assignment allows combining, this makes each
   folder self-contained).
3. Lab3 report re-synced into Lab3/ (TOC fixed), oneliner.sh renamed to
   oneliners.sh.
4. Removed other students' reports that were stored in resources/
   (Gabi Balan L3/L4 pdfs, Serghei Barladean Lab3 docx) — they are not my
   work and must not be submitted from this repository.
5. Removed stray files: "Lab3/pasted file.txt", stale Lab6/SOURCE_STATUS.md
   (it wrongly claimed the Lab 6 assignment sheet was a Lab 7 sheet; the
   sheet was verified genuine).
6. Commit history: one commit per lab added on top of the existing history,
   dated when the work was actually done. Older commits were not rewritten
   and no commit dates were set backwards — the instructor flagged rewritten
   history with backdated dates as a problem, so the plan is to never do it.
7. Table of contents in all 8 reports converted from manually typed text to
   a real Word TOC field (TOC \o "1-2" \h \z \u) with bookmarks on every
   heading and w:updateFields, so Word/LibreOffice rebuild the indexation
   with real page numbers and hyperlinks on open (or via F9 / Update Table).
   The scripts used are fix_toc.py and fix_toc_lab5.py in the repo root.

## What still needs to be done

- Push Temp-2 to origin and merge it into main so the reports are visible on
  the default branch (main currently only has the older history).
- Final read-through of the Lab1/Lab6 docx by the student before submission.
- Open each report once in Word and press F9 (Update Table) if the page
  numbers in the TOC are not refreshed automatically on your Word version.
- Lab5_6/ folder duplicates Lab5+Lab6 material (find.c, mystat.c, report.md);
  it can be removed once the student confirms nothing extra is needed there.

## Rules followed for every report

- Title page filled per the UTM template (student, group, lab number, topic,
  "Checked by: Reitman Patricia, university assistant").
- Purpose section, per-part work, answers to every Observe box, real command
  outputs/figures with `Figure X.Y` captions, own conclusion.
- All code from this repository was run by me; figures were captured from my
  own sessions. No content was copied from classmates.
