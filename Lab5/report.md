# Laboratory Work 5 — The File System with Your Own Hands

**Course:** Operating Systems, FCIM / FAF, UTM, 2026-2027  
**Student:** Pleșu Dinu, FAF-241  
**Environment:** Linux, non-root user

## Purpose

Inspect filesystem object types, inodes, hard and symbolic links, permissions, directory traversal rules, storage usage, mounted filesystems, and `/proc`.

## Part 1: Tree and file types

Use `ls -ld /etc /etc/passwd /bin /dev/null /tmp`, `file`, `ls -l /dev`, and `du -sh` to record the output for this machine. The first character of `ls -l` identifies object type: `d` directory, `-` regular file, `l` symbolic link, `c` character device, or `b` block device. `/bin` may be a symbolic link (commonly to `/usr/bin`) or a directory depending on the distribution. Choose a character and block device from the actual `/dev` listing; device availability differs by VM.

On this host, `/bin` is a symbolic link to `/usr/bin`. The `ls -ld` output shows `/etc` and `/tmp` are directories, `/etc/passwd` is a regular file, and `/dev/null` is a character device. `/dev/null` is the character-device example; `/dev/nvme0n1` is the block-device example. `du -sh` reported 45 MiB for `/var/log` and 17 GiB for `/usr`, so `/usr` is larger by roughly 16.96 GiB.

![Figure 5.1 – File types, devices, and directory sizes](captures/png/lab5-fig1-types-real.png)

This figure shows the first filesystem inspection step: the machine was queried with `ls -ld`, `file`, and `du` to classify directories, regular files, symlinks, and device files. The observed output confirms that object type is visible from metadata and that the same root filesystem contains both ordinary files and kernel-backed device nodes.

## Part 2: Inodes and links

`stat notes.txt` shows the inode number and link count. `ls -li` displays the inode beside each filename. A hard link is another directory entry for the same inode, so removing `notes.txt` removes that name but `hard.txt` still refers to the data. `rm` removes a name; storage is reclaimed only when the final hard link is removed and no process still has the file open.

A symbolic link stores a pathname to its target, not the target data. After deleting `hard.txt`, `soft.txt` remains as a directory entry but points to a missing target; `cat soft.txt` therefore fails. The symlink's size is the byte length of the stored target pathname (`hard.txt` is 8 bytes). On this run, `one.txt` had a logical size of 2 bytes and used 4 KiB; the sparse 1 GiB `big.img` used 0 allocated bytes.

A new directory normally has two links: its own name in its parent and `.` inside itself. Each immediate subdirectory adds a `..` entry pointing to the parent, so two children raise the parent's link count to four.

`ls -l` reports logical file length, while `du` reports allocated storage blocks. A tiny file uses at least one filesystem block (commonly 4 KiB); a sparse 1 GiB file created by `truncate` can have almost no blocks allocated until data is written.

![Figure 5.2 – Inode, hard-link, symbolic-link, directory-link, and sparse-file observations](captures/png/lab5-fig2-links-real.png)

This output captures the inode-link experiments: the same file was referenced through multiple names, a symlink was created to another path, and a sparse file was created with a large logical size but almost no allocated blocks. The task makes the difference between a pathname, an inode, and stored data concrete.

## Part 3: Permissions

| Mode | Symbolic form | Typical use |
|---|---|---|
| `600` | `rw-------` | Private configuration or secret file |
| `644` | `rw-r--r--` | Publicly readable text or source file |
| `755` | `rwxr-xr-x` | Executable program or traversable public directory |
| `700` | `rwx------` | Private directory or owner-only executable |

Ownership identifies which permission class applies; it does not override removed permission bits. With mode `000`, even the owner has no read bit, so an ordinary `cat` is denied.

Record the actual `umask` value. New regular-file permissions are based on `666` minus masked bits; new directories begin from `777` minus masked bits. Directory read permission allows listing names; execute permission allows traversal and lookup by name. A setuid bit on `/usr/bin/passwd` lets the program run with its owner's effective identity to update protected password data. The sticky bit on `/tmp` allows shared writes while restricting deletion/renaming of entries to the file owner, directory owner, or root.

The observed umask was `0022`. It produced `-rw-r--r--` for `new.txt` and `drwxr-xr-x` for `newdir`. For a directory with `u=r,go=`, `ls box` could list `f`, but opening `box/f` failed because there was no execute/search permission on `box`. With `u=x,go=`, listing names failed but reading the known path `box/f` succeeded. `/usr/bin/passwd` has setuid (`s`) and `/tmp` has the sticky (`t`) bit. Reading `/etc/shadow` was denied for the regular user.

![Figure 5.3 – File and directory permission tests, umask, and special bits](captures/png/lab5-fig3-permissions-real.png)

This figure records the permission checks and security bits for the filesystem: the default umask was observed, directory traversal rules were tested, and the setuid/sticky bits were identified on the actual system files. It demonstrates that access depends on permission bits, owner classes, and the directory traversal rule, not just on whether a file exists.

## Part 4: Disks and kernel data as files

`lsblk` showed `/dev/nvme0n1p4` mounted at `/` with Btrfs. `df -h /` reported 651 GiB total, 110 GiB used, 540 GiB available (17%). `/proc/cpuinfo` reported 8 processors and `/proc/meminfo` reported 16,055,104 KiB total RAM. `/proc/self/status` showed `Name: head` because `head` was the process reading that virtual file. `/proc/self/fd` showed descriptors 0, 1, and 2 connected to the terminal/capture output plus the temporary descriptor used to list the directory.

The device tree relevant to `/` is `nvme0n1` → `nvme0n1p4` → `/` (Btrfs); this is a partition of a larger 1.8 TiB NVMe drive, not the whole drive. The complete `lsblk` capture is included below.

![Figure 5.4 – Disk layout and root filesystem usage](captures/png/lab5-fig4-disks-real.png)

This figure shows the system storage view: the root filesystem, its mount point, and the available capacity were inspected with `lsblk` and `df`. The task confirms that storage is visible through a hierarchy of device and mount metadata, rather than as a single monolithic disk image.

![Figure 5.5 – CPU, memory, and `/proc` observations](captures/png/lab5-fig5-proc-real.png)

This final figure captures the kernel-backed view of the current system: `/proc/cpuinfo`, `/proc/meminfo`, and `/proc/self/status` expose live process and machine data as ordinary files. Together they show that the kernel provides a readable synthetic filesystem for runtime process and hardware information.

## Conclusion

The filesystem maps names to inodes and inodes to data and metadata. Hard links share an inode, symbolic links store a path, and permission bits govern reads, writes, and traversal. `df`, `du`, `/proc`, and device nodes expose different views of storage and running-system state.
