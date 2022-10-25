# pre-commit-hooks

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

This is a [pre-commit](https://github.com/pre-commit/pre-commit) hooks repo that integrates the hooks I use most frequently.

## Using this repo

### pre-commit

If you don't know what pre-commit is, you may first want to check their [doc](https://pre-commit.com/).

### Example

Copy this example `.pre-commit-config.yaml` file to the root of your project:

```yaml
repos:
  - repo: https://github.com/d4ilyrun/pre-commit-hooks
    rev: master
    hooks:
      - id: check-clang-format
      - id: check-clang-tidy
      - id: apply-nixpkgs-fmt
      - id: shellcheck
```

Then run `pre-commit install --install-hooks`.
It should apply the selected checks before commiting when new corresponding files are added/modified.

- For more informations about the available hooks, please refer to the [Hooks](#Hooks) section.

## Dependencies

>> These hooks require some dependencies. It is up to the user to make sure those are installed.

## Hooks

| Hook Name                                                                | Type                 | Languages                             | Options                             |
| ------------------------------------------------------------------------ | -------------------- | ------------------------------------- | ----------------------------------- |
| [clang-format](https://clang.llvm.org/docs/ClangFormatStyleOptions.html) | Formatter            | C, C++, ObjC, ObjC++, Java            | --verbose, --apply-fixes            |
| [clang-tidy](https://clang.llvm.org/extra/clang-tidy)                    | Static code analyzer | C, C++, ObjC                          | --verbose, --apply-fixes            |
| [nixpkgs-fmt](https://github.com/nix-community/nixpkgs-fmt)              | Formatter            | Nix                                   | --verbose, --apply-fixes            |
| [shellcheck](https://www.shellcheck.net)                                 | Static code analyzer | Shell                                 | --verbose                           |

### Available pre-commit hooks

| Hook Name                                                                | Available for pre-commit               |
| ------------------------------------------------------------------------ | -------------------------------------- |
| [clang-format](https://clang.llvm.org/docs/ClangFormatStyleOptions.html) | check-clang-format, apply-clang-format |
| [clang-tidy](https://clang.llvm.org/extra/clang-tidy/)                   | check-clang-tidy,   apply-clang-tidy   |
| [nixpkgs-fmt](https://github.com/nix-community/nixpkgs-fmt)              | check-nixpkgs-fmt,  apply-nixpkgs-fmt  |
| [shellcheck](https://www.shellcheck.net)                                 | shellcheck                             |
