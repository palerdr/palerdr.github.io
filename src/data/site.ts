const base = import.meta.env.BASE_URL.replace(/\/$/, '');

export const profile = {
  name: 'James Cenawood',
  description: 'James Cenawood studies computer science at Cornell. This site has his projects and work.',
  blurb: [
    'I study computer science at Cornell. This summer I was a data science intern at Northwell Health.',
    'Since high school I have wanted to solve a gambling game from the manga Usogui, and this year I did.',
  ],
};

export const links = {
  github: 'https://github.com/palerdr',
  email: 'jcc463@cornell.edu',
  linkedin: 'https://www.linkedin.com/in/james-cenawood',
  resume: `${base}/resume.pdf`,
};

export const education = {
  school: 'Cornell University, College of Engineering',
  degree: 'B.S. Computer Science',
  dates: 'August 2024 – May 2028',
  gpa: '3.9',
};

export const skills = [
  {
    label: 'Languages',
    items: ['Python', 'SQL', 'TypeScript', 'Rust', 'C++', 'OCaml'],
  },
  {
    label: 'Libraries & frameworks',
    items: [
      'PyTorch',
      'TensorFlow',
      'scikit-learn',
      'NumPy',
      'pandas',
      'Polars',
      'FastAPI',
      'LangGraph',
      'OpenCV',
      'React',
      'Expo',
    ],
  },
  {
    label: 'Infrastructure',
    items: [
      'PostgreSQL',
      'SQLAlchemy',
      'SQLite',
      'BigQuery',
      'Docker',
      'Supabase',
      'Vercel',
      'Optuna',
      'Weights & Biases',
      'Git',
    ],
  },
];

export type Role = {
  org: string;
  orgUrl?: string;
  title: string;
  dates: string;
  /** One sentence on what I did there. */
  line: string;
  readMore?: string;
};

export const experience: Role[] = [
  {
    org: 'Northwell Health',
    orgUrl: 'https://www.northwell.edu/',
    title: 'Data Science Intern',
    dates: 'Summer 2026',
    line: 'I built the retrieval benchmark for an agent that writes SQL from plain-English questions.',
    readMore: `${base}/projects/northwell`,
  },
  {
    org: 'Cornell Physical Intelligence',
    orgUrl: 'https://cornellphysicalintelligence.com/#about',
    title: 'Software Subteam Lead',
    dates: '2025 to now',
    line: 'I lead the software team for our autonomous drone in Anduril’s AI Grand Prix.',
  },
  {
    org: 'Cornell Extended Reality',
    orgUrl: 'https://cornellxr.com/team/',
    title: 'Software Team Member',
    dates: '2025 to now',
    line: 'I built the memory for a smart-glasses assistant that remembers the people you meet.',
  },
];

export type TabId = 'about' | 'experience' | 'projects' | 'contact';

/** Each tab is its own page and sits at an hour mark on the clock. `angle` is that mark's bearing. */
export const tabs: { id: TabId; label: string; href: string; angle: number }[] = [
  { id: 'about', label: 'About', href: `${base}/about/`, angle: 0 },
  { id: 'experience', label: 'Experience', href: `${base}/experience/`, angle: 60 },
  { id: 'projects', label: 'Projects', href: `${base}/projects/`, angle: 120 },
  { id: 'contact', label: 'Contact', href: `${base}/contact/`, angle: 180 },
];
