// Default user goals
export const defaultUserGoals = {
  annualTarget: 2200000,
  annualQuota: 1400000,
  fyh1Split: 0.4, // 40% in first half
  fyh2Split: 0.6, // 60% in second half
  quarterlyGoals: [
    { quarter: "Q1", target: 440000 }, // 20% of annual
    { quarter: "Q2", target: 440000 }, // 20% of annual
    { quarter: "Q3", target: 660000 }, // 30% of annual
    { quarter: "Q4", target: 660000 }, // 30% of annual
  ],
}

// Historical benchmarks (for AI calculations)
export const industryBenchmarks = {
  meetingsToClosedDeal: 12, // Average meetings needed to close a deal
  emailsPerProspect: 8, // Average emails sent per prospect
  filesPerDeal: 5, // Average files shared per deal
  prospectToOpportunityRate: 0.25, // 25% of prospects become opportunities
  opportunityToWinRate: 0.3, // 30% of opportunities are won
  averageDealSize: 110000, // Average deal size
  amplifyPostsPerMonth: 20, // Recommended social posts per month
  stakeholdersPerDeal: 4.5, // Average stakeholders involved in a deal
}
