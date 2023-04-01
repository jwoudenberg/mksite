{ pkgs }:

let
  writeRuby = pkgs.writers.makeScriptWriter {
    interpreter = "${pkgs.ruby.withPackages (ps: [ ps.redcarpet ])}/bin/ruby";
  };
in writeRuby "/bin/md-to-html" ./md-to-html.rb
