{ pkgs }:

let
  writeRuby = pkgs.writers.makeScriptWriter {
    interpreter = "${pkgs.ruby.withPackages (ps: [ ps.redcarpet ])}/bin/ruby";
  };
in writeRuby "md-to-html" (builtins.readFile ./md-to-html.rb)
