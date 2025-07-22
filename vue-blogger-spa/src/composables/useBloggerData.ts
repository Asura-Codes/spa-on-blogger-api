import { ref, readonly, computed, onMounted } from 'vue';
import type { BloggerData } from '@/types/blogger';

// Default empty blogger data
const defaultBloggerData: BloggerData = {
  blog: {
    title: '',
    url: '',
    homepageUrl: '',
    pageName: '',
    pageType: '',
    locale: '',
    isMobile: false,
    languageDirection: 'ltr',
    metaDescription: '',
    blogId: '',
    version: '',
    author: {
      name: '',
      profileUrl: '',
      photoUrl: ''
    }
  },
  post: {
    id: '',
    title: '',
    url: '',
    author: '',
    timestamp: '',
    content: '',
    labels: [],
    numComments: 0,
    allowComments: false,
    firstImageUrl: '',
    isFirstPost: false,
    relatedPosts: []
  },
  page: {
    id: '',
    title: '',
    url: ''
  },
  navigation: {
    newerPageUrl: '',
    olderPageUrl: '',
    newerPostUrl: '',
    olderPostUrl: ''
  },
  archive: {
    isArchive: false,
    type: '',
    title: '',
    items: []
  },
  search: {
    isSearch: false,
    query: '',
    resultsCount: 0
  }
};

// Create reactive references to hold the blogger data
const bloggerData = ref<BloggerData>(defaultBloggerData);
const isInBloggerEnvironment = ref(false);

/**
 * Composable to access Blogger template data when the app is embedded in Blogger
 */
export function useBloggerData() {
  // Try to get blogger data on component mount
  onMounted(() => {
    updateBloggerData();
  });

  /**
   * Updates the bloggerData ref with data from window.bloggerData if available
   */
  function updateBloggerData() {
    if (window.bloggerData) {
      bloggerData.value = window.bloggerData;
      isInBloggerEnvironment.value = true;
      console.log('Blogger data loaded:', bloggerData.value);
    } else {
      isInBloggerEnvironment.value = false;
      console.log('Not running in Blogger environment');
    }
  }

  /**
   * Force refresh of blogger data
   */
  function refreshBloggerData() {
    updateBloggerData();
    return bloggerData.value;
  }

  // Computed properties for common values
  const blogTitle = computed(() => bloggerData.value.blog.title);
  const currentPageType = computed(() => bloggerData.value.blog.pageType);
  const currentPostTitle = computed(() => bloggerData.value.post.title);
  const currentPostContent = computed(() => bloggerData.value.post.content);

  // Additional computed properties for the enhanced data
  const isArchivePage = computed(() => bloggerData.value.archive.isArchive);
  const isSearchPage = computed(() => bloggerData.value.search.isSearch);
  const searchQuery = computed(() => bloggerData.value.search.query);
  const postLabels = computed(() => bloggerData.value.post.labels || []);
  const hasNewerPage = computed(() => !!bloggerData.value.navigation.newerPageUrl);
  const hasOlderPage = computed(() => !!bloggerData.value.navigation.olderPageUrl);

  return {
    bloggerData: readonly(bloggerData),
    isInBloggerEnvironment: readonly(isInBloggerEnvironment),
    refreshBloggerData,

    // Basic properties
    blogTitle,
    currentPageType,
    currentPostTitle,
    currentPostContent,

    // Enhanced properties
    isArchivePage,
    isSearchPage,
    searchQuery,
    postLabels,
    hasNewerPage,
    hasOlderPage,

    // Full objects for detailed access
    navigation: computed(() => bloggerData.value.navigation),
    archive: computed(() => bloggerData.value.archive),
    search: computed(() => bloggerData.value.search)
  };
}
