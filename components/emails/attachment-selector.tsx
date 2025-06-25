"use client"

import { useState } from "react"
import { Check, File, FileText, Info, Upload } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox"
import { Label } from "@/components/ui/label"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { cn } from "@/lib/utils"
import { FileUpload, type UploadedFileInfo } from "@/components/ui/file-upload"

export interface Attachment {
  id: string
  name: string
  type: string
  size: string
  date: string
  description: string
}

export const availableAttachments: Attachment[] = [
  {
    id: "gartner-dxp",
    name: "Q1 2025 Gartner Magic Quadrant for Digital Experience Platforms (DXP)",
    type: "PDF",
    size: "3.2 MB",
    date: "2025-01-15",
    description: "Latest Gartner analysis of DXP vendors, positioning our company as a Leader.",
  },
  {
    id: "gartner-personalization",
    name: "Q1 2025 Gartner Magic Quadrant for Personalization Engines",
    type: "PDF",
    size: "2.8 MB",
    date: "2025-01-22",
    description:
      "Comprehensive analysis of personalization engine vendors, highlighting our strengths in AI-driven personalization.",
  },
  {
    id: "gartner-cmp",
    name: "Q1 2025 Gartner Magic Quadrant for Content Marketing Platforms (CMP)",
    type: "PDF",
    size: "2.5 MB",
    date: "2025-01-30",
    description: "Evaluation of content marketing platforms, showcasing our improved position from last year.",
  },
  {
    id: "forrester-cms",
    name: "Q1 2025 Forrester Wave for CMS",
    type: "PDF",
    size: "4.1 MB",
    date: "2025-02-10",
    description: "Forrester's analysis of CMS vendors, highlighting our platform's content management capabilities.",
  },
  {
    id: "forrester-optimization",
    name: "Q4 2024 Forrester Wave for Experience Optimization Solutions",
    type: "PDF",
    size: "3.7 MB",
    date: "2024-11-28",
    description: "Detailed evaluation of experience optimization solutions, where we're recognized for innovation.",
  },
]

interface AttachmentSelectorProps {
  selectedAttachments: string[]
  uploadedFiles: UploadedFileInfo[]
  onAttachmentChange: (attachments: string[]) => void
  onUploadedFilesChange: (files: UploadedFileInfo[]) => void
}

export function AttachmentSelector({
  selectedAttachments,
  uploadedFiles,
  onAttachmentChange,
  onUploadedFilesChange,
}: AttachmentSelectorProps) {
  const [expandedAttachment, setExpandedAttachment] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<string>("library")

  const toggleAttachment = (id: string) => {
    if (selectedAttachments.includes(id)) {
      onAttachmentChange(selectedAttachments.filter((attachmentId) => attachmentId !== id))
    } else {
      onAttachmentChange([...selectedAttachments, id])
    }
  }

  const toggleExpandAttachment = (id: string) => {
    setExpandedAttachment(expandedAttachment === id ? null : id)
  }

  const handleFilesSelected = (files: UploadedFileInfo[]) => {
    onUploadedFilesChange(files)
  }

  const totalSelectedCount = selectedAttachments.length + uploadedFiles.length

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-medium">Attachments</h3>
        {totalSelectedCount > 0 && (
          <Badge variant="outline" className="ml-2">
            {totalSelectedCount} selected
          </Badge>
        )}
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="library">Document Library</TabsTrigger>
          <TabsTrigger value="upload">Upload Files</TabsTrigger>
        </TabsList>

        <TabsContent value="library" className="space-y-4">
          <div className="space-y-3">
            {availableAttachments.map((attachment) => (
              <Card
                key={attachment.id}
                className={cn(
                  "border transition-colors",
                  selectedAttachments.includes(attachment.id) ? "border-primary bg-primary/5" : "border-border",
                )}
              >
                <CardContent className="p-4">
                  <div className="flex items-start gap-3">
                    <Checkbox
                      id={`attachment-${attachment.id}`}
                      checked={selectedAttachments.includes(attachment.id)}
                      onCheckedChange={() => toggleAttachment(attachment.id)}
                      className="mt-1"
                    />

                    <div className="flex-1 space-y-1">
                      <div className="flex items-start justify-between">
                        <Label htmlFor={`attachment-${attachment.id}`} className="font-medium cursor-pointer">
                          {attachment.name}
                        </Label>

                        <div className="flex items-center gap-2">
                          <Badge variant="outline" className="ml-2">
                            {attachment.type}
                          </Badge>
                          <Badge variant="outline" className="ml-2">
                            {attachment.size}
                          </Badge>
                          <TooltipProvider>
                            <Tooltip>
                              <TooltipTrigger asChild>
                                <Button
                                  variant="ghost"
                                  size="icon"
                                  className="h-8 w-8"
                                  onClick={() => toggleExpandAttachment(attachment.id)}
                                >
                                  <Info className="h-4 w-4" />
                                  <span className="sr-only">View details</span>
                                </Button>
                              </TooltipTrigger>
                              <TooltipContent>
                                <p>View attachment details</p>
                              </TooltipContent>
                            </Tooltip>
                          </TooltipProvider>
                        </div>
                      </div>

                      {expandedAttachment === attachment.id && (
                        <div className="mt-2 text-sm text-muted-foreground">
                          <p>{attachment.description}</p>
                          <p className="mt-1">Published: {new Date(attachment.date).toLocaleDateString()}</p>
                        </div>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="upload" className="space-y-4">
          <FileUpload
            onFilesSelected={handleFilesSelected}
            maxFiles={5}
            maxSizeMB={10}
            acceptedFileTypes={[".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"]}
          />
        </TabsContent>
      </Tabs>

      {totalSelectedCount > 0 && (
        <div className="mt-4 p-4 border rounded-md bg-muted/30">
          <h4 className="font-medium mb-2">Selected Attachments ({totalSelectedCount})</h4>
          <ul className="space-y-2">
            {selectedAttachments.map((id) => {
              const attachment = availableAttachments.find((a) => a.id === id)
              return attachment ? (
                <li key={id} className="flex items-center gap-2">
                  <Check className="h-4 w-4 text-primary" />
                  <FileText className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm">{attachment.name}</span>
                </li>
              ) : null
            })}
            {uploadedFiles.map((file) => (
              <li key={file.id} className="flex items-center gap-2">
                <Check className="h-4 w-4 text-primary" />
                <Upload className="h-4 w-4 text-muted-foreground" />
                <span className="text-sm">{file.name}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export function SelectedAttachmentsList({
  attachmentIds = [],
  uploadedFiles = [],
}: {
  attachmentIds?: string[]
  uploadedFiles?: UploadedFileInfo[]
}) {
  // Ensure we have arrays even if undefined is passed
  const safeAttachmentIds = attachmentIds || []
  const safeUploadedFiles = uploadedFiles || []

  if (safeAttachmentIds.length === 0 && safeUploadedFiles.length === 0) return null

  return (
    <div className="space-y-2">
      <h4 className="text-sm font-medium">Attachments</h4>
      <ul className="space-y-1">
        {safeAttachmentIds.map((id) => {
          const attachment = availableAttachments.find((a) => a.id === id)
          return attachment ? (
            <li key={id} className="flex items-center gap-2 text-sm">
              <File className="h-4 w-4 text-muted-foreground" />
              <span>{attachment.name}</span>
              <Badge variant="outline" className="ml-auto">
                {attachment.type}
              </Badge>
            </li>
          ) : null
        })}
        {safeUploadedFiles.map((file) => (
          <li key={file.id} className="flex items-center gap-2 text-sm">
            <File className="h-4 w-4 text-muted-foreground" />
            <span>{file.name}</span>
            <Badge variant="outline" className="ml-auto">
              {file.type.toUpperCase()}
            </Badge>
          </li>
        ))}
      </ul>
    </div>
  )
}
