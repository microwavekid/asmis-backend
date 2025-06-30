// PATTERN_REF: ENTITY_SELECTION_PATTERN
// DECISION_REF: DEC_2025-06-27_001: Bonusly UI Pattern Integration

"use client"

import { useState, useRef, useEffect, useCallback } from "react"
import { cn } from "@/lib/utils"
import { Entity, EntityChip } from "./entity-chip"
import { EntitySelectorButtons } from "./entity-selector-buttons"
import { entityColors, EntityType } from "@/lib/utils/colors"

interface AutocompleteMatch {
  entity: Entity
  matchedText: string
  suggestion: string
  startIndex: number
  endIndex: number
}

interface EntityRange {
  entity: Entity
  startIndex: number
  endIndex: number
  triggerIndex: number
}

interface HighlightedTextPart {
  text: string
  isEntity: boolean
  entity?: Entity
}

interface InlineAutocompleteProps {
  value: string
  onChange: (value: string, linkedEntities: Entity[]) => void
  placeholder?: string
  className?: string
  onEntitySearch?: (query: string) => Promise<Entity[]>
  linkedEntities?: Entity[]
  disabled?: boolean
}

interface GhostTextSuggestion {
  suggestion: string
  remainingText: string
  entity: Entity
}

export function InlineAutocomplete({
  value,
  onChange,
  placeholder = "Type your notes here...",
  className,
  onEntitySearch,
  linkedEntities = [],
  disabled = false
}: InlineAutocompleteProps) {
  const [currentMatch, setCurrentMatch] = useState<AutocompleteMatch | null>(null)
  const [isComposing, setIsComposing] = useState(false)
  const [cursorPosition, setCursorPosition] = useState(0)
  const [searchResults, setSearchResults] = useState<Entity[]>([])
  const [entityRanges, setEntityRanges] = useState<EntityRange[]>([])
  const [activeEntityType, setActiveEntityType] = useState<EntityType | null>(null)
  const [ghostText, setGhostText] = useState<GhostTextSuggestion | null>(null)
  const [dropdownPosition, setDropdownPosition] = useState({ x: 0, y: 0 })
  
  const textareaRef = useRef<HTMLTextAreaElement>(null)
  
  // Parse text to identify entity mentions for highlighting
  const parseTextForHighlighting = useCallback((text: string): HighlightedTextPart[] => {
    const parts: HighlightedTextPart[] = []
    let currentIndex = 0
    
    // Find all entity mentions in the text
    const entityMentions: { start: number, end: number, entity: Entity }[] = []
    
    linkedEntities.forEach(entity => {
      // Look for @entity.name, #entity.name, or +entity.name patterns (exact match only)
      const triggers = ['@', '#', '+']
      triggers.forEach(trigger => {
        const escapedName = entity.name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
        const pattern = new RegExp(`\\${trigger}${escapedName}(?=\\s|$|\\n)`, 'gi')
        let match
        while ((match = pattern.exec(text)) !== null) {
          entityMentions.push({
            start: match.index,
            end: match.index + match[0].length,
            entity: entity
          })
        }
      })
    })
    
    // Sort mentions by start position and remove overlaps
    entityMentions.sort((a, b) => a.start - b.start)
    
    // Remove overlapping mentions (keep first one)
    const nonOverlappingMentions = []
    let lastEnd = -1
    for (const mention of entityMentions) {
      if (mention.start >= lastEnd) {
        nonOverlappingMentions.push(mention)
        lastEnd = mention.end
      }
    }
    
    // Build parts array with highlighting
    nonOverlappingMentions.forEach(mention => {
      // Add text before entity
      if (currentIndex < mention.start) {
        parts.push({
          text: text.substring(currentIndex, mention.start),
          isEntity: false
        })
      }
      
      // Add entity
      parts.push({
        text: text.substring(mention.start, mention.end),
        isEntity: true,
        entity: mention.entity
      })
      
      currentIndex = mention.end
    })
    
    // Add remaining text
    if (currentIndex < text.length) {
      parts.push({
        text: text.substring(currentIndex),
        isEntity: false
      })
    }
    
    return parts
  }, [linkedEntities])
  
  // Calculate cursor position for dropdown placement
  const getCursorCoordinates = useCallback((textarea: HTMLTextAreaElement, position: number) => {
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
    
    return {
      x: spanRect.left - textareaRect.left,
      y: spanRect.top - textareaRect.top + 24 // 24px below cursor
    }
  }, [])

  // Mock entity search - replace with real API call
  const mockEntitySearch = useCallback(async (query: string, entityType?: EntityType | null): Promise<Entity[]> => {
    const mockEntities: Entity[] = [
      {
        id: "1",
        type: "stakeholder",
        name: "Sarah Martinez",
        confidence: 0.95,
        attributes: {
          title: "VP Digital Experience",
          email: "sarah.martinez@optimizely.com",
          department: "Product",
          lastContact: "2024-06-20",
          account: "Optimizely Inc"
        }
      },
      {
        id: "2", 
        type: "stakeholder",
        name: "David Chen",
        confidence: 0.92,
        attributes: {
          title: "IT Director",
          email: "david.chen@optimizely.com",
          department: "Technology",
          lastContact: "2024-06-18",
          account: "Optimizely Inc"
        }
      },
      {
        id: "3",
        type: "account",
        name: "Optimizely Inc",
        confidence: 0.90,
        attributes: {
          company: "Optimizely Inc",
          industry: "Technology"
        }
      },
      {
        id: "4",
        type: "deal",
        name: "Q4 Implementation",
        confidence: 0.88,
        attributes: {
          dealValue: 150000,
          dealStage: "technical_evaluation",
          account: "Optimizely Inc"
        }
      }
    ]
    
    // Filter by entity type if specified
    let filtered = mockEntities
    if (entityType) {
      filtered = filtered.filter(entity => entity.type === entityType)
    }
    
    // Filter by query (show all if query is empty)
    if (query === "") {
      return filtered
    }
    
    return filtered.filter(entity => 
      entity.name.toLowerCase().includes(query.toLowerCase())
    )
  }, [])

  // Handle entity type selection from buttons
  const handleEntityTypeSelect = useCallback((type: EntityType, trigger: string) => {
    if (!textareaRef.current) return
    
    const textarea = textareaRef.current
    const start = textarea.selectionStart
    const end = textarea.selectionEnd
    const newValue = value.substring(0, start) + trigger + value.substring(end)
    
    onChange(newValue, linkedEntities)
    setActiveEntityType(type)
    
    // Set cursor position after trigger
    setTimeout(() => {
      textarea.setSelectionRange(start + 1, start + 1)
      textarea.focus()
      setCursorPosition(start + 1)
    }, 0)
  }, [value, linkedEntities, onChange])

  // Extract potential entity mentions from text (improved to handle spaces)
  const extractPotentialEntities = useCallback((text: string, position: number) => {
    // Look backwards from cursor to find trigger character
    for (let i = position - 1; i >= 0; i--) {
      const char = text[i]
      
      if (char === '@' || char === '#' || char === '+') {
        // Make sure trigger is at start or after whitespace
        if (i === 0 || /\s/.test(text[i - 1])) {
          const query = text.substring(i + 1, position)
          return {
            query: query.trim(), // Allow spaces but trim for matching
            startIndex: i + 1,
            endIndex: position,
            triggerIndex: i,
            triggerChar: char
          }
        }
      }
      
      // Stop at line breaks but allow spaces within entity names
      if (char === '\n') {
        break
      }
      
      // If we hit another trigger character, we've gone too far
      if ((char === '@' || char === '#' || char === '+') && i !== position - 1) {
        break
      }
    }
    
    return null
  }, [])

  // Detect active entity type from triggers
  useEffect(() => {
    if (!value || cursorPosition === 0) {
      setActiveEntityType(null)
      return
    }

    // Look backwards from cursor to find the nearest trigger
    let searchPos = cursorPosition - 1
    while (searchPos >= 0) {
      const char = value[searchPos]
      
      // Check for entity triggers
      if (char === '@') {
        setActiveEntityType('stakeholder')
        break
      } else if (char === '#') {
        setActiveEntityType('deal')
        break
      } else if (char === '+') {
        setActiveEntityType('account')
        break
      } else if (char === ' ' || char === '\n') {
        // Stop at word boundary
        setActiveEntityType(null)
        break
      }
      
      searchPos--
    }
  }, [value, cursorPosition])

  // Handle entity search and matching with ghost text
  useEffect(() => {
    if (isComposing || !value) {
      setCurrentMatch(null)
      setSearchResults([])
      setGhostText(null)
      return
    }

    const searchForEntities = async () => {
      const potential = extractPotentialEntities(value, cursorPosition)
      if (!potential) {
        setCurrentMatch(null)
        setSearchResults([])
        setGhostText(null)
        return
      }

      // Update dropdown position
      if (textareaRef.current) {
        const coords = getCursorCoordinates(textareaRef.current, cursorPosition)
        setDropdownPosition(coords)
      }

      try {
        const searchFn = onEntitySearch || ((query: string) => mockEntitySearch(query, activeEntityType))
        const results = await searchFn(potential.query)
        setSearchResults(results)
        
        // Set ghost text and current match if we have results
        if (results.length > 0) {
          const bestMatch = results[0]
          const currentQuery = potential.query.toLowerCase()
          const matchName = bestMatch.name.toLowerCase()
          
          // Calculate ghost text - only show remaining letters
          let remainingText = ""
          if (matchName.startsWith(currentQuery) && currentQuery.length < matchName.length) {
            remainingText = bestMatch.name.substring(potential.query.length)
          }
          
          setGhostText({
            suggestion: bestMatch.name,
            remainingText: remainingText,
            entity: bestMatch
          })
          
          setCurrentMatch({
            entity: bestMatch,
            matchedText: potential.query,
            suggestion: bestMatch.name,
            startIndex: potential.startIndex,
            endIndex: potential.endIndex
          })
        } else {
          setCurrentMatch(null)
          setGhostText(null)
        }
      } catch (error) {
        console.error("Entity search failed:", error)
        setCurrentMatch(null)
        setSearchResults([])
        setGhostText(null)
      }
    }

    const debounceTimer = setTimeout(searchForEntities, 100)
    return () => clearTimeout(debounceTimer)
  }, [value, cursorPosition, isComposing, extractPotentialEntities, onEntitySearch, mockEntitySearch, activeEntityType, getCursorCoordinates])

  // Handle cursor position changes
  const handleSelectionChange = useCallback(() => {
    if (textareaRef.current) {
      setCursorPosition(textareaRef.current.selectionStart)
    }
  }, [])

  // Handle keyboard events
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Tab" && currentMatch) {
      e.preventDefault()
      acceptSuggestion()
    } else if (e.key === "Escape" && currentMatch) {
      e.preventDefault()
      setCurrentMatch(null)
    }
  }

  // Accept a specific entity suggestion
  const acceptEntitySuggestion = useCallback((entity: Entity) => {
    if (!currentMatch) return

    const beforeMatch = value.substring(0, currentMatch.startIndex)
    const afterMatch = value.substring(currentMatch.endIndex)
    
    // Replace the matched text with the entity name
    const newValue = beforeMatch + entity.name + afterMatch
    
    // Add entity to linked entities if not already present
    const isAlreadyLinked = linkedEntities.some(e => e.id === entity.id)
    const newLinkedEntities = isAlreadyLinked 
      ? linkedEntities 
      : [...linkedEntities, entity]
    
    // Clear the current match and search results
    setCurrentMatch(null)
    setSearchResults([])
    
    onChange(newValue, newLinkedEntities)
    
    // Set cursor position after the accepted suggestion
    setTimeout(() => {
      if (textareaRef.current) {
        const newCursorPos = currentMatch.startIndex + entity.name.length
        textareaRef.current.setSelectionRange(newCursorPos, newCursorPos)
        textareaRef.current.focus()
        setCursorPosition(newCursorPos)
      }
    }, 0)
  }, [currentMatch, value, linkedEntities, onChange])

  // Accept the current suggestion (for Tab key)
  const acceptSuggestion = useCallback(() => {
    if (!currentMatch) return
    acceptEntitySuggestion(currentMatch.entity)
  }, [currentMatch, acceptEntitySuggestion])

  // Remove entity from linked entities (keep text but unlink)
  const removeEntity = useCallback((entityId: string) => {
    const newLinkedEntities = linkedEntities.filter(entity => entity.id !== entityId)
    onChange(value, newLinkedEntities)
  }, [linkedEntities, value, onChange])

  return (
    <div className="space-y-3">
      {/* Entity Type Selector Buttons */}
      <EntitySelectorButtons
        onEntityTypeSelect={handleEntityTypeSelect}
        activeType={activeEntityType}
        linkedEntityTypes={[...new Set(linkedEntities.map(e => e.type as EntityType))]}
        className="mb-2"
      />

      {/* Linked Entities Display */}
      {linkedEntities.length > 0 && (
        <div className="flex flex-wrap gap-2">
          <span className="text-xs text-muted-foreground self-center">Linked entities:</span>
          {linkedEntities.map((entity) => (
            <EntityChip
              key={entity.id}
              entity={entity}
              isEditable
              onRemove={removeEntity}
            />
          ))}
        </div>
      )}

      {/* Text Input with Highlighting and Ghost Text */}
      <div className="relative">
        {/* Entity highlighting background layer */}
        <div 
          className="absolute inset-0 pointer-events-none z-5"
          style={{
            padding: textareaRef.current ? getComputedStyle(textareaRef.current).padding : '12px',
            font: textareaRef.current ? getComputedStyle(textareaRef.current).font : 'inherit',
            lineHeight: textareaRef.current ? getComputedStyle(textareaRef.current).lineHeight : 'inherit',
            whiteSpace: 'pre-wrap',
            wordWrap: 'break-word'
          }}
        >
          {parseTextForHighlighting(value).map((part, index) => (
            <span key={index}>
              {part.isEntity ? (
                <span className={cn(
                  "rounded font-medium",
                  part.entity?.type === 'stakeholder' && "bg-blue-500 px-1 py-0.5",
                  part.entity?.type === 'deal' && "bg-purple-500 px-0",
                  part.entity?.type === 'account' && "bg-green-500 px-0"
                )}>
                  <span className="text-transparent">{part.text}</span>
                </span>
              ) : (
                <span className="text-transparent">{part.text}</span>
              )}
            </span>
          ))}
        </div>

        {/* Entity text color layer */}
        <div 
          className="absolute inset-0 pointer-events-none z-15"
          style={{
            padding: textareaRef.current ? getComputedStyle(textareaRef.current).padding : '12px',
            font: textareaRef.current ? getComputedStyle(textareaRef.current).font : 'inherit',
            lineHeight: textareaRef.current ? getComputedStyle(textareaRef.current).lineHeight : 'inherit',
            whiteSpace: 'pre-wrap',
            wordWrap: 'break-word'
          }}
        >
          {parseTextForHighlighting(value).map((part, index) => (
            <span key={index}>
              {part.isEntity ? (
                <span className={cn(
                  "rounded font-medium text-white",
                  part.entity?.type === 'stakeholder' && "px-1 py-0.5",
                  part.entity?.type === 'deal' && "px-0",
                  part.entity?.type === 'account' && "px-0"
                )}>
                  {part.text}
                </span>
              ) : (
                <span className="text-transparent">{part.text}</span>
              )}
            </span>
          ))}
        </div>

        {/* Ghost text layer */}
        {ghostText && ghostText.remainingText && (
          <div 
            className="absolute inset-0 pointer-events-none z-20"
            style={{
              padding: textareaRef.current ? getComputedStyle(textareaRef.current).padding : '12px',
              font: textareaRef.current ? getComputedStyle(textareaRef.current).font : 'inherit',
              lineHeight: textareaRef.current ? getComputedStyle(textareaRef.current).lineHeight : 'inherit',
              whiteSpace: 'pre-wrap',
              wordWrap: 'break-word'
            }}
          >
            <span className="invisible">{value}</span>
            <span className={cn(
              "opacity-60 font-medium",
              activeEntityType === 'stakeholder' && "text-blue-500",
              activeEntityType === 'deal' && "text-purple-500", 
              activeEntityType === 'account' && "text-green-500"
            )}>
              {ghostText.remainingText}
            </span>
          </div>
        )}
        
        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => {
            onChange(e.target.value, linkedEntities)
            handleSelectionChange()
          }}
          onKeyDown={handleKeyDown}
          onSelect={handleSelectionChange}
          onFocus={handleSelectionChange}
          onCompositionStart={() => setIsComposing(true)}
          onCompositionEnd={() => setIsComposing(false)}
          placeholder={placeholder}
          disabled={disabled}
          className={cn(
            "w-full min-h-[120px] p-3 text-sm bg-white/90 border border-gray-200 rounded-md resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent relative z-10",
            "font-mono leading-5",
            className
          )}
          rows={6}
        />
        
        {/* Entity Suggestions Dropdown - Positioned at cursor */}
        {searchResults.length > 0 && (
          <div 
            className="absolute bg-white border border-gray-200 rounded-md shadow-lg z-50 max-h-48 overflow-y-auto min-w-64"
            style={{
              left: `${dropdownPosition.x}px`,
              top: `${dropdownPosition.y}px`
            }}
          >
            {/* Dropdown arrow pointing up */}
            <div className="absolute w-2 h-2 bg-white border-l border-t border-gray-200 transform rotate-45 -top-1 left-4" />
            {searchResults.map((entity, index) => (
              <div
                key={entity.id}
                className={cn(
                  "p-3 cursor-pointer transition-colors duration-150 flex items-center gap-3",
                  index === 0 ? 'bg-blue-50 border-l-2 border-blue-500' : 'hover:bg-gray-50'
                )}
                onClick={() => acceptEntitySuggestion(entity)}
              >
                {/* Avatar */}
                <div className={cn(
                  "w-10 h-10 rounded-full flex items-center justify-center text-white font-medium text-sm",
                  entity.type === 'stakeholder' && "bg-blue-500",
                  entity.type === 'deal' && "bg-purple-500",
                  entity.type === 'account' && "bg-green-500"
                )}>
                  {entity.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()}
                </div>
                
                {/* Content */}
                <div className="flex-1 min-w-0">
                  <div className="font-medium text-gray-900 truncate">{entity.name}</div>
                  {entity.attributes.title && (
                    <div className="text-sm text-gray-600 truncate">
                      @{entity.attributes.email?.split('@')[0] || entity.name.toLowerCase().replace(/\s+/g, '.')} • {entity.attributes.title}
                    </div>
                  )}
                  {entity.attributes.department && (
                    <div className="text-sm text-gray-500 truncate">{entity.attributes.department}</div>
                  )}
                  {entity.type === 'account' && entity.attributes.industry && (
                    <div className="text-sm text-gray-500 truncate">{entity.attributes.industry}</div>
                  )}
                  {entity.type === 'deal' && entity.attributes.dealValue && (
                    <div className="text-sm text-gray-500 truncate">
                      ${(entity.attributes.dealValue / 1000)}k • {entity.attributes.dealStage?.replace(/_/g, ' ')}
                    </div>
                  )}
                </div>
                
                {index === 0 && (
                  <div className="text-xs text-blue-600 font-medium">↵</div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}