#!/usr/bin/env python3
"""Build Lab1_PlesuDinu_FAF-241.docx from the UTM template using the recorded VM outputs."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

TPL = '/home/user/Documents/GitHub/os-2026-PlesuDinu/resources/UTM_Lab_Report_Template.docx'
PNG = '/home/user/Documents/GitHub/os-2026-PlesuDinu/Lab1/captures/png'
OUT = '/home/user/Documents/GitHub/os-2026-PlesuDinu/Lab1/Lab1_PlesuDinu_FAF-241.docx'

doc = Document(TPL)

def set_text(p, text):
    for r in p.runs:
        r.text = ''
    if p.runs:
        p.runs[0].text = text
    else:
        p.add_run(text)

paras = doc.paragraphs
for p in paras:
    if '[Student Name]' in p.text:
        set_text(p, 'Pleșu Dinu FAF-241')
for p in paras:
    if '[N]' in p.text:
        set_text(p, p.text.replace('[N]', '1'))
    if '[Laboratory topic]' in p.text:
        set_text(p, p.text.replace('[Laboratory topic]', 'The OS as a Resource Manager'))
    if '[Instructor, academic title]' in p.text:
        set_text(p, p.text.replace('[Instructor, academic title]', 'Reitman Patricia, university assistant'))

idx_contents = next(i for i, p in enumerate(paras) if p.text.strip() == 'Contents')
toc = ['1.  Purpose of the Work',
       '2.  Initial Setup',
       '3.  Part 1 – Files and Directories',
       '4.  Part 2 – Processes',
       '5.  Part 3 – Memory',
       '6.  Part 4 – Devices and Storage',
       '7.  Conclusion']
for p in paras[idx_contents + 1:]:
    p._p.getparent().remove(p._p)
for entry in toc:
    tp = doc.add_paragraph(entry)
    tp.paragraph_format.space_after = Pt(4)

def fresh_heading(text, level=1):
    h = doc.add_heading(text, level=level)
    for r in h.runs:
        r.font.color.rgb = RGBColor(0, 0, 0)
    return h

def body(text):
    p = doc.add_paragraph(text)
    p.paragraph_format.space_after = Pt(6)
    return p

def code(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    r.font.name = 'Consolas'
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(20, 20, 60)
    return p

def figure(png, caption):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(f'{PNG}/{png}.png', width=Cm(15.5))
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = c.add_run(caption)
    r.italic = True
    r.font.size = Pt(10.5)

doc.add_page_break()

# ==== 1. Purpose ====
fresh_heading('1.  Purpose of the Work')
body('The purpose of this laboratory work is to see how the operating system manages resources '
     'as a file system, a process manager, a memory manager and a device manager, using the '
     'command line as the interface. Every command below was run on my own machine (Ubuntu on '
     'VirtualBox, user vboxuser, kernel 7.0.0-38-generic) and every output shown is the real '
     'output of that run.')

# ==== 2. Initial setup ====
fresh_heading('2.  Initial Setup')
code('mkdir -p ~/os-lab1 && cd os-lab1\nwhoami\nuname -a')
figure('fig1-1-setup', 'Figure 2.1 – Creating the lab folder, printing the user and the kernel')
body('mkdir -p created the folder and its parents if needed, && chained the cd so it only ran '
     'if the creation succeeded, whoami printed my username and uname -a printed the full '
     'system information (kernel version, architecture, date).')

# ==== 3. Part 1 ====
fresh_heading('3.  Part 1 – Files and Directories')
code('pwd\nls -la /\nls -la ~\ncd /etc && ls | head')
figure('fig1-2-tree', 'Figure 3.1 – pwd and the long listing of / with hidden files')
body('pwd confirmed my current directory. ls -la listed directories in long format including '
     'hidden entries: the first character of each line shows the type — d for a directory, l '
     'for a symbolic link (bin -> usr/bin, lib -> usr/lib), - for a regular file. The pipe '
     'ls | head showed exactly the first 10 lines of /etc.')
code('cd ~/os-lab1\nmkdir demo && cd demo\necho "hello operating systems" > note.txt\ncp note.txt copy.txt\nmv copy.txt renamed.txt\nls -l\nrm renamed.txt')
figure('fig1-3-files', 'Figure 3.2 – Create, copy, rename and remove files')
body('echo wrote the text into note.txt, the > redirection created the file because it did not '
     'exist yet, cp copied it, mv renamed the copy and rm removed it.')
code('ls -l note.txt\nchmod 600 note.txt\nls -l note.txt\nchmod 644 note.txt')
figure('fig1-4-chmod', 'Figure 3.3 – chmod changes the permission bits')
body('chmod 600 gave the owner read+write and nothing to the others; 644 gave the owner '
     'read+write and read-only to group and others.')
fresh_heading('3.1.  Observations', 2)
body('The created files were owned by the vboxsf shared-folder group. After chmod they showed '
     'the rw bits for the owner (and for the group in the 644 case), which is exactly what the '
     'permission string rwxrwx---/rw-rw-r-- encodes.')

# ==== 4. Part 2 ====
fresh_heading('4.  Part 2 – Processes')
code('ps aux | head\nps aux | wc -l\ntop')
figure('fig1-5-ps', 'Figure 4.1 – ps aux filtered through head, and top’s live view')
body('ps aux listed every process with its user, PID, CPU and memory usage; wc -l counted '
     'roughly 370 lines, so roughly 370 processes at that moment. top showed the same data '
     'live, including the totals line "392 total, 2 running, 1 zombie".')
code('sleep 300 &\njobs\nps -ef | grep sleep\nkill 13451')
figure('fig1-6-jobs', 'Figure 4.2 – A background job, found with ps, then killed')
body('sleep 300 & submitted the process to the background; jobs listed it with its job number '
     'and PID, ps -ef | grep sleep found it in the full process list, and kill terminated it '
     'by its PID — the shell then reported "Terminated".')
code('sleep 300 &\nPID=$!\nls /proc/$PID/\ncat /proc/$PID/status | head -20\nkill $PID')
figure('fig1-7-proc', 'Figure 4.3 – /proc exposes the live state of the sleep process')
body('$! held the PID of the last background process, so it could be stored in PID and reused. '
     '/proc/PID is a directory the kernel fills with that process’s state: its memory maps, '
     'file descriptors, limits and the status file shown above (Name, State S (sleeping), Pid, '
     'PPid, Uid, memory sizes).')
fresh_heading('4.1.  Observations', 2)
body('PID 1 on my system is systemd, the init/system manager. The sleep process was in state '
     'S (sleeping) because it was waiting on a timer instead of using the CPU. This part showed '
     'how the OS assigns PIDs, keeps track of processes and exposes their information through '
     '/proc.')

# ==== 5. Part 3 ====
fresh_heading('5.  Part 3 – Memory')
code('free -h\ncat /proc/meminfo | head -6\nsleep 300 & PID=$!\ngrep VmRSS /proc/$PID/status\nkill $PID')
figure('fig1-8-free', 'Figure 5.1 – free -h and the first lines of /proc/meminfo')
body('free -h gave the human-readable summary (7.2 GiB total, 1.6 GiB used, 4.0 GiB free, '
     '1.9 GiB buff/cache, 5.6 GiB available, 0B swap) and /proc/meminfo showed the same values '
     'in kB with more detail.')
figure('fig1-9-vmrss', 'Figure 5.2 – VmRSS: resident memory of the sleep process')
body('VmRSS showed the resident (actually in RAM) part of the process — about 0.2 MB for a '
     'sleeping process: executable, libraries, stack and other mappings.')
fresh_heading('5.1.  Observations', 2)
body('The VM had about 7.2 GiB of RAM and no swap. Free memory was roughly 2/3 of available '
     'memory because Linux was using RAM for buffers/cache that can be reclaimed when needed.')

# ==== 6. Part 4 ====
fresh_heading('6.  Part 4 – Devices and Storage')
code('df -h\nlsblk\ndu -sh ~/os-lab1\nls -l /dev | head\nmount | head')
figure('fig1-10-df', 'Figure 6.1 – df -h and lsblk: mounted filesystems and block devices')
body('df -h showed every mounted filesystem and its free space: /dev/sda2 (51G, 15% used) is '
     'mounted on / as ext4, and the VirtualBox shared folder is mounted on /home/vboxuser. '
     'lsblk showed the block devices: sda with the sda1/sda2 partitions and the sr0 CD-ROM.')
figure('fig1-11-du', 'Figure 6.2 – Disk usage of the lab directory')
figure('fig1-12-dev', 'Figure 6.3 – Device files in /dev and the mount table')
body('du -sh reported how much space the lab directory itself used. mount listed every '
     'filesystem with its options: /dev/sda2 on / as ext4, devtmpfs on /dev, sysfs on /sys '
     'and so on. /dev contains device files — character devices such as console (c) and '
     'symbolic links such as cdrom -> sr0 — so programs use them with ordinary file calls. '
     'This is the Unix idea that "everything is a file".')
fresh_heading('6.1.  Observations', 2)
body('The root filesystem / was mounted on /dev/sda2 with the ext4 type. The distinction is '
     'clear now: a disk (sda) holds partitions (sda2), a partition is attached to a directory '
     'by mount (at /), and /dev provides the device interfaces to the kernel drivers.')

# ==== 7. Conclusion ====
fresh_heading('7.  Conclusion')
body('This lab made the four roles of the OS concrete. As a resource manager it gave me a '
     'directory tree to walk with pwd, ls, cd and the pipes head/grep/wc; as a process manager '
     'it let me start, list, inspect through /proc and kill processes with &, jobs, ps and kill; '
     'as a memory manager it showed totals, free/available and per-process VmRSS through free '
     'and /proc/meminfo; as a device manager it showed filesystems, partitions, mount points '
     'and device files through df, lsblk, du, mount and /dev. Working through real outputs '
     'turned the abstract notions of processes, memory and devices into things I can measure '
     'on any Linux machine, which is the base for the following labs.')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT)
print('saved', OUT)
