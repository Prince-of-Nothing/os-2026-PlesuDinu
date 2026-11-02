# Laboratory Work 4: The xv6 Shell from the Outside

**University:** Technical University of Moldova  
**Faculty / Department:** FCIM / FAF  
**Course:** Operating Systems  
**Student:** Pleșu Dinu, FAF-241  
**Checked by:** [Instructor]  
**Chișinău, 2026**

## Purpose

Compare Bash with xv6's small shell, update `sleep` for the current xv6 API, observe how a shell passes arguments to a program, and inspect `user/sh.c`.

## Part 1: Fix `sleep` for Current xv6

The current `user/user.h` declares `int pause(int);`, so this revision uses `pause()` rather than `sleep()`. The updated [`sleep.c`](sleep.c) checks its argument count, reports usage to standard error, waits the requested number of ticks, and exits successfully. The xv6 Makefile registers `$U/_sleep` in `UPROGS`.

Build and test in xv6:

```text
$ sleep 20
$ sleep
usage: sleep <ticks>
```

![Figure 1.1 – `pause` declaration in `user.h` and the updated `sleep.c`](resources/terminal-captures/real/lab4-fig1-sleep-source-real.png)

![Figure 1.2 – `sleep` run with and without an argument in xv6](resources/terminal-captures/real/lab4-fig2-sleep-run-real.png)

## Part 2: Bash versus the xv6 Shell

The table summarizes expected behavior. Capture local listing output in both environments. In xv6, user programs are stored at paths such as `/ls` and `/cat`.

| Command | Bash on Linux | xv6 shell | Reason |
|---|---|---|---|
| `echo hello > f ; cat < f` | Writes `hello` to `f`, then prints `hello`. | Same. | Both support redirection and command lists. |
| `ls \| grep READ` | Prints `README` in the prepared test directory. | Prints `README` if it exists in the xv6 root filesystem. | Both implement pipes. |
| `(echo a; echo b) \| wc` | Counts the two lines. | Also sends both lines through the pipe to `wc`. | xv6 parses parenthesized blocks, lists, and pipes. |
| `echo one ; echo two` | Prints `one` then `two`. | Same. | `;` creates a list command. |
| `echo bg &` | Prints asynchronously; Bash tracks the job and PID. | Starts in the background; no Bash-style `jobs` interface. | xv6 supports `&` but not full job control. |
| `ls *` | Expands `*` to matching names and lists them. | `*` is passed literally; `ls` reports it cannot open that path. | Bash expands globs; xv6 does not. |
| `echo $HOME` | Prints the value of `HOME`. | Prints literal `$HOME`. | Bash expands variables; xv6 does not. |
| `echo "a b"` | Prints `a b` as one argument, without quotes. | Quote characters are literal and the space splits words. | Bash implements quotes; xv6 tokenizes whitespace and operators. |
| `mkdir d ; cd d ; ls ..` | Creates `d`, changes into it, then lists its parent. | In this semicolon list, `cd` is treated as an external command and fails; `ls ..` then runs from the unchanged directory. | xv6's `main()` handles `cd` only when it is the whole input line. Enter `cd d` at its own prompt, then `ls ..` to see the relative `ls` failure; `/ls ..` works. |
| Up arrow, Tab, Ctrl+R | History, completion, and reverse history search. | No matching history or completion features. | These are interactive Bash/readline features. |

Both shells support execution, basic redirection, pipes, command sequences, and background commands. Bash additionally provides variable and pathname expansion, full quote handling, history, completion, and job control. xv6's special `cd` handling is in the shell's input loop, so it works when typed as its own command. After changing into `d`, `/ls ..` works because the executable is addressed from the filesystem root. The feature I would miss most is history with Tab completion, because retyping long commands and absolute paths such as `/ls` is slow; the easiest to add is wildcard expansion, because the shell could reuse the directory-reading code from `ls` and substitute matching names before calling `exec`.

![Figure 2.1 – The command comparison in Bash](resources/terminal-captures/real/lab4-fig3-bash-real.png)

![Figure 2.2 – The same commands in xv6, the `ls` failure after `cd d`, and the `/ls` alternative](resources/terminal-captures/real/lab4-fig4-xv6-real.png)

## Part 3: Who Expands `*`? The `argv` Program

The xv6 program is [`args.c`](args.c); the Linux version is [`args_linux.c`](args_linux.c). Both print `argc` and every `argv` entry. The xv6 Makefile registers `$U/_args`.

In Bash, the `Lab4` folder contains three matching source files. The captured output is:

```text
argc = 5
argv[0] = [./args]
argv[1] = [args.c]
argv[2] = [args_linux.c]
argv[3] = [sleep.c]
argv[4] = [x y]
```

In general, if there are N matching source files, Bash reports `argc = N+2`: the executable name, N filenames, and the single argument `x y`. In xv6, `*.c` is not expanded and quotes are not syntax. The command passes four arguments: `args`, `*.c`, `"x`, and `y"`, so `argc = 4`. Expected xv6 output is:

```text
argc = 4
argv[0] = [args]
argv[1] = [*.c]
argv[2] = ["x]
argv[3] = [y"]
```

The shell performs wildcard expansion and removes syntactic quotes before a program starts. The kernel supplies the argument vector but does not expand `*` or remove quotes. In `args one              two         three`, runs of unquoted whitespace are separators, so extra spaces do not become part of an argument. For `args 'single quoted'`, Bash passes `single quoted` as one argument with no quotes; xv6 treats quotes as ordinary text and splits at the space.

![Figure 3.1 – `args.c` and its `UPROGS` line](resources/terminal-captures/real/lab4-fig5-args-source-real.png)

![Figure 3.2 – `args` output in xv6](resources/terminal-captures/real/lab4-fig6-args-xv6-real.png)

![Figure 3.3 – `args` output in Linux (Bash)](resources/terminal-captures/real/lab4-fig7-args-linux-real.png)

## Part 4: Read the Shell

The five command kinds are `EXEC` (ordinary command), `REDIR` (`<`, `>`, `>>`), `PIPE` (`|`), `LIST` (`;`), and `BACK` (`&`). Parenthesized blocks group existing command kinds rather than defining a sixth executor type.

`cd` is handled in `main()` in `user/sh.c`; it calls `chdir()` in the shell process itself. It cannot run as an ordinary child because changing a child's working directory would leave the parent shell in the old directory. The `runcmd()` switch executes the command structures, and `parseblock()` handles parentheses.

There is no code in `sh.c` implementing pathname (`*`) or variable (`$HOME`) expansion. That explains why xv6 passes those characters to programs literally, unlike Bash.

![Figure 4.1 – Command-kind definitions, `runcmd()` cases, `cd` handling, and the absence of expansion code in `sh.c`](resources/terminal-captures/real/lab4-fig8-sh-source-real.png)

## Conclusion

The xv6 shell demonstrates the core structure of a shell: parse a command, create processes, connect file descriptors, and execute programs. Comparing it with Bash shows that wildcard expansion, variables, quoting rules, history, completion, and job control are additional shell features rather than behavior supplied automatically by the kernel.