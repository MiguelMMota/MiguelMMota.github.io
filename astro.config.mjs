// @ts-check
import { defineConfig } from 'astro/config';
import remarkGithubBlockquoteAlert from 'remark-github-blockquote-alert';

// https://astro.build/config
export default defineConfig({
  site: 'https://miguelmmota.github.io',
  // Uncomment the line below if deploying to a repository that is not YOUR_USERNAME.github.io
  // base: '/your-repo-name',
  markdown: {
    remarkPlugins: [remarkGithubBlockquoteAlert],
  },
});
