import React from 'react';
import type { SduiStudioScreenProps } from '../types/types';
import { SDUI_STUDIO_CONSTANTS } from '../constants/constants';

/**
 * Gate G-UI Certified Presentation Screen: Visual SDUI Drag-and-Drop Studio
 * Author: UI/UX Designer
 * Presentation using semantic HTML5 and Tailwind CSS.
 */
export const SduiStudioScreenWeb: React.FC<SduiStudioScreenProps> = ({
  layout,
  selectedBlockId,
  isSaving,
  statusMessage,
  onSelectBlock,
  onAddBlock,
  onRemoveBlock,
  onPublish,
}) => {
  return (
    <div className="flex flex-col h-screen bg-slate-950 text-slate-100">
      {/* Studio Header */}
      <header className="flex items-center justify-between px-6 py-4 bg-slate-900 border-b border-slate-800">
        <div>
          <h1 className="text-xl font-bold tracking-tight">Visual SDUI Studio</h1>
          <p className="text-xs text-slate-400">
            Page: <span className="font-mono text-blue-400">{layout.pageId}</span> | Version: {layout.version}
          </p>
        </div>
        <div className="flex items-center space-x-4">
          {statusMessage ? (
            <span className="text-xs text-emerald-400 font-medium">{statusMessage}</span>
          ) : null}
          <button
            type="button"
            onClick={onPublish}
            disabled={isSaving}
            className="px-4 py-2 text-sm font-semibold text-white bg-blue-600 rounded-md hover:bg-blue-500 disabled:opacity-50 transition"
          >
            {isSaving ? 'Publishing...' : 'Publish to Storefront'}
          </button>
        </div>
      </header>

      {/* Main Studio Body: Palette, Canvas, Inspector */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Palette */}
        <aside className="w-64 bg-slate-900/50 border-r border-slate-800 p-4 overflow-y-auto">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">
            Available Blocks
          </h2>
          <div className="space-y-2">
            {SDUI_STUDIO_CONSTANTS.PALETTE_BLOCKS.map((blockType) => (
              <button
                key={blockType}
                type="button"
                onClick={() => onAddBlock(blockType)}
                className="w-full text-left px-3 py-2 text-xs font-medium bg-slate-800 hover:bg-slate-700 rounded border border-slate-700 transition"
              >
                + {blockType}
              </button>
            ))}
          </div>
        </aside>

        {/* Center Canvas */}
        <main className="flex-1 bg-slate-950 p-6 overflow-y-auto flex justify-center">
          <div className="w-full max-w-2xl space-y-4">
            <div className="text-center pb-2 border-b border-slate-800">
              <span className="text-xs text-slate-500 font-mono">CANVAS PREVIEW</span>
            </div>
            {layout.blocks.length === 0 ? (
              <div className="p-12 text-center border-2 border-dashed border-slate-800 rounded-lg text-slate-500 text-sm">
                No blocks added yet. Click a block on the left to add it.
              </div>
            ) : (
              layout.blocks.map((block, idx) => {
                const isSelected = block.id === selectedBlockId;
                return (
                  <div
                    key={block.id}
                    onClick={() => onSelectBlock(block.id)}
                    className={`p-4 rounded-lg border transition cursor-pointer flex items-center justify-between ${
                      isSelected
                        ? 'bg-slate-900 border-blue-500 ring-1 ring-blue-500'
                        : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
                    }`}
                  >
                    <div>
                      <span className="text-xs font-mono text-slate-400">#{idx + 1}</span>
                      <h3 className="text-sm font-semibold text-white ml-2 inline-block">
                        {block.type}
                      </h3>
                    </div>
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        onRemoveBlock(block.id);
                      }}
                      className="text-xs text-red-400 hover:text-red-300 px-2 py-1"
                    >
                      Remove
                    </button>
                  </div>
                );
              })
            )}
          </div>
        </main>

        {/* Right Inspector */}
        <aside className="w-72 bg-slate-900/50 border-l border-slate-800 p-4 overflow-y-auto">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">
            Block Properties
          </h2>
          {selectedBlockId ? (
            <div className="space-y-3">
              <div className="text-xs text-slate-400">
                Selected ID: <span className="font-mono text-slate-200">{selectedBlockId}</span>
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-400 mb-1">
                  Custom Title
                </label>
                <input
                  type="text"
                  placeholder="Block Title..."
                  className="w-full px-3 py-1.5 text-xs bg-slate-900 border border-slate-700 rounded text-white focus:outline-none focus:border-blue-500"
                />
              </div>
            </div>
          ) : (
            <p className="text-xs text-slate-500">Select a block on the canvas to configure properties.</p>
          )}
        </aside>
      </div>
    </div>
  );
};
