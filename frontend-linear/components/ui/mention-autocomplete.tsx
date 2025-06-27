"use client"

import { useState, useRef, useEffect, useCallback } from "react"
import { cn } from "@/lib/utils"
import { Check } from "lucide-react"

export interface MentionEntity {
  id: string
  type: "stakeholder" | "deal" | "account"
  name: string
  subtitle?: string
  metadata?: string
  confidence?: number
}

interface MentionTrigger {
  startIndex: number
  endIndex: number
  type: "stakeholder" | "deal" | "account"
  query: string
  symbol: string
}

interface MentionAutocompleteProps {
  value: string
  onChange: (value: string) => void
  onMentionsChange?: (mentions: MentionEntity[]) => void
  placeholder?: string
  className?: string
  disabled?: boolean
  onSearch?: (query: string, type: "stakeholder" | "deal" | "account") => Promise<MentionEntity[]>
}

const TRIGGER_SYMBOLS = {
  "@": "stakeholder",
  "#": "deal",
  "+": "account"
} as const

export function MentionAutocomplete({
  value,
  onChange,
  onMentionsChange,
  placeholder = "Type your notes... Use @ for people, # for deals, + for accounts",
  className,
  disabled = false,
  onSearch
}: MentionAutocompleteProps) {
  const [activeTrigger, setActiveTrigger] = useState<MentionTrigger | null>(null)
  const [searchResults, setSearchResults] = useState<MentionEntity[]>([])
  const [selectedIndex, setSelectedIndex] = useState(0)
  const [mentions, setMentions] = useState<MentionEntity[]>([])
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  const dropdownRef = useRef<HTMLDivElement>(null)

  // Search function that calls the backend API
  const apiSearch = async (query: string, type: "stakeholder" | "deal" | "account"): Promise<MentionEntity[]> => {
    // Allow search with empty query to show all entities of that type
    const searchQuery = query || "a" // Use 'a' as fallback to get results
    
    try {
      const response = await fetch(`http://localhost:8000/api/entities/search?q=${encodeURIComponent(searchQuery)}&type=${type}`)
      if (!response.ok) {
        console.error("Failed to search entities:", response.statusText)
        return []
      }
      const results = await response.json()
      return results.map((item: any) => ({
        id: item.id,
        type: item.type,
        name: item.name,
        subtitle: item.subtitle,
        confidence: item.confidence
      }))
    } catch (error) {
      console.error("Error searching entities:", error)
      return []
    }
  }

  // Detect trigger symbols and extract query
  const detectTrigger = useCallback((text: string, cursorPos: number): MentionTrigger | null => {
    // Look backwards from cursor to find a trigger symbol within the current "word"
    let i = cursorPos - 1
    
    // Only look within the current word/token (until we hit whitespace)
    while (i >= 0 && !/\s/.test(text[i])) {
      const char = text[i]
      
      // Check if we hit a trigger symbol
      if (char in TRIGGER_SYMBOLS) {
        // Check if it's at the start or preceded by whitespace
        if (i === 0 || /\s/.test(text[i - 1])) {
          const query = text.substring(i + 1, cursorPos)
          return {
            startIndex: i,
            endIndex: cursorPos,
            type: TRIGGER_SYMBOLS[char as keyof typeof TRIGGER_SYMBOLS],
            query: query,
            symbol: char
          }
        }
        return null
      }
      
      i--
    }
    
    return null
  }, [])

  // Handle text changes and detect triggers
  const handleChange = useCallback((e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newValue = e.target.value
    const cursorPos = e.target.selectionStart
    
    onChange(newValue)
    
    // Detect trigger by looking backwards from cursor
    const trigger = detectTrigger(newValue, cursorPos)
    setActiveTrigger(trigger)
    
    if (trigger) {
      // Mock search with filtering based on query
      let mockResults: MentionEntity[] = []
      
      if (trigger.type === "stakeholder") {
        mockResults = [
          { id: "s1", type: "stakeholder", name: "Sarah Martinez", subtitle: "VP Digital Experience • Optimizely Inc" },
          { id: "s2", type: "stakeholder", name: "Sarah Johnson", subtitle: "CFO • Linear Software" },
          { id: "s3", type: "stakeholder", name: "David Chen", subtitle: "IT Director • Optimizely Inc" },
          { id: "s4", type: "stakeholder", name: "David Park", subtitle: "VP Sales • Salesforce Corp" }
        ]
      } else if (trigger.type === "deal") {
        mockResults = [
          { id: "d1", type: "deal", name: "Q4 Implementation", subtitle: "Technical Evaluation • Optimizely Inc • $150k" },
          { id: "d2", type: "deal", name: "Q4 Expansion", subtitle: "Negotiation • Salesforce Corp • $200k" },
          { id: "d3", type: "deal", name: "Q4 Renewal", subtitle: "Closing • Linear Software • $50k" }
        ]
      } else if (trigger.type === "account") {
        mockResults = [
          { id: "a1", type: "account", name: "Optimizely Inc", subtitle: "Enterprise • Technology • San Francisco" },
          { id: "a2", type: "account", name: "Salesforce Corp", subtitle: "Enterprise • Technology • San Francisco" },
          { id: "a3", type: "account", name: "Linear Software", subtitle: "Mid-Market • Technology • New York" }
        ]
      }
      
      // Filter results based on query
      if (trigger.query) {
        const queryLower = trigger.query.toLowerCase()
        mockResults = mockResults.filter(result =>
          result.name.toLowerCase().includes(queryLower)
        )
      }
      
      setSearchResults(mockResults)
      setSelectedIndex(0)
    } else {
      setSearchResults([])
    }
  }, [onChange, detectTrigger])

  // Handle keyboard navigation
  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (!activeTrigger || searchResults.length === 0) return

    switch (e.key) {
      case "ArrowDown":
        e.preventDefault()
        setSelectedIndex(prev => (prev + 1) % searchResults.length)
        break
      case "ArrowUp":
        e.preventDefault()
        setSelectedIndex(prev => (prev - 1 + searchResults.length) % searchResults.length)
        break
      case "Enter":
      case "Tab":
        e.preventDefault()
        if (searchResults[selectedIndex]) {
          acceptMention(searchResults[selectedIndex])
        }
        break
      case "Escape":
        e.preventDefault()
        setActiveTrigger(null)
        setSearchResults([])
        break
    }
  }, [activeTrigger, searchResults, selectedIndex])

  // Accept a mention
  const acceptMention = useCallback((entity: MentionEntity) => {
    if (!activeTrigger || !textareaRef.current) return

    const before = value.substring(0, activeTrigger.startIndex)
    const after = value.substring(activeTrigger.endIndex)
    const newValue = before + activeTrigger.symbol + entity.name + " " + after
    
    onChange(newValue)
    
    // Update mentions list
    const newMentions = [...mentions, entity]
    setMentions(newMentions)
    onMentionsChange?.(newMentions)
    
    // Reset state
    setActiveTrigger(null)
    setSearchResults([])
    
    // Set cursor position after the mention
    setTimeout(() => {
      if (textareaRef.current) {
        const newPos = activeTrigger.startIndex + activeTrigger.symbol.length + entity.name.length + 1
        textareaRef.current.setSelectionRange(newPos, newPos)
        textareaRef.current.focus()
      }
    }, 0)
  }, [activeTrigger, value, onChange, mentions, onMentionsChange])

  // Get accurate cursor position using the proper browser method
  const getCaretCoordinates = () => {
    if (!textareaRef.current || !activeTrigger) return { top: 0, left: 0 }

    const textarea = textareaRef.current
    
    // This is the technique Cursor and other editors use
    // Create a div element with the same styling as the textarea
    const div = document.createElement('div')
    const computedStyle = window.getComputedStyle(textarea)
    
    // Copy the essential style properties
    const properties = [
      'fontFamily', 'fontSize', 'fontWeight', 'fontStyle', 'letterSpacing',
      'textTransform', 'wordSpacing', 'textIndent', 'whiteSpace', 'lineHeight',
      'paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft',
      'borderTopWidth', 'borderRightWidth', 'borderBottomWidth', 'borderLeftWidth',
      'borderStyle', 'overflowWrap', 'wordWrap', 'wordBreak'
    ]
    
    properties.forEach(prop => {
      div.style[prop as any] = computedStyle[prop as any]
    })
    
    div.style.position = 'absolute'
    div.style.visibility = 'hidden'
    div.style.whiteSpace = 'pre-wrap'
    div.style.wordWrap = 'break-word'
    div.style.top = '0'
    div.style.left = '0'
    div.style.width = textarea.clientWidth + 'px'
    div.style.height = 'auto'
    
    // Split the text at the trigger position
    const textBeforeCursor = textarea.value.substring(0, activeTrigger.startIndex)
    const textAfterCursor = textarea.value.substring(activeTrigger.startIndex)
    
    // Add the text before cursor
    div.appendChild(document.createTextNode(textBeforeCursor))
    
    // Add a span element at cursor position to measure
    const span = document.createElement('span')
    span.appendChild(document.createTextNode('|'))
    div.appendChild(span)
    
    // Add the text after cursor
    div.appendChild(document.createTextNode(textAfterCursor))
    
    // Add to DOM to measure
    document.body.appendChild(div)
    
    // Get the span position
    const spanRect = span.getBoundingClientRect()
    const textareaRect = textarea.getBoundingClientRect()
    
    // Calculate relative position
    const coordinates = {
      top: spanRect.top - textareaRect.top + textareaRect.height + 4,
      left: spanRect.left - textareaRect.left + textareaRect.left
    }
    
    // Clean up
    document.body.removeChild(div)
    
    return coordinates
  }

  return (
    <div className="relative">
      <textarea
        ref={textareaRef}
        value={value}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        disabled={disabled}
        className={cn(
          "w-full min-h-[120px] p-3 text-sm",
          "bg-white dark:bg-gray-900",
          "border border-gray-200 dark:border-gray-800",
          "rounded-md resize-none",
          "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
          "placeholder:text-gray-400",
          disabled && "opacity-50 cursor-not-allowed",
          className
        )}
        rows={6}
      />

      {/* Autocomplete Dropdown */}
      {activeTrigger && searchResults.length > 0 && (
        <div
          ref={dropdownRef}
          className="fixed z-50 w-80 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-md shadow-lg overflow-hidden"
          style={{
            top: getCaretCoordinates().top,
            left: getCaretCoordinates().left
          }}
        >
          <div className="max-h-64 overflow-y-auto">
            {searchResults.map((result, index) => (
              <button
                key={result.id}
                type="button"
                className={cn(
                  "w-full px-3 py-2 text-left",
                  "hover:bg-gray-100 dark:hover:bg-gray-800",
                  "transition-colors",
                  "flex items-center justify-between gap-2",
                  selectedIndex === index && "bg-gray-100 dark:bg-gray-800"
                )}
                onClick={() => acceptMention(result)}
                onMouseEnter={() => setSelectedIndex(index)}
              >
                <div className="flex-1 min-w-0">
                  <div className="font-medium text-sm truncate">{result.name}</div>
                  {result.subtitle && (
                    <div className="text-xs text-gray-500 truncate">{result.subtitle}</div>
                  )}
                </div>
                {selectedIndex === index && (
                  <Check className="h-4 w-4 text-blue-600 flex-shrink-0" />
                )}
              </button>
            ))}
          </div>
          <div className="px-3 py-2 text-xs text-gray-500 border-t border-gray-200 dark:border-gray-800">
            <kbd className="px-1 py-0.5 bg-gray-100 dark:bg-gray-800 rounded text-xs">↑↓</kbd> Navigate
            {" "}
            <kbd className="px-1 py-0.5 bg-gray-100 dark:bg-gray-800 rounded text-xs">Enter</kbd> Select
            {" "}
            <kbd className="px-1 py-0.5 bg-gray-100 dark:bg-gray-800 rounded text-xs">Esc</kbd> Close
          </div>
        </div>
      )}
    </div>
  )
}