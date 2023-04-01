{
  description = "groceries";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = import nixpkgs { system = system; };
      in {
        packages.md-to-html = pkgs.callPackage ./md-to-html/default.nix { };
        packages.table-of-contents =
          pkgs.callPackage ./table-of-contents/default.nix { };

        devShell = pkgs.mkShell {
          buildInputs = [ pkgs.nushell pkgs.haskellPackages.shelltestrunner ];
        };
      });
}
