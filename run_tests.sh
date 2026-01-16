#!/bin/bash
# run_tests.sh - Run all tests and auto-commit on success

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                  RUNNING TEST SUITE                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if containers are running
if ! docker-compose ps | grep -q "web.*Up"; then
    echo "🐳 Starting Docker containers..."
    docker-compose up -d
    sleep 3
fi

echo "🧪 Running tests..."
echo ""

# Run pytest and capture output
TEST_OUTPUT=$(docker-compose exec -T web python -m pytest tests/ -v --tb=short 2>&1)
TEST_EXIT_CODE=$?

# Display test output
echo "$TEST_OUTPUT"

# Count passing tests
PASS_COUNT=$(echo "$TEST_OUTPUT" | grep -c "PASSED" || echo "0")
FAIL_COUNT=$(echo "$TEST_OUTPUT" | grep -c "FAILED" || echo "0")

echo ""
echo "╔════════════════════════════════════════════════════════════╗"

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "║           ✅ ALL TESTS PASSED ($PASS_COUNT/$PASS_COUNT)              ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    
    # Auto-commit
    COMMIT_MSG="✓ All $PASS_COUNT tests passing - auto-commit [$PASS_COUNT/$PASS_COUNT tests]"
    
    echo "📝 Auto-committing..."
    git add -A
    git commit -m "$COMMIT_MSG" || echo "⚠️  Nothing new to commit"
    
    echo ""
    echo "🚀 Auto-pushing to master..."
    git push origin master || echo "⚠️  Nothing to push"
    
    echo ""
    echo "✅ Tests passed, code committed and pushed!"
    echo ""
    exit 0
else
    echo "║           ❌ TESTS FAILED ($FAIL_COUNT failures)            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo "❌ Tests failed. Fix the issues and try again."
    echo ""
    exit 1
fi
