import React, { useRef, useEffect, useState, useCallback } from 'react';
import { motion } from 'framer-motion';

interface DrawingCanvasProps {
  width: number;
  height: number;
  onDrawingChange: (hasContent: boolean) => void;
  onImageData: (imageData: string) => void;
}

interface Point {
  x: number;
  y: number;
}

interface Stroke {
  points: Point[];
  color: string;
  width: number;
  tool: 'pen' | 'brush' | 'marker' | 'eraser';
}

const AdvancedDrawingCanvas: React.FC<DrawingCanvasProps> = ({
  width,
  height,
  onDrawingChange,
  onImageData,
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [currentStroke, setCurrentStroke] = useState<Stroke | null>(null);
  const [strokes, setStrokes] = useState<Stroke[]>([]);
  const [currentColor, setCurrentColor] = useState('#000000');
  const [currentWidth, setCurrentWidth] = useState(5);
  const [currentTool, setCurrentTool] = useState<'pen' | 'brush' | 'marker' | 'eraser'>('pen');
  const [hasContent, setHasContent] = useState(false);

  const getMousePos = useCallback((e: React.MouseEvent<HTMLCanvasElement>): Point => {
    const canvas = canvasRef.current;
    if (!canvas) return { x: 0, y: 0 };
    
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    
    return {
      x: (e.clientX - rect.left) * scaleX,
      y: (e.clientY - rect.top) * scaleY,
    };
  }, []);

  const getTouchPos = useCallback((e: React.TouchEvent<HTMLCanvasElement>): Point => {
    const canvas = canvasRef.current;
    if (!canvas) return { x: 0, y: 0 };
    
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    
    const touch = e.touches[0];
    return {
      x: (touch.clientX - rect.left) * scaleX,
      y: (touch.clientY - rect.top) * scaleY,
    };
  }, []);

  const startDrawing = useCallback((point: Point) => {
    setIsDrawing(true);
    const newStroke: Stroke = {
      points: [point],
      color: currentTool === 'eraser' ? '#FFFFFF' : currentColor,
      width: currentTool === 'eraser' ? currentWidth * 2 : currentWidth,
      tool: currentTool,
    };
    setCurrentStroke(newStroke);
  }, [currentColor, currentWidth, currentTool]);

  const draw = useCallback((point: Point) => {
    if (!isDrawing || !currentStroke) return;
    
    const updatedStroke = {
      ...currentStroke,
      points: [...currentStroke.points, point],
    };
    setCurrentStroke(updatedStroke);
  }, [isDrawing, currentStroke]);

  const stopDrawing = useCallback(() => {
    if (!isDrawing || !currentStroke) return;
    
    setStrokes(prev => [...prev, currentStroke]);
    setCurrentStroke(null);
    setIsDrawing(false);
    
    // Check if canvas has content
    const hasDrawnContent = strokes.length > 0 || currentStroke?.points.length > 1;
    setHasContent(hasDrawnContent);
    onDrawingChange(hasDrawnContent);
  }, [isDrawing, currentStroke, strokes.length, onDrawingChange]);

  const redrawCanvas = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    
    // Clear canvas
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw all strokes
    strokes.forEach(stroke => {
      if (stroke.points.length < 2) return;
      
      ctx.beginPath();
      ctx.strokeStyle = stroke.color;
      ctx.lineWidth = stroke.width;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      
      // Apply tool-specific styling
      if (stroke.tool === 'brush') {
        ctx.globalAlpha = 0.7;
        ctx.lineWidth = stroke.width * 1.5;
      } else if (stroke.tool === 'marker') {
        ctx.globalAlpha = 0.5;
        ctx.lineWidth = stroke.width * 2;
      } else if (stroke.tool === 'eraser') {
        ctx.globalCompositeOperation = 'destination-out';
      } else {
        ctx.globalAlpha = 1.0;
        ctx.globalCompositeOperation = 'source-over';
      }
      
      ctx.moveTo(stroke.points[0].x, stroke.points[0].y);
      for (let i = 1; i < stroke.points.length; i++) {
        ctx.lineTo(stroke.points[i].x, stroke.points[i].y);
      }
      ctx.stroke();
      
      // Reset composite operation
      ctx.globalCompositeOperation = 'source-over';
      ctx.globalAlpha = 1.0;
    });
    
    // Draw current stroke
    if (currentStroke && currentStroke.points.length > 1) {
      ctx.beginPath();
      ctx.strokeStyle = currentStroke.color;
      ctx.lineWidth = currentStroke.width;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      
      if (currentStroke.tool === 'brush') {
        ctx.globalAlpha = 0.7;
        ctx.lineWidth = currentStroke.width * 1.5;
      } else if (currentStroke.tool === 'marker') {
        ctx.globalAlpha = 0.5;
        ctx.lineWidth = currentStroke.width * 2;
      } else if (currentStroke.tool === 'eraser') {
        ctx.globalCompositeOperation = 'destination-out';
      }
      
      ctx.moveTo(currentStroke.points[0].x, currentStroke.points[0].y);
      for (let i = 1; i < currentStroke.points.length; i++) {
        ctx.lineTo(currentStroke.points[i].x, currentStroke.points[i].y);
      }
      ctx.stroke();
      
      ctx.globalCompositeOperation = 'source-over';
      ctx.globalAlpha = 1.0;
    }
    
    // Update image data
    const imageData = canvas.toDataURL('image/png');
    onImageData(imageData);
  }, [strokes, currentStroke, onImageData]);

  useEffect(() => {
    redrawCanvas();
  }, [redrawCanvas]);

  const clearCanvas = useCallback(() => {
    setStrokes([]);
    setCurrentStroke(null);
    setHasContent(false);
    onDrawingChange(false);
    
    const canvas = canvasRef.current;
    if (canvas) {
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.fillStyle = '#FFFFFF';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        onImageData(canvas.toDataURL('image/png'));
      }
    }
  }, [onDrawingChange, onImageData]);

  const undoLastStroke = useCallback(() => {
    if (strokes.length > 0) {
      setStrokes(prev => prev.slice(0, -1));
      const newHasContent = strokes.length > 1;
      setHasContent(newHasContent);
      onDrawingChange(newHasContent);
    }
  }, [strokes.length, onDrawingChange]);

  // Mouse events
  const handleMouseDown = (e: React.MouseEvent<HTMLCanvasElement>) => {
    e.preventDefault();
    const point = getMousePos(e);
    startDrawing(point);
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    e.preventDefault();
    const point = getMousePos(e);
    draw(point);
  };

  const handleMouseUp = (e: React.MouseEvent<HTMLCanvasElement>) => {
    e.preventDefault();
    stopDrawing();
  };

  // Touch events
  const handleTouchStart = (e: React.TouchEvent<HTMLCanvasElement>) => {
    e.preventDefault();
    const point = getTouchPos(e);
    startDrawing(point);
  };

  const handleTouchMove = (e: React.TouchEvent<HTMLCanvasElement>) => {
    e.preventDefault();
    const point = getTouchPos(e);
    draw(point);
  };

  const handleTouchEnd = (e: React.TouchEvent<HTMLCanvasElement>) => {
    e.preventDefault();
    stopDrawing();
  };

  return (
    <div className="relative">
      <canvas
        ref={canvasRef}
        width={width}
        height={height}
        className="drawing-canvas"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={stopDrawing}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
      />
      
      {/* Drawing tools overlay */}
      <div className="absolute top-4 left-4 flex gap-2">
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={clearCanvas}
          className="bg-white/90 hover:bg-white text-gray-700 px-3 py-2 rounded-lg shadow-md transition-colors"
        >
          Clear
        </motion.button>
        
        {strokes.length > 0 && (
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={undoLastStroke}
            className="bg-white/90 hover:bg-white text-gray-700 px-3 py-2 rounded-lg shadow-md transition-colors"
          >
            Undo
          </motion.button>
        )}
      </div>
      
      {/* Tool indicator */}
      <div className="absolute top-4 right-4 bg-white/90 px-3 py-2 rounded-lg shadow-md">
        <div className="flex items-center gap-2 text-sm text-gray-700">
          <div 
            className="w-4 h-4 rounded-full border-2 border-gray-300"
            style={{ backgroundColor: currentColor }}
          />
          <span className="capitalize">{currentTool}</span>
          <span className="text-xs">•</span>
          <span>{currentWidth}px</span>
        </div>
      </div>
    </div>
  );
};

export default AdvancedDrawingCanvas;
