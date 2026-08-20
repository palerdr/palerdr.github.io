// @ts-check
import { defineConfig, fontProviders } from 'astro/config';

const SITE = 'https://palerdr.github.io';
const BASE = '/jc-personal';

export default defineConfig({
  site: SITE,
  base: BASE,
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
