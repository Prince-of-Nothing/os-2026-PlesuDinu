# Laboratory Work 6 — Inside the xv6 File System

**Course:** Operating Systems, FCIM / FAF, UTM, 2026-2027  
**Student:** Pleșu Dinu, FAF-241  
**Environment:** Linux, xv6 on QEMU

## Purpose and build

This lab investigates xv6 directory entries, inodes, hard links, filesystem
limits, and recursive directory traversal. The submitted implementation is
contained in [`mystat.c`](mystat.c), [`find.c`](find.c), and [`Makefile`](Makefile).
The Makefile registers `$U/_mystat\` and `$U/_find\` in `UPROGS`.

The tree was built and tested with:

```text
make clean
make CPUS=1
make qemu CPUS=1
```

QEMU was exited with `Ctrl-A`, then `X`.

## Part 1 — Read what xv6 shows

The xv6 `ls` output contains `name`, `type`, `inode number`, and `size in
bytes`. The type constants in `kernel/stat.h` are:

- `T_DIR = 1`: directory
- `T_FILE = 2`: regular file
- `T_DEVICE = 3`: device file

The root directory has inode 1 because `ROOTINO` is 1 in `kernel/fs.h`. The
root's `.` and `..` entries refer to the same inode: the root is its own parent.

An empty directory has size 32 bytes. `struct dirent` contains a two-byte inode
number and a `DIRSIZ`-byte name, where `DIRSIZ` is 14, so one entry is
`2 + 14 = 16` bytes. The two entries in a newly created directory are `.` and
`..`, therefore `2 * 16 = 32` bytes.

## Part 2 — Write `mystat`

`mystat.c` calls `stat()` for every path argument, converts the type using
`typename()`, and prints the path, type, inode, link count, and size. Errors
are printed to file descriptor 2 and processing continues with the next
argument.

The assignment workflow produced the following observations:

```text
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

After `ln`, both directory entries have the same inode and the link count is
2. Removing `README` removes only that name: `r2` still has inode 2, the same
size, and readable data, while the link count becomes 1.

In `kernel/sysfile.c`, `sys_unlink` decrements the link count:

```c
ip->nlink--;
iupdate(ip);
```

The data blocks are not freed merely because one name is removed. They are
reclaimed after the final hard link disappears and the inode is truncated and
released. The xv6 `struct dinode` contains `type`, `major`, `minor`, `nlink`,
`size`, and `addrs[NDIRECT + 1]`; it has no symbolic-link or permission fields.

## Part 3 — Measure the limits

The relevant constants are:

```text
BSIZE     = 1024
NDIRECT   = 12
NINDIRECT = BSIZE / sizeof(uint) = 256
DIRSIZ    = 14
```

A directory name longer than 14 characters is truncated in its directory entry,
so `averyveryverylongname` is displayed as `averyveryveryl`.

The largest file uses 12 direct blocks plus one indirect block:

```text
12 * 1024 + (1024 / 4) * 1024
= 12,288 + 262,144
= 274,432 bytes
```

The recorded `mkfs` output was:

```text
nmeta 47 (boot, super, log blocks 31, inode blocks 13, bitmap blocks 1) blocks 1953 total 2000
```

Thus the image has 2000 blocks. The metadata consists of the boot and
superblock entries, 31 log blocks, 13 inode blocks, and one bitmap block;
1953 blocks remain for data.

## Part 4 — Write `find`

`find <dir> <name>` prints every path under `<dir>` whose final component
matches `<name>`. The implementation:

1. opens and stats the starting path;
2. reads directory entries one at a time;
3. skips free entries (`inum == 0`) and `.`/`..`;
4. builds a complete child path in a bounded buffer;
5. compares the final component with `strcmp`;
6. recurses into child directories; and
7. closes every descriptor it opens.

On a fresh filesystem image:

```text
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

Directory traversal order may vary, but all matching paths must be printed.
Closing each directory is necessary because xv6 allows only a small number of
open files per process.

## Conclusion

xv6 implements a compact filesystem using fixed-size directory records,
inodes, hard links, direct and indirect block addresses, and a bitmap. The
`mystat` program exposes inode metadata, while `find` demonstrates how a
filesystem utility walks directories without following `.` or `..`.
