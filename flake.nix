{
  description = "groceries";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = import nixpkgs { inherit system; };
      in {
        apps.md-to-html = {
          type = "app";
          program = "${pkgs.callPackage ./md-to-html/default.nix { }}";
        };
      });
}
