# Q1. How many requests failed?
grep -c ' FAIL ' access.log
# Q2. How many different pages were requested, and which?
cut -d' ' -f5 access.log | sort -u | awk '{ print } END { printf "different pages: %d\n", NR }'
# Q3. How many requests did each page get?
cut -d' ' -f5 access.log | sort | uniq -c | sort -k2
# Q4. Which user or users have the most failed requests, and how many?
grep ' FAIL ' access.log | cut -d' ' -f3 | sort | uniq -c | sort -rn | awk 'NR == 1 { max = $1; print; next } $1 == max { print; next } { exit }'
# Q5. How many requests did user3 make, and how many of them failed?
awk '$3 == "user3" { total++; if ($4 == "FAIL") failed++ } END { printf "user3: %d requests, %d failed\n", total, failed }' access.log
# Q6. Print the last 3 failed requests, showing only time and user.
grep ' FAIL ' access.log | cut -d' ' -f2,3 | tail -3
# Q7. Which login shells appear in /etc/passwd, and how many accounts use each?
cut -d: -f7 /etc/passwd | sort | uniq -c | sort -rn
# Q8. Compare the line counts and explain the extra total line from ls -l.
printf 'ls: '; ls /etc | wc -l; printf 'ls -l: '; ls -l /etc | wc -l
