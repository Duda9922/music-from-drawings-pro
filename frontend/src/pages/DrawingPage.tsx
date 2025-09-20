import React, { useState, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Play, Download, Share2, Palette, Brush, Eraser, RotateCcw } from 'lucide-react';
import AdvancedDrawingCanvas from '../components/AdvancedDrawingCanvas';
import ColorPicker from '../components/ColorPicker';
import BrushSizeSlider from '../components/BrushSizeSlider';
import ToolSelector from '../components/ToolSelector';
import MusicPlayer from '../components/MusicPlayer';
import AnalysisDisplay from '../components/AnalysisDisplay';
import { useDrawingStore } from '../hooks/useDrawingStore';
import { useMusicGeneration } from '../hooks/useMusicGeneration';

const DrawingPage: React.FC = () => {
  const [canvasSize, setCanvasSize] = useState({ width: 800, height: 600 });
  const [showColorPicker, setShowColorPicker] = useState(false);
  const [showBrushSize, setShowBrushSize] = useState(false);
  const [showTools, setShowTools] = useState(false);
  
  const {
    currentColor,
    setCurrentColor,
    currentWidth,
    setCurrentWidth,
    currentTool,
    setCurrentTool,
    hasContent,
    imageData,
    setImageData,
    setHasContent
  } = useDrawingStore();

  const {
    generateMusic,
    isGenerating,
    musicResult,
    analysis,
    error
  } = useMusicGeneration();

  const handleGenerateMusic = useCallback(async () => {
    if (!imageData) return;
    
    try {
      await generateMusic(imageData);
    } catch (err) {
      console.error('Error generating music:', err);
    }
  }, [imageData, generateMusic]);

  const handleDownload = useCallback(() => {
    if (!imageData) return;
    
    const link = document.createElement('a');
    link.download = `drawing-${Date.now()}.png`;
    link.href = imageData;
    link.click();
  }, [imageData]);

  const handleShare = useCallback(async () => {
    if (!imageData) return;
    
    try {
      await navigator.share({
        title: 'My Drawing',
        text: 'Check out this drawing I created!',
        files: [new File([imageData], 'drawing.png', { type: 'image/png' })]
      });
    } catch (err) {
      // Fallback to copying to clipboard
      navigator.clipboard.writeText(window.location.href);
    }
  }, [imageData]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-8"
        >
          <h1 className="text-4xl font-bold gradient-text mb-4">
            🎨 Create Your Musical Masterpiece
          </h1>
          <p className="text-gray-600 text-lg">
            Draw something amazing and watch it transform into music using AI
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Drawing Canvas */}
          <div className="lg:col-span-2">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className="card p-6"
            >
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-semibold text-gray-800">Drawing Canvas</h2>
                <div className="flex gap-2">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setShowColorPicker(!showColorPicker)}
                    className="p-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors"
                  >
                    <Palette className="w-5 h-5" />
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setShowBrushSize(!showBrushSize)}
                    className="p-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors"
                  >
                    <Brush className="w-5 h-5" />
                  </motion.button>
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => setShowTools(!showTools)}
                    className="p-2 rounded-lg bg-gray-100 hover:bg-gray-200 transition-colors"
                  >
                    <Eraser className="w-5 h-5" />
                  </motion.button>
                </div>
              </div>

              {/* Tool panels */}
              {showColorPicker && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="mb-4"
                >
                  <ColorPicker
                    color={currentColor}
                    onChange={setCurrentColor}
                  />
                </motion.div>
              )}

              {showBrushSize && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="mb-4"
                >
                  <BrushSizeSlider
                    value={currentWidth}
                    onChange={setCurrentWidth}
                  />
                </motion.div>
              )}

              {showTools && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="mb-4"
                >
                  <ToolSelector
                    value={currentTool}
                    onChange={setCurrentTool}
                  />
                </motion.div>
              )}

              {/* Canvas */}
              <div className="flex justify-center">
                <AdvancedDrawingCanvas
                  width={canvasSize.width}
                  height={canvasSize.height}
                  onDrawingChange={setHasContent}
                  onImageData={setImageData}
                />
              </div>

              {/* Action buttons */}
              <div className="flex justify-center gap-4 mt-6">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleGenerateMusic}
                  disabled={!hasContent || isGenerating}
                  className="btn-primary flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isGenerating ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                      Generating...
                    </>
                  ) : (
                    <>
                      <Play className="w-4 h-4" />
                      Generate Music
                    </>
                  )}
                </motion.button>

                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleDownload}
                  disabled={!hasContent}
                  className="btn-secondary flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Download className="w-4 h-4" />
                  Download
                </motion.button>

                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={handleShare}
                  disabled={!hasContent}
                  className="btn-secondary flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Share2 className="w-4 h-4" />
                  Share
                </motion.button>
              </div>
            </motion.div>
          </div>

          {/* Analysis and Music Panel */}
          <div className="space-y-6">
            {/* Visual Analysis */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
            >
              <AnalysisDisplay analysis={analysis} />
            </motion.div>

            {/* Music Player */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
            >
              <MusicPlayer
                musicResult={musicResult}
                isGenerating={isGenerating}
                error={error}
              />
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DrawingPage;
