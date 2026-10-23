# Laboratory Work 2 — Meet the OS You Will Build
### Course: Operating Systems
### Author: Pleșu Dinu FAF-241
## Part 1. Build it and boot it
```bash
make qemu
```
## Part 2. Use xv6 as the Unix it is

1. Three programs xv6 ships with: `echo`, `cat`, `console`.

2. For a pipe to work, two OS features must exist: (a) process creation, so the kernel can run the two ends of the pipe as separate processes (via `fork`); and (b) an inter-process communication mechanism, where the kernel keeps a shared buffer accessible through file descriptors so one process's `write` can be read by the other process via `read`.

3. The xv6 shell implements only the bare minimum — parsing, `fork`/`exec`, pipes, and I/O redirection — while the Linux shell (bash) builds on the same core ideas but adds job control, scripting, variables, and many built-in commands.

## Part 3 — Memory

While analysing cat.c, I have noticed that the c program makes numerous system calls, including read() - gets user input, exit() - ends the program with a status, write() - writes to the output stream, open() - opens a file and close() - closes a file. The sys_read returns a uint64 and is defined in kernel/sysfile.c, on line 68. The files in the kernel define the instructions that the kernel is able to do, and how it does them, while the files defined in user allow the user to interact with the kernel's implemented behavior using programs.

### Observations

The root filesystem `/` was mounted on `/dev/sda2`. One useful device example is the real-time clock device, such as `/dev/rtc` or `/dev/rtc0`, which gives access to the system hardware clock. The idea of "everything is a file" means that many devices and system resources are exposed through file-like interfaces, so programs can interact with them using similar operations to normal files. This part showed the difference between filesystems, disks, partitions, mount points and device interfaces.

## Conclusion

This lab reinforced how an operating system manages files, processes, memory, and devices/I/O. Using commands such as `ls`, `ps`, `free`, `df`, and `lsblk` allowed hands-on verification of concepts like mount points, device files in `/dev`, and resource reporting. The exercises clarified how these components interact and prepared me to apply system diagnostics in future labs.