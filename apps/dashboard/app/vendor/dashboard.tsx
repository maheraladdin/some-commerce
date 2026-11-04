import React from 'react';
import { useVendorPortal } from '@/features/commercial-models/modules/multi-vendor-marketplace/behaviours/vendor-portal-dashboard/logic/useVendorPortal';
import { VendorPortalScreenWeb } from '@/features/commercial-models/modules/multi-vendor-marketplace/behaviours/vendor-portal-dashboard/designs/VendorPortalScreen.web';

export default function VendorDashboardRoute() {
  const state = useVendorPortal('vendor-1');
  return <VendorPortalScreenWeb {...state} />;
}
