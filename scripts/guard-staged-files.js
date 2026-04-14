#!/usr/bin/env node

/**
 * Root repository commit guard:
 * 1) blocks temporary/debug files from being committed
 * 2) blocks UTF-8 BOM in text files
 * 3) blocks obvious mojibake markers and replacement char U+FFFD in text files
 */

const { execFileSync } = require('node:child_process');
const path = require('node:path');

const TEXT_FILE_EXTENSIONS = new Set([
  '.ts',
  '.tsx',
  '.js',
  '.jsx',
  '.mjs',
  '.cjs',
  '.json',
  '.md',
  '.txt',
  '.yml',
  '.yaml',
  '.css',
  '.scss',
  '.html',
  '.xml',
  '.csv',
  '.ndjson',
  '.toml',
]);

const TEMP_FILE_PATTERNS = [
  /(^|\/)\.tmp[-_.]/i,
  /(^|\/)tmp[-_.]/i,
  /(^|\/)tmp-head-/i,
  /\.tmp$/i,
  /\.bak$/i,
  /\.orig$/i,
  /\.swp$/i,
  /\.swo$/i,
];

const MOJIBAKE_MARKERS = [
  '鏀惰棌',
  '閲婁箟',
  '渚嬪彞',
  '鍗曡瘝',
  '鐭ヨ瘑',
  '璇剧▼',
  '宸插',
  '涓嬩竴',
  '鍙ｈ',
  '杩戜箟',
];

function runGit(args, asBuffer = false) {
  return execFileSync('git', args, {
    encoding: asBuffer ? null : 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  });
}

function tryRunGit(args, asBuffer = false) {
  try {
    return runGit(args, asBuffer);
  } catch {
    return asBuffer ? Buffer.alloc(0) : '';
  }
}

function getStagedFiles() {
  const output = runGit(['diff', '--cached', '--name-only', '--diff-filter=ACMR']);
  return output
    .split(/\r?\n/g)
    .map((line) => line.trim())
    .filter(Boolean);
}

function isLikelyTextFile(filePath, bytes) {
  const ext = path.extname(filePath).toLowerCase();
  if (TEXT_FILE_EXTENSIONS.has(ext)) return true;
  if (bytes.length === 0) return true;
  for (let i = 0; i < bytes.length; i += 1) {
    if (bytes[i] === 0x00) return false;
  }
  return true;
}

function hasBOM(bytes) {
  return bytes.length >= 3 && bytes[0] === 0xef && bytes[1] === 0xbb && bytes[2] === 0xbf;
}

function collectViolations(files) {
  const blockedTempFiles = [];
  const bomViolations = [];
  const mojibakeViolations = [];

  files.forEach((file) => {
    const normalized = file.replace(/\\/g, '/');
    if (TEMP_FILE_PATTERNS.some((pattern) => pattern.test(normalized))) {
      blockedTempFiles.push(file);
    }

    let bytes;
    try {
      bytes = runGit(['show', `:${file}`], true);
    } catch {
      return;
    }

    if (!isLikelyTextFile(file, bytes)) return;
    if (hasBOM(bytes)) {
      bomViolations.push(file);
    }

    const text = bytes.toString('utf8');
    const headText = tryRunGit(['show', `HEAD:${file}`], true).toString('utf8');
    const stagedReplacementCount = (text.match(/\uFFFD/g) || []).length;
    const headReplacementCount = (headText.match(/\uFFFD/g) || []).length;
    if (stagedReplacementCount > headReplacementCount) {
      mojibakeViolations.push(`${file} (new replacement char U+FFFD found)`);
      return;
    }

    // Allow this guard script to carry marker literals for detection rules.
    if (normalized === 'scripts/guard-staged-files.js') {
      return;
    }

    const marker = MOJIBAKE_MARKERS.find((item) => {
      const stagedCount = (text.match(new RegExp(item, 'g')) || []).length;
      const headCount = (headText.match(new RegExp(item, 'g')) || []).length;
      return stagedCount > headCount;
    });
    if (marker) {
      mojibakeViolations.push(`${file} (new marker: ${marker})`);
    }
  });

  return { blockedTempFiles, bomViolations, mojibakeViolations };
}

function printList(title, list) {
  if (!list.length) return;
  process.stderr.write(`\n[guard] ${title}\n`);
  list.forEach((item) => process.stderr.write(`  - ${item}\n`));
}

function main() {
  const files = getStagedFiles();
  if (files.length === 0) {
    process.stdout.write('[guard] No staged files. Skip.\n');
    return;
  }

  const { blockedTempFiles, bomViolations, mojibakeViolations } = collectViolations(files);
  const failed = blockedTempFiles.length > 0 || bomViolations.length > 0 || mojibakeViolations.length > 0;
  if (!failed) {
    process.stdout.write('[guard] Staged file guard passed.\n');
    return;
  }

  process.stderr.write('\n[guard] Commit blocked by staged file constraints.\n');
  printList('Temporary/debug files are not allowed:', blockedTempFiles);
  printList('UTF-8 BOM found (must be UTF-8 without BOM):', bomViolations);
  printList('Mojibake/replacement-char found:', mojibakeViolations);
  process.stderr.write('\n[guard] Fix the listed files and commit again.\n');
  process.exit(1);
}

main();
