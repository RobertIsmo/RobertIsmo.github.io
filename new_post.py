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

    # Generate slug from title
    title_slug = slugify(title)

    # Get current date
    today = datetime.date.today()
    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")

    # Define the base blog directory
    blog_base_dir = Path("blog")

    # Construct the path for the new blog post directory
    # e.g., blog/2025/06/05/my-new-post-title/
    new_post_dir = blog_base_dir / year / month / day / title_slug

    # Create the directory, including any necessary parent directories
    try:
        new_post_dir.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {new_post_dir}")
    except OSError as e:
        print(f"Error creating directory {new_post_dir}: {e}")
        return

    # Define the path for the index.md file
    index_md_path = new_post_dir / "index.md"

    # Define the initial content for index.md with front matter
    markdown_content = f"""---
title: {title}
author: Your Name Here
date: {today.isoformat()}
---

# {title}

Start writing your blog post here!
"""

    # Write the content to the index.md file
    try:
        index_md_path.write_text(markdown_content, encoding='utf-8')
        print(f"Created Markdown file: {index_md_path}")
        print("\nYour new blog post is ready! You can now edit the 'index.md' file.")
    except OSError as e:
        print(f"Error writing to file {index_md_path}: {e}")

if __name__ == "__main__":
    create_new_blog_post()
