#!/usr/bin/env bash
set -u

repo="$HOME/Documents/GitHub/os-2026-PlesuDinu"
capture="$repo/resources/terminal-captures"

{
  printf '%s\n' '== Part 1: command lookup =='
  type cd
  type ls
  type echo
  command -v ls
  printf '%s\n' '== PATH directories =='
  printf '%s\n' "$PATH" | tr ':' '\n'
  printf '%s\n' '== missing command status =='
  nosuchprog 2>&1
  printf 'exit code: %s\n' "$?"
  printf '%s\n' '== ls modification-time option =='
  ls --help | grep -m1 'sort by time'
  printf '%s\n' '== Part 2: shell expansion =='
  cd "$HOME/os-lab3/play" || exit 1
  printf '$ echo *.c\n'; echo *.c
  printf '$ echo file?.txt\n'; echo file?.txt
  printf '$ echo [a-b]*\n'; echo [a-b]*
  printf '$ echo *.xyz\n'; echo *.xyz
  printf '$ ls alfa beta.txt\n'; ls alfa beta.txt 2>&1 || true
  printf '$ ls "alfa beta.txt"\n'; ls "alfa beta.txt"
  printf '$ echo '\''$HOME'\'' "$HOME" \\$HOME\n'; echo '$HOME' "$HOME" \$HOME
  printf '$ echo {1..5} ; echo $((7 * 6))\n'; echo {1..5} ; echo $((7 * 6))
  printf '$ echo "today is $(date +%%A), I am $(whoami)"\n'; echo "today is $(date +%A), I am $(whoami)"
  printf '$ touch log{1..3}.txt && ls log*\n'; touch log{1..3}.txt && ls log*
} > "$capture/lab3-parts1-2.txt" 2>&1

temp_dir=$(mktemp -d)
(
  cd "$temp_dir" || exit 1
  printf '%s\n' '== Part 3: redirection, chaining, jobs =='
  printf '$ ls /etc /nope > out.txt 2> err.txt\n'
  ls /etc /nope > out.txt 2> err.txt
  printf '$ wc -l out.txt; cat err.txt\n'
  wc -l out.txt
  cat err.txt
  printf '$ ls /etc /nope > all.txt 2>&1; tail -2 all.txt\n'
  ls /etc /nope > all.txt 2>&1
  tail -2 all.txt
  printf '$ ls /etc /nope 2>&1 > all2.txt\n'
  ls /etc /nope 2>&1 > all2.txt
  printf 'errors in all2.txt: '
  grep -c nope all2.txt || true
  printf '$ echo first > notes.md; echo second >> notes.md; cat notes.md\n'
  echo first > notes.md
  echo second >> notes.md
  cat notes.md
  printf '$ wc -l < out.txt\n'
  wc -l < out.txt
  printf '$ false || echo failed; true && echo succeeded; echo done\n'
  false || echo failed
  true && echo succeeded
  echo done
  printf '$ sleep 100 &\njobs\nkill %%1\njobs\n'
  sleep 100 &
  job_pid=$!
  jobs
  kill "$job_pid"
  wait "$job_pid" 2>/dev/null || true
  jobs
) > "$capture/lab3-part3.txt" 2>&1
rm -rf "$temp_dir"

{
  printf '%s\n' '== Part 4: oneliners.sh =='
  cd /tmp || exit 1
  bash "$repo/Lab3/oneliners.sh"
  printf '%s\n' '== Part 5: report.sh =='
  bash "$repo/Lab3/report.sh" /tmp/access.log
  bash "$repo/Lab3/report.sh" /tmp/no-such-log
  printf 'missing-file exit: %s\n' "$?"
} > "$capture/lab3-scripts.txt" 2>&1