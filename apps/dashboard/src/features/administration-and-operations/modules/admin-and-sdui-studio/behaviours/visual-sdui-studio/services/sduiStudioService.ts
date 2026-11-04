import { SDUI_STUDIO_CONSTANTS } from '../constants/constants';
import type { SduiPageLayout } from '../types/types';

export const sduiStudioService = {
  async fetchLayout(pageId: string): Promise<SduiPageLayout> {
    const res = await fetch(`${SDUI_STUDIO_CONSTANTS.ENDPOINTS.LAYOUT}?pageId=${pageId}`);
    if (!res.ok) {
      throw new Error(`Failed to load SDUI layout: ${res.statusText}`);
    }
    return res.json();
  },

  async publishLayout(layout: SduiPageLayout): Promise<{ success: boolean; publishedVersion: number }> {
    const res = await fetch(SDUI_STUDIO_CONSTANTS.ENDPOINTS.PUBLISH, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(layout),
    });
    if (!res.ok) {
      throw new Error(`Failed to publish SDUI layout: ${res.statusText}`);
    }
    return res.json();
  },
};
