import React from 'react';
import type { VendorPortalScreenProps } from '../types/types';

/**
 * Gate G-UI Certified Presentation Screen: Vendor Portal Dashboard
 * Author: UI/UX Designer
 * Presentation using semantic HTML5 and Tailwind CSS.
 */
export const VendorPortalScreenWeb: React.FC<VendorPortalScreenProps> = ({
  orders,
  escrow,
  isLoading,
  onPrintAwb,
  onRefresh,
}) => {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-8 space-y-8">
      {/* Top Bar */}
      <header className="flex items-center justify-between border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Merchant Vendor Portal</h1>
          <p className="text-sm text-slate-400">Manage orders, fulfillment, and escrow payouts.</p>
        </div>
        <button
          type="button"
          onClick={onRefresh}
          disabled={isLoading}
          className="px-4 py-2 text-sm font-semibold bg-slate-800 hover:bg-slate-700 rounded-md border border-slate-700 transition"
        >
          {isLoading ? 'Refreshing...' : 'Refresh Data'}
        </button>
      </header>

      {/* Escrow Financial Metrics */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-lg">
          <p className="text-xs uppercase font-medium text-slate-400">Escrow On Hold</p>
          <p className="text-2xl font-bold text-amber-400 mt-2">
            {(escrow.escrowHoldMinor / 100).toFixed(2)} {escrow.currency}
          </p>
          <p className="text-xs text-slate-500 mt-1">Pending order delivery confirmation</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-lg">
          <p className="text-xs uppercase font-medium text-slate-400">Available For Payout</p>
          <p className="text-2xl font-bold text-emerald-400 mt-2">
            {(escrow.availableForPayoutMinor / 100).toFixed(2)} {escrow.currency}
          </p>
          <p className="text-xs text-slate-500 mt-1">Eligible for instant bank transfer</p>
        </div>
        <div className="bg-slate-900 border border-slate-800 p-6 rounded-lg">
          <p className="text-xs uppercase font-medium text-slate-400">Total Settled</p>
          <p className="text-2xl font-bold text-slate-200 mt-2">
            {(escrow.totalSettledMinor / 100).toFixed(2)} {escrow.currency}
          </p>
          <p className="text-xs text-slate-500 mt-1">Lifetime fulfilled transactions</p>
        </div>
      </section>

      {/* Sub-Orders Fulfillment Table */}
      <section className="bg-slate-900 border border-slate-800 rounded-lg overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-800">
          <h2 className="text-base font-semibold text-white">Pending Sub-Orders</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-xs uppercase text-slate-400 border-b border-slate-800">
              <tr>
                <th scope="col" className="px-6 py-3">Sub-Order ID</th>
                <th scope="col" className="px-6 py-3">Items</th>
                <th scope="col" className="px-6 py-3">Total Amount</th>
                <th scope="col" className="px-6 py-3">Status</th>
                <th scope="col" className="px-6 py-3">Ship-By Deadline</th>
                <th scope="col" className="px-6 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {orders.map((ord) => (
                <tr key={ord.subOrderId} className="hover:bg-slate-800/40 transition">
                  <td className="px-6 py-4 font-mono font-medium text-blue-400">{ord.subOrderId}</td>
                  <td className="px-6 py-4">{ord.itemCount} items</td>
                  <td className="px-6 py-4 font-semibold text-white">
                    {(ord.totalMinor / 100).toFixed(2)} {ord.currency}
                  </td>
                  <td className="px-6 py-4">
                    <span
                      className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                        ord.status === 'AWB_PRINTED'
                          ? 'bg-blue-900/60 text-blue-300 border border-blue-700'
                          : 'bg-amber-900/60 text-amber-300 border border-amber-700'
                      }`}
                    >
                      {ord.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-xs font-mono text-slate-400">{ord.shipByDeadline}</td>
                  <td className="px-6 py-4 text-right">
                    <button
                      type="button"
                      onClick={() => onPrintAwb(ord.subOrderId)}
                      className="px-3 py-1.5 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-500 rounded transition"
                    >
                      Print AWB
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
};
