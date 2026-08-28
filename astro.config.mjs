// @ts-check
import { defineConfig, fontProviders } from 'astro/config';
import sitemap from '@astrojs/sitemap';

const SITE = 'https://palerdr.github.io';

export default defineConfig({
  site: SITE,
  integrations: [sitemap()],
  // Hovering a mark swings the pointer to it, so the page is already in hand by
  // the time it is clicked and the sweep starts on the frame after the click.
  prefetch: { prefetchAll: true, defaultStrategy: 'hover' },
  // One family for the whole site, as on situational-awareness.ai. Benne ships a
  // single weight and no italic, so bold and oblique are synthesised — which is
  // what that site does too.
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
