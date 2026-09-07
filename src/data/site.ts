const base = import.meta.env.BASE_URL.replace(/\/$/, '');

export const profile = {
  name: 'James Cenawood',
  tagline: 'I obsess over problems.',
  description:
    'James Cenawood studies computer science at Cornell and builds systems he can prove correct, '
    + 'from an exact game solver to a retrieval benchmark.',
  blurb: [
    'I study computer science at Cornell. This summer I was a data science intern at Northwell Health.',
    'Since high school I have been obsessed with a gambling game from a manga. I spent months on it ' +
      'and proved a simplification that cut the solve from a projected five years to 50 seconds. ' +
      'Most of my work has that shape: I take a problem people argue about by feel and make it ' +
      'precise enough to compute.',
  ],
  location: 'Ithaca, NY',
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
  coursework: [
    'Probability & Statistical Inference',
    'Stochastic Processes',
    'Data Science',
    'Discrete Mathematics',
    'Linear Algebra',
    'OOP and Data Structures',
    'Functional Programming',
    'Calculus',
  ],
  inProgress: ['Machine Learning', 'Analysis of Algorithms'],
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
  location?: string;
  note?: string;
  bullets: string[];
  readMore?: { href: string; label: string };
};

export const experience: Role[] = [
  {
    org: 'Northwell Health',
    orgUrl: 'https://www.northwell.edu/',
    title: 'Data Science Intern',
    dates: 'June 2026 – August 2026',
    location: 'New Hyde Park, NY',
    bullets: [
      'The warehouse holds more tables than one analyst can keep in their head, and most of the people who need answers from it do not write SQL. I worked on an agent that takes a question in English and drafts SQL against the real schema from the documentation it retrieves. It has no access to patient data and executes nothing.',
      'I built the retrieval benchmark. It grouped questions by kind, and the groups showed the system did well on questions that named a table and failed on questions phrased in business terms, which are the questions the staff without SQL ask. Fusing BM25 full-text search with dense-vector retrieval raised hit@5 from 53.8% to 75%.',
      'I also tied for first in the intern Kaggle competition with a CatBoost and TabNet blend, validated by group so that passengers travelling together stayed in one fold.',
    ],
    readMore: { href: `${base}/projects/northwell`, label: 'Read the write-up' },
  },
  {
    org: 'Cornell Physical Intelligence',
    orgUrl: 'https://cornellphysicalintelligence.com/#about',
    title: 'Software Subteam Lead',
    dates: 'December 2025 – Present',
    location: 'Ithaca, NY',
    bullets: [
      'I lead the eight-person software subteam building a drone that flies a race course with no pilot and no external positioning. Our entry passed Virtual Qualifier 1 of Anduril’s AI Grand Prix at 17.2 seconds.',
      'Most of my own time went into making the project workable for coding agents. The simulator is a closed-source Windows app and the only source of an official score, so I wrote the PowerShell layer that launches it and scores a run. An agent can now fly a candidate policy and read back a scored result with nobody at the machine.',
      'Qualification blocks certain telemetry, so I wrote agent rules that treat reading it as an error, plus an iteration prompt that fixes the procedure: one hypothesis and the smallest change per attempt, then promote or revert.',
      'I also run the subteam’s technical interviews, more than twenty so far, on a problem set I wrote around gates and trajectories.',
    ],
  },
  {
    org: 'Cornell Extended Reality',
    orgUrl: 'https://cornellxr.com/team/',
    title: 'Software Team Member',
    dates: 'August 2025 – Present',
    location: 'Ithaca, NY',
    bullets: [
      'I designed the memory backend for a smart-glasses assistant that keeps track of the people the wearer has met: what they talked about, and how each person connects to the people already stored.',
      'I also built the resolver that maps “the guy from the climbing gym” onto one stored person. If a description fits more than one, it hands the model the details that separate them so the assistant asks a follow-up question. I added speech recognition after that, so the assistant stores conversations without a manual step.',
    ],
  },
];

export const sections = [
  { id: 'intro', num: '01', label: 'Intro' },
  { id: 'experience', num: '02', label: 'Experience' },
  { id: 'projects', num: '03', label: 'Projects' },
  { id: 'contact', num: '04', label: 'Contact' },
];
