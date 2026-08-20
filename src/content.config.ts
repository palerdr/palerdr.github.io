import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    tagline: z.string(),
    summary: z.string(),
    order: z.number(),
    year: z.coerce.string(),
    award: z.string().optional(),
    stack: z.array(z.string()),
    stats: z
      .array(z.object({ value: z.string(), label: z.string() }))
      .default([]),
    links: z.array(z.object({ href: z.string(), label: z.string() })).default([]),
    /** Show as a card in the projects section. Northwell lives under experience instead. */
    listed: z.boolean().default(true),
    /** Render a deep-dive page at /projects/<id>. */
    writeup: z.boolean().default(false),
  }),
});

export const collections = { projects };
