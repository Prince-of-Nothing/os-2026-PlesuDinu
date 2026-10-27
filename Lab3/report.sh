log=${1:-}
if [ ! -f "$log" ]; then
    printf 'no such file: %s\n' "$log" >&2
    exit 1
fi

total=$(wc -l < "$log")
fails=$(grep -c ' FAIL ' "$log")
printf '%s requests, %s failed\n' "$total" "$fails"

for user_number in {0..6}; do
    user="user${user_number}"
    failures=$(awk -v user="$user" '$3 == user && $4 == "FAIL" { count++ } END { print count + 0 }' "$log")
    printf '%s: %s failures\n' "$user" "$failures"
done
