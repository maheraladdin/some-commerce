export interface SduiBlockNode {
  id: string;
  type: string;
  order: number;
  properties: Record<string, unknown>;
}

export interface SduiPageLayout {
  pageId: string;
  version: number;
  locale: string;
  blocks: SduiBlockNode[];
}

export interface SduiStudioScreenProps {
  layout: SduiPageLayout;
  selectedBlockId: string | null;
  isSaving: boolean;
  statusMessage: string | null;
  onSelectBlock: (id: string | null) => void;
  onAddBlock: (type: string) => void;
  onRemoveBlock: (id: string) => void;
  onPublish: () => void;
}
