{
  description = "A minimal Python dev environment from requirements-dev.txt";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    pyproject-nix.url = "github:pyproject-nix/pyproject.nix";
  };

  outputs = { self, nixpkgs, flake-utils, pyproject-nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        python = pkgs.python313;

        # 1. Explicitly load your dev requirements file
        project = pyproject-nix.lib.project.loadRequirementsTxt {
          projectRoot = ./.;
          requirements = ./requirements-dev.txt;
        };

        pythonEnv = 
          (
            # Render requirements.txt into a Python withPackages environment
            pkgs.python3.withPackages (project.renderers.withPackages { inherit python; })
          );

      in
      {
        # 3. This devShell will have your dev packages
        devShells.default = pkgs.mkShell {
          buildInputs = [ pythonEnv ];
        };
      }
    );
}
