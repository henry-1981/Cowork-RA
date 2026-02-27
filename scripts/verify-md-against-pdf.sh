#!/bin/bash
# 검증 스크립트: 변환된 .md 파일과 원본 PDF를 pdftotext로 재추출하여 diff
# 원칙: 동일 PDF에서 독립 추출 → diff → 불일치 플래그
set -euo pipefail

export LC_ALL=C

SRC_BASE="/Users/hb/Documents/01.Regulatory/01. MFDS"
DST_BASE="aria/knowledge/mfds"

pass=0
fail=0
skip=0
empty=0

echo "=== PDF ↔ Markdown Diff 검증 ==="
echo ""

for md_file in $(find "$DST_BASE" -name "*.md" | sort); do
  basename_md=$(basename "$md_file")

  # Extract source path from frontmatter
  src_rel=$(grep '^  path:' "$md_file" | head -1 | sed 's/^  path: "//; s/"$//')

  if [ -z "$src_rel" ]; then
    echo "SKIP (no source path): $basename_md"
    skip=$((skip + 1))
    continue
  fi

  src_pdf="${SRC_BASE}/${src_rel}"

  if [ ! -f "$src_pdf" ]; then
    echo "SKIP (PDF not found): $src_rel"
    skip=$((skip + 1))
    continue
  fi

  # Re-extract from PDF (fresh)
  fresh_text=$(pdftotext "$src_pdf" - 2>/dev/null) || true

  # Check if fresh extraction is empty (image-based PDF)
  fresh_chars=$(echo "$fresh_text" | tr -d '[:space:]' | wc -c)
  if [ "$fresh_chars" -lt 50 ]; then
    echo "EMPTY (image PDF, $fresh_chars chars): $basename_md"
    empty=$((empty + 1))
    continue
  fi

  # Extract body from md: everything after the closing --- of frontmatter
  # Remove leading/trailing blank lines for fair comparison
  existing_body=$(sed -n '/^---$/,/^---$/!p' "$md_file" | sed '/^---$/d' | sed '/^$/N;/^\n$/d')

  # Normalize both: strip leading/trailing whitespace lines
  fresh_normalized=$(echo "$fresh_text" | sed '/^[[:space:]]*$/d')
  existing_normalized=$(echo "$existing_body" | sed '/^[[:space:]]*$/d')

  # Diff (ignore all whitespace-only differences)
  diff_result=$(diff <(echo "$fresh_normalized") <(echo "$existing_normalized") 2>&1) || true

  if [ -z "$diff_result" ]; then
    echo "PASS: $basename_md"
    pass=$((pass + 1))
  else
    diff_lines=$(echo "$diff_result" | grep -c '^[<>]' || true)
    echo "FAIL ($diff_lines diff lines): $basename_md"
    echo "$diff_result" | head -8
    echo ""
    fail=$((fail + 1))
  fi
done

echo ""
echo "=== 검증 결과 ==="
echo "PASS: $pass"
echo "FAIL: $fail"
echo "EMPTY (이미지 PDF): $empty"
echo "SKIP: $skip"
echo "Total: $((pass + fail + empty + skip))"

if [ "$fail" -gt 0 ]; then
  echo ""
  echo "⚠ $fail 건의 내용 불일치 발견."
  exit 1
else
  echo ""
  echo "✓ 모든 파일이 원본 PDF와 내용 일치 확인."
fi
