"use client"

import { useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { mockAccounts, mockOpportunities } from "@/lib/mock-data"
import { Check, Copy, Download, FileText, Mail, Save } from "lucide-react"
import { useToast } from "@/hooks/use-toast"

interface EmailDetailDialogProps {
  email: any
  isOpen: boolean
  onClose: () => void
  onApprove: (emailId: string) => void
  onUpdate: (updatedEmail: any) => void
}

export function EmailDetailDialog({ email, isOpen, onClose, onApprove, onUpdate }: EmailDetailDialogProps) {
  const { toast } = useToast()
  const [activeTab, setActiveTab] = useState("preview")
  const [editedBody, setEditedBody] = useState(email.body || "")
  const [isEditing, setIsEditing] = useState(false)
  const [isDownloading, setIsDownloading] = useState(false)

  const account = mockAccounts.find((a) => a.id === (email.accountId || ""))
  const opportunity = mockOpportunities.find((o) => o.id === (email.opportunityId || ""))

  const handleSaveEdit = () => {
    // If the email was in pending status, move it to drafting
    const newStatus = email.status === "pending" ? "drafting" : email.status

    onUpdate({
      ...email,
      body: editedBody,
      status: newStatus,
    })
    setIsEditing(false)

    const statusMessage =
      email.status === "pending" ? "Email has been updated and moved to Drafting" : "Your changes have been saved"

    toast({
      title: "Email updated",
      description: statusMessage,
    })
  }

  const handleApprove = () => {
    onApprove(email.id)
  }

  const handleCopyToClipboard = () => {
    const emailText = `Subject: ${email.subject}

${email.body || ""}`

    navigator.clipboard.writeText(emailText)

    toast({
      title: "Copied to clipboard",
      description: "Email content has been copied to your clipboard",
    })
  }

  const handleDownloadText = () => {
    setIsDownloading(true)

    setTimeout(() => {
      const emailText = `Subject: ${email.subject}

${email.body || ""}`

      const element = document.createElement("a")
      const file = new Blob([emailText], { type: "text/plain" })
      element.href = URL.createObjectURL(file)
      element.download = `email-${email.id}.txt`
      document.body.appendChild(element)
      element.click()
      document.body.removeChild(element)

      setIsDownloading(false)

      toast({
        title: "Email downloaded",
        description: "Email has been downloaded as a text file",
      })
    }, 500)
  }

  const handleDownloadOutlook = () => {
    setIsDownloading(true)

    setTimeout(() => {
      // Create a simple .eml file
      const emlContent = `From: ${email.senderName} <${email.senderEmail}>
To: ${email.recipientName} <${email.recipientEmail}>
Subject: ${email.subject}
Date: ${new Date().toUTCString()}
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 7bit

${email.body || ""}`

      const element = document.createElement("a")
      const file = new Blob([emlContent], { type: "message/rfc822" })
      element.href = URL.createObjectURL(file)
      element.download = `email-${email.id}.eml`
      document.body.appendChild(element)
      element.click()
      document.body.removeChild(element)

      setIsDownloading(false)

      toast({
        title: "Email downloaded",
        description: "Email has been downloaded as an Outlook file",
      })
    }, 500)
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-3xl max-h-[90vh] overflow-hidden flex flex-col">
        <DialogHeader>
          <DialogTitle>Email Review</DialogTitle>
        </DialogHeader>

        <div className="flex-1 overflow-hidden flex flex-col">
          <div className="grid grid-cols-3 gap-4 mb-4">
            <div>
              <p className="text-sm font-medium mb-1">Account</p>
              <div className="flex items-center gap-2">
                <Badge variant="outline">{account?.name}</Badge>
              </div>
            </div>
            <div>
              <p className="text-sm font-medium mb-1">Opportunity</p>
              <Badge variant="outline">{opportunity?.name || "N/A"}</Badge>
            </div>
            <div>
              <p className="text-sm font-medium mb-1">Priority</p>
              <Badge
                className={
                  email.priority === "high"
                    ? "bg-red-100 text-red-800 hover:bg-red-100"
                    : email.priority === "medium"
                      ? "bg-amber-100 text-amber-800 hover:bg-amber-100"
                      : "bg-green-100 text-green-800 hover:bg-green-100"
                }
              >
                {email.priority}
              </Badge>
            </div>
          </div>

          <div className="mb-4">
            <p className="text-sm font-medium mb-1">Subject</p>
            <p className="text-base font-semibold">{email.subject}</p>
          </div>

          <div className="mb-4">
            <p className="text-sm font-medium mb-1">Recipient</p>
            <p>
              {email.recipientName} &lt;{email.recipientEmail}&gt;
            </p>
          </div>

          <Separator className="mb-4" />

          <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 overflow-hidden flex flex-col">
            <TabsList className="mb-4">
              <TabsTrigger value="preview">Preview</TabsTrigger>
              <TabsTrigger value="edit" disabled={email.status === "approved"}>
                Edit
              </TabsTrigger>
              <TabsTrigger value="export" disabled={email.status !== "approved"}>
                Export
              </TabsTrigger>
            </TabsList>

            <TabsContent value="preview" className="flex-1 overflow-auto">
              <div className="whitespace-pre-wrap">{email.body || ""}</div>
            </TabsContent>

            <TabsContent value="edit" className="flex-1 overflow-hidden flex flex-col">
              {isEditing ? (
                <Textarea
                  value={editedBody}
                  onChange={(e) => setEditedBody(e.target.value)}
                  className="flex-1 min-h-[200px] font-mono text-sm"
                />
              ) : (
                <div className="whitespace-pre-wrap flex-1 overflow-auto">{email.body || ""}</div>
              )}
            </TabsContent>

            <TabsContent value="export" className="flex-1">
              <div className="space-y-4">
                <div className="rounded-lg border p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <FileText className="h-5 w-5 text-muted-foreground" />
                      <div>
                        <p className="font-medium">Plain Text Format</p>
                        <p className="text-sm text-muted-foreground">Download as a simple text file</p>
                      </div>
                    </div>
                    <Button variant="outline" onClick={handleDownloadText} disabled={isDownloading}>
                      <Download className="h-4 w-4 mr-2" />
                      Download .txt
                    </Button>
                  </div>
                </div>

                <div className="rounded-lg border p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Mail className="h-5 w-5 text-muted-foreground" />
                      <div>
                        <p className="font-medium">Outlook Format</p>
                        <p className="text-sm text-muted-foreground">Download as an Outlook compatible file</p>
                      </div>
                    </div>
                    <Button variant="outline" onClick={handleDownloadOutlook} disabled={isDownloading}>
                      <Download className="h-4 w-4 mr-2" />
                      Download .eml
                    </Button>
                  </div>
                </div>

                <div className="rounded-lg border p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Copy className="h-5 w-5 text-muted-foreground" />
                      <div>
                        <p className="font-medium">Copy to Clipboard</p>
                        <p className="text-sm text-muted-foreground">Copy the email content to your clipboard</p>
                      </div>
                    </div>
                    <Button variant="outline" onClick={handleCopyToClipboard}>
                      <Copy className="h-4 w-4 mr-2" />
                      Copy
                    </Button>
                  </div>
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </div>

        <div className="flex justify-end gap-2 mt-4">
          <Button variant="outline" onClick={onClose}>
            Close
          </Button>
          {email.status !== "approved" && !isEditing && (
            <>
              <Button variant="outline" onClick={() => setIsEditing(true)}>
                <Save className="mr-2 h-4 w-4" />
                Edit
              </Button>
              <Button onClick={handleApprove} className="gap-2">
                <Check className="h-4 w-4" />
                Approve
              </Button>
            </>
          )}
          {isEditing && (
            <Button onClick={handleSaveEdit}>
              <Save className="mr-2 h-4 w-4" />
              Save Changes
            </Button>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}
