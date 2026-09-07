# James Cenawood — Personal Site

Personal site. Astro, static output, no client-side JS.

```sh
npm install
npm run dev      # http://localhost:4321
npm run build    # -> dist/
npm run check    # astro check
```

## Content

| What | Where |
| --- | --- |
| Bio, skills, roles, education, nav sections | `src/data/site.ts` |
| Projects (frontmatter + write-up body) | `src/content/projects/*.md` |
| Schema for project frontmatter | `src/content.config.ts` |
| Type scale, palette, spacing | `src/styles/global.css` |

Adding a project is one Markdown file in `src/content/projects/`. Set `writeup: true` to get a
page at `/projects/<filename>`; set `listed: false` to keep it off the home page grid.

## Résumé

`public/resume.pdf` is the deployed copy. It is currently the exported PDF supplied directly, and
`resume/qresume0.tex` is a LaTeX version of the same content, kept in sync by hand. It
intentionally omits a postal address. To rebuild the downloadable copy from the TeX instead:

```sh
mkdir -p tmp/pdfs
tectonic --outdir tmp/pdfs resume/qresume0.tex
cp tmp/pdfs/qresume0.pdf public/resume.pdf
```

Only `public/resume.pdf` is deployed. Generated and legacy PDFs under `resume/` are ignored.

## Deploy

GitHub Actions deploys every push to `main` to the account-level GitHub Pages site:

<https://palerdr.github.io/>
