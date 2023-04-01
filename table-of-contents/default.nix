{ pkgs }:

let
  writeNu =
    pkgs.writers.makeScriptWriter { interpreter = "${pkgs.nushell}/bin/nu"; };
in writeNu "/bin/table-of-contents" ./table-of-contents.nu
