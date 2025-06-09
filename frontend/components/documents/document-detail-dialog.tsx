"use client"

import type React from "react"

import { useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { mockAccounts } from "@/lib/mock-data"
import { Download, FileText } from "lucide-react"
import { format } from "date-fns"

interface DocumentDetailDialogProps {
  document: any
  isOpen: boolean
  onClose: () => void
  onUpdate: (updatedDocument: any) => void
}

export function DocumentDetailDialog({ document, isOpen, onClose, onUpdate }: DocumentDetailDialogProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [documentData, setDocumentData] = useState({
    ...document,
  })

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setDocumentData({
      ...documentData,
      [name]: value,
    })
  }

  const handleSelectChange = (name: string, value: string) => {
    setDocumentData({
      ...documentData,
      [name]: value,
    })
  }

  const handleSave = () => {
    onUpdate(documentData)
    setIsEditing(false)
  }

  const getFileIcon = (fileType: string) => {
    switch (fileType.toLowerCase()) {
      case "pdf":
        return <FileText className="h-12 w-12 text-red-500" />
      case "doc":
      case "docx":
        return <FileText className="h-12 w-12 text-blue-500" />
      case "xls":
      case "xlsx":
        return <FileText className="h-12 w-12 text-green-500" />
      case "ppt":
      case "pptx":
        return <FileText className="h-12 w-12 text-orange-500" />
      default:
        return <FileText className="h-12 w-12 text-gray-500" />
    }
  }

  const getAccountName = (accountId: string) => {
    const account = mockAccounts.find((a) => a.id === accountId)
    return account ? account.name : "Unknown Account"
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[650px]">
        <DialogHeader>
          <DialogTitle>Document Details</DialogTitle>
        </DialogHeader>

        <Tabs defaultValue="details">
          <TabsList className="mb-4">
            <TabsTrigger value="details">Details</TabsTrigger>
            <TabsTrigger value="preview">Preview</TabsTrigger>
            <TabsTrigger value="ai-context">AI Context</TabsTrigger>
          </TabsList>

          <TabsContent value="details" className="space-y-4">
            {isEditing ? (
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="name">Document Name</Label>
                  <Input
                    id="name"
                    name="name"
                    value={documentData.name}
                    onChange={handleInputChange}
                    placeholder="Enter document name"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="description">Description</Label>
                  <Textarea
                    id="description"
                    name="description"
                    value={documentData.description}
                    onChange={handleInputChange}
                    placeholder="Brief description of the document"
                    rows={3}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="category">Category</Label>
                  <Select
                    value={documentData.category}
                    onValueChange={(value) => handleSelectChange("category", value)}
                  >
                    <SelectTrigger id="category">
                      <SelectValue placeholder="Select category" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="product">Product Information</SelectItem>
                      <SelectItem value="case-study">Case Study</SelectItem>
                      <SelectItem value="technical">Technical Documentation</SelectItem>
                      <SelectItem value="contract">Contract</SelectItem>
                      <SelectItem value="proposal">Proposal</SelectItem>
                      <SelectItem value="presentation">Presentation</SelectItem>
                      <SelectItem value="other">Other</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {!document.isGlobal && (
                  <div className="space-y-2">
                    <Label htmlFor="account">Associated Account</Label>
                    <Select
                      value={documentData.accountId}
                      onValueChange={(value) => handleSelectChange("accountId", value)}
                    >
                      <SelectTrigger id="account">
                        <SelectValue placeholder="Select account" />
                      </SelectTrigger>
                      <SelectContent>
                        {mockAccounts.map((account) => (
                          <SelectItem key={account.id} value={account.id}>
                            {account.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                )}
              </div>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center gap-4">
                  {getFileIcon(document.fileType)}
                  <div>
                    <h3 className="text-lg font-medium">{document.name}</h3>
                    <p className="text-sm text-muted-foreground">
                      {document.fileType.toUpperCase()} · {(document.fileSize / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm font-medium">Category</p>
                    <Badge variant="outline" className="mt-1">
                      {document.category}
                    </Badge>
                  </div>
                  <div>
                    <p className="text-sm font-medium">Uploaded</p>
                    <p className="text-sm mt-1">
                      {format(new Date(document.uploadedAt), "PPP")} by {document.uploadedBy}
                    </p>
                  </div>
                  {!document.isGlobal && (
                    <div>
                      <p className="text-sm font-medium">Associated Account</p>
                      <p className="text-sm mt-1">{getAccountName(document.accountId)}</p>
                    </div>
                  )}
                  <div>
                    <p className="text-sm font-medium">Document Type</p>
                    <p className="text-sm mt-1">
                      {document.isGlobal ? "Global Optimizely Document" : "Account-Specific Document"}
                    </p>
                  </div>
                </div>

                <div>
                  <p className="text-sm font-medium">Description</p>
                  <p className="text-sm mt-1">{document.description || "No description provided."}</p>
                </div>
              </div>
            )}
          </TabsContent>

          <TabsContent value="preview" className="min-h-[300px] flex flex-col items-center justify-center">
            <FileText className="h-16 w-16 text-muted-foreground mb-4" />
            <h3 className="text-lg font-medium">Document Preview</h3>
            <p className="text-sm text-muted-foreground mb-4">
              Preview not available. Download the document to view its contents.
            </p>
            <Button variant="outline" onClick={() => alert(`Downloading ${document.name}`)}>
              <Download className="mr-2 h-4 w-4" />
              Download
            </Button>
          </TabsContent>

          <TabsContent value="ai-context" className="space-y-4">
            {isEditing ? (
              <div className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="ai-relevance">AI Relevance</Label>
                  <Select
                    value={documentData.aiRelevance}
                    onValueChange={(value) => handleSelectChange("aiRelevance", value)}
                  >
                    <SelectTrigger id="ai-relevance">
                      <SelectValue placeholder="Select relevance" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="high">High - Critical for AI context</SelectItem>
                      <SelectItem value="medium">Medium - Important reference</SelectItem>
                      <SelectItem value="low">Low - Background information</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="ai-notes">Notes for AI</Label>
                  <Textarea
                    id="ai-notes"
                    name="aiNotes"
                    value={documentData.aiNotes}
                    onChange={handleInputChange}
                    placeholder="Special instructions for how the AI should use this document"
                    rows={5}
                  />
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <div>
                  <p className="text-sm font-medium">AI Relevance</p>
                  <Badge
                    className={
                      document.aiRelevance === "high"
                        ? "bg-green-100 text-green-800 hover:bg-green-100 mt-1"
                        : document.aiRelevance === "medium"
                          ? "bg-blue-100 text-blue-800 hover:bg-blue-100 mt-1"
                          : "bg-gray-100 text-gray-800 hover:bg-gray-100 mt-1"
                    }
                  >
                    {document.aiRelevance === "high"
                      ? "High - Critical for AI context"
                      : document.aiRelevance === "medium"
                        ? "Medium - Important reference"
                        : "Low - Background information"}
                  </Badge>
                </div>

                <div>
                  <p className="text-sm font-medium">Notes for AI</p>
                  <p className="text-sm mt-1 whitespace-pre-wrap">
                    {document.aiNotes || "No special instructions provided for the AI."}
                  </p>
                </div>
              </div>
            )}
          </TabsContent>
        </Tabs>

        <div className="flex justify-end gap-2 pt-4">
          {isEditing ? (
            <>
              <Button variant="outline" onClick={() => setIsEditing(false)}>
                Cancel
              </Button>
              <Button onClick={handleSave}>Save Changes</Button>
            </>
          ) : (
            <>
              <Button variant="outline" onClick={onClose}>
                Close
              </Button>
              <Button onClick={() => setIsEditing(true)}>Edit</Button>
            </>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}
