export const VENDOR_PORTAL_CONSTANTS = {
  ENDPOINTS: {
    SUB_ORDERS: '/admin/vendor/sub-orders',
    ESCROW_BALANCE: '/admin/vendor/escrow',
    PRINT_AWB: '/admin/vendor/awb',
  },
  POLL_INTERVAL_MS: 30_000,
  DEFAULT_PAGE_SIZE: 20,
} as const;
