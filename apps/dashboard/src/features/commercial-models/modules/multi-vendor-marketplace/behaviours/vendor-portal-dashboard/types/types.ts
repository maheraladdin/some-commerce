export interface SubOrderSummary {
  subOrderId: string;
  orderId: string;
  itemCount: number;
  totalMinor: number;
  currency: string;
  status: 'PENDING_FULFILLMENT' | 'AWB_PRINTED' | 'DISPATCHED' | 'DELIVERED';
  shipByDeadline: string;
}

export interface EscrowBalanceSummary {
  escrowHoldMinor: number;
  availableForPayoutMinor: number;
  totalSettledMinor: number;
  currency: string;
}

export interface VendorPortalScreenProps {
  orders: SubOrderSummary[];
  escrow: EscrowBalanceSummary;
  isLoading: boolean;
  onPrintAwb: (subOrderId: string) => void;
  onRefresh: () => void;
}
