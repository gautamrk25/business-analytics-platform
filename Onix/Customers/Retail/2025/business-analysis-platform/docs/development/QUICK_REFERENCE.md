# Quick Reference Card - Always Follow This Order

## 🔴 STOP! Before ANY Implementation:

```bash
# 1. Check what to do next
cat PROJECT_STATUS.md | grep -A 10 "Current Focus"

# 2. Verify dependencies
cat IMPLEMENTATION_SEQUENCE.md | grep -A 20 "Phase"

# 3. Read workflow
cat DEVELOPMENT_WORKFLOW.md
```

## 📋 Implementation Steps (NEVER SKIP):

1. **STATUS** → Check PROJECT_STATUS.md
2. **TESTS** → Write tests FIRST (TDD_CHECKLIST.md)
3. **CODE** → Implement (CLAUDE.md patterns)
4. **VERIFY** → Run all tests
5. **UPDATE** → Update PROJECT_STATUS.md

## 🔍 Key Files by Purpose:

| What I Need | Which File |
|------------|------------|
| What to do next? | PROJECT_STATUS.md |
| How to implement? | CLAUDE.md |
| Test requirements? | TDD_CHECKLIST.md |
| Build order? | IMPLEMENTATION_SEQUENCE.md |
| API specs? | backend_api_design.md |
| Agent design? | AI_AGENTS_IMPLEMENTATION.md |
| Troubleshooting? | ERROR_RECOVERY.md |

## ⚡ Commands to Always Run:

```bash
# Start of session
grep -A 10 "Current Focus" PROJECT_STATUS.md

# Before coding
grep -A 20 "Phase 2" IMPLEMENTATION_SEQUENCE.md

# After implementation
python -m pytest tests/ -v
```

## ❌ Never Do This:
- Skip tests
- Implement without checking status
- Forget to update docs
- Code without reading patterns

## ✅ Always Do This:
- Check PROJECT_STATUS.md first
- Write tests before code
- Follow DEVELOPMENT_WORKFLOW.md
- Update status after completion

**Remember:** DEVELOPMENT_WORKFLOW.md is your bible!