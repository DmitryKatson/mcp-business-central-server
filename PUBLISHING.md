# Publishing to PyPI Guide

## Prerequisites

1. **PyPI Account**
   - Create account at https://pypi.org/
   - Enable 2FA for security
   - Create API token for secure uploads

2. **Install Build Tools**
   ```bash
   pip install build twine
   ```

## Manual Publishing Process

### 1. Prepare Release

```bash
# Update version in pyproject.toml if needed
# Commit all changes
git add .
git commit -m "Prepare for release v1.0.1"
```

### 2. Build Package

```bash
# Clean previous builds (if they exist)
rm -rf dist/ build/
find . -name "*.egg-info" -type d -exec rm -rf {} + 2>/dev/null || true

# Build distribution packages
python -m build
```

This creates:
- `dist/mcp_business_central-1.0.0-py3-none-any.whl` (wheel)
- `dist/mcp-business-central-1.0.0.tar.gz` (source distribution)

### 3. Test Upload (Recommended)

```bash
# Upload to Test PyPI first
twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ mcp-business-central
```

### 4. Production Upload

```bash
# Upload to production PyPI
twine upload dist/*
```

### 5. Tag Release

```bash
git tag v1.0.0
git push origin v1.0.0
```

## Automated Publishing (GitHub Actions)

The repository includes a GitHub Actions workflow that automatically:
1. Builds the package when you push a git tag
2. Publishes to PyPI
3. Creates a GitHub release

### Setup Automated Publishing

1. **Add PyPI API Token to GitHub Secrets**
   - Go to your repository Settings → Secrets and variables → Actions
   - Add new repository secret: `PYPI_API_TOKEN`
   - Value: Your PyPI API token (starts with `pypi-`)

2. **Create Release**
   ```bash
   git tag v1.0.1
   git push origin v1.0.1
   ```

The workflow will automatically build and publish to PyPI.

## Version Management

Update version in `pyproject.toml`:

```toml
[project]
name = "mcp-business-central"
version = "1.0.1"  # Update this
```

## Troubleshooting

### Common Issues

1. **Authentication Error**
   ```bash
   twine upload --username __token__ --password your-api-token dist/*
   ```

2. **Version Already Exists**
   - PyPI doesn't allow re-uploading the same version
   - Increment version number in `pyproject.toml`

3. **Build Failures**
   ```bash
   # Check for syntax errors
   python -m py_compile src/mcp_business_central/**/*.py
   
   # Validate package structure
   python -m build --check
   ```

## Verification

After publishing, verify the package:

```bash
# Install from PyPI
pip install mcp-business-central

# Test the installation
mcp-business-central --help
```

## Best Practices

1. **Always test on Test PyPI first**
2. **Use semantic versioning** (MAJOR.MINOR.PATCH)
3. **Update changelog** before releasing
4. **Tag releases** in git for traceability
5. **Test installation** after publishing
