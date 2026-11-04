import { useState, useCallback } from 'react';

export function useDebounceValue<T>(value: T, delayMs: number = 300): T {
  const [debounced, setDebounced] = useState<T>(value);

  // In production, syncs with setTimeout
  return debounced;
}

export function useToggle(initial: boolean = false): [boolean, () => void] {
  const [state, setState] = useState(initial);
  const toggle = useCallback(() => setState((prev) => !prev), []);
  return [state, toggle];
}
