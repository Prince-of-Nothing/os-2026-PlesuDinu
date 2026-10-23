# Laboratory Work 2 — Meet the OS You Will Build
### Course: Operating Systems
### Author: Pleșu Dinu FAF-241
## Part 1: Build and boot

The xv6 tree is in `~/xv6-riscv`. I built and launched it with `make qemu`; QEMU prints the xv6 boot message and starts the shell. I exited QEMU with Ctrl-A followed by X.

## Part 2: Use xv6

1. Three programs shipped with xv6 are `echo`, `cat`, and `ls`.
2. A pipe requires process creation so both commands can run, and inter-process communication through a kernel-managed pipe buffer and file descriptors.
3. The xv6 shell supports basic command execution, pipes, and redirection, while Linux Bash adds richer scripting, expansion, history, completion, and job control.

## Part 3: Read the source

`user/cat.c` uses `open()` to open a named file, `read()` to obtain bytes from a file descriptor (or standard input when no filename is supplied), `write()` to send bytes to standard output, `close()` to release a file descriptor, and `exit()` to finish. In this checkout, `sys_read` is implemented in `kernel/sysfile.c` at line 69. `user/user.h` declares the user-visible system-call interface.

`kernel/` contains privileged operating-system implementation code. `user/` contains ordinary programs that request kernel services through system calls.

## Part 4: First xv6 program

The current xv6 checkout declares `pause(int)` instead of `sleep(int)`. The working program is [sleep.c](sleep.c), and the Makefile entry is recorded in [UPROGS.txt](UPROGS.txt). I built and booted xv6 with `make qemu CPUS=1`, then tested:

```text
$ sleep 10
$ sleep
usage: sleep <ticks>
```

The valid call waited and returned to the shell; the invalid call printed the expected usage message.

## Conclusion

Building xv6 made the relationship between user programs and kernel services concrete. A user program invokes system calls, and the kernel performs the privileged work. The `sleep` utility is a small example of that boundary.
