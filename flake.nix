{
  description = "My pre-commit hooks!";

  inputs = rec {
    nixpkgs = {
      type = "github";
      owner = "NixOs";
      repo = "nixpkgs";
      ref = "release-22.05";
    };
    pre-commit-hooks = {
      type = "github";
      owner = "cachix";
      repo = "pre-commit-hooks.nix";
      ref = "master";
    };
    flake-utils = {
      type = "github";
      owner = "numtide";
      repo = "flake-utils";
      ref = "master";
    };
  };

  outputs = { self, nixpkgs, pre-commit-hooks, flake-utils }:
    let
      attrsets = nixpkgs.lib.attrsets;

      build-format-hook = (name: hook:
        [
          { name = "check-${name}"; value = hook; }
          {
            name = "apply-${name}";
            value = hook;
            # Concat "--apply-fixes" to args
            #value = attrsets.recursiveUpdate hook {
            #  args = (if attrsets.hasAttrByPath ["args"] hook then hook.args else []) ++ ["--apply-fixes"];
            #};
          }
        ]
      );

      format-hook =
        (build-format-hook "clang-format" {
          enable = true;
          name = "Check that all source files follow the clang-format configuration";
          language = "python";
          entry = "clang-format-hook";
          types_or = [ "c" "c++" "c#" "objective-c" "java" ];
        })
        ++
        (build-format-hook "clang-tidy" {
          enable = true;
          name = "Check that all source files follow the clang-tidy configuration";
          language = "python";
          entry = "clang-tidy-hook";
          types_or = [ "c" "c++" "c#" "objective-c" "java" ];
        })
        ++
        (build-format-hook "nixpkgs-fmt" {
          enable = true;
          name = "Check that all Nix files are formatted correctly";
          language = "python";
          entry = "clang-tidy-hook";
          types_or = [ "c" "c++" "c#" "objective-c" "java" ];
        })
      ;
    in
    flake-utils.lib.eachDefaultSystem (system:
      {
        checks = {
          pre-commits = pre-commit-hooks.lib.${system}.run {
            src = ./.;
            hooks = builtins.listToAttrs format-hook;
          };
        };
      }
    );
}
