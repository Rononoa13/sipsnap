# SipSnap Real-World Menu Dataset

This directory contains real-world menu photographs used to evaluate SipSnap's
menu extraction accuracy.

## Purpose

The dataset is separate from automated unit/API tests.

It is used to evaluate:

- item extraction
- missing items
- incorrect items
- price accuracy
- category accuracy
- latency
- complete processing failures

## Planned structure

```text
test-menus/
├── README.md
├── images/
│   ├── 001.jpg
│   ├── 002.jpg
│   └── ...
└── expected/
    ├── 001.json
    ├── 002.json
    └── ...