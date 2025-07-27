# Changelog and Commit Message Conventions

Guidelines for writing changelog entries and commit messages in the 925stackai project.

## Commit Message Format

### Conventional Commits Standard

This project follows the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types

* **feat**: A new feature for the user
* **fix**: A bug fix for the user
* **docs**: Documentation changes
* **style**: Code style changes (formatting, missing semicolons, etc.)
* **refactor**: Code refactoring without changing functionality
* **perf**: Performance improvements
* **test**: Adding or updating tests
* **build**: Changes to build system or dependencies
* **ci**: Changes to CI/CD configuration
* **chore**: Maintenance tasks, tool updates

### Scope Examples

* **agents**: Changes to agent implementations
* **api**: API endpoint modifications
* **ui**: Streamlit interface updates
* **pricing**: Quote calculation logic
* **memory**: Memory persistence system
* **config**: Configuration changes
* **deploy**: Deployment-related changes

### Example Commit Messages

```bash
# Feature additions
feat(agents): add analysis agent for business metrics
feat(api): implement quote history endpoint
feat(ui): add real-time quote preview in chat

# Bug fixes
fix(pricing): correct travel charge calculation for distances >20km
fix(memory): resolve vector store indexing issue
fix(ui): handle empty response from quoting agent

# Documentation
docs(api): update endpoint documentation with examples
docs(agents): add memory agent integration guide
docs: update installation instructions for Windows

# Refactoring
refactor(pricing): extract calculation logic into separate modules
refactor(agents): simplify agent orchestrator interface

# Performance improvements
perf(memory): optimize vector search query performance
perf(api): add response caching for quote requests

# Testing
test(agents): add unit tests for quoting agent edge cases
test(integration): add end-to-end quote generation tests

# Build and deployment
build: update dependencies to latest stable versions
ci: add automated testing workflow
deploy: configure Docker health checks
```

### Multi-line Commit Messages

For complex changes, use the body and footer sections:

```bash
feat(agents): add customer segmentation analysis

Implement new analysis capabilities including:
- Customer lifetime value calculation
- Behavioral pattern recognition  
- Geographic clustering analysis
- Seasonal trend detection

The analysis agent integrates with the existing memory
system and provides REST API endpoints for external access.

Closes #123
Co-authored-by: Jane Smith <jane@example.com>
```

## Changelog Format

### Structure

Changelogs follow the [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New features that have been added

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Now removed features

### Fixed
- Any bug fixes

### Security
- Vulnerability fixes

## [1.2.0] - 2024-07-15

### Added
- Analysis agent for business metrics and insights
- Customer segmentation capabilities
- Real-time quote preview in Streamlit UI
- API endpoint for quote history retrieval

### Changed
- Improved quote calculation performance by 40%
- Updated pricing structure for 2024 rates
- Enhanced error handling in memory persistence

### Fixed
- Travel charge calculation for distances over 20km
- Vector store indexing issue causing slow searches
- Streamlit UI timeout errors during quote generation

### Security
- Added API rate limiting
- Implemented request validation for all endpoints
```

### Version Numbering

Follow [Semantic Versioning](https://semver.org/) (SemVer):

* **MAJOR.MINOR.PATCH** (e.g., 2.1.0)
* **MAJOR**: Breaking changes or major new features
* **MINOR**: New features, backward compatible
* **PATCH**: Bug fixes, backward compatible

### Change Categories

* **Added**: New features, endpoints, capabilities
* **Changed**: Modifications to existing functionality
* **Deprecated**: Features marked for future removal
* **Removed**: Features that have been deleted
* **Fixed**: Bug fixes and corrections
* **Security**: Security-related improvements

## Branch Naming Conventions

### Branch Types

* **feature/**: New features (`feature/analysis-agent`)
* **bugfix/**: Bug fixes (`bugfix/travel-charge-calculation`)
* **hotfix/**: Critical fixes for production (`hotfix/security-patch`)
* **docs/**: Documentation updates (`docs/api-examples`)
* **refactor/**: Code refactoring (`refactor/agent-orchestrator`)
* **test/**: Testing improvements (`test/integration-tests`)

### Branch Naming Examples

```bash
# Good branch names
feature/customer-analytics-dashboard
bugfix/streamlit-connection-timeout
hotfix/pricing-calculation-error
docs/deployment-guide-docker
refactor/memory-agent-interface
test/quote-generation-edge-cases

# Avoid generic names
feature/new-feature
bugfix/fix-bug
update/changes
```

## Pull Request Guidelines

### PR Title Format

Use the same format as commit messages:

```
feat(agents): add business analytics dashboard
fix(pricing): resolve weekend surcharge calculation
docs: update API documentation with examples
```

### PR Description Template

```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] Changelog updated
```

## Release Process

### Pre-release Checklist

1. Update version numbers in relevant files
2. Update CHANGELOG.md with release notes
3. Run full test suite
4. Update documentation
5. Create release branch
6. Final testing and validation

### Release Commit Example

```bash
git commit -m "chore: release version 1.2.0

- Update version numbers across all modules
- Finalize changelog for v1.2.0 release
- Update documentation for new features"
```

### Tag Format

```bash
# Create annotated tag
git tag -a v1.2.0 -m "Release version 1.2.0

Major new features:
- Business analytics dashboard
- Enhanced quote calculation engine
- Improved API documentation

Bug fixes:
- Travel charge calculation accuracy
- Memory persistence stability"
```

## Automated Tools

### commitlint Configuration

The project uses commitlint to enforce commit message standards:

```javascript
// commitlint.config.cjs
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      [
        'feat',
        'fix',
        'docs', 
        'style',
        'refactor',
        'perf',
        'test',
        'build',
        'ci',
        'chore'
      ]
    ],
    'scope-enum': [
      2,
      'always',
      [
        'agents',
        'api',
        'ui',
        'pricing',
        'memory',
        'config',
        'deploy',
        'tests'
      ]
    ]
  }
};
```

### Git Hooks

Pre-commit hook example:

```bash
#!/bin/sh
# .git/hooks/pre-commit

# Run tests
npm run test
if [ $? -ne 0 ]; then
  echo "Tests must pass before commit."
  exit 1
fi

# Check commit message format
npx commitlint --edit $1
```

## Best Practices

### Commit Messages

1. **Use imperative mood**: "Add feature" not "Added feature"
2. **Keep subject line under 50 characters**
3. **Capitalize first letter of subject**
4. **No period at end of subject line**
5. **Use body to explain what and why, not how**

### Changelog Maintenance

1. **Update with every release**
2. **Group similar changes together**
3. **Use clear, user-focused language**
4. **Link to relevant issues/PRs**
5. **Include breaking change warnings**

### Version Management

1. **Follow semantic versioning strictly**
2. **Document breaking changes clearly**
3. **Provide migration guides for major versions**
4. **Test thoroughly before releasing**

These conventions ensure consistent, readable project history and make it easier for contributors to understand changes and for automated tools to generate releases and changelogs.
