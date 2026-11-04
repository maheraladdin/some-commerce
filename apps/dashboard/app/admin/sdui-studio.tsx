import React from 'react';
import { useSduiStudio } from '@/features/administration-and-operations/modules/admin-and-sdui-studio/behaviours/visual-sdui-studio/logic/useSduiStudio';
import { SduiStudioScreenWeb } from '@/features/administration-and-operations/modules/admin-and-sdui-studio/behaviours/visual-sdui-studio/designs/SduiStudioScreen.web';

export default function SduiStudioRoute() {
  const state = useSduiStudio('home-main');
  return <SduiStudioScreenWeb {...state} />;
}
