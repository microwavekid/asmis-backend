export interface Email {
  id: string
  subject: string
  to: string
  from: string
  content: string
  status: "draft" | "pending" | "sent" | "approved" | "rejected"
  createdAt: string
  updatedAt: string
  accountId?: string
  attachments?: Attachment[]
  isExecutiveEmail?: boolean
  executiveSender?: string
}

export interface Attachment {
  id: string
  name: string
  size: number
  type: string
  url: string
}

export interface ExecutiveEmailTemplate {
  id: string
  name: string
  description: string
  executiveSender: string
  subject: string
  content: string
  createdAt: string
  updatedAt: string
}

export interface EmailRecipient {
  id: string
  name: string
  email: string
  company: string
  role?: string
}

export interface EmailGenerationSettings {
  tone: "formal" | "conversational" | "consultative"
  length: "concise" | "standard" | "comprehensive"
  includeAttachments: boolean
  followUpRequest: boolean
}
