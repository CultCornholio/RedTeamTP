# Contributing to RedTeamTP

First off, thanks for taking the time to contribute! 🎉👍

The following is a set of guidelines for contributing to RedTeamTP. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

- **Check if the bug has already been reported** by searching on GitHub under [Issues](https://github.com/CultCornholio/RedTeamTP/issues).
- If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/CultCornholio/RedTeamTP/issues/new). Be sure to include:
  - A clear title and description
  - As much relevant information as possible
  - A code sample or an executable test case demonstrating the expected behavior that is not occurring
  - Steps to reproduce the issue

### Suggesting Enhancements

- **Check if the enhancement has already been suggested** by searching on GitHub under [Issues](https://github.com/CultCornholio/RedTeamTP/issues).
- If you don't find an open issue addressing the enhancement, [open a new one](https://github.com/CultCornholio/RedTeamTP/issues/new).
  - Use a clear and descriptive title
  - Provide a detailed description of the suggested enhancement
  - Explain why this enhancement would be useful to most RedTeamTP users

### Pull Requests

1. Fork the repository
2. Create a branch for your feature or fix (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Run the tests to ensure they pass
5. Commit your changes with descriptive commit messages
6. Push to your branch (`git push origin feature/your-feature-name`)
7. Open a Pull Request

#### Pull Request Guidelines

- Update the README.md with details of changes to the interface, if appropriate
- Update the documentation with any changes to the API
- The PR should work for Python 3.10+
- Include or update tests for your changes
- Ensure all CI checks pass
- Follow the style guidelines

## Development Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```
3. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Testing

- Write tests for new features and bug fixes
- Run tests before submitting a PR:
  ```bash
  pytest tests/
  ```

## Style Guidelines

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [flake8](https://flake8.pycqa.org/) for linting

## Documentation

- Update documentation when changing code
- Follow markdown guidelines
- Keep documentation concise but comprehensive

## Security Considerations

- Never commit sensitive data (API keys, passwords, etc.)
- Be mindful of the security implications of your code
- Report security vulnerabilities privately to the project maintainers

## License

By contributing to RedTeamTP, you agree that your contributions will be licensed under the project's MIT License.
