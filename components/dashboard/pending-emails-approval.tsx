import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Check, X } from "lucide-react"
import Link from "next/link"

export function PendingEmailsApproval() {
  // Mock data for pending emails
  const pendingEmails = [
    {
      id: "email-1",
      subject: "Proposal Follow-up: Next Steps",
      recipient: "john.doe@acmecorp.com",
      timestamp: "2 hours ago",
      preview:
        "Thank you for your time during our meeting yesterday. As discussed, I'm sending over the additional information...",
    },
    {
      id: "email-2",
      subject: "Product Demo Invitation",
      recipient: "sarah.smith@techgiant.com",
      timestamp: "Yesterday",
      preview:
        "I'd like to invite you to an exclusive demonstration of our latest features that address the challenges we discussed...",
    },
    {
      id: "email-3",
      subject: "Quarterly Business Review",
      recipient: "michael.johnson@nextgen.com",
      timestamp: "3 days ago",
      preview:
        "As we approach the end of the quarter, I'd like to schedule our quarterly business review to discuss our progress...",
    },
  ]

  return (
    <Card className="h-[400px]">
      <CardHeader>
        <CardTitle>Pending Email Approvals</CardTitle>
        <CardDescription>AI-generated emails awaiting your review</CardDescription>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[300px] pr-4">
          <div className="space-y-4">
            {pendingEmails.map((email) => (
              <div key={email.id} className="rounded-lg border p-3">
                <div className="flex items-center justify-between">
                  <h4 className="font-medium">{email.subject}</h4>
                  <span className="text-xs text-muted-foreground">{email.timestamp}</span>
                </div>
                <p className="mt-1 text-xs text-muted-foreground">To: {email.recipient}</p>
                <p className="mt-2 text-sm line-clamp-2">{email.preview}</p>
                <div className="mt-3 flex items-center justify-between">
                  <Button variant="outline" size="sm" asChild>
                    <Link href={`/emails/${email.id}`}>View</Link>
                  </Button>
                  <div className="flex space-x-2">
                    <Button variant="outline" size="icon" className="h-8 w-8">
                      <X className="h-4 w-4" />
                      <span className="sr-only">Reject</span>
                    </Button>
                    <Button variant="outline" size="icon" className="h-8 w-8">
                      <Check className="h-4 w-4" />
                      <span className="sr-only">Approve</span>
                    </Button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  )
}
