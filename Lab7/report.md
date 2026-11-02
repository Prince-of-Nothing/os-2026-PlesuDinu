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

![Figure 1.1 – `run`: parent PID, child PID and parent PID, `ls -l` output, and the exit status](captures/png/lab7-fig1-run-real.png)

This screenshot captures the process-creation task: the parent prints its PID, forks, and the child executes `ls -l` in place of itself. The displayed PID values and exit status show the relationship between parent and child and confirm that the child can run a different program while the parent continues to wait for completion.

## Part 2: A zombie, on purpose

[`zombie.c`](zombie.c) lets the child finish and delays the parent's `waitpid()` by 20 seconds. During the delay, `ps -o pid,ppid,stat,cmd` should show the child with `Z` in the state column and `[ls] <defunct>`. The parent reaps it when `waitpid()` runs; after that, the child entry disappears.

```sh
gcc -Wall -Wextra -o zombie zombie.c
./zombie >/dev/null &
sleep 2
ps -o pid,ppid,stat,cmd
```

![Figure 2.1 – `zombie`: the child is `Z` (defunct) while the parent sleeps](captures/png/lab7-fig2-zombie-real.png)

This figure shows the intentional zombie state: the child exits, but the parent delays `waitpid()`, so the process remains in `Z` state until reaped. The output makes visible the important OS rule that a terminated child can still occupy a process table entry until the parent calls `waitpid()`.

## Part 3: Redirection

[`redirect.c`](redirect.c) closes descriptor 1 in the child before opening `out.txt`. `open()` returns descriptor 1 because it allocates the lowest available descriptor. `ls` still writes to standard output, but that descriptor now refers to `out.txt`, so the listing is not printed on the terminal. To redirect standard error, close descriptor 2 before `open()`.

![Figure 3.1 – `redirect`: `open` returns descriptor 1 and the listing goes to `out.txt`](captures/png/lab7-fig3-redirect-real.png)

This result is the redirection experiment in action: the child closes standard output, opens `out.txt`, and receives descriptor 1 because the lowest available file descriptor is reused. The listing therefore goes to the file, not to the terminal, which proves that file descriptors control where process output is sent.

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

![Figure 4.1 – `pipeline` and `pipeline3` match the shell pipelines (227 and 350)](captures/png/lab7-fig4-pipeline-real.png)

This pipeline capture validates both the single-stage and the three-stage pipe examples: the output counts match the corresponding shell commands when run on the same system. The exercise demonstrates that pipes connect the standard output of one process to the standard input of another, and that proper shutdown of unused ends is essential for correct EOF behavior.

## Conclusion

`fork()` creates a child, `exec()` replaces its program, and `waitpid()` collects its exit status. File descriptors make redirection and pipes composable: the programs keep using standard input/output while the process setup changes what those descriptors refer to. Closing every unused pipe end is necessary for EOF and termination.