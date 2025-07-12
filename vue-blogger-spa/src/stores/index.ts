// stores/index.ts
import { createPinia } from 'pinia';

export const pinia = createPinia();

// re-export all stores
export * from './blog';
export * from './page';
