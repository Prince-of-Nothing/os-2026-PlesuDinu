# Laboratory Work 5 — The File System with Your Own Hands

**Course:** Operating Systems, FCIM / FAF, UTM, 2026-2027  
**Student:** Pleșu Dinu, FAF-241  
**Environment:** Linux, non-root user

## Purpose

Inspect filesystem object types, inodes, hard and symbolic links, permissions, directory traversal rules, storage usage, mounted filesystems, and `/proc`.

## Part 1: Tree and file types

Use `ls -ld /etc /etc/passwd /bin /dev/null /tmp`, `file`, `ls -l /dev`, and `du -sh` to record the output for this machine. The first character of `ls -l` identifies object type: `d` directory, `-` regular file, `l` symbolic link, `c` character device, or `b` block device. `/bin` may be a symbolic link (commonly to `/usr/bin`) or a directory depending on the distribution. Choose a character and block device from the actual `/dev` listing; device availability differs by VM.

On this host, `/bin` is a symbolic link to `/usr/bin`. The `ls -ld` output shows `/etc` and `/tmp` are directories, `/etc/passwd` is a regular file, and `/dev/null` is a character device. `/dev/null` is the character-device example; `/dev/nvme0n1` is the block-device example. `du -sh` reported 45 MiB for `/var/log` and 17 GiB for `/usr`, so `/usr` is larger by roughly 16.96 GiB.

![Figure 5.1 – File types, devices, and directory sizes](resources/terminal-captures/real/lab5-fig1-types-real.png)

## Part 2: Inodes and links

`stat notes.txt` shows the inode number and link count. `ls -li` displays the inode beside each filename. A hard link is another directory entry for the same inode, so removing `notes.txt` removes that name but `hard.txt` still refers to the data. `rm` removes a name; storage is reclaimed only when the final hard link is removed and no process still has the file open.

A symbolic link stores a pathname to its target, not the target data. After deleting `hard.txt`, `soft.txt` remains as a directory entry but points to a missing target; `cat soft.txt` therefore fails. The symlink's size is the byte length of the stored target pathname (`hard.txt` is 8 bytes). On this run, `one.txt` had a logical size of 2 bytes and used 4 KiB; the sparse 1 GiB `big.img` used 0 allocated bytes.

A new directory normally has two links: its own name in its parent and `.` inside itself. Each immediate subdirectory adds a `..` entry pointing to the parent, so two children raise the parent's link count to four.

`ls -l` reports logical file length, while `du` reports allocated storage blocks. A tiny file uses at least one filesystem block (commonly 4 KiB); a sparse 1 GiB file created by `truncate` can have almost no blocks allocated until data is written.

![Figure 5.2 – Inode, hard-link, symbolic-link, directory-link, and sparse-file observations](resources/terminal-captures/real/lab5-fig2-links-real.png)

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

![Figure 5.3 – File and directory permission tests, umask, and special bits](resources/terminal-captures/real/lab5-fig3-permissions-real.png)

## Part 4: Disks and kernel data as files

`lsblk` showed `/dev/nvme0n1p4` mounted at `/` with Btrfs. `df -h /` reported 651 GiB total, 110 GiB used, 540 GiB available (17%). `/proc/cpuinfo` reported 8 processors and `/proc/meminfo` reported 16,055,104 KiB total RAM. `/proc/self/status` showed `Name: head` because `head` was the process reading that virtual file. `/proc/self/fd` showed descriptors 0, 1, and 2 connected to the terminal/capture output plus the temporary descriptor used to list the directory.

The device tree relevant to `/` is `nvme0n1` → `nvme0n1p4` → `/` (Btrfs); this is a partition of a larger 1.8 TiB NVMe drive, not the whole drive. The complete `lsblk` capture is included below.

![Figure 5.4 – Disk layout and root filesystem usage](resources/terminal-captures/real/lab5-fig4-disks-real.png)

![Figure 5.5 – CPU, memory, and `/proc` observations](resources/terminal-captures/real/lab5-fig5-proc-real.png)

## Conclusion

The filesystem maps names to inodes and inodes to data and metadata. Hard links share an inode, symbolic links store a path, and permission bits govern reads, writes, and traversal. `df`, `du`, `/proc`, and device nodes expose different views of storage and running-system state.

---

# Laboratory Work 6 — Inside the xv6 File System

**Course:** Operating Systems, FCIM / FAF, UTM, 2026-2027  
**Student:** Pleșu Dinu, FAF-241  
**Environment:** Linux, xv6 on QEMU

## Part 1. Read what xv6 shows you

The `ls` output is a table of `name, type, inode, size`, and the type codes are decoded by `kernel/stat.h`:

- `T_DIR = 1` → directory
- `T_FILE = 2` → regular file
- `T_DEVICE = 3` → device file

The root directory has inode 1 because `ROOTINO` is defined as 1 in `kernel/fs.h`. For the root, `.` and `..` are both the same entry because a directory's own `.` points to itself and its `..` points back to the directory itself; for the root, those are the same inode.

An empty directory has size 32 because a directory entry is fixed-size: `sizeof(struct dirent) = 2 + 14 = 16` bytes. Therefore an empty directory with just `.` and `..` contains exactly two entries and has `2 * 16 = 32` bytes.

![Figure 6.1 – `ls` output in xv6: name, type, inode number, and size](resources/terminal-captures/real/lab6-fig1-ls-real.png)

## Part 2. Write mystat

The required implementation is a small user program that calls `stat()`, converts the file type with a helper, and prints inode, link count, and size. In the xv6 tree, the program was added as `user/mystat.c` and the corresponding build line was added in the `UPROGS` list.

Example output from the assignment workflow:

```
$ mystat README . console
README: file, inode 2, links 1, size 2441 bytes
.: directory, inode 1, links 1, size 1024 bytes
console: device, inode 25, links 1, size 0 bytes
$ ln README r2
$ mystat README r2
README: file, inode 2, links 2, size 2441 bytes
r2: file, inode 2, links 2, size 2441 bytes
$ rm README
$ mystat r2
r2: file, inode 2, links 1, size 2441 bytes
$ cat r2 | wc
```

The important invariant is that the inode number stays the same after `ln`: both names refer to the same file. After the first name is deleted, the file still exists as long as another hard link remains. The link count changes from 2 to 1 but the data remains accessible through the surviving name. The actual data blocks are freed only when the last hard link disappears and the inode gets reclaimed; the unlink path decrements `nlink` but does not immediately free data.

The decrement is visible in `kernel/sysfile.c`:

```
ip->nlink--;
iupdate(ip);
```

This is the assignment's `sys_unlink()` path. The file's data blocks are eventually reclaimed using inode truncation and free-block accounting when the link count reaches zero, not as part of the unlink itself.

The `struct dinode` in `kernel/fs.h` contains the key on-disk inode fields:

- `short type`
- `short major`
- `short minor`
- `short nlink`
- `uint size`
- `uint addrs[NDIRECT + 1]`

This is enough to represent regular files, directories, device files, link counts, file length, and the direct/indirect block pointers.

![Figure 6.2 – `mystat` before and after `ln` and `rm`](resources/terminal-captures/real/lab6-fig2-mystat-real.png)

## Part 3. Measure the limits

The relevant constants are:

```
$ grep -n "define BSIZE\|define NDIRECT\|define NINDIRECT\|define DIRSIZ" kernel/fs.h
#define BSIZE   1024
#define NDIRECT   12
#define NINDIRECT (BSIZE / sizeof(uint))
#define DIRSIZ 14
```

`DIRSIZ` explains the directory-entry name limit. `mkdir averyveryverylongname` creates a name longer than 14 characters, and the name is truncated to fit in the 14-byte `dirent.name` array. `ls` displays the shortened entry rather than a longer path component.

The maximum xv6 file size is computed as:

```
12 direct blocks + 1 indirect block
= 12 * BSIZE + (BSIZE / 4) * BSIZE
= 12 * 1024 + 256 * 1024
= 12288 + 262144
= 274432 bytes
```

This is the largest file supported by the `NDIRECT + NINDIRECT` model in `kernel/fs.h`.

The actual `nmeta` output from the build was:

```
nmeta 47 (boot, super, log blocks 31, inode blocks 13, bitmap blocks 1) blocks 1953 total 2000
```

So the disk holds 2000 blocks in total, 47 are metadata (boot/super/log/inodes/bitmap), and the remaining 1953 blocks are data blocks.

![Figure 6.3 – The constants in `kernel/fs.h` and the link-count code in `sys_unlink`](resources/terminal-captures/real/lab6-fig3-limits-real.png)

![Figure 6.4 – A directory name longer than `DIRSIZ` is truncated by `mkdir`](resources/terminal-captures/real/lab6-fig4-longname-real.png)

## Part 4. Write find

The assignment requires a recursive directory walk that skips `.` and `..`, ignores zeroed entries (`inum == 0`), and compares names with `strcmp`. The implementation added in `user/find.c` follows the same pattern as `user/ls.c`: open a directory, read each `dirent`, build the full path, and recurse into subdirectories when needed.

Example test run:

```
$ mkdir a
$ mkdir a/b
$ echo x > a/b/r2
$ echo y > a/r2
$ ln cat r2
$ find . r2
./a/b/r2
./a/r2
./r2
$ find a b
a/b
```

This demonstrates the intended behavior: `find` searches under the target directory and prints every path whose final component matches the requested file name, without descending into `.` or `..`.

![Figure 6.5 – `find` finds every `r2`, including the directory named `b`](resources/terminal-captures/real/lab6-fig5-find-real.png)

## Conclusion

The xv6 filesystem is compact but faithful to the concepts behind larger filesystems: directories are just files of directory entries, inodes store metadata and block addresses, and hard links share the same inode object. Understanding `DIRSIZ`, inode link counts, and block layout makes the design of `mystat` and `find` straightforward, and it shows how even a small OS can implement a filesystem with much of the same conceptual machinery as modern systems.