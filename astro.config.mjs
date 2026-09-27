// @ts-check
import { defineConfig, fontProviders } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { unified } from '@astrojs/markdown-remark';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

const SITE = 'https://palerdr.github.io';

export default defineConfig({
  site: SITE,
  integrations: [sitemap()],
  // Hovering a mark swings the pointer to it, so the page is already in hand by
  // the time it is clicked and the sweep starts on the frame after the click.
  prefetch: { prefetchAll: true, defaultStrategy: 'hover' },
  // Write math in the write-ups as $…$ inline and $$…$$ for displays. KaTeX
  // renders it at build time, and the built pages load no math script.
  markdown: {
    processor: unified({
      remarkPlugins: [remarkMath],
      rehypePlugins: [rehypeKatex],
    }),
  },
  // One family for the whole site. Benne ships a single weight and no italic,
  // so bold and oblique are synthesised.
  fonts: [
    {
      provider: fontProviders.fontsource(),
      name: 'Benne',
      cssVariable: '--font-body',
      weights: [400],
      styles: ['normal'],
    },
  ],
});
