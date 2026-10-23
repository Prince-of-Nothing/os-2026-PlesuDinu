# Laboratory Work 5 & 6 — Filesystem Fundamentals and xv6

**Course:** Operating Systems, FCIM / FAF, UTM, 2026-2027  
**Student:** Pleșu Dinu, FAF-241  
**Environment:** Linux + xv6 on QEMU

This folder consolidates the work for Lab 5 and Lab 6 into one place, following the same layout used in the reference repository for the combined assignment.

---

## Lab 5 — The File System with Your Own Hands

### Purpose

Inspect filesystem object types, inodes, hard and symbolic links, permissions, directory traversal rules, storage usage, mounted filesystems, and `/proc`.

### Core observations

- `ls -ld` shows object types: directories, regular files, symlinks, and device files.
- A hard link adds another directory entry pointing to the same inode.
- A symbolic link stores a pathname, not the target file's contents.
- Permission bits determine read, write, and traversal rights.
- `du` shows allocated blocks; `df` shows filesystem usage; `/proc` exposes kernel and process state.

### Typical commands used

```
ls -ld /etc /etc/passwd /bin /dev/null /tmp
ls -l /dev
stat notes.txt
ls -li
umask
lsblk
df -h /
cat /proc/meminfo
```

### Summary

The filesystem maps names to inodes and inodes to data and metadata. Hard links share the same inode; symbolic links point to another path; permissions and `/proc` provide insight into how the system exposes files and state.

---

## Lab 6 — Inside the xv6 File System

### Purpose

Understand how filesystems work inside xv6: inode metadata, directory entries, link counts, path traversal, and file-size limits.

### Core observations

- `T_DIR`, `T_FILE`, and `T_DEVICE` are defined in `kernel/stat.h`.
- The root directory is inode 1 (`ROOTINO`).
- Directory entries are fixed-size records containing a name and inode number.
- A hard link preserves the same inode number while incrementing `nlink`.
- `DIRSIZ` limits the length of a component name in xv6.
- The largest xv6 file is limited by direct and indirect blocks.

### Essential example

```
$ mystat README . console
README: file, inode 2, links 1, size 2441 bytes
.: directory, inode 1, links 1, size 1024 bytes
console: device, inode 25, links 1, size 0 bytes

$ ln README r2
$ mystat README r2
README: file, inode 2, links 2, size 2441 bytes
r2: file, inode 2, links 2, size 2441 bytes
```

### Summary

The xv6 filesystem is small but conceptually similar to real systems: directories are special files of directory entries, inodes hold metadata and block pointers, and hard links share the same inode object. A recursive `find` utility and a `mystat` utility are the practical exercises that illustrate these ideas.

---

## Combined file set

This combined folder is intended to hold the filesystem-related exercises together:

- `mystat.c`
- `find.c`
- `Makefile`
- `notes.md`

The original separate lab folders remain for reference, but the filesystem work is now centralized in this one directory.
