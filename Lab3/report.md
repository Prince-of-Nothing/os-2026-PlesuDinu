# Laboratory Work 3: The Command Line

**Course:** Operating Systems, FCIM / FAF, UTM, 2026-2027  
**Student:** Pleșu Dinu, FAF-241  
**Checked by:** [Instructor]  
**Chișinău, 2026**

## Purpose

Practice Bash command lookup, shell expansion, quoting, redirection, pipelines, process control, and small scripts. Use filters to answer questions about a generated access log.

## Initial Setup

The laboratory uses an artificial web access log with 500 entries, generated in `~/os-lab3` and checked before running the one-liners.

```
mkdir -p ~/os-lab3 && cd ~/os-lab3
for i in $(seq 1 500); do
  echo "2026-10-05 10:$(printf %02d $((i % 60))) user$((i % 7)) $([ $((i % 5)) -eq 0 ] && echo FAIL || echo OK) /page$((i % 4))"
done > access.log
head -3 access.log; wc -l access.log
```

## Part 1: Move Fast, Find Help

Tab completes a unique path prefix, such as `/et` to `/etc`. If several entries match, pressing Tab twice displays the candidates. Ctrl+R starts reverse history search; typing part of a previous command finds it, and Enter runs the selected command.

`cd` is a Bash builtin because it must change the current shell process's working directory. `ls` is an external program found through `PATH`; `echo` is normally a Bash builtin, though external implementations also exist. `which ls` reports the executable found on `PATH`. `PATH` is a colon-separated list of directories, and `tr ':' '\n'` displays one directory per line. Bash returns status 127 when a command cannot be found. The `ls` option that sorts by modification time is `-t` (`-lt` combines this order with long format).

**Observed on this host:** `cd` and `echo` are Bash builtins; `ls` resolves to `/usr/bin/ls`. The inherited `PATH` contains 16 directory entries (some repeat). A missing command returned 127. `ls -t` sorts by modification time, newest first.

![Figure 1.1 – Part 1: command lookup, PATH, missing-command status, and the `ls` time option](resources/terminal-captures/real/lab3-part1-grouped-real.png)

## Part 2: What the Shell Does to Your Line

Run the commands in the assignment after creating the six files. The table records the expected output on Bash; the weekday and account name depend on the computer. Add your own prediction before running each command and note any differences.

| Command | Expected output | Explanation |
|---|---|---|
| `echo *.c` | `a.c b.c` | Bash expands the wildcard before starting `echo`. |
| `echo file?.txt` | `file1.txt file2.txt` | `?` matches exactly one character. |
| `echo [a-b]*` | `a.c alfa beta.txt b.c` | The bracket expression matches names beginning with `a` or `b`; the name containing a space remains one argument. |
| `echo *.xyz` | `*.xyz` | With default Bash settings, an unmatched glob remains literal. |
| `ls alfa beta.txt` | Error: neither separate path exists | The shell passes two arguments, `alfa` and `beta.txt`. |
| `ls "alfa beta.txt"` | Lists `alfa beta.txt` | Quoting preserves the embedded space as part of one argument. |
| `echo '$HOME' "$HOME" \$HOME` | `$HOME <home-directory> $HOME` | Single quotes and backslash suppress expansion; double quotes allow parameter expansion. |
| `echo {1..5} ; echo $((7 * 6))` | `1 2 3 4 5`, then `42` | Bash performs brace and arithmetic expansion before `echo`. |
| `echo "today is $(date +%A), I am $(whoami)"` | Current weekday and account name | Bash runs the command substitutions first. |
| `touch log{1..3}.txt && ls log*` | `log1.txt log2.txt log3.txt` | Brace expansion creates three names; `&&` runs `ls` only if `touch` succeeds. |

The shell, not `echo`, expands `*.c`. `ls alfa beta.txt` can be fixed with `ls 'alfa beta.txt'` or `ls alfa\ beta.txt`. Single quotes preserve enclosed characters literally. Double quotes preserve word boundaries but still allow parameter, command, and arithmetic expansion. `ls` may quote a filename in its display to make embedded whitespace unambiguous; those display quotes are not part of the filename.

![Figure 2.1 – Part 2: file list, globbing, quoting, spaces, and expansions](resources/terminal-captures/real/lab3-part2-grouped-real.png)

## Part 3: Redirection, Chaining, and Jobs

`ls /etc /nope > out.txt 2> err.txt` writes the `/etc` listing to `out.txt` and the missing-path diagnostic to `err.txt`. In `ls /etc /nope > all.txt 2>&1`, standard output is first redirected to `all.txt`, then standard error is made a copy of that destination, so both streams go into the file. In `ls /etc /nope 2>&1 > all.txt`, standard error first copies the original standard output (the terminal), then only standard output moves to the file; the error remains on the terminal.

`wc -l < access.log` reads standard input, so it prints only the count. `wc -l access.log` opens a named file and includes its name in the output. `;` runs the next command regardless of the previous status; `&&` runs it only after success; `||` runs it only after failure. A trailing `&` starts a background job; `jobs` lists it, and `kill %1` requests its termination.

![Figure 3.1 – Part 3: redirection, command chaining, and background jobs](resources/terminal-captures/real/lab3-part3-grouped-real.png)

## Part 4: One-Liners

The runnable answers are in [`oneliners.sh`](oneliners.sh). For the assignment's deterministic 500-line data set:

| Question | Result |
|---|---|
| Q1 failed requests | 100 |
| Q2 distinct pages | 4: `/page0`, `/page1`, `/page2`, `/page3` |
| Q3 requests per page | 125 each |
| Q4 users with the most failures | `user3` and `user5`, 15 failures each |
| Q5 user3 requests | 72 requests, 15 failed |
| Q6 last three failed requests | `10:10 user0`, `10:15 user5`, `10:20 user3` |
| Q7 login shells | Depends on local `/etc/passwd`; the script groups identical shell paths. |
| Q8 `ls` line counts | `ls -l` includes one additional `total` summary line. |

The bonus command selects failed requests whose minute ends in zero; the generated data contains 50 such requests.

![Figure 4.1 – Part 4: `oneliners.sh` results for Q1–Q8](resources/terminal-captures/real/lab3-part4-grouped-real.png)

## Part 5: First Script

[`report.sh`](report.sh) checks that its input file exists, reports total and failed requests, then loops through `user0` to `user6` and prints each user's failed-request count. The shebang `#!/usr/bin/env bash` asks the environment to locate Bash to interpret the script. Without execute permission, `./report.sh` fails with a permission error; after `chmod +x report.sh` it can be run directly. `./` names a path in the current directory because that directory is normally not included in `PATH`. Writing the diagnostic to file descriptor 2 keeps it on standard error; `exit 1` communicates failure to the calling shell.

For a missing file, expected behavior is `no such file: nope.log` on standard error followed by exit status 1. The cron bonus was not run.

![Figure 5.1 – Part 5: `report.sh` source, normal output, and missing-file handling](resources/terminal-captures/real/lab3-part5-grouped-real.png)

## Conclusion

The shell parses and transforms command lines before programs receive their arguments. Globbing, quoting, variable expansion, command substitution, redirection, pipelines, and job control are shell responsibilities, while utilities such as `grep`, `cut`, `sort`, and `wc` perform focused operations that can be combined. The scripts make those operations repeatable and checkable.