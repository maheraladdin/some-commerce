export const SDUI_STUDIO_CONSTANTS = {
  ENDPOINTS: {
    LAYOUT: '/admin/sdui/layout',
    PUBLISH: '/admin/sdui/publish',
  },
  DEFAULT_LOCALE: 'en-US',
  SUPPORTED_LOCALES: ['en-US', 'ar-EG', 'ar-SA'] as const,
  PALETTE_BLOCKS: [
    'HeroBannerBlock',
    'ProductCarouselBlock',
    'CountdownTimerBlock',
    'GridCategoryBlock',
    'TestimonialBlock',
  ] as const,
} as const;
