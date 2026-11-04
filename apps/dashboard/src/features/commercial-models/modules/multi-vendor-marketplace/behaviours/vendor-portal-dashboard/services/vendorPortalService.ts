import { VENDOR_PORTAL_CONSTANTS } from '../constants/constants';
import type { EscrowBalanceSummary, SubOrderSummary } from '../types/types';

export const vendorPortalService = {
  async fetchSubOrders(vendorId: string): Promise<SubOrderSummary[]> {
    const res = await fetch(`${VENDOR_PORTAL_CONSTANTS.ENDPOINTS.SUB_ORDERS}?vendorId=${vendorId}`);
    if (!res.ok) {
      throw new Error(`Failed to load sub-orders: ${res.statusText}`);
    }
    return res.json();
  },

  async fetchEscrowBalance(vendorId: string): Promise<EscrowBalanceSummary> {
    const res = await fetch(`${VENDOR_PORTAL_CONSTANTS.ENDPOINTS.ESCROW_BALANCE}?vendorId=${vendorId}`);
    if (!res.ok) {
      throw new Error(`Failed to load escrow balance: ${res.statusText}`);
    }
    return res.json();
  },
};
