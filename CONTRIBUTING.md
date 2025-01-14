# Contributing to snotify

Thank you for considering contributing to snotify! We welcome contributions from the community to help improve the project.

## Getting Started

1. **Fork the repository**: Click the "Fork" button at the top right of the repository page to create a copy of the repository under your own GitHub account.

2. **Clone your fork**: Clone your forked repository to your local machine.

   ```bash
   git clone https://github.com/your-username/snotify.git
   cd snotify
   ```

3. **Create a branch**: Create a new branch for your feature or bug fix.

   ```bash
   git checkout -b feature/your-feature-name
   ```

## Setting Up the Development Environment

1. **Install dependencies**: Install the required Python packages for development.

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

2. **Set up pre-commit hooks**: We use pre-commit hooks to ensure code quality. Install the hooks by running:

   ```bash
   pre-commit install
   ```

   This will automatically run checks on your code before each commit, including formatting with Black, linting with Ruff, and other checks.

## Making Changes

1. **Make your changes**: Implement your feature or bug fix.

2. **Run tests**: Ensure that all tests pass by running:

   ```bash
   pytest
   ```

3. **Commit your changes**: Commit your changes with a descriptive commit message.

   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

4. **Push your branch**: Push your branch to your forked repository.

   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a pull request**: Go to the original repository and create a pull request from your branch.

## Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

Thank you for your contributions!
