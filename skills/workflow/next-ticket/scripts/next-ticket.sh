#!/usr/bin/env bash
# Survey a tickets folder and pick the next open ticket, so the agent
# doesn't have to read every file just to find it. Selection mirrors the
# next-ticket skill: prefer an In progress ticket, else the lowest-ordinal
# Not started ticket whose blockers are all Completed.
#
# Usage: next-ticket.sh [tickets-dir]   (default: ai/tickets)
set -euo pipefail

dir="${1:-ai/tickets}"
if [ ! -d "$dir" ]; then
  echo "No tickets folder at: $dir" >&2
  exit 1
fi

# First non-empty content line under "## <heading>", stripped of markdown noise.
section() {
  awk -v h="## $2" '
    $0 == h {f=1; next}
    f && /^## / {exit}
    f && NF {
      gsub(/`|\*/, ""); sub(/^[-[:space:]]+/, ""); sub(/[[:space:]]+$/, "")
      print; exit
    }
  ' "$1"
}

# Blocking ticket filenames referenced in the "## Blocked by" section.
blockers() {
  awk '
    $0 == "## Blocked by" {f=1; next}
    f && /^## / {exit}
    f {print}
  ' "$1" | grep -oE '[0-9]+-[A-Za-z0-9_-]+\.md' | sort -u || true
}

# Tickets anywhere under the folder, as paths relative to it, ordered
# globally by basename so the zero-padded ordinal decides across subfolders.
files=$(cd "$dir" && find . -type f -name '*.md' | sed 's|^\./||' \
  | grep -E '(^|/)[0-9]+-[^/]*\.md$' \
  | awk -F/ '{print $NF "|" $0}' | sort | cut -d'|' -f2) || true
if [ -z "$files" ]; then
  echo "No tickets found in: $dir" >&2
  exit 1
fi

# Blockers are referenced by basename, so duplicates would be ambiguous.
dups=$(printf '%s\n' $files | awk -F/ '{print $NF}' | sort | uniq -d)
if [ -n "$dups" ]; then
  echo "warning: duplicate ticket filenames across subfolders: $dups" >&2
fi

index=""
printf '%-45s %-6s %-10s %-12s %s\n' "TICKET" "TYPE" "CATEGORY" "STATUS" "BLOCKED BY"
for f in $files; do
  path="$dir/$f"
  status=$(section "$path" "Status");     [ -n "$status" ] || status="?"
  type=$(section "$path" "Type");         type=${type%% *}; [ -n "$type" ] || type="?"
  category=$(section "$path" "Category"); category=${category%% *}; [ -n "$category" ] || category="Build"
  b=$(blockers "$path" | paste -sd ',' -); [ -n "$b" ] || b="None"
  printf '%-45s %-6s %-10s %-12s %s\n' "$f" "$type" "$category" "$status" "$b"
  index="$index${f##*/}|$status
"
done

status_of() {
  printf '%s' "$index" | awk -F'|' -v k="$1" '$1==k {print $2; exit}'
}

echo
for f in $files; do
  if [ "$(status_of "${f##*/}")" = "In progress" ]; then
    echo "NEXT: $dir/$f (In progress — prefer finishing it)"
    exit 0
  fi
done

for f in $files; do
  [ "$(status_of "${f##*/}")" = "Not started" ] || continue
  ok=1
  for b in $(blockers "$dir/$f"); do
    if [ "$(status_of "$b")" != "Completed" ]; then
      ok=0
      break
    fi
  done
  if [ "$ok" = 1 ]; then
    echo "NEXT: $dir/$f (Not started, blockers satisfied)"
    exit 0
  fi
done

echo "NEXT: none — every open ticket is blocked, or the set is complete."
