# Laboratory Work 7 — Three Small Programs: Processes, Redirection, a Pipe

**Course:** Operating Systems, FCIM / FAF, UTM  
**Student:** Pleșu Dinu, FAF-241

## Purpose

Write three small C programs that show how Linux creates and replaces processes, redirects file descriptors, and connects commands with a pipe.

## Part 1: `fork`, `exec`, and `wait`

[`run.c`](run.c) prints the parent's PID, forks, and has the child execute `ls -l`. `execlp()` replaces the child process image, so the error message after it is reached only if execution fails. The child prints `getppid()`, which is the PID of its parent process. The parent observes status 0 when `ls` exits normally and 127 when `execlp()` fails and the child explicitly calls `exit(127)`.

Run:

```sh
gcc -Wall -Wextra -o run run.c
./run
```

The PID values and directory listing vary. When testing a missing command, replace the `execlp("ls", ...)` line with `execlp("nosuchprog", "nosuchprog", (char *)NULL)`.

![Figure 1.1 – `run`: parent PID, child PID and parent PID, `ls -l` output, and the exit status](resources/terminal-captures/real/lab7-fig1-run-real.png)

## Part 2: A zombie, on purpose

[`zombie.c`](zombie.c) lets the child finish and delays the parent's `waitpid()` by 20 seconds. During the delay, `ps -o pid,ppid,stat,cmd` should show the child with `Z` in the state column and `[ls] <defunct>`. The parent reaps it when `waitpid()` runs; after that, the child entry disappears.

```sh
gcc -Wall -Wextra -o zombie zombie.c
./zombie >/dev/null &
sleep 2
ps -o pid,ppid,stat,cmd
```

![Figure 2.1 – `zombie`: the child is `Z` (defunct) while the parent sleeps](resources/terminal-captures/real/lab7-fig2-zombie-real.png)

## Part 3: Redirection

[`redirect.c`](redirect.c) closes descriptor 1 in the child before opening `out.txt`. `open()` returns descriptor 1 because it allocates the lowest available descriptor. `ls` still writes to standard output, but that descriptor now refers to `out.txt`, so the listing is not printed on the terminal. To redirect standard error, close descriptor 2 before `open()`.

![Figure 3.1 – `redirect`: `open` returns descriptor 1 and the listing goes to `out.txt`](resources/terminal-captures/real/lab7-fig3-redirect-real.png)

## Part 4: A pipe

[`pipeline.c`](pipeline.c) connects `ls /etc` to `wc -l`; its output should equal the shell pipeline `ls /etc | wc -l` when run against the same filesystem. The parent closes both pipe ends after forking. If it mistakenly retains the write end, `wc` never receives EOF. In that broken version `wc` waits for more input, while `ls` can exit.

[`pipeline3.c`](pipeline3.c) is the optional three-stage pipeline for `ls /usr/bin | grep x | wc -l`.

Compile and compare:

```sh
gcc -Wall -Wextra -o pipeline pipeline.c
./pipeline
ls /etc | wc -l
gcc -Wall -Wextra -o pipeline3 pipeline3.c
./pipeline3
ls /usr/bin | grep x | wc -l
```

![Figure 4.1 – `pipeline` and `pipeline3` match the shell pipelines (227 and 350)](resources/terminal-captures/real/lab7-fig4-pipeline-real.png)

## Conclusion

`fork()` creates a child, `exec()` replaces its program, and `waitpid()` collects its exit status. File descriptors make redirection and pipes composable: the programs keep using standard input/output while the process setup changes what those descriptors refer to. Closing every unused pipe end is necessary for EOF and termination.