# Contribution guide



## Getting started

### Install dependencies

We use `git` for version management.

Install `git` with your choice of package manager.

With `pacman` this can be done by running:

```
pacman -Syy git
```

The software is written in Python. We use `pyenv` to manage Python versions.

Install `pyenv` with your choice of package manager.

With `pacman` this can be done by running:

```
pacman -Syy pyenv
```

We use Python `3.12.9` as that is the latest well-supported version.
Install Python `3.12.9` with pyenv with the following command:

```
pyenv install 3.12.9
```

To verify that Python has been successfully installed, run:

```
pyenv versions
```

You should see `3.12.9` in the list of avalible versions.


### Clone the repository

To clone the repository type this command in the shell of your choice:

```bash
git clone https://szofttech.inf.elte.hu/szofttech-ab-2025/group-07/csapat5 <local-clone-path>
```

and verify that the repository has been cloned correctly using:

```bash
cd <local-clone-path>
git status
```

you should see that you are up to date with `origin/master`.

### Setup python virtual environment

Our preferred way to manage python packages is using pip3 and virtual environments.

You can set up a virtual environment with the correct Python version using `pyenv`.

Set the pyenv Python version to `3.12.9` by running:

```bash
pyenv local 3.12.9
```

Verify that the python version has been set correctly by running:

```bash
pyenv exec python --version
```

You should see that the Python version is `3.12.9`

To create a python virtual environment with the currently selected version run:

```bash
pyenv exec python -m venv .venv
```

To activate the environment run:

```bash
source .venv/bin/activate
```

To deactivate it run:

```bash
deactivate
```

To verify that the environment has been setup correctly, run the following commands with in an active virtual environment:

```bash
python --version
which python
```

In the output of the first command you should see that the current python version is `3.12.9`.
In the output of the second command you should see that the current python command is the one from the virtual environment.

### Install requirements

We use `pip` to manage python packages. `pip` comes installed with Python.

Requiremnts can be installed automatically with the requirements.txt file founds in the repo root.

Install the requirements into your virtual environment with the following command:

```bash
pip3 install -r requirements.txt
```

You should see `pip` installing the required python packages.

## Coding style

### General style

We comform mostly to pep8 guidelines: https://peps.python.org/pep-0008/
We use the black formatter to ensure this.

### Type hints

We enforce type hinting in function signatures with `mypy`. Type hinting inside of function bodies is usually unnessecarry. If you need/want to duck-type, use `Any`.

### Other naming conventions

Prefix pure abstract classes with the letter `I`.
Example:

```python
class ISomeInterface(ABC):
    ...
```

Prefix abstract classes with `A`.
Example:

```python
class ASomeAbstract(ABC):
    ...
```

### Tools

You can use tools to comform to the rules mentioned above with the floowing tools:

- black
- isort
- flake8
- mypy

Example usage (from repo root):

```bash
black .
isort .
flake8 .
mypy .
```

## Branching strategy

We use a single protected branch called `master`. This branch is always kept in a working state as a best effort.
The only way to change the state of the `master` branch is through pull requests.
Development happens on so-called "feature branches".

The strategy for feature branching is:
- Start at the most recent revision of `master` (`git fetch` or `git pull`)
- The branch should contain a feature, working iteration of a feature, or a bugfix
- Long-running feature branches should be avoided, to avoid conflicts as much as possible

Feature branches are merged back into `master` via a pull request, we use squash merging to keep the history of `master` clean
If a change turns out to break `master` it will be reverted through a pull request via `git revert`

## Making a pull request

A pull request will only be accepted, if it conforms to the following rules:
- The PR title is prefixed by the ticket number(s) it belongs to (if it has one)
- The code is formatted correctly according to the CI
- The code is well tested
- All tests pass upon a merge
- The changes pass code-review

## Setup linters and formatters (vscode)

The linters and formatters are installed by `pip`, if you haven't already, from the repo root run:

```bash
python -m venv .venv
source .venv/bin/activte
pip3 install -r requirements.txt
```

You can integrate the linters and formatters into vscode by installing the following extensions:
- Black Formatter (ms-python)
- Flake8 (ms-python)
- Mypy Type Checker (ms-python)
- isort (ms-python)

You should also turn off:
- Pylance

Next, to turn on format on save, in the settings, under "Default Formatter" choose "Black Formatter" from the dropdown.
After choosing `black` as your default formatter you should enable "Format on Save"
To also run isort, go to "Code Actions On Save", click on "Edit in settings.json", and paste the following line:

```json
"source.organizeImports": "always"
```

## Git quick-start

### Getting started

After cloning the repositiory, and setting it as your working directory, navigate to the `master` branch with:

```bash
git switch master
```

Make sure your `master` branch is the most recent revision by running:

```bash
git pull
```

or running:

```bash
git fetch
```

Now you are ready to open your feature branch, make sure your branch name is descriptive. You can open a new branch by running:

```bash
git branch my-branch-name
```

Switch to your new branch by running:

```bash
git switch my-branch-name
```

### Git workflow

After making a few related changes, you should create a commit. To make a commit you need to stage your changes. You can see which files changed with:

```bash
git status
```

To add your changes to the commit, stage them:

```bash
git add my-file
```

Or if you removed a file:

```bash
git rm my-file
```

After you have staged your changes, you can check what will be included in the commit by running:

```bash
git status
```

once again.

When you are ready to make your commit, run:

```bash
git commit -m "commit message"
```

The commit message should be brief and descriptive.

After making commits, you can check your commits with:

```bash
git log
```

This will show commit hashes

To revert a commit use: `git revert commit-hash`
To discard all changes and go back to a previous commit state use: `git reset --hard commit-hash`

After you have made the changes to the code-base that you wanted, or you want to save your changes remotely, upload your branch with:

```bash
git push --set-upstream origin my-branch-name
```

This will create a remote branch, you can always update this branch by doing:

```bash
git push
```

You can create a merge-request for your branch via the gitlab UI. If there is a merge conflict, you need to resolve the conflict and `git push` again.

### Resolving a merge conflict

There are 2 ways to resolve a merge-conflict. Both of the start by getting the fresh `master` locally. You can do this by running:

```bash
git fetch
```

#### Resolving a conflict via git merge

The first and preferred way to resolve a merge conflict is via `git merge`.

Start resolving the conflict by merging your base branch (in most cases `master`) back into your branch:

```bash
git merge master
```

Because merging is a commutative operation, you should get the same conflict, as when gitlab tried to merge the two branches.

Check which files conflict via:

```bash
git status
```

Resolve the conflicts by editing those files. Add your changes with:

```bash
git add my-files
```

After all conflicts have been resolved continue the merge with:

```bash
git merge --continue
```

When the merge is done, it will open an editor to edit the message of the merge commit, just close the editor with: `:q`

After resolving the conflict, you can update your remote branch via `git push`

#### Resolving a conflict via git rebase

The second way is to use `git rebase`. You can rebase by running:

```bash
git rebase master
```

This will start putting your commits onto the current revision of `master`, when it encounters the conflict, it will stop and ask you to intervene.

Check which files have the conflict via:

```bash
git status
```

You need to go to that file, and resolve the conflict via an editor, vscode has a builtin merge conflict editor. After you have resolved the conflict stage your change with:

```bash
git add my-file
```

After you staged your change, you can continue the rebase, by running:

```bash
git rebase --continue
```

This will continue to the next conflict if there is one. After there are no more conflicts, you can update your branch on the remote with:

```bash
git push
```

## TODO

Add more sections.
