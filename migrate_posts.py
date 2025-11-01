#!/usr/bin/env python3
"""
Script to migrate Hugo blog posts to Astro format.
Handles Hugo shortcodes and converts them to standard Markdown.
"""

import re
from pathlib import Path
import shutil

HUGO_BLOG = Path("../miguel_mota.gitlab.io")
ASTRO_BLOG = Path(".")

def convert_hugo_shortcodes(content):
    """Convert Hugo shortcodes to standard Markdown"""

    # Convert figure shortcode: {{< figure src="/path/image.png" >}}
    # to: ![](/path/image.png)
    content = re.sub(
        r'\{\{<\s*figure\s+src="([^"]+)"\s*>\}\}',
        r'![](\1)',
        content
    )

    # Convert notice shortcode: {{< notice note >}}text{{< /notice >}}
    # to: > **Note:** text
    def replace_notice(match):
        notice_type = match.group(1)
        notice_content = match.group(2).strip()
        return f"> **{notice_type.title()}:** {notice_content}"

    content = re.sub(
        r'\{\{<\s*notice\s+(\w+)\s*>\}\}(.*?)\{\{<\s*/notice\s*>\}\}',
        replace_notice,
        content,
        flags=re.DOTALL
    )

    # Convert tooltip/definition shortcodes to simple text
    # {{< tooltip >}}text{{< definition >}}def{{< /definition >}}{{< /tooltip >}}
    # to: text (def)
    content = re.sub(
        r'\{\{<\s*tooltip\s*>\}\}(.*?)\{\{<\s*definition\s*>\}\}(.*?)\{\{<\s*/definition\s*>\}\}\{\{<\s*/tooltip\s*>\}\}',
        r'\1',
        content,
        flags=re.DOTALL
    )

    # Convert ref shortcode: {{< ref "file.md" >}}
    # to: /blog/slug (simplified)
    def replace_ref(match):
        ref_file = match.group(1)
        # Extract slug from filename
        slug = ref_file.replace('.md', '').replace('content/post/', '')
        return f'/blog/{slug}'

    content = re.sub(
        r'\{\{<\s*ref\s+"([^"]+)"\s*>\}\}',
        replace_ref,
        content
    )

    return content

def extract_frontmatter_and_content(file_path):
    """Extract YAML frontmatter and content from a Markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match YAML frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if match:
        frontmatter = match.group(1)
        body = match.group(2)
        return frontmatter, body
    return "", content

def convert_frontmatter(frontmatter):
    """Convert Hugo frontmatter to Astro format"""
    lines = frontmatter.split('\n')
    result = []

    for line in lines:
        # Skip subtitle field (we can add it as description if needed)
        if line.startswith('subtitle:'):
            # Convert to description
            result.append(line.replace('subtitle:', 'description:'))
        else:
            result.append(line)

    return '\n'.join(result)

def migrate_post(hugo_post_path, astro_blog_dir):
    """Migrate a single Hugo post to Astro format"""
    frontmatter, content = extract_frontmatter_and_content(hugo_post_path)

    # Convert frontmatter
    new_frontmatter = convert_frontmatter(frontmatter)

    # Convert shortcodes in content
    new_content = convert_hugo_shortcodes(content)

    # Create new file
    new_file_content = f"---\n{new_frontmatter}\n---\n{new_content}"

    # Use original filename
    output_path = astro_blog_dir / hugo_post_path.name

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(new_file_content)

    print(f"✓ Migrated: {hugo_post_path.name}")
    return output_path

def copy_images(hugo_static_dir, astro_public_dir):
    """Copy images from Hugo static directory to Astro public directory"""
    if hugo_static_dir.exists():
        # Copy all image directories
        for item in hugo_static_dir.iterdir():
            if item.is_dir():
                dest = astro_public_dir / item.name
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(item, dest)
                print(f"✓ Copied images: {item.name}")

def main():
    # Setup directories
    hugo_posts_dir = HUGO_BLOG / "content" / "post"
    astro_blog_dir = ASTRO_BLOG / "src" / "content" / "blog"
    hugo_static_dir = HUGO_BLOG / "static"
    astro_public_dir = ASTRO_BLOG / "public"

    # Create blog directory if it doesn't exist
    astro_blog_dir.mkdir(parents=True, exist_ok=True)

    print("\n=== Migrating Blog Posts ===\n")

    # Migrate all posts
    posts = sorted(hugo_posts_dir.glob("*.md"))
    for post in posts:
        migrate_post(post, astro_blog_dir)

    print(f"\nMigrated {len(posts)} posts")

    print("\n=== Copying Images ===\n")
    copy_images(hugo_static_dir, astro_public_dir)

    print("\n✅ Migration complete!")

if __name__ == "__main__":
    main()
