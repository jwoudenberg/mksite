let menu_li = { |path|
  let title = (
    open $path | from xml
      | get "content" | where tag == head | first
      | get "content" | where tag == title | first
      | get "content" | get "content" | str join
  )
  let a = {
    tag: "a"
    attributes: { href: $path }
    content: [$title]
  }
  { tag: "li", content: [$a] }
}

def main [...file] {
  let lis = ($file | each $menu_li)
  let ul = { tag: "ul", content: $lis }
  $ul | to xml -p 2
}
