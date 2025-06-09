// Define types for AI suggestions
export interface AITask {
  id: string
  accountId: string
  title: string
  description: string
  timeEstimate: "0-5" | "15" | "30" | "30+" // in minutes
  priority: "high" | "medium" | "low"
  dueDate: string
  status: "pending" | "completed" | "dismissed"
  createdAt: string
  type: "research" | "follow-up" | "preparation" | "outreach" | "analysis"
  relatedTo?: {
    type: "opportunity" | "contact" | "meeting" | "email"
    id: string
    name: string
  }
}

export interface AIEmailSuggestion {
  id: string
  accountId: string
  subject: string
  preview: string
  recipientName: string
  recipientEmail: string
  priority: "high" | "medium" | "low"
  status: "pending" | "approved" | "rejected"
  createdAt: string
  intent: string
  opportunityId?: string
}

// Generate mock AI tasks for each account
export const mockAITasks: AITask[] = [
  // Acme Corp (id: "1") Tasks
  {
    id: "task-1-1",
    accountId: "1",
    title: "Review Acme Corp's latest quarterly report",
    description:
      "Their Q1 report was just published. Review for insights on technology investments and potential expansion areas.",
    timeEstimate: "30",
    priority: "medium",
    dueDate: "2023-05-20",
    status: "pending",
    createdAt: "2023-05-15T10:30:00Z",
    type: "research",
  },
  {
    id: "task-1-2",
    accountId: "1",
    title: "Send follow-up email to John Smith",
    description: "Follow up on the technical discussion from last week's call regarding API integration requirements.",
    timeEstimate: "0-5",
    priority: "high",
    dueDate: "2023-05-16",
    status: "pending",
    createdAt: "2023-05-15T11:45:00Z",
    type: "follow-up",
    relatedTo: {
      type: "contact",
      id: "contact-1",
      name: "John Smith",
    },
  },
  {
    id: "task-1-3",
    accountId: "1",
    title: "Prepare personalization demo",
    description: "Create a custom demo showing how our personalization engine would work with Acme's product catalog.",
    timeEstimate: "30+",
    priority: "medium",
    dueDate: "2023-05-25",
    status: "pending",
    createdAt: "2023-05-14T09:15:00Z",
    type: "preparation",
  },

  // Globex Corporation (id: "2") Tasks
  {
    id: "task-2-1",
    accountId: "2",
    title: "Research Globex's manufacturing processes",
    description: "Gather information on their current manufacturing processes to identify optimization opportunities.",
    timeEstimate: "30+",
    priority: "medium",
    dueDate: "2023-05-22",
    status: "pending",
    createdAt: "2023-05-14T14:20:00Z",
    type: "research",
  },
  {
    id: "task-2-2",
    accountId: "2",
    title: "Connect with Sarah Johnson on LinkedIn",
    description:
      "She recently joined as Director of Digital Transformation. Send a connection request with a personalized note.",
    timeEstimate: "0-5",
    priority: "low",
    dueDate: "2023-05-17",
    status: "pending",
    createdAt: "2023-05-15T08:30:00Z",
    type: "outreach",
    relatedTo: {
      type: "contact",
      id: "contact-2",
      name: "Sarah Johnson",
    },
  },
  {
    id: "task-2-3",
    accountId: "2",
    title: "Analyze competitor solutions used by Globex",
    description: "Research which competitor products they're currently using and prepare comparison points.",
    timeEstimate: "30",
    priority: "high",
    dueDate: "2023-05-19",
    status: "pending",
    createdAt: "2023-05-13T16:45:00Z",
    type: "analysis",
  },
  {
    id: "task-2-4",
    accountId: "2",
    title: "Schedule technical deep dive",
    description: "Coordinate with their IT team for a technical deep dive session on integration capabilities.",
    timeEstimate: "15",
    priority: "medium",
    dueDate: "2023-05-18",
    status: "pending",
    createdAt: "2023-05-15T13:10:00Z",
    type: "follow-up",
  },
  {
    id: "task-2-5",
    accountId: "2",
    title: "Prepare ROI calculator",
    description: "Customize our ROI calculator with Globex-specific metrics and industry benchmarks.",
    timeEstimate: "30",
    priority: "high",
    dueDate: "2023-05-23",
    status: "pending",
    createdAt: "2023-05-14T11:20:00Z",
    type: "preparation",
  },
  {
    id: "task-2-6",
    accountId: "2",
    title: "Share industry whitepaper",
    description: "Send them our latest manufacturing industry whitepaper with a personalized note.",
    timeEstimate: "0-5",
    priority: "low",
    dueDate: "2023-05-16",
    status: "pending",
    createdAt: "2023-05-15T09:45:00Z",
    type: "outreach",
  },

  // Initech (id: "3") Tasks
  {
    id: "task-3-1",
    accountId: "3",
    title: "Research Initech's recent product launches",
    description:
      "They launched a new software platform last month. Research features and potential integration points.",
    timeEstimate: "15",
    priority: "medium",
    dueDate: "2023-05-18",
    status: "pending",
    createdAt: "2023-05-15T10:00:00Z",
    type: "research",
  },
  {
    id: "task-3-2",
    accountId: "3",
    title: "Reconnect with former champion",
    description:
      "Michael Brown was our champion before they churned. Reach out to understand their current challenges.",
    timeEstimate: "0-5",
    priority: "high",
    dueDate: "2023-05-17",
    status: "pending",
    createdAt: "2023-05-15T11:30:00Z",
    type: "outreach",
    relatedTo: {
      type: "contact",
      id: "contact-3",
      name: "Michael Brown",
    },
  },

  // Wayne Enterprises (id: "4") Tasks
  {
    id: "task-4-1",
    accountId: "4",
    title: "Prepare expansion proposal",
    description: "Create a proposal for expanding our solution to their international offices.",
    timeEstimate: "30+",
    priority: "high",
    dueDate: "2023-05-24",
    status: "pending",
    createdAt: "2023-05-13T14:15:00Z",
    type: "preparation",
  },
  {
    id: "task-4-2",
    accountId: "4",
    title: "Schedule quarterly business review",
    description: "It's time for our quarterly business review. Coordinate with stakeholders for scheduling.",
    timeEstimate: "15",
    priority: "medium",
    dueDate: "2023-05-19",
    status: "pending",
    createdAt: "2023-05-15T09:20:00Z",
    type: "follow-up",
  },
  {
    id: "task-4-3",
    accountId: "4",
    title: "Analyze usage metrics",
    description:
      "Review their platform usage metrics to identify optimization opportunities and potential upsell points.",
    timeEstimate: "30",
    priority: "medium",
    dueDate: "2023-05-22",
    status: "pending",
    createdAt: "2023-05-14T13:40:00Z",
    type: "analysis",
  },
  {
    id: "task-4-4",
    accountId: "4",
    title: "Send case study",
    description: "Share the recently published case study from a similar client in their industry.",
    timeEstimate: "0-5",
    priority: "low",
    dueDate: "2023-05-16",
    status: "pending",
    createdAt: "2023-05-15T10:50:00Z",
    type: "outreach",
  },
  {
    id: "task-4-5",
    accountId: "4",
    title: "Prepare for security review",
    description: "Their security team wants to conduct a review. Gather necessary documentation and prepare responses.",
    timeEstimate: "30+",
    priority: "high",
    dueDate: "2023-05-26",
    status: "pending",
    createdAt: "2023-05-12T15:30:00Z",
    type: "preparation",
  },
  {
    id: "task-4-6",
    accountId: "4",
    title: "Check in with new stakeholder",
    description: "Lisa Johnson recently joined as VP of Digital. Send a brief welcome message.",
    timeEstimate: "0-5",
    priority: "medium",
    dueDate: "2023-05-17",
    status: "pending",
    createdAt: "2023-05-15T11:15:00Z",
    type: "outreach",
    relatedTo: {
      type: "contact",
      id: "contact-4",
      name: "Lisa Johnson",
    },
  },
  {
    id: "task-4-7",
    accountId: "4",
    title: "Review contract renewal terms",
    description: "Their contract is up for renewal in 3 months. Review terms and prepare for negotiation.",
    timeEstimate: "30",
    priority: "medium",
    dueDate: "2023-05-23",
    status: "pending",
    createdAt: "2023-05-14T10:25:00Z",
    type: "analysis",
  },

  // Stark Industries (id: "5") Tasks
  {
    id: "task-5-1",
    accountId: "5",
    title: "Research Stark's new innovation initiative",
    description: "They announced a new innovation initiative last week. Research details and alignment opportunities.",
    timeEstimate: "15",
    priority: "medium",
    dueDate: "2023-05-19",
    status: "pending",
    createdAt: "2023-05-15T08:45:00Z",
    type: "research",
  },
  {
    id: "task-5-2",
    accountId: "5",
    title: "Follow up on technical requirements",
    description: "Their engineering team had questions about our API. Follow up with detailed documentation.",
    timeEstimate: "15",
    priority: "high",
    dueDate: "2023-05-17",
    status: "pending",
    createdAt: "2023-05-15T10:15:00Z",
    type: "follow-up",
  },
  {
    id: "task-5-3",
    accountId: "5",
    title: "Prepare custom demo",
    description: "Create a customized demo focusing on their specific use cases in the energy sector.",
    timeEstimate: "30+",
    priority: "high",
    dueDate: "2023-05-25",
    status: "pending",
    createdAt: "2023-05-13T13:20:00Z",
    type: "preparation",
  },
]

// Generate mock AI email suggestions for each account
export const mockAIEmailSuggestions: AIEmailSuggestion[] = [
  // Acme Corp (id: "1") Email Suggestions
  {
    id: "email-1-1",
    accountId: "1",
    subject: "Follow-up: Next Steps After Our Technical Discussion",
    preview:
      "Hi John, I wanted to follow up on our technical discussion last week regarding the API integration requirements. Based on your team's feedback, I've put together some additional documentation that addresses...",
    recipientName: "John Smith",
    recipientEmail: "john.smith@acmecorp.com",
    priority: "high",
    status: "pending",
    createdAt: "2023-05-15T10:45:00Z",
    intent: "Follow-up on technical discussion",
  },
  {
    id: "email-1-2",
    accountId: "1",
    subject: "Personalization Engine: Custom Demo Invitation",
    preview:
      "Hi Sarah, Based on our recent conversations about enhancing customer experiences, I've prepared a custom demonstration of how our personalization engine would work specifically with Acme's product catalog...",
    recipientName: "Sarah Williams",
    recipientEmail: "sarah.williams@acmecorp.com",
    priority: "medium",
    status: "pending",
    createdAt: "2023-05-14T15:30:00Z",
    intent: "Demo invitation",
  },

  // Globex Corporation (id: "2") Email Suggestions
  {
    id: "email-2-1",
    accountId: "2",
    subject: "Manufacturing Process Optimization: Initial Findings",
    preview:
      "Hi Michael, Following our discussion about optimizing Globex's manufacturing processes, I've conducted some initial research and identified several potential areas where our solution could deliver significant improvements...",
    recipientName: "Michael Chen",
    recipientEmail: "michael.chen@globexcorp.com",
    priority: "high",
    status: "pending",
    createdAt: "2023-05-15T09:20:00Z",
    intent: "Share research findings",
  },
  {
    id: "email-2-2",
    accountId: "2",
    subject: "Welcome to Globex & Introduction to Our Solutions",
    preview:
      "Hi Sarah, Congratulations on your recent appointment as Director of Digital Transformation at Globex Corporation! I noticed your announcement on LinkedIn and wanted to reach out to introduce myself...",
    recipientName: "Sarah Johnson",
    recipientEmail: "sarah.johnson@globexcorp.com",
    priority: "medium",
    status: "pending",
    createdAt: "2023-05-14T11:15:00Z",
    intent: "New stakeholder introduction",
  },
  {
    id: "email-2-3",
    accountId: "2",
    subject: "Manufacturing Industry Insights: Latest Whitepaper",
    preview:
      "Hi Robert, I thought you might be interested in our latest whitepaper on 'Digital Transformation in Manufacturing: 2023 Trends and Insights.' Given Globex's current initiatives, the section on predictive maintenance...",
    recipientName: "Robert Davis",
    recipientEmail: "robert.davis@globexcorp.com",
    priority: "low",
    status: "pending",
    createdAt: "2023-05-13T14:50:00Z",
    intent: "Share industry insights",
  },
  {
    id: "email-2-4",
    accountId: "2",
    subject: "Technical Deep Dive: Proposed Agenda",
    preview:
      "Hi James, Following up on our conversation about scheduling a technical deep dive, I've prepared a proposed agenda that covers the integration capabilities you expressed interest in. I've also included...",
    recipientName: "James Wilson",
    recipientEmail: "james.wilson@globexcorp.com",
    priority: "medium",
    status: "pending",
    createdAt: "2023-05-15T13:25:00Z",
    intent: "Technical meeting preparation",
  },

  // Initech (id: "3") Email Suggestions
  {
    id: "email-3-1",
    accountId: "3",
    subject: "Reconnecting: New Opportunities for Collaboration",
    preview:
      "Hi Michael, It's been a while since we last spoke, and I noticed Initech recently launched a new software platform. I'd love to reconnect and learn more about your current initiatives and challenges...",
    recipientName: "Michael Brown",
    recipientEmail: "michael.brown@initech.com",
    priority: "high",
    status: "pending",
    createdAt: "2023-05-15T08:30:00Z",
    intent: "Reengagement with former customer",
  },

  // Wayne Enterprises (id: "4") Email Suggestions
  {
    id: "email-4-1",
    accountId: "4",
    subject: "Quarterly Business Review: Scheduling Request",
    preview:
      "Hi Thomas, It's time for our quarterly business review to discuss the progress we've made and plan for the upcoming quarter. Based on the insights from our platform analytics, I've identified several key areas...",
    recipientName: "Thomas Wayne",
    recipientEmail: "thomas.wayne@wayne-enterprises.com",
    priority: "high",
    status: "pending",
    createdAt: "2023-05-15T09:45:00Z",
    intent: "QBR scheduling",
  },
  {
    id: "email-4-2",
    accountId: "4",
    subject: "International Expansion Proposal: Executive Summary",
    preview:
      "Hi Bruce, As discussed in our last meeting, I've prepared a comprehensive proposal for expanding our solution to Wayne Enterprises' international offices. The attached executive summary outlines the key benefits...",
    recipientName: "Bruce Wayne",
    recipientEmail: "bruce.wayne@wayne-enterprises.com",
    priority: "high",
    status: "pending",
    createdAt: "2023-05-14T16:20:00Z",
    intent: "Expansion proposal",
  },
  {
    id: "email-4-3",
    accountId: "4",
    subject: "Welcome to Wayne Enterprises & Introduction",
    preview:
      "Hi Lisa, Congratulations on your recent appointment as VP of Digital at Wayne Enterprises! I'm reaching out to introduce myself as your dedicated account manager for the partnership between our companies...",
    recipientName: "Lisa Johnson",
    recipientEmail: "lisa.johnson@wayne-enterprises.com",
    priority: "medium",
    status: "pending",
    createdAt: "2023-05-15T11:30:00Z",
    intent: "New stakeholder introduction",
  },
  {
    id: "email-4-4",
    accountId: "4",
    subject: "Case Study: Success Story in the Defense Sector",
    preview:
      "Hi Thomas, I wanted to share a recently published case study that I believe would be relevant to Wayne Enterprises. It details how another client in the defense sector achieved a 35% improvement in operational efficiency...",
    recipientName: "Thomas Wayne",
    recipientEmail: "thomas.wayne@wayne-enterprises.com",
    priority: "low",
    status: "pending",
    createdAt: "2023-05-13T10:15:00Z",
    intent: "Share success story",
  },

  // Stark Industries (id: "5") Email Suggestions
  {
    id: "email-5-1",
    accountId: "5",
    subject: "Technical Requirements: API Documentation",
    preview:
      "Hi Tony, Following up on the questions your engineering team had about our API capabilities, I've attached comprehensive documentation that addresses each of the points raised. Specifically, the section on authentication...",
    recipientName: "Tony Stark",
    recipientEmail: "tony.stark@stark-industries.com",
    priority: "high",
    status: "pending",
    createdAt: "2023-05-15T10:30:00Z",
    intent: "Technical follow-up",
  },
  {
    id: "email-5-2",
    accountId: "5",
    subject: "Innovation Initiative: Potential Collaboration Opportunities",
    preview:
      "Hi Pepper, I recently read about Stark Industries' new innovation initiative and wanted to reach out to discuss how our solutions might align with your objectives. Based on the public announcement, I see several areas...",
    recipientName: "Pepper Potts",
    recipientEmail: "pepper.potts@stark-industries.com",
    priority: "medium",
    status: "pending",
    createdAt: "2023-05-14T13:45:00Z",
    intent: "Innovation collaboration",
  },
]

// Helper function to get tasks for a specific account
export function getTasksForAccount(accountId: string): AITask[] {
  return mockAITasks.filter((task) => task.accountId === accountId)
}

// Helper function to get email suggestions for a specific account
export function getEmailSuggestionsForAccount(accountId: string): AIEmailSuggestion[] {
  return mockAIEmailSuggestions.filter((email) => email.accountId === accountId)
}

// Helper function to get tasks by time estimate
export function getTasksByTimeEstimate(tasks: AITask[], timeEstimate: "0-5" | "15" | "30" | "30+"): AITask[] {
  return tasks.filter((task) => task.timeEstimate === timeEstimate)
}
