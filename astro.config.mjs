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
  // The pairing from oneraynyday.github.io (Hyde): PT Sans for the text and
  // Abril Fatface for the name in the sidebar.
  fonts: [
    {
      provider: fontProviders.fontsource(),
      name: 'PT Sans',
      cssVariable: '--font-body',
      weights: [400, 700],
      styles: ['normal', 'italic'],
    },
    {
      provider: fontProviders.fontsource(),
      name: 'Abril Fatface',
      cssVariable: '--font-title',
      weights: [400],
      styles: ['normal'],
    },
  ],
});
