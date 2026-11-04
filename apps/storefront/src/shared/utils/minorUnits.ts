const CURRENCY_DECIMALS: Record<string, number> = {
  JPY: 0,
  KRW: 0,
  BIF: 0,
  CLP: 0,
  DJF: 0,
  GNF: 0,
  ISK: 0,
  KMF: 0,
  PYG: 0,
  RWF: 0,
  UGX: 0,
  VND: 0,
  VUV: 0,
  XAF: 0,
  XOF: 0,
  XPF: 0,
  BHD: 3,
  JOD: 3,
  KWD: 3,
  OMR: 3,
  TND: 3,
};

export function getCurrencyDecimals(currency: string): number {
  return CURRENCY_DECIMALS[currency.toUpperCase()] ?? 2;
}

export function formatMinorUnits(amountMinor: string | number, currency: string = 'SAR'): string {
  try {
    const rawStr = String(amountMinor ?? '0').split('.')[0].trim();
    const decimals = getCurrencyDecimals(currency);
    if (!rawStr || rawStr === '0') {
      return decimals === 0 ? `0 ${currency}` : `0.${'0'.repeat(decimals)} ${currency}`;
    }
    const isNegative = rawStr.startsWith('-');
    const digits = isNegative ? rawStr.slice(1) : rawStr;
    if (decimals === 0) {
      const formatted = digits.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
      return `${isNegative ? '-' : ''}${formatted} ${currency}`;
    }
    const padded = digits.padStart(decimals + 1, '0');
    const whole = padded.slice(0, -decimals);
    const fraction = padded.slice(-decimals);
    const formattedWhole = whole.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return `${isNegative ? '-' : ''}${formattedWhole}.${fraction} ${currency}`;
  } catch {
    return `${amountMinor} ${currency}`;
  }
}
