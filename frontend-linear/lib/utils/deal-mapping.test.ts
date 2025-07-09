// PATTERN_REF: UI_DEBUGGING_PATTERN
// DECISION_REF: DEC_2025-07-08_004 - Comprehensive test coverage for deal mapping
import { describe, it, expect } from 'vitest'
import { 
  mapDealIntelligenceToDeal, 
  mapDealsIntelligenceToDeals,
  type Deal 
} from './deal-mapping'
import { DealIntelligence } from '@/types/intelligence'

describe('Deal Mapping Utilities', () => {
  describe('mapDealIntelligenceToDeal', () => {
    it('should map all basic fields correctly', () => {
      const mockDeal: DealIntelligence = {
        dealId: 'deal-123',
        dealName: 'Test Deal',
        accountName: 'Test Account',
        stage: 'technical_evaluation',
        dealValue: 250000,
        health: { score: 85, trend: 'stable' },
        meddpiccAnalysis: {
          overallScore: 0.75,
          completenessScore: 0.80,
          riskFactors: ['Budget not confirmed'],
          decisionProcess: {
            estimatedCloseDate: '2024-06-30'
          }
        },
        nextActions: [
          { id: '1', title: 'Schedule demo', priority: 'high', dueDate: '2024-05-01' }
        ],
        momentum: { velocity: 'accelerating', keyMilestones: [] }
      }

      const result = mapDealIntelligenceToDeal(mockDeal)

      expect(result).toEqual({
        id: 'deal-123',
        name: 'Test Deal',
        account: 'Test Account',
        stage: 'Technical Evaluation',
        health: 85,
        value: 250000,
        closeDate: '2024-06-30T00:00:00.000Z',
        meddpiccScore: 0.75,
        confidence: 0.80,
        priority: 'high',
        nextActions: ['Schedule demo'],
        risks: ['Budget not confirmed']
      })
    })

    describe('stage formatting', () => {
      it('should format snake_case stages to Display Case', () => {
        const testCases = [
          { input: 'discovery', expected: 'Discovery' },
          { input: 'technical_evaluation', expected: 'Technical Evaluation' },
          { input: 'business_evaluation', expected: 'Business Evaluation' },
          { input: 'negotiation', expected: 'Negotiation' },
          { input: 'closing', expected: 'Closing' },
          { input: 'closed_won', expected: 'Closed Won' },
          { input: 'closed_lost', expected: 'Closed Lost' }
        ]

        testCases.forEach(({ input, expected }) => {
          const deal: DealIntelligence = {
            dealId: '1',
            dealName: 'Test',
            accountName: 'Account',
            stage: input,
            health: { score: 50, trend: 'stable' }
          }
          
          const result = mapDealIntelligenceToDeal(deal)
          expect(result.stage).toBe(expected)
        })
      })

      it('should handle unknown stages gracefully', () => {
        const deal: DealIntelligence = {
          dealId: '1',
          dealName: 'Test',
          accountName: 'Account',
          stage: 'custom_stage_name',
          health: { score: 50, trend: 'stable' }
        }
        
        const result = mapDealIntelligenceToDeal(deal)
        expect(result.stage).toBe('Custom Stage Name')
      })
    })

    describe('close date extraction', () => {
      it('should prioritize MEDDPICC decision process date', () => {
        const deal: DealIntelligence = {
          dealId: '1',
          dealName: 'Test',
          accountName: 'Account',
          stage: 'negotiation',
          health: { score: 80, trend: 'stable' },
          meddpiccAnalysis: {
            decisionProcess: {
              estimatedCloseDate: '2024-07-15'
            }
          },
          momentum: {
            keyMilestones: [
              { name: 'Contract signing', dueDate: '2024-08-01' }
            ]
          }
        }
        
        const result = mapDealIntelligenceToDeal(deal)
        expect(result.closeDate).toBe('2024-07-15T00:00:00.000Z')
      })

      it('should fallback to momentum milestone dates', () => {
        const deal: DealIntelligence = {
          dealId: '1',
          dealName: 'Test',
          accountName: 'Account',
          stage: 'negotiation',
          health: { score: 80, trend: 'stable' },
          momentum: {
            keyMilestones: [
              { name: 'Technical review', dueDate: '2024-06-01' },
              { name: 'Contract signing', dueDate: '2024-08-01' },
              { name: 'Close deal', dueDate: '2024-08-15' }
            ]
          }
        }
        
        const result = mapDealIntelligenceToDeal(deal)
        expect(result.closeDate).toBe('2024-08-01T00:00:00.000Z')
      })

      it('should use stage-based default dates as last resort', () => {
        const now = Date.now()
        const testCases = [
          { stage: 'closing', expectedDays: 7 },
          { stage: 'negotiation', expectedDays: 30 },
          { stage: 'business_evaluation', expectedDays: 60 },
          { stage: 'technical_evaluation', expectedDays: 75 },
          { stage: 'discovery', expectedDays: 90 }
        ]

        testCases.forEach(({ stage, expectedDays }) => {
          const deal: DealIntelligence = {
            dealId: '1',
            dealName: 'Test',
            accountName: 'Account',
            stage,
            health: { score: 50, trend: 'stable' }
          }
          
          const result = mapDealIntelligenceToDeal(deal)
          const resultDate = new Date(result.closeDate)
          const expectedDate = new Date(now + expectedDays * 24 * 60 * 60 * 1000)
          
          // Allow 1 second tolerance for test execution time
          expect(Math.abs(resultDate.getTime() - expectedDate.getTime())).toBeLessThan(1000)
        })
      })
    })

    describe('confidence score extraction', () => {
      it('should prefer completeness score', () => {
        const deal: DealIntelligence = {
          dealId: '1',
          dealName: 'Test',
          accountName: 'Account',
          stage: 'discovery',
          health: { score: 70, trend: 'stable' },
          meddpiccAnalysis: {
            completenessScore: 0.90,
            overallScore: 0.75
          }
        }
        
        const result = mapDealIntelligenceToDeal(deal)
        expect(result.confidence).toBe(0.90)
      })

      it('should fallback to overall score with adjustment', () => {
        const deal: DealIntelligence = {
          dealId: '1',
          dealName: 'Test',
          accountName: 'Account',
          stage: 'discovery',
          health: { score: 70, trend: 'stable' },
          meddpiccAnalysis: {
            overallScore: 0.75
          }
        }
        
        const result = mapDealIntelligenceToDeal(deal)
        expect(result.confidence).toBeCloseTo(0.60, 2) // 0.75 * 0.8
      })

      it('should use health score as final fallback', () => {
        const deal: DealIntelligence = {
          dealId: '1',
          dealName: 'Test',
          accountName: 'Account',
          stage: 'discovery',
          health: { score: 80, trend: 'stable' }
        }
        
        const result = mapDealIntelligenceToDeal(deal)
        expect(result.confidence).toBe(56) // 80 * 0.7
      })

      it('should handle missing data gracefully', () => {
        const deal: DealIntelligence = {
          dealId: '1',
          dealName: 'Test',
          accountName: 'Account',
          stage: 'discovery'
        }
        
        const result = mapDealIntelligenceToDeal(deal)
        expect(result.confidence).toBe(0)
      })
    })

    describe('priority derivation', () => {
      it('should set high priority for critical actions', () => {
        const deal: DealIntelligence = {
          dealId: '1',
          dealName: 'Test',
          accountName: 'Account',
          stage: 'discovery',
          health: { score: 90, trend: 'stable' },
          nextActions: [
            { id: '1', title: 'Action 1', priority: 'low', dueDate: '2024-05-01' },
            { id: '2', title: 'Action 2', priority: 'critical', dueDate: '2024-05-01' }
          ]
        }
        
        const result = mapDealIntelligenceToDeal(deal)
        expect(result.priority).toBe('high')
      })

      it('should set high priority for poor health', () => {
        const deal: DealIntelligence = {
          dealId: '1',
          dealName: 'Test',
          accountName: 'Account',
          stage: 'discovery',
          health: { score: 45, trend: 'declining' }
        }
        
        const result = mapDealIntelligenceToDeal(deal)
        expect(result.priority).toBe('high')
      })

      it('should set high priority for closing/negotiation stages', () => {
        const testStages = ['closing', 'negotiation']
        
        testStages.forEach(stage => {
          const deal: DealIntelligence = {
            dealId: '1',
            dealName: 'Test',
            accountName: 'Account',
            stage,
            health: { score: 75, trend: 'stable' }
          }
          
          const result = mapDealIntelligenceToDeal(deal)
          expect(result.priority).toBe('high')
        })
      })

      it('should set medium priority for medium actions', () => {
        const deal: DealIntelligence = {
          dealId: '1',
          dealName: 'Test',
          accountName: 'Account',
          stage: 'discovery',
          health: { score: 70, trend: 'stable' },
          nextActions: [
            { id: '1', title: 'Action 1', priority: 'medium', dueDate: '2024-05-01' }
          ]
        }
        
        const result = mapDealIntelligenceToDeal(deal)
        expect(result.priority).toBe('medium')
      })

      it('should set low priority for healthy deals', () => {
        const deal: DealIntelligence = {
          dealId: '1',
          dealName: 'Test',
          accountName: 'Account',
          stage: 'discovery',
          health: { score: 85, trend: 'improving' }
        }
        
        const result = mapDealIntelligenceToDeal(deal)
        expect(result.priority).toBe('low')
      })
    })

    describe('risk extraction', () => {
      it('should aggregate risks from multiple sources', () => {
        const deal: DealIntelligence = {
          dealId: '1',
          dealName: 'Test',
          accountName: 'Account',
          stage: 'negotiation',
          health: { score: 55, trend: 'declining' },
          meddpiccAnalysis: {
            riskFactors: ['No champion identified', 'Budget constraints'],
            competition: {
              competitors: [
                { name: 'Competitor A', status: 'evaluating' },
                { name: 'Competitor B', status: 'eliminated' }
              ]
            }
          },
          momentum: {
            velocity: 'stalled'
          }
        }
        
        const result = mapDealIntelligenceToDeal(deal)
        expect(result.risks).toContain('No champion identified')
        expect(result.risks).toContain('Budget constraints')
        expect(result.risks).toContain('Low deal health')
        expect(result.risks).toContain('Deal momentum issues')
        expect(result.risks).toContain('Active competition')
        expect(result.risks.length).toBe(5)
      })

      it('should handle missing risk data gracefully', () => {
        const deal: DealIntelligence = {
          dealId: '1',
          dealName: 'Test',
          accountName: 'Account',
          stage: 'discovery',
          health: { score: 85, trend: 'stable' }
        }
        
        const result = mapDealIntelligenceToDeal(deal)
        expect(result.risks).toEqual([])
      })

      it('should detect velocity-based risks', () => {
        const velocities = ['stalled', 'reversing']
        
        velocities.forEach(velocity => {
          const deal: DealIntelligence = {
            dealId: '1',
            dealName: 'Test',
            accountName: 'Account',
            stage: 'discovery',
            health: { score: 75, trend: 'stable' },
            momentum: { velocity }
          }
          
          const result = mapDealIntelligenceToDeal(deal)
          expect(result.risks).toContain('Deal momentum issues')
        })
      })
    })
  })

  describe('mapDealsIntelligenceToDeals', () => {
    it('should map multiple deals correctly', () => {
      const mockDeals: DealIntelligence[] = [
        {
          dealId: '1',
          dealName: 'Deal 1',
          accountName: 'Account 1',
          stage: 'discovery',
          health: { score: 80, trend: 'stable' }
        },
        {
          dealId: '2',
          dealName: 'Deal 2',
          accountName: 'Account 2',
          stage: 'negotiation',
          health: { score: 60, trend: 'declining' }
        }
      ]

      const results = mapDealsIntelligenceToDeals(mockDeals)
      
      expect(results).toHaveLength(2)
      expect(results[0].id).toBe('1')
      expect(results[0].stage).toBe('Discovery')
      expect(results[1].id).toBe('2')
      expect(results[1].stage).toBe('Negotiation')
    })

    it('should handle empty array', () => {
      const results = mapDealsIntelligenceToDeals([])
      expect(results).toEqual([])
    })
  })
})