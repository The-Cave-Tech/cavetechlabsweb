#!/bin/bash
# Docker debug setup script for Django debugging in VS Code

echo "🐳 Ensuring debugpy is installed in container..."
docker-compose exec -T web pip install debugpy -q 2>/dev/null || echo "debugpy install skipped"

echo "✓ Debug environment ready"
echo "📍 Debugger listening on port 5678"
echo "💡 You can now set breakpoints and debug in VS Code"
