# Miguel Mota - Personal Website

A minimal, modern personal website built with [Astro](https://astro.build), featuring a blog, projects showcase, and about page.

## Features

- 📝 Blog with Markdown support
- 🚀 Fast, static site generation
- 📱 Responsive, minimal design
- 🌙 Dark mode support (automatic based on system preference)
- 🔄 Auto-deployment to GitHub Pages via GitHub Actions
- 📦 Zero JavaScript by default (ships only HTML and CSS)

## Structure

```
miguel-personal-site/
├── src/
│   ├── content/
│   │   ├── blog/          # Blog posts (Markdown files)
│   │   ├── projects/      # Project pages (Markdown files)
│   │   └── config.ts      # Content collections configuration
│   ├── layouts/
│   │   ├── BaseLayout.astro    # Main layout with nav/footer
│   │   └── BlogPost.astro      # Blog post layout
│   └── pages/
│       ├── index.astro         # Home page
│       ├── about.astro         # About page
│       ├── blog/
│       │   ├── index.astro     # Blog listing page
│       │   └── [...slug].astro # Dynamic blog post pages
│       └── projects/
│           ├── index.astro     # Projects listing page
│           └── [...slug].astro # Dynamic project pages
├── public/                # Static assets (images, favicon, etc.)
└── .github/workflows/     # GitHub Actions for auto-deployment
```

## Local Development

### Prerequisites

- Node.js 18+ installed
- npm or pnpm

### Getting Started

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```
   Open [http://localhost:4321](http://localhost:4321) in your browser

3. **Build for production:**
   ```bash
   npm run build
   ```

4. **Preview production build:**
   ```bash
   npm run preview
   ```

## Adding Content

### Adding a New Blog Post

1. Create a new Markdown file in `src/content/blog/`:
   ```bash
   # Filename format: YYYY-MM-DD-post-slug.md
   touch src/content/blog/2025-01-15-my-new-post.md
   ```

2. Add frontmatter and content:
   ```markdown
   ---
   title: My New Post Title
   date: 2025-01-15
   description: A brief description of the post (optional)
   tags: ["python", "tutorial"]  # optional
   draft: false  # set to true to hide from production
   ---

   Your content here using standard Markdown...

   ## Headings
   - Lists
   - Code blocks
   - Images: ![alt text](/image-path.png)
   ```

3. Add images to `public/` directory (e.g., `public/2025-01-15-my-new-post/image.png`)

4. Commit and push - the site will auto-deploy!

### Adding a New Project

1. Create a new Markdown file in `src/content/projects/`:
   ```bash
   touch src/content/projects/my-project.md
   ```

2. Add frontmatter and content:
   ```markdown
   ---
   title: My Project Name
   description: What this project does
   date: 2025-01-15  # optional
   tags: ["python", "automation"]  # optional
   ---

   Project details, code samples, etc...
   ```

### Frontmatter Options

**Blog Posts:**
- `title` (required): Post title
- `date` (required): Publication date
- `description` (optional): Short description for SEO and post listings
- `tags` (optional): Array of tags for categorization
- `draft` (optional): Set to `true` to hide from production

**Projects:**
- `title` (required): Project name
- `description` (optional): Short description
- `date` (optional): Project date
- `tags` (optional): Array of tags

## Deployment to GitHub Pages

### Initial Setup

1. **Create a new GitHub repository:**
   - Go to GitHub and create a new repository
   - For a user site: name it `YOUR_USERNAME.github.io`
   - For a project site: name it anything you like

2. **Update `astro.config.mjs`:**
   ```js
   export default defineConfig({
     site: 'https://YOUR_USERNAME.github.io',
     // If using a project repo (not YOUR_USERNAME.github.io):
     // base: '/repo-name',
   });
   ```

3. **Initialize git and push:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

4. **Enable GitHub Pages:**
   - Go to your repository settings on GitHub
   - Navigate to **Pages** (under "Code and automation")
   - Under "Build and deployment":
     - Source: **GitHub Actions**
   - The GitHub Action will automatically deploy on every push to `main`

### Publishing Updates

Simply commit and push your changes:

```bash
git add .
git commit -m "Add new blog post"
git push
```

GitHub Actions will automatically build and deploy your site within a few minutes.

## Customization

### Changing Site Title and Info

Edit `src/layouts/BaseLayout.astro`:
- Update `siteTitle` variable
- Modify navigation links

### Styling

The site uses inline styles for simplicity. To customize:
- Edit the CSS variables in `src/layouts/BaseLayout.astro` (under `:root`)
- Colors, fonts, spacing are all defined there
- Dark mode colors are in `@media (prefers-color-scheme: dark)`

### Adding New Pages

1. Create a new `.astro` file in `src/pages/`
2. Use the BaseLayout:
   ```astro
   ---
   import BaseLayout from '../layouts/BaseLayout.astro';
   ---

   <BaseLayout title="Page Title">
     <h1>Your content here</h1>
   </BaseLayout>
   ```

## Tech Stack

- **Framework:** [Astro 5](https://astro.build)
- **Deployment:** GitHub Pages
- **CI/CD:** GitHub Actions
- **Styling:** Native CSS (no framework)
- **Content:** Markdown with frontmatter

## License

MIT

## Contact

- Email: miguelmota.contacts@gmail.com
- GitLab: [@miguel_mota](https://gitlab.com/miguel_mota)
