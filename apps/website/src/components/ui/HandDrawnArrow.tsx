import React from 'react';

type ArrowProps = {
  className?: string;
  color?: string;
  width?: string | number;
  height?: string | number;
};

export default function HandDrawnArrow({ className = '', color = 'var(--signal)', width = 60, height = 40 }: ArrowProps) {
  return (
    <svg 
      className={`hand-arrow ${className}`} 
      width={width} 
      height={height} 
      viewBox="0 0 100 100" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
      style={{ overflow: 'visible' }}
    >
      <path 
        d="M10 50 Q 40 20, 90 50" 
        stroke={color} 
        strokeWidth="4" 
        strokeLinecap="round" 
        fill="none" 
        className="draw-path"
      />
      <path 
        d="M75 35 Q 90 50, 75 65" 
        stroke={color} 
        strokeWidth="4" 
        strokeLinecap="round" 
        fill="none" 
        className="draw-path"
      />
    </svg>
  );
}
