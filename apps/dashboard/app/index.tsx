import React from 'react';
import { Link } from 'expo-router';

export default function DashboardIndex() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col items-center justify-center p-6">
      <div className="max-w-md w-full bg-slate-900 border border-slate-800 rounded-lg p-8 shadow-xl">
        <h1 className="text-2xl font-bold text-center text-white mb-2">some-commerce Portal</h1>
        <p className="text-sm text-center text-slate-400 mb-8">
          Enterprise merchant, vendor & visual design control panel.
        </p>

        <div className="space-y-4">
          <Link
            href="/admin/sdui-studio"
            className="block w-full text-center px-4 py-3 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-md transition shadow"
          >
            Launch Visual SDUI Studio (US-12.1.1)
          </Link>
          <Link
            href="/vendor/dashboard"
            className="block w-full text-center px-4 py-3 bg-slate-800 hover:bg-slate-700 text-white font-semibold rounded-md border border-slate-700 transition"
          >
            Open Vendor Merchant Portal (US-11.1.4)
          </Link>
        </div>
      </div>
    </div>
  );
}
