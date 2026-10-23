# Lab 6 notes — xv6 filesystem observations

## Part 1. Read what xv6 shows you

1. `T_DIR = 1`, `T_FILE = 2`, `T_DEVICE = 3` in `kernel/stat.h`.
2. The root directory has inode number 1 because `ROOTINO` is defined as 1 in `kernel/fs.h`. The entries `.` and `..` are both the same there because a directory's `.` entry points to itself and `..` points back to the parent; for the root, both are the root directory itself.
3. An empty directory has size 32 because each directory entry is 16 bytes: 2-byte inode number + 14-byte name field. The two entries are `.` and `..`.

## Part 2. Write mystat

Example session:

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
    1       8      40
```

What changed: the link count increased from 1 to 2 when the new hard link was created, and both names referred to the same inode. After `rm README`, the inode still existed as long as `r2` remained; only the remaining link count changed from 2 to 1. The file data itself did not change, and the inode number stayed the same. The actual data blocks are not freed immediately on unlink; they are released only when the file's link count reaches zero and the inode is reclaimed via `itrunc`/`bfree`.

The decrement appears in `kernel/sysfile.c`:

```
ip->nlink--;
iupdate(ip);
```

This happens in `sys_unlink()`. The file data blocks are freed later when the last link is removed and the inode is truncated/reclaimed, not inside the unlink path itself.

The xv6 inode `struct dinode` in `kernel/fs.h` holds:

- `short type`
- `short major`
- `short minor`
- `short nlink`
- `uint size`
- `uint addrs[NDIRECT + 1]`

That means xv6 stores file type, device numbers for devices, link count, length, and block pointers.

## Part 3. Measure the limits

```
$ grep -n "define BSIZE\|define NDIRECT\|define NINDIRECT\|define DIRSIZ" kernel/fs.h
#define BSIZE   1024
#define NDIRECT   12
#define NINDIRECT (BSIZE / sizeof(uint))
#define DIRSIZ 14
```

`mkdir averyveryverylongname` creates a pathname that exceeds the `DIRSIZ` limit of 14 characters, so the directory entry is truncated to 14 bytes and `ls` shows a shortened name. This is explained by `DIRSIZ` in `kernel/fs.h`.

Largest file size:

```
12 direct blocks + 1 indirect block
= 12 * BSIZE + (BSIZE / 4) * BSIZE
= 12 * 1024 + 256 * 1024
= 12288 + 262144
= 274432 bytes
```

This is the same as `(NDIRECT + NINDIRECT) * BSIZE` with `NDIRECT = 12` and `NINDIRECT = BSIZE / 4`.

The actual `nmeta` output from the build was:

```
nmeta 47 (boot, super, log blocks 31, inode blocks 13, bitmap blocks 1) blocks 1953 total 2000
```

So the disk has 2000 blocks total. Metadata occupies 47 blocks (boot/super/log/inode/bitmap), leaving 1953 blocks for data.

## Part 4. Write find

Example test:

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

`find` walks the directory tree recursively, skips `.` and `..`, ignores free entries (`inum == 0`), and compares names with `strcmp`. It opens every visited directory and closes it before returning, so it respects the limit of 16 open files per process.

## Conclusion

The xv6 file system is small but instructive: directories are just special files containing dirent records, names are limited by `DIRSIZ`, and inodes carry the metadata necessary to manage size, hard links, and block addresses. A hard link shares one inode, the data blocks are reclaimed only when the last link disappears, and `find` is a straightforward directory walk that demonstrates the same recursion ideas behind real filesystem tools.
