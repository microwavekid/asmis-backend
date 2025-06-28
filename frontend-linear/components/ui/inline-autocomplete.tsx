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
  
  const textareaRef = useRef<HTMLTextAreaElement>(null)

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

  // Extract potential entity mentions from text
  const extractPotentialEntities = useCallback((text: string, position: number) => {
    // Look for trigger characters directly before cursor
    if (position > 0 && ['@', '#', '+'].includes(text[position - 1])) {
      const triggerChar = text[position - 1]
      // Make sure it's at start or after whitespace
      if (position === 1 || /\s/.test(text[position - 2])) {
        return {
          query: "",
          startIndex: position,
          endIndex: position
        }
      }
    }

    // Look for trigger with text after it
    for (let i = position - 1; i >= 0; i--) {
      const char = text[i]
      if (char === '@' || char === '#' || char === '+') {
        // Make sure trigger is at start or after whitespace
        if (i === 0 || /\s/.test(text[i - 1])) {
          const query = text.substring(i + 1, position)
          return {
            query: query,
            startIndex: i + 1,
            endIndex: position
          }
        }
      } else if (/\s/.test(char)) {
        // Stop at whitespace if no trigger found
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

  // Handle entity search and matching
  useEffect(() => {
    if (isComposing || !value) {
      setCurrentMatch(null)
      setSearchResults([])
      return
    }

    const searchForEntities = async () => {
      const potential = extractPotentialEntities(value, cursorPosition)
      if (!potential) {
        setCurrentMatch(null)
        setSearchResults([])
        return
      }

      try {
        const searchFn = onEntitySearch || ((query: string) => mockEntitySearch(query, activeEntityType))
        const results = await searchFn(potential.query)
        setSearchResults(results)
        
        if (results.length > 0) {
          const bestMatch = results[0]
          const suggestion = bestMatch.name
          
          // Show match for any query with results
          if (potential.query === "" || suggestion.toLowerCase().startsWith(potential.query.toLowerCase())) {
            setCurrentMatch({
              entity: bestMatch,
              matchedText: potential.query,
              suggestion: suggestion,
              startIndex: potential.startIndex,
              endIndex: potential.endIndex
            })
          } else {
            setCurrentMatch(null)
          }
        } else {
          setCurrentMatch(null)
        }
      } catch (error) {
        console.error("Entity search failed:", error)
        setCurrentMatch(null)
      }
    }

    const debounceTimer = setTimeout(searchForEntities, 300)
    return () => clearTimeout(debounceTimer)
  }, [value, cursorPosition, isComposing, extractPotentialEntities, onEntitySearch, mockEntitySearch, activeEntityType])

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

      {/* Text Input */}
      <div className="relative">
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
            "w-full min-h-[120px] p-3 text-sm bg-white border border-gray-200 rounded-md resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
            "font-mono leading-5",
            className
          )}
          rows={6}
        />
        
        {/* Entity Suggestions Dropdown */}
        {searchResults.length > 0 && currentMatch && (
          <div className="absolute top-full left-0 right-0 mt-2 bg-white border border-gray-200 rounded-md shadow-lg z-50 max-h-48 overflow-y-auto">
            {/* Dropdown arrow pointing up */}
            <div className="absolute w-2 h-2 bg-white border-l border-t border-gray-200 transform rotate-45 -top-1 left-4" />
            {searchResults.map((entity) => (
              <div
                key={entity.id}
                className={cn(
                  "p-3 cursor-pointer border-b border-gray-100 last:border-b-0 transition-colors duration-150",
                  entity.id === currentMatch.entity.id ? 'bg-blue-50' : 'hover:bg-gray-50'
                )}
                onClick={() => acceptEntitySuggestion(entity)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-sm">{entity.name}</span>
                      <span className="text-xs text-gray-500 capitalize">{entity.type}</span>
                    </div>
                    {entity.attributes.title && (
                      <p className="text-xs text-gray-600 mt-1">{entity.attributes.title}</p>
                    )}
                    {entity.attributes.account && (
                      <p className="text-xs text-gray-500 mt-1">
                        <span className="text-gray-400">Account:</span> {entity.attributes.account}
                      </p>
                    )}
                  </div>
                  <div className="flex items-center gap-1 ml-2">
                    <div className="w-8 bg-gray-200 rounded-full h-1">
                      <div 
                        className="h-1 rounded-full bg-green-500"
                        style={{ width: `${entity.confidence * 100}%` }}
                      />
                    </div>
                    <span className="text-xs text-gray-400">{Math.round(entity.confidence * 100)}%</span>
                  </div>
                </div>
                {entity.id === currentMatch.entity.id && (
                  <div className="flex items-center gap-2 text-xs text-blue-600 mt-2">
                    <kbd className="px-1 py-0.5 text-xs bg-blue-100 border border-blue-200 rounded">Tab</kbd>
                    <span>to accept</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}