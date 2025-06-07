"use client"

import type React from "react"

import { useState } from "react"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { mockAccounts } from "@/lib/mock-data"
import { Upload } from "lucide-react"

interface DocumentUploadDialogProps {
  isOpen: boolean
  onClose: () => void
  onUpload: (document: any) => void
  activeTab: string
}

export function DocumentUploadDialog({ isOpen, onClose, onUpload, activeTab }: DocumentUploadDialogProps) {
  const [file, setFile] = useState<File | null>(null)
  const [documentData, setDocumentData] = useState({
    name: "",
    description: "",
    category: "",
    accountId: "",
    isGlobal: activeTab === "global",
    aiRelevance: "medium",
    aiNotes: "",
  })
  const [isUploading, setIsUploading] = useState(false)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0]
      setFile(selectedFile)

      // Auto-fill name from filename if empty
      if (!documentData.name) {
        setDocumentData({
          ...documentData,
          name: selectedFile.name.split(".")[0], // Remove extension
        })
      }
    }
  }

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

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    if (!file) return

    setIsUploading(true)

    // In a real app, this would upload the file to a server
    setTimeout(() => {
      const fileExtension = file.name.split(".").pop() || ""

      onUpload({
        ...documentData,
        fileType: fileExtension,
        fileSize: file.size,
        uploadedAt: new Date().toISOString(),
        uploadedBy: "Current User",
      })

      // Reset form
      setFile(null)
      setDocumentData({
        name: "",
        description: "",
        category: "",
        accountId: "",
        isGlobal: activeTab === "global",
        aiRelevance: "medium",
        aiNotes: "",
      })
      setIsUploading(false)
    }, 1000)
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[550px]">
        <DialogHeader>
          <DialogTitle>Upload Document</DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="file-upload">Document File</Label>
            <div
              className="border-2 border-dashed rounded-md p-6 text-center cursor-pointer"
              onClick={() => document.getElementById("file-upload")?.click()}
            >
              <input
                id="file-upload"
                type="file"
                className="hidden"
                onChange={handleFileChange}
                accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx,.txt"
              />
              {file ? (
                <div className="space-y-1">
                  <p className="font-medium">{file.name}</p>
                  <p className="text-sm text-muted-foreground">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                </div>
              ) : (
                <div className="space-y-2">
                  <Upload className="h-8 w-8 mx-auto text-muted-foreground" />
                  <p className="text-sm font-medium">Click to upload or drag and drop</p>
                  <p className="text-xs text-muted-foreground">PDF, Word, Excel, PowerPoint, or Text files</p>
                </div>
              )}
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="name">Document Name</Label>
            <Input
              id="name"
              name="name"
              value={documentData.name}
              onChange={handleInputChange}
              placeholder="Enter document name"
              required
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
            <Select value={documentData.category} onValueChange={(value) => handleSelectChange("category", value)}>
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

          {activeTab === "account" && (
            <div className="space-y-2">
              <Label htmlFor="account">Associated Account</Label>
              <Select
                value={documentData.accountId}
                onValueChange={(value) => handleSelectChange("accountId", value)}
                required={!documentData.isGlobal}
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
              rows={3}
            />
          </div>

          <div className="flex justify-end gap-2 pt-4">
            <Button type="button" variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" disabled={!file || isUploading}>
              {isUploading ? "Uploading..." : "Upload Document"}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  )
}
