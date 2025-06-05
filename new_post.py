import datetime
import re
from pathlib import Path

def slugify(text):
    """
    Converts a given string into a URL-friendly slug.
    - Lowercases the string.
    - Replaces non-alphanumeric characters with hyphens.
    - Removes leading/trailing hyphens.
    - Collapses multiple hyphens into a single hyphen.
    """
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)  # Remove non-word chars (except spaces and hyphens)
    text = re.sub(r'[\s_]+', '-', text)   # Replace spaces and underscores with a single hyphen
    text = text.strip('-')                # Remove leading/trailing hyphens
    return text

def create_new_blog_post():
    """
    Prompts the user for a blog post title, creates the dated directory structure,
    and initializes an index.md file with basic front matter.
    """
    title = input("Enter the title for your new blog post: ")
    if not title:
        print("Blog post creation cancelled: A title is required.")
        return

    title_slug = slugify(title)

    today = datetime.date.today()
    year = today.strftime("%Y")
    month_num = today.strftime("%m")
    day_num = today.strftime("%d")
    
    formatted_date = today.strftime("%B %d, %Y")

    blog_base_dir = Path("blog")

    new_post_dir = blog_base_dir / year / month_num / day_num / title_slug

    try:
        new_post_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {new_post_dir}")
    except OSError as e:
        print(f"Error creating directory {new_post_dir}: {e}")
        return

    index_md_path = new_post_dir / "index.md"

    markdown_content = f"""Title: {title}
Subtitle: <subtitle goes here>
Author: Robert Ismo
Date: {formatted_date}


Start writing your blog post here!
"""
    try:
        index_md_path.write_text(markdown_content, encoding='utf-8')
        print(f"Created Markdown file: {index_md_path}")
        print("\nYour new blog post is ready! You can now edit the 'index.md' file.")
    except OSError as e:
        print(f"Error writing to file {index_md_path}: {e}")

if __name__ == "__main__":
    create_new_blog_post()
