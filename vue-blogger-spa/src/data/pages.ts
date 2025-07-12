export interface BlogPage {
  id: string;
  title: string;
  content: string;
  published: string;
  updated: string;
  url: string;
}

export const samplePages: BlogPage[] = [
  {
    id: "page-1",
    title: "About Us",
    content: "<p>This is the about us page content.</p>",
    published: "2025-06-15",
    updated: "2025-06-15",
    url: "/p/about-us.html"
  },
  {
    id: "page-2",
    title: "Contact",
    content: "<p>This is the contact page content.</p>",
    published: "2025-06-16",
    updated: "2025-06-16",
    url: "/p/contact.html"
  }
];
