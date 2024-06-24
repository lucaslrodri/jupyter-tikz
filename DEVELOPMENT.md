# Development Guide

## Prerequisites

Before you begin, install Poetry, which manages dependencies and handles the project's packaging. Follow the instructions on their [official website](https://python-poetry.org/docs/#installation) to install Poetry.

## Getting Started

### 1. Clone the Repository

First, **fork the repository** and then clone your fork to create a local copy on your computer. Use the following command:

```shell
git clone https://github.com/your_name/jupyter-tikz.git
```

> [!IMPORTANT]
> Don't forget to replace `your_name` with your GitHub username.

#### 2. Create a new branch

Before making any changes, switch to a new branch to keep your developments organized:

```shell
git checkout -b feature-branch-name
```

#### 3. Develop your feature or fix a bug

Make your changes in the codebase. If you're adding a feature or updating documentation, ensure your updates are clear and comprehensive.

#### 4. Test your changes

The project utilizes [pytest](https://docs.pytest.org/) for testing. Create tests for your new feature and run them. If you use VS Code, you can follow this guide [here](https://code.visualstudio.com/docs/python/testing). Additionally, build the project using `poetry build` and install the package on your machine to test it in a Jupyter Notebook.

#### 5. Submit a pull request

Once your changes are ready and tested, push your branch to GitHub, and then submit a pull request from your fork to the main repository. Provide a clear description of the changes and any other relevant information.
