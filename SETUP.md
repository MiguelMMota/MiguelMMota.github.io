# Quick Setup Guide

## What I've Built For You

Your new personal website includes:

✅ **7 blog posts** migrated from Hugo
✅ **8 projects** ready to showcase
✅ **Clean, minimal design** with dark mode support
✅ **GitHub Actions** configured for auto-deployment
✅ **All images** copied and working

## Next Steps

### 1. Test Locally (Optional)

To see your site locally before deploying:

```bash
npm run dev
```

Open http://localhost:4321 in your browser.

### 2. Create GitHub Repository

You have two options:

**Option A: User/Organization Site (Recommended)**
- Repository name: `YOUR_USERNAME.github.io`
- Your site will be at: `https://YOUR_USERNAME.github.io`
- No need to configure `base` in config

**Option B: Project Site**
- Repository name: anything (e.g., `personal-site`)
- Your site will be at: `https://YOUR_USERNAME.github.io/personal-site`
- **Must** uncomment and set `base: '/personal-site'` in `astro.config.mjs`

### 3. Update Configuration

Edit `astro.config.mjs`:

```js
export default defineConfig({
  site: 'https://YOUR_GITHUB_USERNAME.github.io',
  // Only if using Option B (project site):
  // base: '/your-repo-name',
});
```

Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username.

### 4. Push to GitHub

```bash
# If not already initialized
git init
git add .
git commit -m "Initial commit: Astro blog"

# Add your GitHub remote
git branch -M main
git remote add origin git@github.com:YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

**Important:** Use your **GitHub** SSH credentials, not GitLab!

Based on your SSH config, you might need:
- `git@github.com:YOUR_USERNAME/YOUR_REPO.git` (default GitHub)
- `git@github-personal:YOUR_USERNAME/YOUR_REPO.git` (if using personal GitHub key)

### 5. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings**
3. Scroll to **Pages** (left sidebar)
4. Under "Build and deployment":
   - **Source**: Select "GitHub Actions"
5. Done! The site will deploy automatically

After a few minutes, your site will be live!

## Daily Workflow: Adding New Posts

### Quick Method

1. Create file: `src/content/blog/YYYY-MM-DD-title.md`
2. Add content:
   ```markdown
   ---
   title: My Post Title
   date: 2025-01-15
   description: Brief description
   tags: ["python", "web"]
   ---

   Your content here...
   ```
3. Commit and push:
   ```bash
   git add .
   git commit -m "Add new post: My Post Title"
   git push
   ```
4. Wait ~2 minutes - your post is live!

### With Images

1. Add images to `public/YYYY-MM-DD-title/`
2. Reference in markdown: `![alt text](/YYYY-MM-DD-title/image.png)`

## Troubleshooting

### Build fails with "site is required"
- Make sure you updated `astro.config.mjs` with your GitHub username

### 404 on GitHub Pages
- Check that Pages is set to "GitHub Actions" source
- If using a project repo, make sure `base` is set correctly
- Wait a few minutes after pushing

### Images not showing
- Images must be in `public/` directory
- Paths should start with `/` (e.g., `/folder/image.png`)

### Local dev server shows errors
- Run `npm install` again
- Delete `node_modules` and run `npm install`

## Support

For Astro-specific questions: https://docs.astro.build
For this setup: Check the main README.md

Your site is ready to go! 🚀
