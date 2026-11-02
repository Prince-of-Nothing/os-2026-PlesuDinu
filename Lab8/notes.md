# Laboratory Work 8 — The Same Calls, Inside Your Own OS

**Course:** Operating Systems, FCIM / FAF, UTM  
**Student:** Pleșu Dinu, FAF-241

## Purpose

Repeat the Lab 7 process and pipe experiments inside xv6, using its smaller system-call interface.

## Part 1: `run`

[`run.c`](run.c) uses `getpid()`, `fork()`, `exec()`, `wait()`, and `exit()`. The Linux Lab 7 version uses `getpid()`, `fork()`, `execlp()`, and `waitpid()`. The core operations match: create a child, replace its program, then wait for it. The API details differ because xv6 has its own small user library and no glibc/PATH search.

The text `hello from the child` is printed by the `echo` program after `exec()` replaces the child. In the missing-program experiment, xv6's sample child explicitly calls `exit(1)` after failed `exec`, while the Linux program calls `exit(127)`; the parent reports the child's chosen status.

![Figure 1.1 – xv6: run forks a child that execs echo and the parent reports its status](resources/terminal-captures/real/lab8-fig1-run-real.png)

## Part 2: `pingpong`

[`pingpong.c`](pingpong.c) creates two pipes because each pipe carries bytes in one direction: one parent-to-child and one child-to-parent. The parent blocks in `read()` until the child writes a byte to the response pipe; `wait()` then ensures the child has terminated before the parent exits. The child prints `received ping` before returning the byte, so it appears before `received pong`.

Build and test in `~/xv6-riscv` after adding `$U/_run\` and `$U/_pingpong\` to `UPROGS`:

```text
$ run
parent: my pid is 3
child: my pid is 4
hello from the child
parent: child 4 ended with status 0
$ pingpong
10: received ping
9: received pong
```

![Figure 2.1 – xv6: pingpong over two pipes (ping is received before pong)](resources/terminal-captures/real/lab8-fig2-pingpong-real.png)

PIDs vary between runs. The Makefile entry is included in [UPROGS.txt](UPROGS.txt).

## Conclusion

The same process and pipe concepts work in xv6 as on Linux, but xv6 exposes a smaller system-call interface. `fork()` and `exec()` separate process creation from program replacement; pipes and disciplined descriptor closing provide one-way communication, and two pipes enable a request/reply exchange.