"use client"

import { Card, CardContent } from "@/components/ui/card"

interface EmailPreviewProps {
  subject: string
  body: string
}

export function EmailPreview({ subject, body }: EmailPreviewProps) {
  return (
    <Card className="border-dashed">
      <CardContent className="p-6">
        <div className="space-y-4">
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <div className="font-semibold text-sm">Subject:</div>
              <div>{subject}</div>
            </div>
          </div>
          <div className="border-t pt-4">
            <div className="whitespace-pre-line">{body}</div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
