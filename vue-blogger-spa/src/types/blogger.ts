/**
 * Type definitions for Blogger template data
 * These types represent the data available in the Blogger template environment
 */

export interface BloggerData {
  blog: BloggerBlog;
  post: BloggerPost;
  page: BloggerPage;
  navigation: BloggerNavigation;
  archive: BloggerArchive;
  search: BloggerSearch;
}

export interface BloggerBlog {
  title: string;
  url: string;
  homepageUrl: string;
  pageName: string;
  pageType: string;
  locale: string;
  isMobile: boolean;
  languageDirection: string;
  metaDescription: string;
  blogId: string;
  version: string;
  author: BloggerAuthor;
}

export interface BloggerAuthor {
  name: string;
  profileUrl: string;
  photoUrl: string;
}

export interface BloggerPost {
  id: string;
  title: string;
  url: string;
  author: string;
  timestamp: string;
  content: string;
  labels: string[];
  numComments: number;
  allowComments: boolean;
  firstImageUrl: string;
  isFirstPost: boolean;
  featuredImage?: string;
  relatedPosts: BloggerRelatedPost[];
}

export interface BloggerRelatedPost {
  id: string;
  title: string;
  url: string;
}

export interface BloggerPage {
  id: string;
  title: string;
  url: string;
}

export interface BloggerNavigation {
  newerPageUrl: string;
  olderPageUrl: string;
  newerPostUrl: string;
  olderPostUrl: string;
}

export interface BloggerArchive {
  isArchive: boolean;
  type: string;
  title: string;
  items: any[];
}

export interface BloggerSearch {
  isSearch: boolean;
  query: string;
  resultsCount: number;
}

// Augment the Window interface to include the bloggerData property
declare global {
  interface Window {
    bloggerData?: BloggerData;
    data?: any; // The raw Blogger data object
  }
}
