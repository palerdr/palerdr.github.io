const base = import.meta.env.BASE_URL.replace(/\/$/, '');

export const profile = {
  name: 'James Cenawood',
  tagline: 'I obsess over problems.',
  description:
    'Cornell CS. I take problems people reason about informally, make them precise enough to '
    + 'compute with, then check the answer.',
  blurb: [
    'CS at Cornell, currently a data science intern at Northwell Health.',
    'My work has one shape. Take something people reason about informally (a gambling game from ' +
      'a manga, a training program, whether a search system is returning the right documents), ' +
      'make it precise enough to compute with, then check the answer.',
    'The checking is not the last step but the whole problem. Producing an answer is rarely the ' +
      'hard part; knowing whether to believe it is where the time goes.',
  ],
  location: 'Ithaca, NY',
};

export const links = {
  github: 'https://github.com/palerdr',
  email: 'jcc463@cornell.edu',
  linkedin: 'https://www.linkedin.com/in/james-cenawood-8882b6300',
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
    items: ['Python', 'C++', 'Rust', 'SQL', 'TypeScript', 'OCaml'],
  },
  {
    label: 'Libraries & frameworks',
    items: [
      'PyTorch',
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
    location: 'New York, NY',
    bullets: [
      'A hospital data warehouse is too large for any one person to hold, and most of the people who need answers from it do not write SQL. The agent takes the question in English, finds the schema documentation that covers it, and drafts SQL against the real schema. It touches no patient data, executes nothing, and validates every query before returning it.',
      'I own the evaluation. Everything rests on retrieval: an agent working from the wrong table still writes SQL that reads well and runs, so the most consequential failure in the system is also the least visible one.',
      'The benchmark groups questions by kind rather than averaging them into a single score, and the grouping is what found the problem. The system does well on questions that name a table or a column and poorly on questions phrased in business terms, which is nearly everything the people who cannot write SQL will ask. That gap does not close by searching harder.',
      'I also tied for first in the intern Kaggle competition, on a CatBoost and TabNet blend validated by group rather than at random.',
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
      'I lead the eight-person software subteam building a drone that flies a race course with no pilot and no external positioning, navigating from camera input and its own motion estimate. Our entry qualified for Virtual Qualifier 1 of Anduril’s AI Grand Prix.',
      'Most of my own time went somewhere less visible: making the project something AI agents could work inside. The simulator is a closed-source Windows app and the only source of an official score, so I wrote the PowerShell layer that drives it: launch, menus, window focus, scoring, summarising a run. An agent can now fly a candidate policy and get a scored result back with nobody at the machine.',
      'The other half is rules. Cascading context with an enforced read order, and an iteration prompt that fixes the procedure: name the failure, one hypothesis, the smallest change, three live attempts, promote or revert. Qualification blocks certain telemetry, so the rules make consuming it illegal rather than merely unwise, and no agent can wander into a disqualifying change.',
      'I also run the subteam’s technical interviews, twenty-odd so far, on a problem set I wrote: LeetCode in shape, drone in substance, so candidates reason about gates and trajectories instead of generic arrays.',
    ],
  },
  {
    org: 'Cornell Extended Reality',
    orgUrl: 'https://cornellxr.com/team/',
    title: 'Software Team Member',
    dates: 'August 2025 – Present',
    location: 'Ithaca, NY',
    bullets: [
      'I designed the memory backend for a smart-glasses assistant that keeps track of the people the wearer has met: what was discussed, what is known about them and when it was learned, and how they connect to everyone else already stored. That is the context handed to the dialog model.',
      'I also built the resolver that maps “the guy from the climbing gym” onto a specific person. When a description fits more than one, it hands the model the details that separate them, so the assistant asks rather than guessing and being confidently wrong. More recently I added speech recognition, so conversations store themselves.',
    ],
  },
];

export const sections = [
  { id: 'intro', num: '01', label: 'Intro' },
  { id: 'experience', num: '02', label: 'Experience' },
  { id: 'projects', num: '03', label: 'Projects' },
  { id: 'contact', num: '04', label: 'Contact' },
];
