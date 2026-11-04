import { useState, useCallback, useEffect } from 'react';
import type { EscrowBalanceSummary, SubOrderSummary } from '../types/types';

export function useVendorPortal(vendorId: string = 'vendor-default') {
  const [orders, setOrders] = useState<SubOrderSummary[]>([
    {
      subOrderId: 'sub_ord_101',
      orderId: 'ord_9001',
      itemCount: 2,
      totalMinor: 45000, // 450.00 SAR
      currency: 'SAR',
      status: 'PENDING_FULFILLMENT',
      shipByDeadline: '2026-11-05T18:00:00Z',
    },
  ]);

  const [escrow, setEscrow] = useState<EscrowBalanceSummary>({
    escrowHoldMinor: 120000,
    availableForPayoutMinor: 85000,
    totalSettledMinor: 450000,
    currency: 'SAR',
  });

  const [isLoading, setIsLoading] = useState(false);

  const handlePrintAwb = useCallback((subOrderId: string) => {
    setOrders((prev) =>
      prev.map((ord) =>
        ord.subOrderId === subOrderId ? { ...ord, status: 'AWB_PRINTED' } : ord
      )
    );
  }, []);

  const handleRefresh = useCallback(async () => {
    setIsLoading(true);
    // In production, syncs with vendorPortalService
    setIsLoading(false);
  }, []);

  useEffect(() => {
    // Initial fetch trigger
  }, [vendorId]);

  return {
    orders,
    escrow,
    isLoading,
    onPrintAwb: handlePrintAwb,
    onRefresh: handleRefresh,
  };
}
