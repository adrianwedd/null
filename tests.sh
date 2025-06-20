#!/bin/bash
set -e
# Check word count of SELF_AUDIT
wc_word=$(wc -w < SELF_AUDIT.md)
if [ "$wc_word" -lt 5000 ]; then
  echo "SELF_AUDIT.md must be at least 5000 words, found $wc_word" >&2
  exit 1
fi
# Ensure no placeholders remain
if grep -R "{{" SELF_AUDIT.md AGENTS.md CODEX_TASKS.md README.md; then
  echo "Placeholders detected" >&2
  exit 1
fi
# Check agent count
agent_count=$(grep -c '^I am \*\*' AGENTS.md)
if [ "$agent_count" -lt 8 ]; then
  echo "Expected at least 8 agents, found $agent_count" >&2
  exit 1
fi
# Check number of codex tasks
task_count=$(grep -c '^id:' CODEX_TASKS.md)
if [ "$task_count" -lt 20 ] || [ "$task_count" -gt 30 ]; then
  echo "Expected 20-30 tasks, found $task_count" >&2
  exit 1
fi
# Check axis coverage
for axis in Security Privacy Reliability Ethics Sustainability TechDebt ProcessDebt; do
  count=$(grep -c "axis: $axis" CODEX_TASKS.md)
  if [ "$count" -lt 2 ]; then
    echo "Axis $axis appears only $count times" >&2
    exit 1
  fi
done

echo "All tests passed."
