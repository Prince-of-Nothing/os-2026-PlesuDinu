#!/usr/bin/env bash
set -u

repo="$HOME/Documents/GitHub/os-2026-PlesuDinu"
temp_dir=$(mktemp -d)
cd "$temp_dir" || exit 1
touch README

{
  printf '%s\n' '== Lab 4 Part 2: Bash commands =='
  printf '$ echo hello > f; cat < f\n'; echo hello > f; cat < f
  printf '$ ls | grep READ\n'; ls | grep READ
  printf '$ (echo a; echo b) | wc\n'; (echo a; echo b) | wc
  printf '$ echo one; echo two\n'; echo one; echo two
  printf '$ echo bg &\n'; echo bg &
  bg_pid=$!
  wait "$bg_pid"
  printf '$ ls *\n'; ls *
  printf '$ echo $HOME\n'; echo "$HOME"
  printf '$ echo "a b"\n'; echo "a b"
  printf '$ mkdir d; cd d; ls ..\n'; mkdir d; cd d; ls ..
  printf '%s\n' 'Up arrow, Tab, and Ctrl+R require an interactive terminal; see note in report.'
} > "$repo/resources/terminal-captures/lab4-bash.txt" 2>&1

{
  printf '%s\n' '== Lab 4 Part 3: Linux args =='
  cd "$repo/Lab4" || exit 1
  gcc -Wall -Wextra -o args args_linux.c
  printf '$ ./args *.c "x y"\n'
  ./args *.c "x y"
  printf '$ ./args $HOME\n'
  ./args "$HOME"
  printf '$ ./args '\''single quoted'\''\n'
  ./args 'single quoted'
  rm -f args
} >> "$repo/resources/terminal-captures/lab4-bash.txt" 2>&1
rm -rf "$temp_dir"