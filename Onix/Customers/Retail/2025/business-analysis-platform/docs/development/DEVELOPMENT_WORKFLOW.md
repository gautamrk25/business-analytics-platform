# Development Workflow for Business Analysis Platform

## ⚠️ CRITICAL: Always Follow This Sequence

This document ensures consistent implementation by providing the exact workflow for every development task.

## 🎯 Pre-Development Checklist

Before implementing ANY feature, check these in order:

1. **Read PROJECT_STATUS.md**
   - Check current phase
   - Identify next priority task
   - Verify dependencies are complete

2. **Consult IMPLEMENTATION_SEQUENCE.md**
   - Confirm task is in correct phase
   - Check all dependencies are met
   - Review implementation rules

3. **Review CLAUDE.md**
   - Understand code patterns
   - Check style guidelines
   - Review API patterns

## 📋 Implementation Workflow

### For Every New Feature:

```
1. CHECK STATUS → 2. WRITE TESTS → 3. IMPLEMENT → 4. VERIFY → 5. UPDATE DOCS
```

### Step 1: Check Status
```python
# First command to run in every session:
cat PROJECT_STATUS.md | grep -A 10 "Current Focus"
```

### Step 2: Write Tests (TDD)
```bash
# Follow TDD_CHECKLIST.md exactly:
1. Create test file: tests/test_<component>.py
2. Write all test cases FIRST
3. Run tests to ensure they fail
4. Document expected behavior
```

### Step 3: Implement Feature
```bash
# Based on component type:
- Building Blocks → Follow building_block_system_design_backend_api.md
- API Endpoints → Follow backend_api_design.md
- AI Agents → Follow AI_AGENTS_IMPLEMENTATION.md
```

### Step 4: Verify Implementation
```bash
# Run tests
python -m pytest tests/test_<component>.py -v

# Check coverage
python -m pytest tests/test_<component>.py --cov=src/<component>

# Run all tests
python -m pytest tests/ -v
```

### Step 5: Update Documentation
```python
# Update PROJECT_STATUS.md with:
- [ ] Mark component as complete
- [ ] Update test status
- [ ] Add to daily progress
- [ ] Identify next task
```

## 🔄 Daily Development Routine

### Session Start:
```bash
# 1. Check current status
cat PROJECT_STATUS.md | grep -A 20 "Current Focus"

# 2. Read todo list
cat PROJECT_STATUS.md | grep "TODO"

# 3. Verify environment
python -m pytest --collect-only
```

### During Development:
```bash
# Always have these files open for reference:
- PROJECT_STATUS.md (current task)
- CLAUDE.md (patterns)
- TDD_CHECKLIST.md (testing)
- ERROR_RECOVERY.md (if issues)
```

### Session End:
```bash
# 1. Update PROJECT_STATUS.md
# 2. Commit with descriptive message
# 3. Document any blockers
```

## 📁 File Reference by Task Type

### Building Blocks:
1. IMPLEMENTATION_SEQUENCE.md → Check phase
2. TDD_CHECKLIST.md → Write tests
3. building_block_system_design_backend_api.md → Implementation

### API Endpoints:
1. backend_api_design.md → Endpoint specs
2. CLAUDE.md → FastAPI patterns
3. TDD_CHECKLIST.md → API tests

### AI Agents:
1. AI_AGENTS_IMPLEMENTATION.md → Architecture
2. TDD_CHECKLIST.md → Agent tests
3. CLAUDE.md → Async patterns

## 🚫 Common Mistakes to Avoid

1. **Never skip tests** - Always write tests first
2. **Never implement without checking dependencies**
3. **Never forget to update PROJECT_STATUS.md**
4. **Never proceed if tests are failing**

## 🔍 Quick Reference Commands

```bash
# Find next task
grep -A 5 "Current Focus" PROJECT_STATUS.md

# Check implementation order
grep -A 20 "Phase 2" IMPLEMENTATION_SEQUENCE.md

# Find coding patterns
grep -A 10 "FastAPI Structure" CLAUDE.md

# Check test requirements
grep -A 10 "Writing Tests" TDD_CHECKLIST.md
```

## 💡 Pro Tips

1. **Keep PROJECT_STATUS.md open** in another window
2. **Update status after EVERY component**
3. **Follow TDD religiously** - no exceptions
4. **Check dependencies before starting**

Remember: This workflow ensures consistency, quality, and prevents confusion!