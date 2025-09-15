# List available commands
default:
    @just --list

# Install all dependencies including dev tools
install:
    uv sync
    uv pip install mypy ruff pandas-stubs

# Format code with ruff
format:
    uv run ruff format src/ simple_example.py
    uv run ruff check --fix src/ simple_example.py

# Lint code with ruff
lint:
    uv run ruff check src/ simple_example.py

# Type check with mypy
type-check:
    uv run mypy src/ simple_example.py

# Run the example
run:
    uv run python simple_example.py

# Clean up generated files
clean:
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete
    rm -rf .mypy_cache .ruff_cache

# Run all checks (format, lint, type-check)
check: format lint type-check

# Full workflow: install, check, and run
all: install check run

# Watch for changes and run checks
watch:
    watchexec -e py -- just check

# Create a new git commit
commit message:
    git add -A
    git commit -m "{{message}}"