#!/bin/bash
# 3-Agent Knowledge DB 검증 파이프라인
# Stage 1: Extractor — MD 파일 메타데이터 + 핵심 식별자 추출
# Stage 2: Verifier — 원본 PDF/HTML 독립 재추출 후 대조
# Stage 3: Structural Checker — 파일명-내용 일치, frontmatter 무결성, 구조 검증
# Stage 4: Index Checker — _index.yaml vs 실제 파일 수 일치 검증 (EU + FDA)
#
# Usage: ./scripts/verify-knowledge-db.sh [--stage 1|2|3|4|all] [--verbose] [--file <path>] [--scope mfds|eu|fda|all]
set -euo pipefail

export LC_ALL=en_US.UTF-8

MFDS_SRC_BASE="/Users/hb/Documents/01.Regulatory/01. MFDS"
EU_SRC_BASE="/Users/hb/Documents/01.Regulatory/03. EU"
FDA_SRC_BASE="/Users/hb/Documents/01.Regulatory/02. FDA"
MFDS_DST_BASE="aria/knowledge/mfds"
EU_DST_BASE="aria/knowledge/eu"
FDA_DST_BASE="aria/knowledge/fda"
REPORT_FILE="/tmp/knowledge-db-verification-report.md"

# Parse args
STAGE="all"
VERBOSE=false
TARGET_FILE=""
SCOPE="all"
while [ $# -gt 0 ]; do
  case $1 in
    --stage) STAGE="$2"; shift 2 ;;
    --verbose) VERBOSE=true; shift ;;
    --file) TARGET_FILE="$2"; shift 2 ;;
    --scope) SCOPE="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# Counters
ext_ok=0; ext_warn=0; ext_fail=0
ver_pass=0; ver_fail=0; ver_empty=0; ver_skip=0
str_ok=0; str_fail=0
issue_count=0

# Issue log file (newline-delimited, avoids bash array issues)
ISSUE_LOG=$(mktemp)
trap "rm -f $ISSUE_LOG" EXIT

add_issue() {
  echo "$1" >> "$ISSUE_LOG"
  issue_count=$((issue_count + 1))
}

log() { echo "$@"; }
verbose() { if $VERBOSE; then echo "  $@"; fi; }

# ============================================================
# Stage 1: Extractor
# ============================================================
stage1_extract() {
  local md_file="$1"
  local basename_md
  basename_md=$(basename "$md_file")

  # Parse YAML frontmatter
  local src_path="" src_title="" src_pages="" src_method="" src_family=""
  src_path=$(grep '^  path:' "$md_file" 2>/dev/null | head -1 | sed 's/^  path: "//; s/"$//') || true
  src_title=$(grep '^  title:' "$md_file" 2>/dev/null | head -1 | sed 's/^  title: "//; s/"$//') || true
  src_pages=$(grep '^  pages:' "$md_file" 2>/dev/null | head -1 | sed 's/^  pages: //') || true
  src_method=$(grep '^  method:' "$md_file" 2>/dev/null | head -1 | sed 's/^  method: //; s/"//g') || true
  src_family=$(grep '^  family:' "$md_file" 2>/dev/null | head -1 | sed 's/^  family: "//; s/"$//') || true

  # Content statistics
  local body_chars body_lines
  body_chars=$(awk '/^---$/{n++; next} n>=2' "$md_file" | tr -d '[:space:]' | wc -c | tr -d ' ')
  body_lines=$(awk '/^---$/{n++; next} n>=2' "$md_file" | wc -l | tr -d ' ')

  # Key identifiers (scope-dependent)
  local identifiers=""
  if echo "$md_file" | grep -q "mfds"; then
    local law_numbers="" gosi_numbers=""
    law_numbers=$(grep -oE '(법률|대통령령|총리령)[[:space:]]*제[0-9]+호' "$md_file" 2>/dev/null | sort -u | head -5 | tr '\n' ', ') || true
    gosi_numbers=$(grep -oE '(고시|식품의약품안전처고시)[[:space:]]*제[0-9]+-[0-9]+호' "$md_file" 2>/dev/null | sort -u | head -5 | tr '\n' ', ') || true
    identifiers="law:${law_numbers} gosi:${gosi_numbers}"
  elif echo "$md_file" | grep -q "eu/"; then
    local chunk_type="" chunk_id=""
    chunk_type=$(grep '^  chunk_type:' "$md_file" 2>/dev/null | head -1 | sed 's/^  chunk_type: "//; s/"$//') || true
    chunk_id=$(grep '^  chunk_id:' "$md_file" 2>/dev/null | head -1 | sed 's/^  chunk_id: "//; s/"$//') || true
    identifiers="family:${src_family} type:${chunk_type} id:${chunk_id}"
  elif echo "$md_file" | grep -q "fda/"; then
    local chunk_type="" chunk_id=""
    chunk_type=$(grep '^  chunk_type:' "$md_file" 2>/dev/null | head -1 | sed 's/^  chunk_type: "//; s/"$//') || true
    chunk_id=$(grep '^  chunk_id:' "$md_file" 2>/dev/null | head -1 | sed 's/^  chunk_id: "//; s/"$//') || true
    identifiers="family:${src_family} type:${chunk_type} id:${chunk_id}"
  fi

  # Validation — Statute/Regulation chunks don't have path/pages
  local status="OK"
  local is_structured=false
  if [ "$src_family" = "REGULATION" ] || [ "$src_family" = "STATUTE" ]; then
    is_structured=true
  fi

  if ! $is_structured && [ -z "$src_path" ]; then
    status="WARN"
    add_issue "Extractor: $basename_md — source path missing in frontmatter"
    ext_warn=$((ext_warn + 1))
  elif [ "$body_chars" -lt 100 ]; then
    status="FAIL"
    add_issue "Extractor: $basename_md — body too small (${body_chars} chars)"
    ext_fail=$((ext_fail + 1))
  else
    ext_ok=$((ext_ok + 1))
  fi

  log "[$status] $basename_md — ${body_chars}c/${body_lines}L, pages:${src_pages:-?}, method:${src_method:-?}"
  verbose "title: $src_title"
  verbose "$identifiers"
}

# ============================================================
# Stage 2: Verifier
# ============================================================
stage2_verify() {
  local md_file="$1"
  local basename_md
  basename_md=$(basename "$md_file")

  local src_rel="" src_method="" src_family=""
  src_rel=$(grep '^  path:' "$md_file" 2>/dev/null | head -1 | sed 's/^  path: "//; s/"$//') || true
  src_method=$(grep '^  method:' "$md_file" 2>/dev/null | head -1 | sed 's/^  method: //; s/"//g') || true
  src_family=$(grep '^  family:' "$md_file" 2>/dev/null | head -1 | sed 's/^  family: "//; s/"$//') || true

  # Statute/Regulation chunks (HTML/XML-based) — skip Stage 2
  if [ "$src_family" = "REGULATION" ] || [ "$src_family" = "STATUTE" ]; then
    verbose "SKIP (structured chunk): $basename_md"
    ver_skip=$((ver_skip + 1))
    return
  fi

  if [ -z "$src_rel" ]; then
    log "[SKIP] $basename_md — no source path"
    ver_skip=$((ver_skip + 1))
    return
  fi

  # Determine source base directory
  local src_base_dir="$MFDS_SRC_BASE"
  if echo "$md_file" | grep -q "eu/"; then
    src_base_dir="$EU_SRC_BASE"
  elif echo "$md_file" | grep -q "fda/"; then
    src_base_dir="$FDA_SRC_BASE/03.Guidance"
  fi

  local src_pdf="${src_base_dir}/${src_rel}"
  if [ ! -f "$src_pdf" ]; then
    log "[SKIP] $basename_md — PDF not found: $src_rel"
    ver_skip=$((ver_skip + 1))
    return
  fi

  # pymupdf-extracted or OCR-based files: compare page count only
  if echo "$src_method" | grep -qi "ocr\|pymupdf"; then
    local pdf_pages yaml_pages
    pdf_pages=$(python3 -c "
import pymupdf
doc = pymupdf.open('$src_pdf')
print(len(doc))
" 2>/dev/null) || pdf_pages="?"
    yaml_pages=$(grep '^  pages:' "$md_file" | head -1 | sed 's/^  pages: //') || yaml_pages="?"

    if [ "$pdf_pages" = "$yaml_pages" ]; then
      log "[PASS] $basename_md — OCR file, page count match ($pdf_pages)"
      ver_pass=$((ver_pass + 1))
    else
      log "[FAIL] $basename_md — OCR page mismatch: PDF=$pdf_pages, YAML=$yaml_pages"
      add_issue "Verifier: $basename_md — OCR page count mismatch (PDF=$pdf_pages vs YAML=$yaml_pages)"
      ver_fail=$((ver_fail + 1))
    fi
    return
  fi

  # pdftotext-based files: full diff comparison
  local fresh_text fresh_chars
  fresh_text=$(pdftotext "$src_pdf" - 2>/dev/null) || true
  fresh_chars=$(echo "$fresh_text" | tr -d '[:space:]' | wc -c | tr -d ' ')

  if [ "$fresh_chars" -lt 50 ]; then
    log "[EMPTY] $basename_md — image-based PDF ($fresh_chars chars)"
    ver_empty=$((ver_empty + 1))
    return
  fi

  # Extract MD body (after frontmatter)
  local existing_body
  existing_body=$(sed -n '/^---$/,/^---$/!p' "$md_file" | sed '/^---$/d' | sed '/^$/N;/^\n$/d')

  # Normalize and diff
  local fresh_norm existing_norm diff_result
  fresh_norm=$(echo "$fresh_text" | sed '/^[[:space:]]*$/d')
  existing_norm=$(echo "$existing_body" | sed '/^[[:space:]]*$/d')
  diff_result=$(diff <(echo "$fresh_norm") <(echo "$existing_norm") 2>&1) || true

  if [ -z "$diff_result" ]; then
    log "[PASS] $basename_md"
    ver_pass=$((ver_pass + 1))
  else
    local diff_lines
    diff_lines=$(echo "$diff_result" | grep -c '^[<>]' || true)
    log "[FAIL] $basename_md — $diff_lines diff lines"
    verbose "$(echo "$diff_result" | head -6)"
    add_issue "Verifier: $basename_md — $diff_lines diff lines vs fresh extraction"
    ver_fail=$((ver_fail + 1))
  fi
}

# ============================================================
# Stage 3: Structural Checker
# ============================================================
stage3_structure() {
  local md_file="$1"
  local basename_md
  basename_md=$(basename "$md_file" .md)
  local issues_found=false

  local src_family=""
  src_family=$(grep '^  family:' "$md_file" 2>/dev/null | head -1 | sed 's/^  family: "//; s/"$//') || true

  # Check 1: YAML frontmatter completeness
  local has_source has_title has_converted
  has_source=$(grep -c '^source:' "$md_file" 2>/dev/null) || has_source=0
  has_title=$(grep -c '^  title:' "$md_file" 2>/dev/null) || has_title=0
  has_converted=$(grep -c '^  converted:' "$md_file" 2>/dev/null) || has_converted=0

  local missing_fields=""
  [ "$has_source" -eq 0 ] && missing_fields+="source "
  [ "$has_title" -eq 0 ] && missing_fields+="title "
  [ "$has_converted" -eq 0 ] && missing_fields+="converted "

  # Family-specific frontmatter checks
  if [ "$src_family" = "REGULATION" ] || [ "$src_family" = "STATUTE" ]; then
    # Structured chunks need chunk_type and chunk_id
    local has_chunk_type has_chunk_id
    has_chunk_type=$(grep -c '^  chunk_type:' "$md_file" 2>/dev/null) || has_chunk_type=0
    has_chunk_id=$(grep -c '^  chunk_id:' "$md_file" 2>/dev/null) || has_chunk_id=0
    [ "$has_chunk_type" -eq 0 ] && missing_fields+="chunk_type "
    [ "$has_chunk_id" -eq 0 ] && missing_fields+="chunk_id "
  else
    # PDF-based files need path and pages
    local has_path has_pages
    has_path=$(grep -c '^  path:' "$md_file" 2>/dev/null) || has_path=0
    has_pages=$(grep -c '^  pages:' "$md_file" 2>/dev/null) || has_pages=0
    [ "$has_path" -eq 0 ] && missing_fields+="path "
    [ "$has_pages" -eq 0 ] && missing_fields+="pages "
  fi

  if [ -n "$missing_fields" ]; then
    add_issue "Structure: $basename_md — missing frontmatter: $missing_fields"
    issues_found=true
  fi

  # Check 2: Directory-content consistency
  local dir_name
  dir_name=$(basename "$(dirname "$md_file")")

  # MFDS directory checks
  if [ "$dir_name" = "01-의료기기법" ]; then
    if ! head -30 "$md_file" | grep -q '의료기기' 2>/dev/null; then
      add_issue "Structure: $basename_md — in 01-의료기기법/ but '의료기기' not in header"
      issues_found=true
    fi
  elif [ "$dir_name" = "02-체외진단의료기기법" ]; then
    if ! head -30 "$md_file" | grep -q '체외진단' 2>/dev/null; then
      add_issue "Structure: $basename_md — in 02-체외진단/ but '체외진단' not in header"
      issues_found=true
    fi
  elif [ "$dir_name" = "03-디지털의료제품법" ]; then
    if ! head -30 "$md_file" | grep -q '디지털' 2>/dev/null; then
      add_issue "Structure: $basename_md — in 03-디지털/ but '디지털' not in header"
      issues_found=true
    fi
  fi

  # FDA directory checks
  if echo "$md_file" | grep -q "fda/01-statute/"; then
    if ! head -30 "$md_file" | grep -qi 'U\.S\.C\.\|United States Code\|FD&C' 2>/dev/null; then
      # Statute files should reference U.S.C. in frontmatter or heading
      if ! grep -q 'chunk_id.*U\.S\.C' "$md_file" 2>/dev/null; then
        add_issue "Structure: $basename_md — in fda/01-statute/ but no U.S.C. reference"
        issues_found=true
      fi
    fi
  elif echo "$md_file" | grep -q "fda/02-regulation/"; then
    if ! grep -q 'chunk_id.*Part' "$md_file" 2>/dev/null; then
      add_issue "Structure: $basename_md — in fda/02-regulation/ but no Part reference in chunk_id"
      issues_found=true
    fi
  fi

  # Check 3: Empty body detection
  local body_chars
  body_chars=$(awk '/^---$/{n++; next} n>=2' "$md_file" | tr -d '[:space:]' | wc -c | tr -d ' ')
  if [ "$body_chars" -lt 50 ]; then
    add_issue "Structure: $basename_md — empty or near-empty body ($body_chars chars)"
    issues_found=true
  fi

  # Check 4: Encoding sanity (control characters) — macOS grep doesn't support -P
  local garbled_count
  garbled_count=$(tr -d '[:print:][:space:]' < "$md_file" | wc -c | tr -d ' ') || garbled_count=0
  if [ "$garbled_count" -gt 500 ]; then
    add_issue "Structure: $basename_md — $garbled_count non-printable characters"
    issues_found=true
  fi

  # Check 5: Quality warnings (non-fatal)
  local total_lines non_empty short_count short_ratio_pct
  total_lines=$(wc -l < "$md_file" | tr -d ' ')
  non_empty=$(grep -c '[^[:space:]]' "$md_file" 2>/dev/null) || non_empty=0
  short_count=$(awk '/^.{1,3}$/' "$md_file" | wc -l | tr -d ' ') || short_count=0
  if [ "$non_empty" -gt 0 ]; then
    short_ratio_pct=$((short_count * 100 / non_empty))
  else
    short_ratio_pct=0
  fi
  if [ "$short_ratio_pct" -gt 20 ]; then
    add_issue "Structure: $basename_md — WARN: short_line_ratio ${short_ratio_pct}% (possible table layout issue)"
  fi
  if [ "$garbled_count" -gt 500 ] && [ "$garbled_count" -le 2000 ]; then
    # Already FAILed above for >500, but add WARN note for borderline cases
    :
  fi

  if $issues_found; then
    log "[FAIL] $basename_md"
    str_fail=$((str_fail + 1))
  else
    log "[OK] $basename_md"
    str_ok=$((str_ok + 1))
  fi
}

# ============================================================
# Stage 4: Index Checker (EU + FDA)
# ============================================================
reg_ok=0; reg_fail=0

stage4_index_check() {
  local base_dir="$1"
  local label="$2"

  log ""
  log "======================================="
  log " Stage 4: $label Index Checker"
  log "======================================="
  log ""

  # Find all directories containing _index.yaml
  local found_any=false
  for index_file in $(find "$base_dir" -name "_index.yaml" 2>/dev/null | sort); do
    found_any=true
    local parent_dir
    parent_dir=$(dirname "$index_file")
    local dir_name
    dir_name=$(basename "$parent_dir")

    # Count chunks listed in _index.yaml
    local yaml_chunks
    yaml_chunks=$(grep -c '  - file:' "$index_file" 2>/dev/null) || yaml_chunks=0

    # Count actual .md files
    local actual_files
    actual_files=$(find "$parent_dir" -maxdepth 1 -name "*.md" -not -name "_*" | wc -l | tr -d ' ')

    if [ "$yaml_chunks" -ne "$actual_files" ]; then
      add_issue "$label: $dir_name — _index.yaml has $yaml_chunks chunks but $actual_files .md files"
      log "[FAIL] $dir_name — chunk count mismatch: index=$yaml_chunks files=$actual_files"
      reg_fail=$((reg_fail + 1))
    else
      log "[OK] $dir_name — $yaml_chunks chunks match"
      reg_ok=$((reg_ok + 1))
    fi

    # Verify each file listed in _index.yaml exists
    local missing_from_index=0
    while IFS= read -r chunk_file; do
      chunk_file=$(echo "$chunk_file" | sed 's/.*- file: //' | tr -d ' ')
      if [ ! -f "${parent_dir}/${chunk_file}" ]; then
        add_issue "$label: $dir_name — listed in _index.yaml but missing: $chunk_file"
        missing_from_index=$((missing_from_index + 1))
      fi
    done < <(grep '  - file:' "$index_file")

    if [ "$missing_from_index" -gt 0 ]; then
      log "[FAIL] $dir_name — $missing_from_index files listed in _index.yaml but missing"
      reg_fail=$((reg_fail + 1))
    fi
  done

  if ! $found_any; then
    log "  (no _index.yaml files found)"
  fi

  log ""
  log "$label Index: OK=$reg_ok FAIL=$reg_fail"
}

# ============================================================
# Main
# ============================================================

# Collect target files into temp file (avoids subshell issues with pipe+while)
FILE_LIST=$(mktemp)
trap "rm -f $ISSUE_LOG $FILE_LIST" EXIT

if [ -n "$TARGET_FILE" ]; then
  echo "$TARGET_FILE" > "$FILE_LIST"
else
  case $SCOPE in
    mfds)
      find "$MFDS_DST_BASE" -name "*.md" | sort > "$FILE_LIST"
      ;;
    eu)
      find "$EU_DST_BASE" -name "*.md" | sort > "$FILE_LIST"
      ;;
    fda)
      find "$FDA_DST_BASE" -name "*.md" | sort > "$FILE_LIST"
      ;;
    all)
      { find "$MFDS_DST_BASE" -name "*.md" 2>/dev/null; find "$EU_DST_BASE" -name "*.md" 2>/dev/null; find "$FDA_DST_BASE" -name "*.md" 2>/dev/null; } | sort > "$FILE_LIST"
      ;;
  esac
fi
TOTAL=$(wc -l < "$FILE_LIST" | tr -d ' ')

# Initialize report
cat > "$REPORT_FILE" << HEADER
# Knowledge DB 3-Agent 검증 리포트

Report date: $(date '+%Y-%m-%d %H:%M')

HEADER

# ---- Stage 1 ----
if [ "$STAGE" = "all" ] || [ "$STAGE" = "1" ]; then
  log ""
  log "======================================="
  log " Stage 1: Extractor ($TOTAL files)"
  log "======================================="
  log ""
  while IFS= read -r f; do
    stage1_extract "$f"
  done < "$FILE_LIST"
  log ""
  log "Extractor: OK=$ext_ok WARN=$ext_warn FAIL=$ext_fail"
fi

# ---- Stage 2 ----
if [ "$STAGE" = "all" ] || [ "$STAGE" = "2" ]; then
  log ""
  log "======================================="
  log " Stage 2: Verifier ($TOTAL files)"
  log "======================================="
  log ""
  while IFS= read -r f; do
    stage2_verify "$f"
  done < "$FILE_LIST"
  log ""
  log "Verifier: PASS=$ver_pass FAIL=$ver_fail EMPTY=$ver_empty SKIP=$ver_skip"
fi

# ---- Stage 3 ----
if [ "$STAGE" = "all" ] || [ "$STAGE" = "3" ]; then
  log ""
  log "======================================="
  log " Stage 3: Structural Checker ($TOTAL files)"
  log "======================================="
  log ""
  while IFS= read -r f; do
    stage3_structure "$f"
  done < "$FILE_LIST"
  log ""
  log "Structure: OK=$str_ok FAIL=$str_fail"
fi

# ---- Stage 4 (Index check for EU + FDA) ----
if [ "$STAGE" = "all" ] || [ "$STAGE" = "4" ]; then
  if [ "$SCOPE" = "eu" ] || [ "$SCOPE" = "all" ]; then
    if [ -d "$EU_DST_BASE" ]; then
      stage4_index_check "$EU_DST_BASE" "EU"
    fi
  fi
  if [ "$SCOPE" = "fda" ] || [ "$SCOPE" = "all" ]; then
    if [ -d "$FDA_DST_BASE" ]; then
      stage4_index_check "$FDA_DST_BASE" "FDA"
    fi
  fi
fi

# ---- Summary ----
log ""
log "======================================="
log " 종합 결과"
log "======================================="
log ""
log "Total files: $TOTAL"
log ""
log "Stage 1 (Extractor):  OK=$ext_ok  WARN=$ext_warn  FAIL=$ext_fail"
log "Stage 2 (Verifier):   PASS=$ver_pass  FAIL=$ver_fail  EMPTY=$ver_empty  SKIP=$ver_skip"
log "Stage 3 (Structure):  OK=$str_ok  FAIL=$str_fail"
if [ "$reg_ok" -gt 0 ] || [ "$reg_fail" -gt 0 ]; then
  log "Stage 4 (Index):      OK=$reg_ok  FAIL=$reg_fail"
fi

# Write report summary
{
  echo "## Summary"
  echo ""
  echo "| Stage | OK/PASS | FAIL | Other |"
  echo "|-------|---------|------|-------|"
  echo "| Extractor | $ext_ok | $ext_fail | WARN=$ext_warn |"
  echo "| Verifier | $ver_pass | $ver_fail | EMPTY=$ver_empty, SKIP=$ver_skip |"
  echo "| Structure | $str_ok | $str_fail | — |"
  if [ "$reg_ok" -gt 0 ] || [ "$reg_fail" -gt 0 ]; then
    echo "| Index | $reg_ok | $reg_fail | — |"
  fi
  echo ""
} >> "$REPORT_FILE"

# Write issues
issue_count=$(wc -l < "$ISSUE_LOG" | tr -d ' ')
if [ "$issue_count" -gt 0 ]; then
  log ""
  log "Issues found: $issue_count"
  {
    echo "## Issues"
    echo ""
    while IFS= read -r line; do
      echo "- $line"
    done < "$ISSUE_LOG"
    echo ""
  } >> "$REPORT_FILE"
else
  log ""
  log "No issues found."
  echo "No issues found." >> "$REPORT_FILE"
fi

log ""
log "Report saved: $REPORT_FILE"

# Exit code
total_fail=$((ext_fail + ver_fail + str_fail + reg_fail))
if [ "$total_fail" -gt 0 ]; then
  exit 1
fi
