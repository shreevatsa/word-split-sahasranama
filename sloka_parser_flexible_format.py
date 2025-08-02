"""Parser for the relaxed sloka input format.
Accepts input like your latest sample: no explicit headers. Structure per śloka:
  * (Optional leading blank lines)
  * One or more Devanāgarī lines (detected by presence of Devanagari characters) until a blank line
  * Segment lines: tokens and literals, with `display= n. lemma: meaning` format for tokens, `---` for line break, and any other line as literal (preserving spaces), until the start of the next śloka (which is two consecutive lines containing Devanagari characters) or EOF.

The script builds for each śloka:
  { dev: <Dev block string>, translitCanonical: <reconstructed from segments>, lines: [ [..first translit line..], [..second..], ... ] }

Usage:
  python flexible_prepare_slokas.py input.txt > slokas_output.js

Example output is a JS snippet: `const data = [...];` which you can paste into the viewer.
"""
import sys
import re
from typing import List, Dict, Any

def contains_devanagari(s: str) -> bool:
    return bool(re.search(r'[\u0900-\u097F]', s))

def parse_flexible(lines: List[str]) -> List[Dict[str, Any]]:
    i = 0
    n = len(lines)
    slokas = []
    while i < n:
        # skip leading blanks
        while i < n and not lines[i].strip():
            i += 1
        if i >= n:
            break
        # Expect Dev block: one or more consecutive lines containing Devanagari
        if not contains_devanagari(lines[i]):
            raise ValueError(f'Expected Devanagari line at {i+1}, got: {lines[i]!r}')
        devanagari_lines = []
        while i < n and lines[i].strip():
            # include lines even if they lack Devanagari after starting, to be permissive
            devanagari_lines.append(lines[i].rstrip('\n'))
            i += 1
        dev_block = '\n'.join(devanagari_lines)
        # skip blank(s)
        while i < n and not lines[i].strip():
            i += 1
        # Now collect segment lines until we detect start of next sloka or EOF
        segment_lines: List[str] = []
        while i < n:
            # check if this is potentially start of next sloka: two consecutive non-empty lines with Devanagari
            if contains_devanagari(lines[i]) and i+1 < n and lines[i+1].strip() and contains_devanagari(lines[i+1]):
                break  # do not consume; next loop will treat as new sloka
            # otherwise, consume line as segment (including blanks, because blank might separate groups)
            if not lines[i].endswith('\n'):
                segment_lines.append(lines[i])
            else:
                segment_lines.append(lines[i].rstrip('\n'))
            i += 1
        # parse segment_lines into structured lines (splitting on '---')
        token_re = re.compile(r'^([\s\S]+?)\s*=\s*(\d+)\.\s*([^:]+):\s*(.+)$')
        lines_parsed: List[List[Any]] = []
        current_line: List[Any] = []
        for raw in segment_lines:
            if raw.strip() == '---':
                lines_parsed.append(current_line)
                current_line = []
                continue
            m = token_re.match(raw)
            if m:
                display = m.group(1)
                nidx = int(m.group(2))
                lemma = m.group(3).strip()
                meaning = m.group(4).strip()
                current_line.append([display, f'{lemma}: {meaning}', nidx])
            else:
                if raw == '':
                    # preserve as empty literal (could be used for spacing) or skip? keep to match original intent
                    current_line.append('')
                else:
                    current_line.append(raw)
        if current_line or not lines_parsed:
            lines_parsed.append(current_line)
        # reconstruct canonical transliteration from segments for convenience
        def concat_segments(seg_lines):
            out = ''
            for line in seg_lines:
                for part in line:
                    if isinstance(part, list):
                        out += part[0]
                    else:
                        out += part
                out += '\n'
            return out.rstrip('\n')
        translit_canonical = concat_segments(lines_parsed)
        slokas.append({
            'dev': dev_block,
            'translitCanonical': translit_canonical,
            'lines': lines_parsed
        })
    return slokas

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python flexible_prepare_slokas.py <input.txt>')
        sys.exit(1)
    path = sys.argv[1]
    with open(path, encoding='utf-8') as f:
        raw_lines = f.readlines()
    # Normalize newlines and keep originals for blank detection
    slokas = parse_flexible(raw_lines)
    import json
    # Output JS data snippet
    print('const data = ' + json.dumps(slokas, ensure_ascii=False, indent=2) + ';')
