#!/usr/bin/env nix-shell
#!nix-shell -i ruby -p "ruby.withPackages (ps: [ps.redcarpet])"

require "redcarpet"
require "yaml"
require "cgi"

contents = $stdin.read.force_encoding('UTF-8')
metadata = {}
if contents.start_with?("---")
  _, frontmatter, contents = contents.split("---")
  metadata = YAML.safe_load(frontmatter)
end
markdown = Redcarpet::Markdown.new(Redcarpet::Render::XHTML, extensions = {})
body = markdown.render(contents)

def puts_meta(key, value)
  case value
    when String
      puts %(<meta name="#{key}" content="#{CGI.escapeHTML(value)}" />)
    when Array
      value.each { |item| puts_meta(key, item) }
  end
end

puts "<!DOCTYPE html>"
puts "<html>"
puts "<head>"
metadata.each { |key, value| puts_meta(key, value) }
puts "</head>"
puts "<body>"
puts body
puts "</body>"
puts "</html>"
