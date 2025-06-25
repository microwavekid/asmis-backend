"use server"

import { availableAttachments } from "@/components/emails/attachment-selector"

// Simple mock document URLs - using placeholder images
const documentMap = {
  "gartner-dxp": {
    url: "/gartner-dxp-2025.png",
    filename: "Q1-2025-Gartner-Magic-Quadrant-DXP.pdf",
  },
  "gartner-personalization": {
    url: "/gartner-mq-personalization-2025.png",
    filename: "Q1-2025-Gartner-Magic-Quadrant-Personalization.pdf",
  },
  "gartner-cmp": {
    url: "/gartner-cmp-2025.png",
    filename: "Q1-2025-Gartner-Magic-Quadrant-CMP.pdf",
  },
  "forrester-cms": {
    url: "/forrester-cms-wave-2025.png",
    filename: "Q1-2025-Forrester-Wave-CMS.pdf",
  },
  "forrester-optimization": {
    url: "/forrester-wave-experience-optimization-2024.png",
    filename: "Q4-2024-Forrester-Wave-Optimization.pdf",
  },
}

export async function getDocumentUrl(documentId: string): Promise<string | null> {
  const document = documentMap[documentId as keyof typeof documentMap]
  if (!document) return null
  return document.url
}

export async function getDocumentUrls(documentIds: string[]): Promise<Record<string, string>> {
  const urls: Record<string, string> = {}

  for (const id of documentIds) {
    const url = await getDocumentUrl(id)
    if (url) {
      urls[id] = url
    }
  }

  return urls
}

export async function createEmailWithAttachments(
  emailContent: string,
  subject: string,
  from: string,
  to: string,
  attachmentIds: string[],
  uploadedFileUrls: { id: string; url: string; name: string }[],
): Promise<{ id: string; downloadUrl: string; filename: string }> {
  const emailId = `email-${Date.now()}`

  // For this demo, we'll create a simple JSON representation
  // In a real implementation, we would generate a proper .eml file
  const emailData = {
    id: emailId,
    from,
    to,
    subject,
    content: emailContent,
    attachments: [
      ...attachmentIds.map((id) => {
        const attachment = availableAttachments.find((a) => a.id === id)
        return {
          id,
          name: attachment?.name || id,
          filename: documentMap[id as keyof typeof documentMap]?.filename || `${id}.pdf`,
        }
      }),
      ...uploadedFileUrls.map((file) => ({
        id: file.id,
        name: file.name,
        filename: file.name,
      })),
    ],
    date: new Date().toISOString(),
  }

  // Convert to JSON string
  const jsonString = JSON.stringify(emailData, null, 2)

  // Create a data URL for the JSON
  const dataUrl = `data:application/json;charset=utf-8,${encodeURIComponent(jsonString)}`

  return {
    id: emailId,
    downloadUrl: dataUrl,
    filename: `${emailId}.eml`,
  }
}
