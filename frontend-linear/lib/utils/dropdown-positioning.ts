// PATTERN_REF: COMPONENT_DATA_MAPPING_PATTERN
// DECISION_REF: DEC_2025-07-08_003
// Dropdown positioning utilities with collision detection and viewport boundaries

export interface DropdownPosition {
  x: number
  y: number
  side: 'top' | 'bottom' | 'left' | 'right'
  align: 'start' | 'center' | 'end'
}

export interface ViewportBounds {
  width: number
  height: number
}

export interface DropdownDimensions {
  width: number
  height: number
}

/**
 * Calculates optimal dropdown position with collision detection
 * @param triggerRect - Bounding rectangle of trigger element
 * @param dropdownSize - Width and height of dropdown
 * @param preferredSide - Preferred side for dropdown placement
 * @param offset - Offset from trigger element
 * @param padding - Padding from viewport edges
 */
export function calculateDropdownPosition(
  triggerRect: DOMRect,
  dropdownSize: DropdownDimensions,
  preferredSide: 'top' | 'bottom' | 'left' | 'right' = 'bottom',
  offset: number = 8,
  padding: number = 16
): DropdownPosition {
  const viewport: ViewportBounds = {
    width: window.innerWidth,
    height: window.innerHeight
  }

  // Define possible positions in order of preference
  const positions: Array<{ side: 'top' | 'bottom' | 'left' | 'right', align: 'start' | 'center' | 'end' }> = [
    { side: preferredSide, align: 'start' },
    { side: preferredSide, align: 'center' },
    { side: preferredSide, align: 'end' },
    // Fallback to opposite side if preferred doesn't fit
    { side: preferredSide === 'bottom' ? 'top' : 'bottom', align: 'start' },
    { side: preferredSide === 'bottom' ? 'top' : 'bottom', align: 'center' },
    { side: preferredSide === 'bottom' ? 'top' : 'bottom', align: 'end' },
    // Try left/right if vertical doesn't work
    { side: 'right', align: 'start' },
    { side: 'left', align: 'start' }
  ]

  for (const pos of positions) {
    const coords = calculatePositionCoordinates(triggerRect, dropdownSize, pos.side, pos.align, offset)
    
    if (fitsInViewport(coords, dropdownSize, viewport, padding)) {
      return {
        x: coords.x,
        y: coords.y,
        side: pos.side,
        align: pos.align
      }
    }
  }

  // If nothing fits, use preferred position with viewport constraints
  const fallbackCoords = calculatePositionCoordinates(triggerRect, dropdownSize, preferredSide, 'start', offset)
  return {
    x: Math.max(padding, Math.min(fallbackCoords.x, viewport.width - dropdownSize.width - padding)),
    y: Math.max(padding, Math.min(fallbackCoords.y, viewport.height - dropdownSize.height - padding)),
    side: preferredSide,
    align: 'start'
  }
}

/**
 * Calculates coordinates for a specific position
 */
function calculatePositionCoordinates(
  triggerRect: DOMRect,
  dropdownSize: DropdownDimensions,
  side: 'top' | 'bottom' | 'left' | 'right',
  align: 'start' | 'center' | 'end',
  offset: number
): { x: number, y: number } {
  let x: number, y: number

  // Calculate base position
  switch (side) {
    case 'bottom':
      x = triggerRect.left
      y = triggerRect.bottom + offset
      break
    case 'top':
      x = triggerRect.left
      y = triggerRect.top - dropdownSize.height - offset
      break
    case 'right':
      x = triggerRect.right + offset
      y = triggerRect.top
      break
    case 'left':
      x = triggerRect.left - dropdownSize.width - offset
      y = triggerRect.top
      break
  }

  // Adjust for alignment
  if (side === 'top' || side === 'bottom') {
    switch (align) {
      case 'center':
        x = triggerRect.left + triggerRect.width / 2 - dropdownSize.width / 2
        break
      case 'end':
        x = triggerRect.right - dropdownSize.width
        break
      // 'start' is already handled by base position
    }
  } else {
    switch (align) {
      case 'center':
        y = triggerRect.top + triggerRect.height / 2 - dropdownSize.height / 2
        break
      case 'end':
        y = triggerRect.bottom - dropdownSize.height
        break
      // 'start' is already handled by base position
    }
  }

  return { x, y }
}

/**
 * Checks if dropdown fits within viewport boundaries
 */
function fitsInViewport(
  position: { x: number, y: number },
  dropdownSize: DropdownDimensions,
  viewport: ViewportBounds,
  padding: number
): boolean {
  return (
    position.x >= padding &&
    position.y >= padding &&
    position.x + dropdownSize.width <= viewport.width - padding &&
    position.y + dropdownSize.height <= viewport.height - padding
  )
}

/**
 * Enhanced cursor position calculation with boundary checking
 * @param textarea - Textarea element
 * @param position - Cursor position in text
 * @param dropdownSize - Dropdown dimensions
 */
export function getCursorCoordinatesWithBounds(
  textarea: HTMLTextAreaElement,
  position: number,
  dropdownSize: DropdownDimensions
): DropdownPosition {
  const div = document.createElement('div')
  const style = getComputedStyle(textarea)
  
  // Copy textarea styles to div for measurement
  div.style.position = 'absolute'
  div.style.visibility = 'hidden'
  div.style.whiteSpace = 'pre-wrap'
  div.style.wordWrap = 'break-word'
  div.style.font = style.font
  div.style.lineHeight = style.lineHeight
  div.style.padding = style.padding
  div.style.border = style.border
  div.style.width = style.width
  div.style.height = style.height
  
  // Add text up to cursor position
  const textBeforeCursor = textarea.value.substring(0, position)
  div.textContent = textBeforeCursor
  
  // Add a span for cursor position
  const cursorSpan = document.createElement('span')
  cursorSpan.textContent = '|'
  div.appendChild(cursorSpan)
  
  document.body.appendChild(div)
  
  const textareaRect = textarea.getBoundingClientRect()
  const spanRect = cursorSpan.getBoundingClientRect()
  
  document.body.removeChild(div)
  
  // Create virtual trigger rect at cursor position
  const cursorRect = new DOMRect(
    spanRect.left,
    spanRect.top,
    2, // Small width for cursor
    spanRect.height
  )
  
  return calculateDropdownPosition(
    cursorRect,
    dropdownSize,
    'bottom', // Prefer bottom
    8 // 8px offset
  )
}

/**
 * Debounced resize handler for dropdown repositioning
 */
export function createResizeHandler(
  repositionCallback: () => void,
  debounceMs: number = 100
): () => void {
  let timeoutId: NodeJS.Timeout | null = null
  
  return () => {
    if (timeoutId) {
      clearTimeout(timeoutId)
    }
    
    timeoutId = setTimeout(() => {
      repositionCallback()
      timeoutId = null
    }, debounceMs)
  }
}