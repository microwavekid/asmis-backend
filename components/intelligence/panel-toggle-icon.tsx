// PATTERN_REF: LINEAR_UI_PATTERN
// DECISION_REF: DEC_2025-06-24_007: Custom panel toggle icon like Linear

import { cn } from "@/lib/utils"

interface PanelToggleIconProps {
  isOpen: boolean
  className?: string
}

export function PanelToggleIcon({ isOpen, className }: PanelToggleIconProps) {
  return (
    <svg
      width="16"
      height="16"
      viewBox="0 0 16 16"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={cn("transition-colors", className)}
    >
      {/* Left panel */}
      <rect
        x="1"
        y="3"
        width="9"
        height="10"
        rx="1"
        stroke="currentColor"
        strokeWidth="1.5"
        fill="none"
      />
      
      {/* Right panel - fills when open with sliding animation */}
      <rect
        x="11"
        y="3"
        width="4"
        height="10"
        rx="1"
        stroke="currentColor"
        strokeWidth="1.5"
        fill="none"
      />
      
      {/* Sliding fill animation */}
      <rect
        x="11"
        y="3"
        width="4"
        height="10"
        rx="1"
        fill="var(--ai-processing)"
        style={{
          transform: `translateX(${isOpen ? '0' : '100%'})`,
          transition: 'transform 300ms cubic-bezier(0.4, 0, 0.2, 1)',
        }}
        mask="url(#panel-mask)"
      />
      
      <defs>
        <mask id="panel-mask">
          <rect x="11" y="3" width="4" height="10" rx="1" fill="white" />
        </mask>
      </defs>
      
      {/* Optional: Chevron indicator */}
      {!isOpen && (
        <path
          d="M12.5 6.5L14 8L12.5 9.5"
          stroke="currentColor"
          strokeWidth="1.5"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="transition-opacity duration-300"
        />
      )}
    </svg>
  )
}