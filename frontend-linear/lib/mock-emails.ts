import type { Email, ExecutiveEmailTemplate } from "@/types/email"

export const mockEmails: Email[] = [
  {
    id: "1",
    subject: "Q3 Business Review - Action Items",
    to: "john.smith@acmeinc.com",
    from: "sales-assistant@yourcompany.com",
    content:
      "Hi John,\n\nFollowing our Q3 business review, I wanted to summarize the key action items we discussed:\n\n1. Schedule technical deep dive with your engineering team\n2. Share updated pricing proposal by end of week\n3. Introduce you to our customer success manager\n\nPlease let me know if you have any questions or if I missed anything.\n\nBest regards,\nSales Assistant",
    status: "pending",
    createdAt: "2023-10-15T10:30:00Z",
    updatedAt: "2023-10-15T10:30:00Z",
    accountId: "1",
    recipients: [
      {
        name: "john.smith",
        email: "john.smith@acmeinc.com",
      },
    ],
  },
  {
    id: "2",
    subject: "Product Roadmap Discussion",
    to: "sarah.johnson@globexcorp.com",
    from: "sales-assistant@yourcompany.com",
    content:
      "Hi Sarah,\n\nI hope this email finds you well. I wanted to follow up on our conversation about our product roadmap.\n\nAs discussed, we're planning to release the following features in Q4:\n\n- Advanced analytics dashboard\n- Custom reporting tools\n- API enhancements\n\nWould you be available next week for a more detailed discussion? I'd be happy to schedule a call with our product team.\n\nBest regards,\nSales Assistant",
    status: "approved",
    createdAt: "2023-10-10T14:45:00Z",
    updatedAt: "2023-10-11T09:15:00Z",
    accountId: "2",
    recipients: [
      {
        name: "sarah.johnson",
        email: "sarah.johnson@globexcorp.com",
      },
    ],
  },
  {
    id: "3",
    subject: "Contract Renewal Information",
    to: "michael.brown@initech.com",
    from: "sales-assistant@yourcompany.com",
    content:
      "Hi Michael,\n\nI hope you're doing well. I'm reaching out regarding your upcoming contract renewal.\n\nYour current contract is set to expire on November 30, 2023. Based on your current usage and growth, I've prepared a renewal proposal that includes:\n\n- 20% increase in user licenses\n- Premium support package\n- Access to our new enterprise features\n\nWould you like to schedule a call to discuss the details? I'm available most of next week.\n\nBest regards,\nSales Assistant",
    status: "sent",
    createdAt: "2023-10-05T11:20:00Z",
    updatedAt: "2023-10-06T16:30:00Z",
    accountId: "3",
    recipients: [
      {
        name: "michael.brown",
        email: "michael.brown@initech.com",
      },
    ],
  },
  {
    id: "4",
    subject: "Strategic Partnership Opportunity",
    to: "lisa.wong@partner.com",
    from: "sales-assistant@yourcompany.com",
    content:
      "Hi Lisa,\n\nFollowing our conversation at the industry conference last week, I wanted to explore the partnership opportunity we discussed.\n\nBased on our complementary product offerings, I believe there's significant potential for:\n\n1. Joint marketing initiatives\n2. Product integrations\n3. Shared go-to-market strategies\n\nI've attached a brief overview of how I envision this partnership. Would you be interested in discussing this further?\n\nBest regards,\nSales Assistant",
    status: "draft",
    createdAt: "2023-10-01T09:00:00Z",
    updatedAt: "2023-10-01T09:00:00Z",
    accountId: "1",
    recipients: [
      {
        name: "lisa.wong",
        email: "lisa.wong@partner.com",
      },
    ],
  },
  {
    id: "5",
    subject: "Introduction to Our New Solution",
    to: "david.miller@prospect.com",
    from: "sales-assistant@yourcompany.com",
    content:
      "Hi David,\n\nIt was great speaking with you yesterday about your challenges with data management and analytics.\n\nBased on our conversation, I believe our new DataFlow solution would be a perfect fit for your needs. It offers:\n\n- Automated data processing\n- Real-time analytics\n- Customizable dashboards\n- Enterprise-grade security\n\nI'd love to arrange a demo for you and your team. Would next Tuesday at 2 PM work for you?\n\nBest regards,\nSales Assistant",
    status: "rejected",
    createdAt: "2023-09-28T15:10:00Z",
    updatedAt: "2023-09-29T10:45:00Z",
    accountId: "2",
    recipients: [
      {
        name: "david.miller",
        email: "david.miller@prospect.com",
      },
    ],
  },
  {
    id: "6",
    subject: "Strategic Partnership Discussion",
    to: "jennifer.parker@globexcorp.com",
    from: "ceo@yourcompany.com",
    content:
      "Dear Jennifer,\n\nI hope this message finds you well. As the CEO of YourCompany, I wanted to personally reach out regarding the potential strategic partnership between our organizations.\n\nHaving followed Globex's impressive growth over the past year, I believe there's a unique opportunity for us to collaborate in ways that would benefit both our companies and customers.\n\nI'd appreciate the opportunity to discuss this further with you. Would you be available for a brief call next week?\n\nBest regards,\n\nJohn Doe\nChief Executive Officer\nYourCompany",
    status: "sent",
    createdAt: "2023-10-12T09:30:00Z",
    updatedAt: "2023-10-12T09:30:00Z",
    accountId: "2",
    isExecutiveEmail: true,
    executiveSender: "ceo",
    recipients: [
      {
        name: "jennifer.parker",
        email: "jennifer.parker@globexcorp.com",
      },
    ],
  },
  {
    id: "7",
    subject: "Technology Roadmap Alignment",
    to: "robert.chen@acmeinc.com",
    from: "cto@yourcompany.com",
    content:
      "Dear Robert,\n\nI've been following the innovative work your team has been doing in the AI space, and I'm impressed with your approach to solving complex industry challenges.\n\nAs we're currently refining our technology roadmap for the coming year, I believe there could be significant value in aligning some of our development efforts.\n\nI'd like to invite you to a private technology briefing with our senior engineering team to explore potential areas of collaboration. Would you be interested in such a discussion?\n\nBest regards,\n\nJane Smith\nChief Technology Officer\nYourCompany",
    status: "approved",
    createdAt: "2023-10-08T14:15:00Z",
    updatedAt: "2023-10-09T11:20:00Z",
    accountId: "1",
    isExecutiveEmail: true,
    executiveSender: "cto",
    recipients: [
      {
        name: "robert.chen",
        email: "robert.chen@acmeinc.com",
      },
    ],
  },
]

export const mockExecutiveEmailTemplates: ExecutiveEmailTemplate[] = [
  {
    id: "1",
    name: "Strategic Partnership Introduction",
    description: "Initial outreach from CEO to potential strategic partners",
    executiveSender: "ceo",
    subject: "Exploring Strategic Partnership Opportunities",
    content:
      "Dear {{recipientName}},\n\nI hope this message finds you well. As the Chief Executive Officer of {{companyName}}, I wanted to personally reach out regarding the potential strategic partnership between our organizations.\n\nHaving followed {{recipientCompany}}'s impressive growth over the past year, I believe there's a unique opportunity for us to collaborate in ways that would benefit both our companies and customers.\n\nI'd appreciate the opportunity to discuss this further with you. Would you be available for a brief call next week?\n\nBest regards,\n\n{{executiveName}}\nChief Executive Officer\n{{companyName}}",
    createdAt: "2023-09-15T10:00:00Z",
    updatedAt: "2023-09-15T10:00:00Z",
  },
  {
    id: "2",
    name: "Technology Collaboration",
    description: "CTO outreach for technical collaboration",
    executiveSender: "cto",
    subject: "Technology Collaboration Opportunity",
    content:
      "Dear {{recipientName}},\n\nI've been following the innovative work your team has been doing in the {{technologyArea}} space, and I'm impressed with your approach to solving complex industry challenges.\n\nAs we're currently refining our technology roadmap for the coming year, I believe there could be significant value in aligning some of our development efforts.\n\nI'd like to invite you to a private technology briefing with our senior engineering team to explore potential areas of collaboration. Would you be interested in such a discussion?\n\nBest regards,\n\n{{executiveName}}\nChief Technology Officer\n{{companyName}}",
    createdAt: "2023-09-20T14:30:00Z",
    updatedAt: "2023-09-20T14:30:00Z",
  },
  {
    id: "3",
    name: "Financial Partnership",
    description: "CFO outreach for financial collaboration",
    executiveSender: "cfo",
    subject: "Financial Partnership Discussion",
    content:
      "Dear {{recipientName}},\n\nI hope this email finds you well. As the Chief Financial Officer of {{companyName}}, I've been analyzing potential strategic financial partnerships that could drive mutual growth.\n\n{{recipientCompany}}'s financial performance and market approach have caught my attention, and I believe there may be opportunities for our organizations to collaborate in ways that strengthen both our positions.\n\nI would welcome the chance to discuss this with you directly. Would you be available for a conversation in the coming weeks?\n\nBest regards,\n\n{{executiveName}}\nChief Financial Officer\n{{companyName}}",
    createdAt: "2023-09-25T11:15:00Z",
    updatedAt: "2023-09-25T11:15:00Z",
  },
]
