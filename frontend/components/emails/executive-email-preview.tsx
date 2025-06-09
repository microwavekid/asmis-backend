import { CardContent, CardHeader, CardTitle, Card } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { SelectedAttachmentsList } from "./attachment-selector"

interface ExecutiveEmailPreviewProps {
  emailContent: string
  subject: string
  executiveSender: string
  recipientName: string
  recipientEmail: string
  attachmentIds?: string[]
}

export function ExecutiveEmailPreview({
  emailContent,
  subject,
  executiveSender,
  recipientName,
  recipientEmail,
  attachmentIds = [],
}: ExecutiveEmailPreviewProps) {
  return (
    <Card className="w-[700px]">
      <CardHeader>
        <CardTitle>Email Preview</CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <div className="flex items-center space-x-4">
          <Avatar>
            <AvatarImage src="https://github.com/shadcn.png" />
            <AvatarFallback>CN</AvatarFallback>
          </Avatar>
          <div>
            <p className="text-sm font-medium leading-none">{executiveSender}</p>
            <p className="text-sm text-muted-foreground">{recipientEmail}</p>
          </div>
        </div>
        <div>
          <p className="text-sm font-medium leading-none">Subject: {subject}</p>
        </div>
        <div>
          <p className="text-sm text-muted-foreground">Dear {recipientName},</p>
          <p className="text-sm text-muted-foreground">{emailContent}</p>
        </div>
        {attachmentIds && attachmentIds.length > 0 && (
          <div className="mt-4 border-t pt-4">
            <SelectedAttachmentsList attachmentIds={attachmentIds} />
          </div>
        )}
      </CardContent>
    </Card>
  )
}
