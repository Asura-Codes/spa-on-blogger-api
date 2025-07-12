export interface BlogPost {
  id: number;
  title: string;
  content: string;
  author: string;
  date: string;
  tags: string[];
}

export const samplePosts: BlogPost[] = [
  {
    id: 1,
    title: 'Getting Started with Vue.js',
    content: 'Vue.js is a progressive framework for building user interfaces. Unlike other monolithic frameworks, Vue is designed from the ground up to be incrementally adoptable.',
    author: 'John Doe',
    date: '2025-06-15',
    tags: ['Vue', 'JavaScript', 'Frontend']
  },
  {
    id: 2,
    title: 'Embedding Vue in Blogger',
    content: 'Learn how to embed a Vue.js SPA into your Blogger site for dynamic functionality without leaving the Blogger platform.',
    author: 'Jane Smith',
    date: '2025-06-20',
    tags: ['Vue', 'Blogger', 'Embedding']
  },
  {
    id: 3,
    title: 'State Management with Pinia',
    content: 'Pinia is the new standard for state management in Vue applications, replacing Vuex. It offers a simpler API with full TypeScript support.',
    author: 'Alex Johnson',
    date: '2025-06-25',
    tags: ['Vue', 'Pinia', 'State Management']
  }
];
