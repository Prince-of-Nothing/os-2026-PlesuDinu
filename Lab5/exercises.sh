#!/usr/bin/env bash
set -eu

work="$HOME/os-lab5"
mkdir -p "$work"
cd "$work"

printf '%s\n' '== File types ==' 
ls -ld /etc /etc/passwd /bin /dev/null /tmp
file /usr/bin/ls /etc/passwd /bin
du -sh /var/log /usr 2>/dev/null || true

printf '%s\n' '== Inodes and links =='
printf 'hello\n' > notes.txt
stat notes.txt
ls -li notes.txt
ln -f notes.txt hard.txt
ls -li notes.txt hard.txt
rm notes.txt
cat hard.txt
ln -sfn hard.txt soft.txt
ls -li hard.txt soft.txt
rm hard.txt
if cat soft.txt; then
  printf '%s\n' 'Unexpected: dangling symlink resolved.'
else
  printf '%s\n' 'Expected: soft.txt is dangling.'
fi
ls -l soft.txt
mkdir -p d/x d/y
ls -ld d
printf 'x\n' > one.txt
ls -l one.txt
du -h one.txt
truncate -s 1G big.img
ls -lh big.img
du -h big.img
rm big.img

printf '%s\n' '== Permissions =='
printf 'secret\n' > s.txt
chmod 600 s.txt
chmod 000 s.txt
if cat s.txt; then
  printf '%s\n' 'Read succeeded (for example, when run as root).'
else
  printf '%s\n' 'Expected: read denied for mode 000.'
fi
chmod u+r s.txt
cat s.txt
umask
touch new.txt
mkdir -p newdir
ls -ld new.txt newdir
mkdir -p box
printf 'hi\n' > box/f
chmod u=r,go= box
ls box || true
cat box/f || true
chmod u=x,go= box
ls box || true
cat box/f || true
chmod 755 box
ls -l /usr/bin/passwd
ls -ld /tmp
cat /etc/shadow >/dev/null 2>&1 || printf '%s\n' 'Expected: /etc/shadow access denied.'

printf '%s\n' '== Disks and proc =='
lsblk
df -h /
mount | grep ' / ' || true
grep -c '^processor' /proc/cpuinfo
head -3 /proc/meminfo
head -5 /proc/self/status
ls -l /proc/self/fd
