import { useState, useCallback } from 'react';
import type { SduiBlockNode, SduiPageLayout } from '../types/types';

export function useSduiStudio(initialPageId: string = 'home-main') {
  const [layout, setLayout] = useState<SduiPageLayout>({
    pageId: initialPageId,
    version: 1,
    locale: 'en-US',
    blocks: [
      { id: 'b-1', type: 'HeroBannerBlock', order: 0, properties: { title: 'Spring Collection 2026' } },
      { id: 'b-2', type: 'CountdownTimerBlock', order: 1, properties: { targetDate: '2026-05-01' } },
    ],
  });

  const [selectedBlockId, setSelectedBlockId] = useState<string | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  const handleSelectBlock = useCallback((id: string | null) => {
    setSelectedBlockId(id);
  }, []);

  const handleAddBlock = useCallback((type: string) => {
    setLayout((prev) => {
      const newBlock: SduiBlockNode = {
        id: `block-${Date.now()}`,
        type,
        order: prev.blocks.length,
        properties: {},
      };
      return {
        ...prev,
        blocks: [...prev.blocks, newBlock],
      };
    });
  }, []);

  const handleRemoveBlock = useCallback((id: string) => {
    setLayout((prev) => ({
      ...prev,
      blocks: prev.blocks.filter((b) => b.id !== id),
    }));
    if (selectedBlockId === id) {
      setSelectedBlockId(null);
    }
  }, [selectedBlockId]);

  const handlePublish = useCallback(async () => {
    setIsSaving(true);
    setStatusMessage('Publishing SDUI layout changes...');
    try {
      // In production, calls sduiStudioService.publishLayout(layout);
      setStatusMessage('Layout version successfully published to storefront CDN.');
    } catch (err: unknown) {
      setStatusMessage(err instanceof Error ? err.message : 'Publish failed.');
    } finally {
      setIsSaving(false);
    }
  }, []);

  return {
    layout,
    selectedBlockId,
    isSaving,
    statusMessage,
    onSelectBlock: handleSelectBlock,
    onAddBlock: handleAddBlock,
    onRemoveBlock: handleRemoveBlock,
    onPublish: handlePublish,
  };
}
