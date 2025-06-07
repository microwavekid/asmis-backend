"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { Copy, Download, Save, Send } from "lucide-react"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import * as z from "zod"

import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { Separator } from "@/components/ui/separator"
import { Switch } from "@/components/ui/switch"
import { ExecutiveEmailPreview } from "./executive-email-preview"
import { useToast } from "@/hooks/use-toast"
import { AttachmentSelector, SelectedAttachmentsList, availableAttachments } from "./attachment-selector"
import type { UploadedFileInfo } from "@/components/ui/file-upload"

const formSchema = z.object({
  executiveSender: z.string({
    required_error: "Please select an executive sender",
  }),
  recipientEmail: z.string().email({
    message: "Please enter a valid email address",
  }),
  recipientName: z.string().min(1, {
    message: "Please enter the recipient's name",
  }),
  recipientCompany: z.string().min(1, {
    message: "Please enter the recipient's company",
  }),
  subject: z.string().min(1, {
    message: "Please enter a subject",
  }),
  relationshipSummary: z.string().min(10, {
    message: "Please provide a brief summary of the relationship or opportunity",
  }),
  actionAsk: z.string().min(10, {
    message: "Please specify what action or ask you want from the recipient",
  }),
  specialConsiderations: z.string().optional(),
  includeAttachments: z.boolean().default(false),
  attachmentIds: z.array(z.string()).default([]),
  tone: z.enum(["formal", "conversational", "consultative"]).default("conversational"),
  length: z.enum(["concise", "standard", "comprehensive"]).default("standard"),
  followUpRequest: z.boolean().default(false),
})

type FormValues = z.infer<typeof formSchema>

const defaultValues: Partial<FormValues> = {
  executiveSender: "",
  recipientEmail: "",
  recipientName: "",
  recipientCompany: "",
  subject: "",
  relationshipSummary: "",
  actionAsk: "",
  specialConsiderations: "",
  includeAttachments: false,
  attachmentIds: [],
  tone: "conversational",
  length: "standard",
  followUpRequest: false,
}

// Mock document map for demonstration purposes
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

export function ExecutiveEmailGenerator() {
  const [isGenerating, setIsGenerating] = useState(false)
  const [isSending, setIsSending] = useState(false)
  const [generatedEmail, setGeneratedEmail] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState("compose")
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFileInfo[]>([])
  const router = useRouter()
  const { toast } = useToast()

  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues,
  })

  async function onSubmit(data: FormValues) {
    setIsGenerating(true)

    try {
      // Simulate a delay for email generation
      await new Promise((resolve) => setTimeout(resolve, 1500))

      const mockEmail = generateMockEmail(data)
      setGeneratedEmail(mockEmail)
      setActiveTab("preview")

      toast({
        title: "Email generated successfully",
        description: "You can now review and edit the email before sending.",
      })
    } catch (error) {
      toast({
        title: "Failed to generate email",
        description: "Please try again or contact support if the issue persists.",
        variant: "destructive",
      })
    } finally {
      setIsGenerating(false)
    }
  }

  function generateMockEmail(data: FormValues): string {
    const {
      executiveSender,
      recipientName,
      recipientCompany,
      relationshipSummary,
      actionAsk,
      specialConsiderations,
      includeAttachments,
      attachmentIds,
    } = data

    const executiveTitle = getExecutiveTitle(executiveSender)
    const companyName = "Your Company"

    let email = `Dear ${recipientName},\n\n`

    // Introduction based on tone
    if (data.tone === "formal") {
      email += `I hope this message finds you well. As the ${executiveTitle} of ${companyName}, I wanted to personally reach out regarding our ongoing relationship with ${recipientCompany}.\n\n`
    } else if (data.tone === "conversational") {
      email += `I hope you're doing well! I wanted to personally connect with you about our work with ${recipientCompany}.\n\n`
    } else {
      email += `I've been following our partnership with ${recipientCompany} and wanted to share some thoughts with you directly.\n\n`
    }

    // Relationship summary
    email += `${relationshipSummary}\n\n`

    // Action/ask
    email += `${actionAsk}\n\n`

    // Special considerations if provided
    if (specialConsiderations && specialConsiderations.length > 0) {
      email += `${specialConsiderations}\n\n`
    }

    // Attachments if included
    if (includeAttachments && attachmentIds && attachmentIds.length > 0) {
      const attachmentNames = attachmentIds.map((id) => {
        const attachment = availableAttachments.find((a) => a.id === id)
        return attachment ? attachment.name : id
      })

      email += `I've attached the following document${
        attachmentNames.length > 1 ? "s" : ""
      } for your reference: ${attachmentNames.join(", ")}.\n\n`
    }

    // Closing based on tone
    if (data.tone === "formal") {
      email += `I look forward to your response and continuing our valuable partnership.\n\n`
    } else if (data.tone === "conversational") {
      email += `Looking forward to hearing your thoughts on this!\n\n`
    } else {
      email += `I'd appreciate your insights on this matter and am available to discuss further at your convenience.\n\n`
    }

    // Follow-up request if enabled
    if (data.followUpRequest) {
      email += `My assistant will follow up with you next week to schedule a brief call if that would be helpful.\n\n`
    }

    // Signature
    email += `Best regards,\n\n`
    email += `[Executive Name]\n`
    email += `${executiveTitle}\n`
    email += `${companyName}`

    return email
  }

  function getExecutiveTitle(executiveType: string): string {
    switch (executiveType) {
      case "ceo":
        return "Chief Executive Officer"
      case "cto":
        return "Chief Technology Officer"
      case "cfo":
        return "Chief Financial Officer"
      case "coo":
        return "Chief Operating Officer"
      default:
        return "Executive"
    }
  }

  function getExecutiveName(executiveType: string): string {
    switch (executiveType) {
      case "ceo":
        return "John Smith"
      case "cto":
        return "Michael Johnson"
      case "cfo":
        return "Sarah Williams"
      case "coo":
        return "David Brown"
      default:
        return "Executive Name"
    }
  }

  function getExecutiveEmail(executiveType: string): string {
    switch (executiveType) {
      case "ceo":
        return "ceo@yourcompany.com"
      case "cto":
        return "cto@yourcompany.com"
      case "cfo":
        return "cfo@yourcompany.com"
      case "coo":
        return "coo@yourcompany.com"
      default:
        return "executive@yourcompany.com"
    }
  }

  async function handleCopyToClipboard() {
    if (generatedEmail) {
      try {
        await navigator.clipboard.writeText(generatedEmail)
        toast({
          title: "Copied to clipboard",
          description: "Email content has been copied to your clipboard.",
        })
      } catch (error) {
        console.error("Failed to copy to clipboard:", error)
        toast({
          title: "Copy failed",
          description: "Could not copy to clipboard. Please try again.",
          variant: "destructive",
        })
      }
    }
  }

  async function handleDownload() {
    if (!generatedEmail) return

    try {
      setIsSending(true)

      // Create a multipart MIME message with attachments
      const executiveType = form.getValues("executiveSender")
      const fromName = getExecutiveName(executiveType)
      const fromEmail = getExecutiveEmail(executiveType)
      const toName = form.getValues("recipientName")
      const toEmail = form.getValues("recipientEmail")
      const subject = form.getValues("subject")
      const boundary = `----=_NextPart_${Math.random().toString(36).substring(2)}`

      // Create email headers
      let emlContent = ""
      emlContent += `From: ${fromName} <${fromEmail}>\r\n`
      emlContent += `To: ${toName} <${toEmail}>\r\n`
      emlContent += `Subject: ${subject}\r\n`
      emlContent += `Date: ${new Date().toUTCString()}\r\n`
      emlContent += `MIME-Version: 1.0\r\n`

      const hasAttachments =
        form.watch("includeAttachments") && form.watch("attachmentIds") && form.watch("attachmentIds").length > 0

      if (hasAttachments) {
        // Multipart message with attachments
        emlContent += `Content-Type: multipart/mixed; boundary="${boundary}"\r\n\r\n`

        // Add the email body as the first part
        emlContent += `--${boundary}\r\n`
        emlContent += `Content-Type: text/plain; charset=utf-8\r\n`
        emlContent += `Content-Transfer-Encoding: 7bit\r\n\r\n`
        emlContent += generatedEmail.replace(/\n/g, "\r\n")
        emlContent += `\r\n\r\n`

        // Add each attachment
        const attachmentIds = form.watch("attachmentIds") || []
        for (const id of attachmentIds) {
          const attachment = availableAttachments.find((a) => a.id === id)
          if (attachment) {
            const filename = documentMap[id as keyof typeof documentMap]?.filename || `${id}.pdf`

            emlContent += `--${boundary}\r\n`
            emlContent += `Content-Type: application/pdf; name="${filename}"\r\n`
            emlContent += `Content-Disposition: attachment; filename="${filename}"\r\n`
            emlContent += `Content-Transfer-Encoding: base64\r\n\r\n`

            // Add placeholder base64 content (this would be the actual file content in a real implementation)
            // This is a minimal valid PDF in base64 format
            emlContent += `JVBERi0xLjMKJcTl8uXrp/Og0MTGCjQgMCBvYmoKPDwgL0xlbmd0aCA1IDAgUiAvRmlsdGVyIC9GbGF0ZURl\r\n`
            emlContent += `Y29kZSA+PgpzdHJlYW0KeAErVAhUKFQwNFIwMlKwsdEPcFUwMDNUsFLwc1XQD6gEsQxNIApMwdVEwdXE\r\n`
            emlContent += `QBWuJgpXEwWrktSKEtucxJJUhZLU4hKF5MzcgvxKABJQFVAKZW5kc3RyZWFtCmVuZG9iago1IDAgb2Jq\r\n`
            emlContent += `CjEwNgplbmRvYmoKMiAwIG9iago8PCAvVHlwZSAvUGFnZSAvUGFyZW50IDMgMCBSIC9SZXNvdXJjZXMg\r\n`
            emlContent += `NiAwIFIgL0NvbnRlbnRzIDQgMCBSIC9NZWRpYUJveCBbMCAwIDYxMiA3OTJdCj4+CmVuZG9iago2IDAg\r\n`
            emlContent += `b2JqCjw8IC9Qcm9jU2V0IFsgL1BERiAvVGV4dCBdIC9Db2xvclNwYWNlIDw8IC9DczEgNyAwIFIgPj4g\r\n`
            emlContent += `L0ZvbnQgPDwgL1RUMiA5IDAgUgovVFQ0IDExIDAgUiA+PiA+PgplbmRvYmoKMTIgMCBvYmoKPDwgL0xl\r\n`
            emlContent += `bmd0aCAxMyAwIFIgL04gMyAvQWx0ZXJuYXRlIC9EZXZpY2VSR0IgL0ZpbHRlciAvRmxhdGVEZWNvZGUg\r\n`
            emlContent += `Pj4Kc3RyZWFtCngBnZZ3VFPZFofPvTe90BIiICX0GnoJINI7SBUEUYlJgFAChoQmdkQFRhQRKVZkVMAB\r\n`
            emlContent += `R8MIioyMBEsLBi0i6/3+mPnc+8frne8J3b3Pe/cuf3/2Xcs/N+P9ehZ31Y0DQqsXAUxlCQBMU0IwBwAg\r\n`
            emlContent += `TEeIR7ZxEQBCZjEegDUXiIgKi2sQAKBGRoYjzQmKs5woGhsYKDMVJGNRGRiUoBoz4AEYGMmIAKEMI0LW\r\n`
            emlContent += `EwlA4fLEgoLEY4QNUBAQ5wSFRMUwJFBoJAg0GBpGZFBYrBCAyFBYKFVYXKxAA0rFiUNAZBBYMDQsQlFU\r\n`
            emlContent += `KhMSMhhsCkNDGxsrKwYpDgYKCXFzc3N7MZAcHRwc3hxE+7qrq7u8vsHDxcXLm5HIrO/o6u7d8fLz9vf5\r\n`
            emlContent += `+vz8Aad93v2Rh4dYWQOAp+gvANSTGJoXJIDU0QHQkgFQd6b7/+zq6trnSgX/XSYG+3+Jtl5UAGBZRwDw\r\n`
            emlContent += `vxzGJAKQRGfoaKRBPgYk9BmS0GJIQZXSYFRLqNLXjUbD4eK4MaatUK/Xj0aVwXg8XS5Xq/VGo9VuJJOp\r\n`
            emlContent += `dCaTzeULxVKlWqvXG81Wu9PtdHv9wbA/GE1ms8V8sUZgLVaCwWQyQ2Q6Z7Bh0RMJIBsJgCgQiCQSmUJl\r\n`
            emlContent += `sDgcHo9PEAgkEpnK4PL4AqFILJHK5AqlSq3R6vQGo8lssdk5XB5fIBSJJVKZXKFUqTVand5gtFlsdoc\r\n`
            emlContent += `TpfYEQpFYIpXJFUqVWqPV6Q1Gk9litzhdbo8XyGLz+AKhSCyRyuQKpUqt0er0BqPJbLHa7A6ny+3x+v\r\n`
            emlContent += `wBoTAUjkRj8UQylc5kc/lCsVSu1OqNZqvd6fZ4ff5AMBSORGPxRDKVzmRz+UK9QW8wWQBYAJAzGgAoGZ\r\n`
            emlContent += `FLAiCQFQAIZIGbmwgAEFwBQFwQ3h8A4EWeSgCgspcNgNLSAoBwA4BSHQDIZQWLpQCguK0AoHMrAIhJAU\r\n`
            emlContent += `BcFgCIGQGAuCEAELOEJRcAhLYAQEwKAMI7ACAmBQCxLQAQEwOAuBwAxIwAQEwKAGJbACBmBABiUgAQlw\r\n`
            emlContent += `MAMSMAEJMCgHgaAIgZAYCYEQCISQFAbAsAxMQAIC4HADEjABCTAoDYFgCIiQFAXA4AYkYAICYFALE5AB\r\n`
            emlContent += `AzAgAxKQCIywGAmBEAiEkBQGwOAMSMAEBMCgDicgAQMwIAMSkAiM0BgJgRAIhJAUBcDgBiRgAgJgUAs\r\n`
            emlContent += `TkAEDMCADEpAIjLAUDMCADEpAAgNgcAYkYAICYFAHE5AIgZAYCYFADE5gBAzAgAxKQAIC4HADEjABCT\r\n`
            emlContent += `AoDYHACIGQGAmBQAxOUAIGYEAGJSABCbAwAxIwAQkwKAuBwAxIwAQEwKAGJzACBmBABiUgAQlwOAmBE\r\n`
            emlContent += `AiEkBQGwOAMSMAEBMCgDicgAQMwIAMSkAiM0BgJgRAIhJAUBcDgBiRgAgJgUAsTkAEDMCADEpAIjLAU\r\n`
            emlContent += `DMCADEpAAgNgcAYkYAICYFAHE5AIgZAYCYFADE5gBAzAgAxKQAIC4HADEjABCTAoDYHACIGQGAmBQAx\r\n`
            emlContent += `OUAIGYEAGJSABCbAwAxIwAQkwKAuBwAxIwAQEwKAGJzACBmBABiUgAQlwOAmBEAiEkBQGwOAMSMAEBM\r\n`
            emlContent += `CgDicgAQMwIAMSkAiM0BgJgRAIhJAUBcDgBiRgAgJgUAsTkAEDMCADEpAIjLAUDMCADEpAAgNgcAYkY\r\n`
            emlContent += `AICYFALEtABATA4C4HADEjABATAoAYlsAICYGAHE5AIgZAYCYFADEtgBATAwA4nIAEDMCADEpAIhtAY\r\n`
            emlContent += `CYGADEpQAgZgQAYlIAENsCADExAIhLAUDMCADEpAAgNgcAYkYAICYFAHE5AIgZAYCYFADE5gBAzAgAx\r\n`
            emlContent += `KQAQEwOAMSMAEBMCgDicgAQMwIAMSkAiM0BgJgRAIhJAUBcDgBiRgAgJgUAsTkAEDMCADEpAIjLAUDM\r\n`
            emlContent += `CADEpAAgNgcAYkYAICYFAHE5AIgZAYCYFADE5gBAzAgAxKQAIC4HADEjABCTAoDYHACIGQGAmBQAxOU\r\n`
            emlContent += `AIGYEAGJSABCbAwAxIwAQkwKAuBwAxIwAQEwKAGJzACBmBABiUgAQlwOAmBEAiEkBQGwOAMSMAEBMCg\r\n`
            emlContent += `DicgAQMwIAMSkAiM0BgJgRAIhJAUBcDgBiRgAgJgUAsTkAEDMCADEpAIjLAUDMCADEpAAgNgcAYkYAI\r\n`
            emlContent += `CYFALEtABATA4C4HADEjABATAoAYlsAICYGAHE5AIgZAYCYFADEtgBATAwA4nIAEDMCADEpAIhtAYCY\r\n`
            emlContent += `GADEpQAgZgQAYlIAENsCADExAIhLAUDMCADEpAAgNgcAYkYAICYFAHE5AIgZAYCYFADE5gBAzAgAxKQ\r\n`
            emlContent += `AQEwOAMSMAEBMCgDicgAQMwIAMSkAiM0BgJgRAIhJAUBcDgBiRgAgJgUAsTkAEDMCADEpAIjLAUDMCA\r\n`
            emlContent += `DEpAAgNgcAYkYAICYFAHE5AIgZAYCYFADE5gBAzAgAxKQAIC4HADEjABCTAoDYHACIGQGAmBQAxOUAI\r\n`
            emlContent += `GYEAGJSABCbAwAxIwAQkwKAuBwAxIwAQEwKAGJzACBmBABiUgAQlwOAmBEAiEkBQGwOAMSMAEBMCgDi\r\n`
            emlContent += `cgAQMwIAMSkAiM0BgJgRAIhJAUBcDgBiRgAgJgUAsTkAEDMCADEpAIjLAUDMCADEpAAgNgcAYkYAICY\r\n`
            emlContent += `FALEtABATA4C4HADEjABATAoAYlsAICYGAHE5AIgZAYCYFADEtgBATAwA4nIAEDMCADEpAIhtAYCYGA\r\n`
            emlContent += `DEpQAgZgQAYlIAENsCADExAIhLAUDMCADEpAAgNgcAYkYAICYFAHE5AIgZAYCYFADE5gBAzAgAxKQAQ\r\n`
            emlContent += `EwOAMSMAEBMCgDicgAQMwIAMSkAiM0BgJgRAIhJAUBcDgBiRgAgJgUAsTkAEDMCADEpAIjLAUDMCADE\r\n`
            emlContent += `pAAgNgcAYkYAICYFAHE5AIgZAYCYFADE5gBAzAgAxKQAIC4HADEjABCTAoDYHACIGQGAmBQAxOUAIGY\r\n`
            emlContent += `EAGJSABCbAwAxIwAQkwKAuBwAxIwAQEwKAGJzACBmBABiUgAQlwOAmBEAiEkBQGwOAMSMAEBMCgDicg\r\n`
            emlContent += `AQMwIAMSkAiM0BgJgRAIhJAUBcDgBiRgAgJgUAsTkAEDMCADEpAIjLAUDMCADEpAAgNgcAYkYAICYFA\r\n`
            emlContent += `LEtABATA4C4HADEjABATAoAYlsAICYGAHE5AIgZAYCYFADEtgBATAwA4nIAEDMCADEpAIhtAYCYGADE\r\n`
            emlContent += `pQAgZgQAYlIAENsCADExAIhLAUDMCADEpAAgNgcAYkYAICYFAHE5AIgZAYCYFADE5gBAzAgAxKQAQEw\r\n`
            emlContent += `OAMSMAEBMCgDicgAQMwIAMSkAiM0BgJgRAIhJAUBcDgBiRgAgJgUAsTkAEDMCADEpAIjLAUDMCADEpA\r\n`
            emlContent += `AgNgcAYkYAICYFAHE5AIgZAYCYFADE5gBAzAgAxKQAIC4HADEjABCTAoDYHACIGQGAmBQAxOU`
            emlContent += `\r\n\r\n`
          }
        }

        // Add uploaded files if any
        if (uploadedFiles && uploadedFiles.length > 0) {
          for (const file of uploadedFiles) {
            emlContent += `--${boundary}\r\n`
            emlContent += `Content-Type: application/octet-stream; name="${file.name}"\r\n`
            emlContent += `Content-Disposition: attachment; filename="${file.name}"\r\n`
            emlContent += `Content-Transfer-Encoding: base64\r\n\r\n`

            // Add placeholder base64 content
            emlContent += `JVBERi0xLjMKJcTl8uXrp/Og0MTGCjQgMCBvYmoKPDwgL0xlbmd0aCA1IDAgUiAvRmlsdGVyIC9GbGF0ZURl\r\n`
            emlContent += `Y29kZSA+PgpzdHJlYW0KeAErVAhUKFQwNFIwMlKwsdEPcFUwMDNUsFLwc1XQD6gEsQxNIApMwdVEwdXE\r\n`
            emlContent += `QBWuJgpXEwWrktSKEtucxJJUhZLU4hKF5MzcgvxKABJQFVAKZW5kc3RyZWFtCmVuZG9iago1IDAgb2Jq\r\n`
            emlContent += `\r\n\r\n`
          }
        }

        // Close the multipart message
        emlContent += `--${boundary}--\r\n`
      } else {
        // Simple text email without attachments
        emlContent += `Content-Type: text/plain; charset=utf-8\r\n\r\n`
        emlContent += generatedEmail.replace(/\n/g, "\r\n")
      }

      // Create a blob and download it
      const blob = new Blob([emlContent], { type: "message/rfc822" })
      const url = URL.createObjectURL(blob)

      const element = document.createElement("a")
      element.href = url
      element.download = `executive-email-${Date.now()}.eml`
      document.body.appendChild(element)
      element.click()
      document.body.removeChild(element)

      // Clean up the URL object
      URL.revokeObjectURL(url)

      toast({
        title: "Email downloaded",
        description:
          "Email has been downloaded in .eml format with attachments, ready to open in Outlook or other email clients.",
      })
    } catch (error) {
      console.error("Error downloading email:", error)
      toast({
        title: "Download failed",
        description: "There was an error creating the email file. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsSending(false)
    }
  }

  function handleSaveTemplate() {
    toast({
      title: "Template saved",
      description: "This email has been saved as a template for future use.",
    })
  }

  async function handleSendEmail() {
    try {
      setIsSending(true)

      // Simulate sending the email
      await new Promise((resolve) => setTimeout(resolve, 1500))

      toast({
        title: "Email sent",
        description: "Your email has been sent successfully with all attachments.",
      })

      // Redirect after a short delay
      setTimeout(() => {
        router.push("/emails")
      }, 1000)
    } catch (error) {
      console.error("Error sending email:", error)
      toast({
        title: "Failed to send email",
        description: "There was an error sending your email. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsSending(false)
    }
  }

  return (
    <div className="container mx-auto py-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Executive Email Generator</h1>
          <p className="text-muted-foreground">Create professional emails from your executives to key stakeholders</p>
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList>
          <TabsTrigger value="compose">Compose</TabsTrigger>
          <TabsTrigger value="preview" disabled={!generatedEmail}>
            Preview
          </TabsTrigger>
        </TabsList>

        <TabsContent value="compose" className="space-y-4">
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Left column - Email details */}
                <div className="space-y-6 md:col-span-2">
                  <Card>
                    <CardContent className="pt-6">
                      <div className="space-y-4">
                        <FormField
                          control={form.control}
                          name="executiveSender"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel>Executive Sender</FormLabel>
                              <Select onValueChange={field.onChange} defaultValue={field.value}>
                                <FormControl>
                                  <SelectTrigger>
                                    <SelectValue placeholder="Select an executive" />
                                  </SelectTrigger>
                                </FormControl>
                                <SelectContent>
                                  <SelectItem value="ceo">CEO</SelectItem>
                                  <SelectItem value="cto">CTO</SelectItem>
                                  <SelectItem value="cfo">CFO</SelectItem>
                                  <SelectItem value="coo">COO</SelectItem>
                                </SelectContent>
                              </Select>
                              <FormDescription>Select which executive will be sending this email</FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <FormField
                            control={form.control}
                            name="recipientEmail"
                            render={({ field }) => (
                              <FormItem>
                                <FormLabel>Recipient Email</FormLabel>
                                <FormControl>
                                  <Input placeholder="email@company.com" {...field} />
                                </FormControl>
                                <FormMessage />
                              </FormItem>
                            )}
                          />

                          <FormField
                            control={form.control}
                            name="recipientName"
                            render={({ field }) => (
                              <FormItem>
                                <FormLabel>Recipient Name</FormLabel>
                                <FormControl>
                                  <Input placeholder="John Doe" {...field} />
                                </FormControl>
                                <FormMessage />
                              </FormItem>
                            )}
                          />
                        </div>

                        <FormField
                          control={form.control}
                          name="recipientCompany"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel>Recipient Company</FormLabel>
                              <FormControl>
                                <Input placeholder="Acme Inc." {...field} />
                              </FormControl>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="subject"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel>Subject Line</FormLabel>
                              <FormControl>
                                <Input placeholder="Meeting Follow-up: Next Steps" {...field} />
                              </FormControl>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="relationshipSummary"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel>Relationship/Opportunity Summary</FormLabel>
                              <FormControl>
                                <Textarea
                                  placeholder="Briefly describe the relationship or opportunity context"
                                  className="min-h-[100px]"
                                  {...field}
                                />
                              </FormControl>
                              <FormDescription>
                                Provide context about your relationship with the recipient or the opportunity you're
                                discussing
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="actionAsk"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel>Action/Ask</FormLabel>
                              <FormControl>
                                <Textarea
                                  placeholder="What specific action do you want the recipient to take?"
                                  className="min-h-[100px]"
                                  {...field}
                                />
                              </FormControl>
                              <FormDescription>
                                Clearly state what you want the recipient to do or what you're asking for
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="specialConsiderations"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel>Special Considerations (Optional)</FormLabel>
                              <FormControl>
                                <Textarea
                                  placeholder="Any special considerations or additional context"
                                  className="min-h-[100px]"
                                  {...field}
                                />
                              </FormControl>
                              <FormDescription>
                                Include any additional context, timing considerations, or other important details
                              </FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="includeAttachments"
                          render={({ field }) => (
                            <FormItem className="flex flex-row items-center justify-between rounded-lg border p-4">
                              <div className="space-y-0.5">
                                <FormLabel className="text-base">Include Attachments</FormLabel>
                                <FormDescription>Add file attachments to your email</FormDescription>
                              </div>
                              <FormControl>
                                <Switch checked={field.value} onCheckedChange={field.onChange} />
                              </FormControl>
                            </FormItem>
                          )}
                        />

                        {form.watch("includeAttachments") && (
                          <FormField
                            control={form.control}
                            name="attachmentIds"
                            render={({ field }) => (
                              <FormItem>
                                <FormControl>
                                  <AttachmentSelector
                                    selectedAttachments={field.value || []}
                                    uploadedFiles={uploadedFiles || []}
                                    onAttachmentChange={field.onChange}
                                    onUploadedFilesChange={setUploadedFiles}
                                  />
                                </FormControl>
                                <FormMessage />
                              </FormItem>
                            )}
                          />
                        )}
                      </div>
                    </CardContent>
                  </Card>
                </div>

                {/* Right column - Email settings */}
                <div className="space-y-6">
                  <Card>
                    <CardContent className="pt-6">
                      <h3 className="text-lg font-medium mb-4">Email Settings</h3>

                      <div className="space-y-6">
                        <FormField
                          control={form.control}
                          name="tone"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel>Email Tone</FormLabel>
                              <Select onValueChange={field.onChange} defaultValue={field.value}>
                                <FormControl>
                                  <SelectTrigger>
                                    <SelectValue placeholder="Select tone" />
                                  </SelectTrigger>
                                </FormControl>
                                <SelectContent>
                                  <SelectItem value="formal">Formal</SelectItem>
                                  <SelectItem value="conversational">Conversational</SelectItem>
                                  <SelectItem value="consultative">Consultative</SelectItem>
                                </SelectContent>
                              </Select>
                              <FormDescription>Choose the tone that best fits the relationship</FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="length"
                          render={({ field }) => (
                            <FormItem>
                              <FormLabel>Email Length</FormLabel>
                              <Select onValueChange={field.onChange} defaultValue={field.value}>
                                <FormControl>
                                  <SelectTrigger>
                                    <SelectValue placeholder="Select length" />
                                  </SelectTrigger>
                                </FormControl>
                                <SelectContent>
                                  <SelectItem value="concise">Concise</SelectItem>
                                  <SelectItem value="standard">Standard</SelectItem>
                                  <SelectItem value="comprehensive">Comprehensive</SelectItem>
                                </SelectContent>
                              </Select>
                              <FormDescription>Choose how detailed the email should be</FormDescription>
                              <FormMessage />
                            </FormItem>
                          )}
                        />

                        <FormField
                          control={form.control}
                          name="followUpRequest"
                          render={({ field }) => (
                            <FormItem className="flex flex-row items-center justify-between rounded-lg border p-4">
                              <div className="space-y-0.5">
                                <FormLabel className="text-base">Request Follow-up</FormLabel>
                                <FormDescription>Mention that your assistant will follow up</FormDescription>
                              </div>
                              <FormControl>
                                <Switch checked={field.value} onCheckedChange={field.onChange} />
                              </FormControl>
                            </FormItem>
                          )}
                        />
                      </div>

                      <Separator className="my-6" />

                      <div className="space-y-4">
                        <h3 className="text-lg font-medium">Template Options</h3>
                        <div className="grid grid-cols-1 gap-2">
                          <Button variant="outline" type="button" className="justify-start">
                            <Save className="mr-2 h-4 w-4" />
                            Load Template
                          </Button>
                          <Button variant="outline" type="button" className="justify-start">
                            <Save className="mr-2 h-4 w-4" />
                            Save as Template
                          </Button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Button type="submit" className="w-full" size="lg" disabled={isGenerating}>
                    {isGenerating ? "Generating..." : "Generate Email"}
                  </Button>
                </div>
              </div>
            </form>
          </Form>
        </TabsContent>

        <TabsContent value="preview" className="space-y-4">
          {generatedEmail && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="md:col-span-2">
                <ExecutiveEmailPreview
                  emailContent={generatedEmail}
                  subject={form.getValues("subject") || ""}
                  executiveSender={form.getValues("executiveSender") || ""}
                  recipientName={form.getValues("recipientName") || ""}
                  recipientEmail={form.getValues("recipientEmail") || ""}
                  attachmentIds={form.watch("includeAttachments") ? form.watch("attachmentIds") || [] : []}
                />
                {form.watch("includeAttachments") && (
                  <div className="mt-4 border-t pt-4">
                    <SelectedAttachmentsList
                      attachmentIds={form.watch("attachmentIds") || []}
                      uploadedFiles={uploadedFiles || []}
                    />
                  </div>
                )}
              </div>

              <div className="space-y-6">
                <Card>
                  <CardContent className="pt-6">
                    <h3 className="text-lg font-medium mb-4">Email Actions</h3>
                    <div className="space-y-3">
                      <TooltipProvider>
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Button variant="outline" className="w-full justify-start" onClick={handleCopyToClipboard}>
                              <Copy className="mr-2 h-4 w-4" />
                              Copy to Clipboard
                            </Button>
                          </TooltipTrigger>
                          <TooltipContent>
                            <p>Copy the email content to your clipboard</p>
                          </TooltipContent>
                        </Tooltip>
                      </TooltipProvider>

                      <TooltipProvider>
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Button
                              variant="outline"
                              className="w-full justify-start"
                              onClick={handleDownload}
                              disabled={isSending}
                            >
                              <Download className="mr-2 h-4 w-4" />
                              {isSending ? "Preparing Download..." : "Download as .EML"}
                            </Button>
                          </TooltipTrigger>
                          <TooltipContent>
                            <p>Download as .EML file for use in Outlook and other email clients</p>
                          </TooltipContent>
                        </Tooltip>
                      </TooltipProvider>

                      <TooltipProvider>
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Button variant="outline" className="w-full justify-start" onClick={handleSaveTemplate}>
                              <Save className="mr-2 h-4 w-4" />
                              Save as Template
                            </Button>
                          </TooltipTrigger>
                          <TooltipContent>
                            <p>Save this email as a template for future use</p>
                          </TooltipContent>
                        </Tooltip>
                      </TooltipProvider>

                      <Separator />

                      <Button className="w-full" onClick={handleSendEmail} disabled={isSending}>
                        <Send className="mr-2 h-4 w-4" />
                        {isSending ? "Sending..." : "Send Email"}
                      </Button>

                      <Button variant="outline" className="w-full" onClick={() => setActiveTab("compose")}>
                        Edit Email
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  )
}
