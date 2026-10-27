# Laboratory Work 1 — The OS as a Resource Manager
### Course: Operating Systems
### Author: Pleșu Dinu FAF-241
## Theory
The following commands are used in this lab:

- mkdir -p DIR: create DIR and parent directories if needed.
- cd DIR: change current directory to DIR.
- whoami: print the current user name.
- uname -a: print kernel and system information.
- pwd: print current working directory.
- ls -la PATH: list directory contents in long format, include hidden files.
- ls -l PATH: list directory contents in long format.
- ls | head: pipe ls output to head to show first 10 lines.
- head: show first lines of input (default 10).
- mkdir NAME: create a directory.
- echo "text" > file: write text into file (overwrite).
- cp SRC DST: copy files.
- mv SRC DST: move or rename files.
- rm FILE: remove file.
- chmod MODE FILE: change file permissions (numeric modes like 600, 644).
- ps aux: show running processes with detailed, user-oriented info.
- ps -ef: show all processes in full-format listing.
- grep PATTERN: filter input lines matching PATTERN.
- wc -l: count lines of input.
- top: interactive process and system monitor.
- sleep N &: run sleep in background; '&' submits a job to the background.
- jobs: list current shell background jobs.

## Initial setup
```bash
mkdir -p ~/os-lab1 && cd ~/os-lab1
whoami
uname -a
```

Output:

```text
vboxuser
Linux Shameless 7.0.0-38-generic #38-Ubuntu SMP PREEMPT_DYNAMIC Fri Sep  4 09:10:14 UTC 2026 x86_64 GNU/Linux
 07:19:28 up 5 min,  1 user,  load average: 7.80, 6.73, 3.11
```

I created a separate folder for the lab, checked my username, the running kernel and how long the system had been up. `mkdir -p` created the folder if needed, while `&&` made `cd` run only if the first command succeeded.

## Part 1 — Files and directories

```bash
pwd
ls -la /
ls -la ~
cd /etc && ls | head
```

Output:

```text
/home/vboxuser/os-lab1
total 80
drwxr-xr-x  20 root root  4096 Oct  5 06:05 .
drwxr-xr-x  20 root root  4096 Oct  5 06:05 ..
lrwxrwxrwx   1 root root     7 Apr 20 08:46 bin -> usr/bin
drwxr-xr-x   3 root root  4096 Oct  5 07:09 boot
dr-xr-xr-x   2 root root  4096 Oct  5 06:00 cdrom
drwxr-xr-x  19 root root  4160 Oct  5 07:14 dev
drwxr-xr-x 142 root root 12288 Oct  5 07:12 etc
drwxr-xr-x   3 root root  4096 Oct  5 06:44 home
lrwxrwxrwx   1 root root     7 Apr 20 08:46 lib -> usr/lib
lrwxrwxrwx   1 root root     9 Apr 20 08:46 lib64 -> usr/lib64
drwx------   2 root root 16384 Oct  5 06:08 lost+found
drwxr-xr-x   2 root root  4096 Aug 26 05:27 media
drwxr-xr-x   2 root root  4096 Aug 26 05:27 mnt
drwxr-xr-x   3 root root  4096 Oct  5 07:02 opt
dr-xr-xr-x 402 root root     0 Oct  5 07:13 proc
drwx------   5 root root  4096 Oct  5 07:08 root
drwxr-xr-x  42 root root  1020 Oct  5 07:15 run
lrwxrwxrwx   1 root root     8 Apr 20 08:46 sbin -> usr/sbin
drwxr-xr-x  16 root root  4096 Aug 26 05:35 snap
drwxr-xr-x   2 root root  4096 Aug 26 05:27 srv
dr-xr-xr-x  13 root root     0 Oct  5 07:13 sys
drwxrwxrwt  15 root root   360 Oct  5 07:24 tmp
drwxr-xr-x  12 root root  4096 Aug 26 05:27 usr
drwxr-xr-x  14 root root  4096 Oct  5 07:07 var
total 416
drwxrwx--- 1 root vboxsf   8192 Oct  5 07:19  .
drwxr-xr-x 3 root root     4096 Oct  5 06:44  ..
drwxrwx--- 1 root vboxsf   4096 Oct  5 07:17  .cache
drwxrwx--- 1 root vboxsf   4096 Oct  5 07:13  .config
drwxrwx--- 1 root vboxsf      0 Oct  5 07:12  .gnupg
drwxrwx--- 1 root vboxsf      0 Oct  5 07:10  .local
drwxrwx--- 1 root vboxsf      0 Oct  5 07:09  .ssh
-rwxrwx--- 1 root vboxsf      6 Oct  5 07:16  .vboxclient-clipboard-tty2-control.pid
-rwxrwx--- 1 root vboxsf      6 Oct  5 07:16  .vboxclient-clipboard-tty2-service.pid
-rwxrwx--- 1 root vboxsf      6 Oct  5 07:16  .vboxclient-draganddrop-tty2-control.pid
-rwxrwx--- 1 root vboxsf      6 Oct  5 07:16  .vboxclient-draganddrop-tty2-service.pid
-rwxrwx--- 1 root vboxsf      6 Oct  5 07:16  .vboxclient-hostversion-tty2-control.pid
-rwxrwx--- 1 root vboxsf      6 Oct  5 07:16  .vboxclient-hostversion-tty2-service.pid
-rwxrwx--- 1 root vboxsf      6 Oct  5 07:16  .vboxclient-seamless-tty2-control.pid
-rwxrwx--- 1 root vboxsf      6 Oct  5 07:16  .vboxclient-seamless-tty2-service.pid
-rwxrwx--- 1 root vboxsf      6 Oct  5 07:16  .vboxclient-vmsvga-session-tty2-control.pid
-rwxrwx--- 1 root vboxsf      6 Oct  5 07:16  .vboxclient-vmsvga-session-tty2-service.pid
drwxrwx--- 1 root vboxsf      0 Oct  5 07:10  Desktop
drwxrwx--- 1 root vboxsf      0 Oct  5 07:10  Documents
drwxrwx--- 1 root vboxsf      0 Oct  5 07:10  Downloads
-rwxrwx--- 1 root vboxsf 196979 Oct  5 05:39 'L1_FAF-24x_Xxxxx Xxxxxx.pdf'
-rwxrwx--- 1 root vboxsf 202004 Oct  5 05:40 'L2_FAF-24x_Xxxxx Xxxxxx.pdf'
drwxrwx--- 1 root vboxsf      0 Oct  5 07:10  Music
drwxrwx--- 1 root vboxsf      0 Oct  5 07:10  Pictures
drwxrwx--- 1 root vboxsf      0 Oct  5 07:10  Public
drwxrwx--- 1 root vboxsf      0 Oct  5 07:10  Templates
drwxrwx--- 1 root vboxsf      0 Oct  5 07:10  Videos
drwxrwx--- 1 root vboxsf      0 Oct  5 07:19  os-lab1
drwxrwx--- 1 root vboxsf      0 Oct  5 07:20  snap
ModemManager
NetworkManager
PackageKit
UPower
X11
adduser.conf
alsa
alternatives
anacrontab
apm

```

`pwd` showed my current directory. `ls -la` showed long file information, including hidden files, and `ls | head` made it show exactly 10 lines.

```bash
cd ~/os-lab1
mkdir demo && cd demo
echo "hello operating systems" > note.txt
cp note.txt copy.txt
mv copy.txt renamed.txt
ls -l
rm renamed.txt
```

Output:

```text
total 0
-rwxrwx--- 1 root vboxsf 24 Oct  5 07:31 note.txt
-rwxrwx--- 1 root vboxsf 24 Oct  5 07:31 renamed.txt
```

Here I created a directory and a text file, copied it, renamed the copy and then removed it. `echo` produced text and `>` redirected that text into `note.txt`. as `note.txt` wasn't yet present, the os created the file!

```bash
ls -l note.txt
chmod 600 note.txt
ls -l note.txt
chmod 644 note.txt
```

Output:

```text
-rwxrwx--- 1 root vboxsf 24 Oct  5 07:31 note.txt
-rwxrwx--- 1 root vboxsf 24 Oct  5 07:31 note.txt

```

`chmod` changed the permissions of the file. In `600`, the owner has read and write permissions and everyone else has none. In `644`, the owner can read and write, while group and others can only read.

### Observations

The files I created were owned by `vboxsf` and there is no group associated with them. It is a rw file that has rw permissions for the owner and group, and no permissions for others.

## Part 2 — Processes

```bash
ps aux | head
ps aux | wc -l
top
```

Output:

```text
Tasks: 392 total,   2 running, 389 sleeping,   0 stopped,   1 zombie
%Cpu(s):  0.9 us,  6.5 sy,  0.0 ni, 90.7 id,  0.0 wa,  0.0 hi,  1.9 si,  0.0 st 
MiB Mem :   7420.0 total,   3050.6 free,   2537.1 used,   2165.9 buff/cache     
MiB Swap:      0.0 total,      0.0 free,      0.0 used.   4882.9 avail Mem 

    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND  
   4616 vboxuser  20   0   11.1g 496872 215600 R 143.4   6.5  41:30.31 gnome-s+ 
   7341 vboxuser  20   0 6680640 419696 137612 S  52.3   5.5   2:14.93 ptyxis   
   7994 vboxuser  20   0 7111360 366056 160104 S   5.3   4.8   1:02.52 papers   
     15 root      20   0       0      0      0 I   1.7   0.0   0:28.31 rcu_pre+ 
   9266 root      20   0       0      0      0 I   1.3   0.0   0:00.31 kworker+ 
    325 root      20   0       0      0      0 I   1.0   0.0   0:02.93 kworker+ 
   8419 root      20   0       0      0      0 I   1.0   0.0   0:01.63 kworker+ 
   9049 root      20   0       0      0      0 I   1.0   0.0   0:00.49 kworker+ 
    124 root      20   0       0      0      0 I   0.7   0.0   0:04.79 kworker+ 
    402 root      20   0       0      0      0 I   0.7   0.0   0:00.13 kworker+ 
   8886 root      20   0       0      0      0 I   0.7   0.0   0:02.25 kworker+ 
   9370 root      20   0       0      0      0 I   0.7   0.0   0:00.04 kworker+ 
    121 root      20   0       0      0      0 I   0.3   0.0   0:03.79 kworker+ 
    126 root      20   0       0      0      0 I   0.3   0.0   0:02.58 kworker+ 
    497 root      20   0       0      0      0 S   0.3   0.0   0:00.94 jbd2/sd+ 
    505 root      20   0       0      0      0 I   0.3   0.0   0:02.46 kworker+ 
   1440 message+  20   0   12688   9308   4740 S   0.3   0.1   0:18.60 dbus-da+ 

```

`ps` showed running processes, `wc -l` counted the lines, and `top` showed a live view of process, CPU and memory activity.

```bash
sleep 300 &
jobs
ps -ef | grep sleep
kill 13451
```

Output:

```text
[1] 13451
[1]+  Running                    sleep 300 &
vboxuser   13451    8228 99 11:27 pts/0    00:00:00 sleep 300
vboxuser   13453    8228 33 11:27 pts/0    00:00:00 grep sleep
[1]+  Terminated                 sleep 300
```

`sleep 300 &` started a process in the background. `jobs` showed the shell job, `ps -ef | grep sleep` found it in the full process list, and `kill` terminated it using its PID.

```bash
sleep 300 &
PID=$!
ls /proc/$PID/
cat /proc/$PID/status | head -20
kill $PID
```

Output:

```text
cat /proc/$PID/status | head -20 # state, memory, threads
[1] 13481
arch_status	    fdinfo	       net	      setgroups
attr		    gid_map	       ns	      smaps
autogroup	    io		       numa_maps      smaps_rollup
auxv		    ksm_merging_pages  oom_adj	      stack
cgroup		    ksm_stat	       oom_score      stat
clear_refs	    latency	       oom_score_adj  statm
cmdline		    limits	       pagemap	      status
comm		    loginuid	       patch_state    syscall
coredump_filter	    map_files	       personality    task
cpu_resctrl_groups  maps	       projid_map     timens_offsets
cwd		    mem		       root	      timers
environ		    mountinfo	       sched	      timerslack_ns
exe		    mounts	       schedstat      uid_map
fd		    mountstats	       sessionid      wchan
Name:	sleep
Umask:	0002
State:	S (sleeping)
Tgid:	13481
Ngid:	0
Pid:	13481
PPid:	8228
TracerPid:	0
Uid:	1000	1000	1000	1000
Gid:	1000	1000	1000	1000
FDSize:	256
Groups:	4 24 27 30 46 100 111 114 974 1000 
NStgid:	13481
NSpid:	13481
NSpgid:	13481
NSsid:	8228
Kthread:	0
VmPeak:	   16112 kB
VmSize:	   16112 kB
VmLck:	       0 kB
[1]+  Terminated                 sleep 300
```

`$!` contained the PID of the last background process, so I saved it in `PID`. The `/proc/$PID` directory exposed live information about that process, including its state, parent PID, memory data and other kernel-maintained information.

### Observations

PID 1 on my system was `systemd`, which is the main system manager started during boot. `ps aux | wc -l` gave roughly 370 running processes, although the exact number changed between runs. The `sleep` process had the state `S (sleeping)`, which made sense because it was waiting instead of actively using the CPU. This part showed how the OS keeps track of processes, assigns PIDs and exposes process information through `/proc` directories.

## Part 3 — Memory

```bash
free -h
cat /proc/meminfo | head -6
```

Output:

```text
sleep 300 & PID=$!
grep VmRSS /proc/$PID/status # real RAM used by this process
kill $PID
               total        used        free      shared  buff/cache   available
Mem:           7.2Gi       1.6Gi       4.0Gi        41Mi       1.9Gi       5.6Gi
Swap:             0B          0B          0B
MemTotal:        7598072 kB
MemFree:         4184516 kB
MemAvailable:    5877904 kB
Buffers:           51672 kB
Cached:          1872036 kB
SwapCached:            0 kB
[1] 13599
VmRSS:	     912 kB
[1]+  Terminated                 sleep 300
```

`free -h` gave a readable summary of RAM and swap. `/proc/meminfo` showed the same information in more detail. I noticed that `free` memory was roughly 2/3  of the `available` memory because Linux was using some RAM for cache that could be reused when needed.

```bash
sleep 300 & PID=$!
grep VmRSS /proc/$PID/status
kill $PID
```

Output:

```text
[1] 13632
VmRSS:	     204 kB
[1]+  Terminated                 sleep 300
```

`VmRSS` showed how much physical RAM was resident for the process. Even a simple sleeping process still used several megabytes for its executable, libraries, stack and other mappings.

### Observations

The VM had about 7.2 GiB of RAM. Around 4 GiB was completely free at one point, but much more was still available because cached memory can be reassigned. No swap was configured, so the swap size was `0B`. The `sleep` process used about 0.2 MB of resident memory, which was more than I thought considering that Nasa's space shuttle ran on only one MB of RAM. 

## Part 4 — Devices and storage

```bash
df -h
lsblk
du -sh ~/os-lab1
ls -l /dev | head
mount | head
```

Output:

```text
Filesystem      Size  Used Avail Use% Mounted on
tmpfs           1.5G  1.9M  1.5G   1% /run
/dev/sda2        51G  6.9G   42G  15% /
tmpfs           3.7G     0  3.7G   0% /dev/shm
tmpfs           3.7G  8.0K  3.7G   1% /tmp
none            1.0M     0  1.0M   0% /run/credentials/systemd-journald.service
none            1.0M     0  1.0M   0% /run/credentials/systemd-resolved.service
Shared          699G  535G  164G  77% /home/vboxuser
tmpfs           742M   80K  742M   1% /run/user/1000
```

```text
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
loop0    7:0    0     4K  1 loop /snap/bare/5
loop1    7:1    0  66.8M  1 loop /snap/core24/1643
loop2    7:2    0    20M  1 loop /snap/desktop-security-center/151
loop3    7:3    0 260.3M  1 loop /snap/firefox/8763
loop4    7:4    0  16.5M  1 loop /snap/firmware-updater/226
loop5    7:5    0 614.5M  1 loop /snap/gnome-46-2404/164
loop6    7:6    0  91.7M  1 loop /snap/gtk-common-themes/1535
loop7    7:7    0   1.5M  1 loop /snap/hwctl/123
loop8    7:8    0   402M  1 loop /snap/mesa-2404/1839
loop9    7:9    0  18.8M  1 loop /snap/prompting-client/222
loop10   7:10   0  11.8M  1 loop /snap/snap-store/1390
loop11   7:11   0  50.1M  1 loop /snap/snapd/27710
loop12   7:12   0   828K  1 loop /snap/snapd-desktop-integration/391
loop13   7:13   0  44.7M  1 loop /snap/snapd/28254
loop14   7:14   0   1.5M  1 loop /snap/hwctl/131
loop16   7:16   0  14.2M  1 loop /snap/desktop-security-center/206
sda      8:0    0  51.7G  0 disk 
├─sda1   8:1    0     1M  0 part 
└─sda2   8:2    0  51.7G  0 part /
sr0     11:0    1  1024M  1 rom  

```

```text
512	/home/vboxuser/os-lab1
```

`df -h` showed mounted filesystems and their free space. `lsblk` showed block devices such as disks and partitions. `du -sh` showed how much disk space my lab directory used.

```text
total 0
crw-r--r--  1 root     root     10, 235 Oct  5 11:25 autofs
drwxr-xr-x  2 root     root        460 Oct  5 11:26 block
drwxr-xr-x  2 root     root         80 Oct  5 11:17 bsg
crw-------  1 root     root     10, 234 Oct  5 11:17 btrfs-control
drwxr-xr-x  3 root     root         60 Oct  5 11:17 bus
lrwxrwxrwx+ 1 root     root          3 Oct  5 11:17 cdrom -> sr0
drwxr-xr-x  2 root     root       4020 Oct  5 11:25 char
crw-------  1 root     tty       5,   1 Oct  5 11:25 console
lrwxrwxrwx  1 root     root         11 Oct  5 11:16 core -> /proc/kcore
tmpfs on /run type tmpfs (rw,nosuid,nodev,size=1519616k,nr_inodes=819200,mode=755,inode64)
/dev/sda2 on / type ext4 (rw,relatime)
devtmpfs on /dev type devtmpfs (rw,nosuid,size=2704484k,nr_inodes=676121,mode=755,inode64)
tmpfs on /dev/shm type tmpfs (rw,nosuid,nodev,inode64,usrquota)
devpts on /dev/pts type devpts (rw,nosuid,noexec,relatime,gid=5,mode=600,ptmxmode=000)
sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)
securityfs on /sys/kernel/security type securityfs (rw,nosuid,nodev,noexec,relatime)
cgroup2 on /sys/fs/cgroup type cgroup2 (rw,nosuid,nodev,noexec,relatime,nsdelegate,memory_recursiveprot,memory_hugetlb_accounting)
none on /sys/fs/pstore type pstore (rw,nosuid,nodev,noexec,relatime)
bpf on /sys/fs/bpf type bpf (rw,nosuid,nodev,noexec,relatime,mode=700)

```

`mount` showed which filesystem was attached to which point in the directory tree. In my case `/dev/sda2` was mounted at `/` and used the `ext4` filesystem.

`/dev` contained special device entries rather than normal text files. These entries give programs a file-like way to interact with devices and kernel drivers, which helped me understand the Unix idea that "everything is a file".

### Observations

The root filesystem `/` was mounted on `/dev/sda2`. One useful device example is the real-time clock device, such as `/dev/rtc` or `/dev/rtc0`, which gives access to the system hardware clock. The idea of "everything is a file" means that many devices and system resources are exposed through file-like interfaces, so programs can interact with them using similar operations to normal files. This part showed the difference between filesystems, disks, partitions, mount points and device interfaces.

## Conclusion

This lab reinforced how an operating system manages files, processes, memory, and devices/I/O. Using commands such as `ls`, `ps`, `free`, `df`, and `lsblk` allowed hands-on verification of concepts like mount points, device files in `/dev`, and resource reporting. The exercises clarified how these components interact and prepared me to apply system diagnostics in future labs.