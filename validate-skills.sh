#!/usr/bin/env bash
# validate-skills.sh — lint Agent Skills (SKILL.md files) per agentskills.io spec.
#
# Checks per skill:
#   - Frontmatter is present and valid YAML delimiters (--- ... ---)
#   - Required fields: name, description
#   - name is lowercase kebab-case, 1-64 chars, no leading/trailing/consecutive hyphens
#   - name matches parent directory
#   - description is 1-1024 chars
#   - body is <500 lines (warning only)
#
# Exit code: number of errors. 0 = all valid.
#
# Usage:
#   ./validate-skills.sh                 # validate ./skills and ./.claude/skills
#   ./validate-skills.sh path/to/skills  # validate a specific directory

set -uo pipefail

ERRORS=0
WARNINGS=0
CHECKED=0

validate_skill() {
  local file="$1"
  local dir_name
  dir_name="$(basename "$(dirname "$file")")"
  CHECKED=$((CHECKED + 1))

  # Extract frontmatter (lines between first two --- markers)
  local frontmatter
  frontmatter="$(awk '
    BEGIN { in_fm = 0; started = 0 }
    /^---[[:space:]]*$/ {
      if (!started) { started = 1; in_fm = 1; next }
      else if (in_fm) { in_fm = 0; exit }
    }
    in_fm { print }
  ' "$file")"

  if [ -z "$frontmatter" ]; then
    echo "ERROR: $file — missing or empty YAML frontmatter"
    ERRORS=$((ERRORS + 1))
    return
  fi

  # Extract name
  local name
  name="$(printf '%s\n' "$frontmatter" | awk -F': *' '/^name:/ { sub(/^name: */, "", $0); print; exit }')"
  name="${name%\"}"; name="${name#\"}"
  name="${name%\'}"; name="${name#\'}"

  # Extract description (first line only; multi-line descriptions are permitted but we check length of the whole YAML value)
  local description
  description="$(printf '%s\n' "$frontmatter" | awk '
    /^description:/ {
      sub(/^description: */, "", $0)
      print
      while ((getline next_line) > 0) {
        if (next_line ~ /^[a-zA-Z_-]+:/) break
        print next_line
      }
      exit
    }
  ' | sed 's/^"//;s/"$//')"

  # name present
  if [ -z "$name" ]; then
    echo "ERROR: $file — missing 'name' field"
    ERRORS=$((ERRORS + 1))
    return
  fi

  # name matches dir
  if [ "$name" != "$dir_name" ]; then
    echo "ERROR: $file — name '$name' must match parent directory '$dir_name'"
    ERRORS=$((ERRORS + 1))
  fi

  # name is kebab-case, 1-64 chars
  if [ ${#name} -lt 1 ] || [ ${#name} -gt 64 ]; then
    echo "ERROR: $file — name '$name' length ${#name} not in 1-64"
    ERRORS=$((ERRORS + 1))
  fi

  # lowercase check (bash 3.2 compatible)
  local name_lower
  name_lower="$(printf '%s' "$name" | tr '[:upper:]' '[:lower:]')"
  if [ "$name_lower" != "$name" ]; then
    echo "ERROR: $file — name '$name' must be lowercase"
    ERRORS=$((ERRORS + 1))
  fi

  if [[ "$name" == *--* ]]; then
    echo "ERROR: $file — name '$name' contains consecutive hyphens"
    ERRORS=$((ERRORS + 1))
  fi
  if [[ "$name" == -* ]] || [[ "$name" == *- ]]; then
    echo "ERROR: $file — name '$name' has leading or trailing hyphen"
    ERRORS=$((ERRORS + 1))
  fi
  if [[ ! "$name" =~ ^[a-z0-9-]+$ ]]; then
    echo "ERROR: $file — name '$name' must be [a-z0-9-] only"
    ERRORS=$((ERRORS + 1))
  fi

  # description
  if [ -z "$description" ]; then
    echo "ERROR: $file — missing 'description' field"
    ERRORS=$((ERRORS + 1))
  else
    local desc_len=${#description}
    if [ "$desc_len" -gt 1024 ]; then
      echo "ERROR: $file — description is $desc_len chars (max 1024)"
      ERRORS=$((ERRORS + 1))
    fi
  fi

  # body size warning
  local body_lines
  body_lines=$(wc -l < "$file")
  if [ "$body_lines" -gt 500 ]; then
    echo "WARN:  $file — body is $body_lines lines (>500 recommended — move detail into references/)"
    WARNINGS=$((WARNINGS + 1))
  fi
}

# Collect target directories
targets=()
if [ $# -gt 0 ]; then
  targets=("$@")
else
  [ -d "./skills" ] && targets+=("./skills")
  [ -d "./.claude/skills" ] && targets+=("./.claude/skills")
fi

if [ ${#targets[@]} -eq 0 ]; then
  echo "No skills directory found. Pass a path or run from a repo with ./skills or ./.claude/skills."
  exit 1
fi

# Find all SKILL.md files and validate
while IFS= read -r -d '' skill_file; do
  validate_skill "$skill_file"
done < <(find "${targets[@]}" -type f -name 'SKILL.md' -print0 2>/dev/null)

echo "---"
echo "Checked $CHECKED skills — $ERRORS errors, $WARNINGS warnings"
exit "$ERRORS"
