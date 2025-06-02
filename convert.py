import markdown
from markdown.extensions.meta import MetaExtension
from pathlib import Path

def extract_date_from_path(md_path):
    parts = md_path.parts
    try:
        year, month, day = parts[-5], parts[-4], parts[-3]
        return f"{year}-{month}-{day}"
    except IndexError:
        return ""

def convert_md_file(md_path):
    md_text = md_path.read_text(encoding='utf-8')
    md = markdown.Markdown(extensions=[MetaExtension()])
    html_body = md.convert(md_text)
    meta = md.Meta

    title = meta.get('title', ['Untitled'])[0]
    subtitle = meta.get('subtitle', [''])[0]
    author = meta.get('author', [''])[0]
    updated_date = meta.get('date', [''])[0]
    created_date = extract_date_from_path(md_path)

    date_line = f"<p><em class=\"metadata\">Created: {created_date}</em></p>"
    if updated_date:
        date_line += f"\n<p><em class=\"metadata\">Updated: {updated_date}</em></p>"

    author_line = f"<p><em class=\"metadata\">{author}</em></p>" if author else ""

    header_info = f"<h1 class=\"title\">{title}</h1>"
    if subtitle:
        header_info += f"<h2 class=\"subtitle\">{subtitle}</h2>"
    header_info += f"{author_line}\n{date_line}"

    template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>{title}</title>
	<link rel="stylesheet" href="/main.css">
</head>
<body class="blogbody">
        <a href="/">Go Home</a>
  	<section class="blog">
                <div class=\"headerinfo\">
                        {header_info}
                </div>
	  	{html_body}
	</section>
</body>
</html>"""

    html_path = md_path.with_suffix('.html')
    html_path.write_text(template, encoding='utf-8')

def get_blog_metadata(md_path):
    md_text = md_path.read_text(encoding='utf-8')
    md = markdown.Markdown(extensions=[MetaExtension()])
    md.convert(md_text)
    meta = md.Meta
    title = meta.get('title', ['Untitled'])[0]
    subtitle = meta.get('subtitle', [''])[0]
    author = meta.get('author', [''])[0]
    created_date = extract_date_from_path(md_path)
    updated_date = meta.get('date', [''])[0]
    return {
        "title": title,
        "subtitle": subtitle,
        "author": author,
        "created_date": created_date,
        "updated_date": updated_date,
        "path": md_path.with_suffix('.html').as_posix()
    }

def generate_index():
    blog_dir = Path("blog")
    template_path = Path("template.html")
    output_path = Path("index.html")

    template_html = template_path.read_text(encoding='utf-8')

    blogs = []
    for md_file in blog_dir.rglob("*.md"):
        blogs.append(get_blog_metadata(md_file))

    blogs.sort(key=lambda b: b['created_date'])

    blog_entries = []
    for b in blogs:
        subtitle_html = f"<br><em>{b['subtitle']}</em>" if b['subtitle'] else ""
        author_html = f"<small>{b['author']}</small>" if b['author'] else ""
        updated_html = f"<small>Updated: {b['updated_date']}</small>" if b['updated_date'] else ""
        date_html = f"<small>Created: {b['created_date']}</small>"
        blog_entries.append(
            f'<p><span><a href="{b["path"]}">{b["title"]}</a> by {author_html} {date_html} {updated_html}</span>{subtitle_html}</p>'
        )
    replacement_html = "\n\t\t\t".join(blog_entries)

    new_html = template_html.replace("<!-- Start Here -->", replacement_html)

    output_path.write_text(new_html, encoding='utf-8')

def convert_blog():
    blog_dir = Path("blog")
    for md_file in blog_dir.rglob("*.md"):
        convert_md_file(md_file)

def main():
    convert_blog()
    generate_index()

if __name__ == "__main__":
    main()
