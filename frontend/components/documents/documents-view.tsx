"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { DocumentsList } from "./documents-list"
import { DocumentUploadDialog } from "./document-upload-dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { mockAccounts } from "@/lib/mock-data"
import { Plus, Search, SortAsc } from "lucide-react"
import { mockDocuments } from "@/lib/mock-documents"

export function DocumentsView() {
  const [selectedAccount, setSelectedAccount] = useState<string>("all")
  const [searchQuery, setSearchQuery] = useState("")
  const [isUploadDialogOpen, setIsUploadDialogOpen] = useState(false)
  const [documents, setDocuments] = useState(mockDocuments)
  const [activeTab, setActiveTab] = useState("account")
  const [sortBy, setSortBy] = useState("name")

  // Filter documents based on selected account and search query
  const filteredDocuments = documents
    .filter((doc) => {
      // Filter by account
      if (activeTab === "account") {
        if (selectedAccount !== "all" && doc.accountId !== selectedAccount) {
          return false
        }
        if (doc.isGlobal) {
          return false
        }
      } else {
        // In global tab, only show global documents
        if (!doc.isGlobal) {
          return false
        }
      }

      // Filter by search query
      if (searchQuery) {
        const query = searchQuery.toLowerCase()
        return (
          doc.name.toLowerCase().includes(query) ||
          doc.description.toLowerCase().includes(query) ||
          doc.category.toLowerCase().includes(query)
        )
      }

      return true
    })
    .sort((a, b) => {
      // Sort documents
      switch (sortBy) {
        case "name":
          return a.name.localeCompare(b.name)
        case "date":
          return new Date(b.uploadedAt).getTime() - new Date(a.uploadedAt).getTime()
        case "size":
          return b.fileSize - a.fileSize
        case "relevance":
          const relevanceOrder = { high: 0, medium: 1, low: 2 }
          return (
            relevanceOrder[a.aiRelevance as keyof typeof relevanceOrder] -
            relevanceOrder[b.aiRelevance as keyof typeof relevanceOrder]
          )
        default:
          return 0
      }
    })

  const handleDocumentUpload = (newDocument: any) => {
    setDocuments([...documents, { ...newDocument, id: `doc-${documents.length + 1}` }])
    setIsUploadDialogOpen(false)
  }

  const handleDocumentDelete = (documentId: string) => {
    setDocuments(documents.filter((doc) => doc.id !== documentId))
  }

  const handleDocumentUpdate = (updatedDocument: any) => {
    setDocuments(documents.map((doc) => (doc.id === updatedDocument.id ? { ...doc, ...updatedDocument } : doc)))
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Documents Repository</h1>
        <Button onClick={() => setIsUploadDialogOpen(true)}>
          <Plus className="mr-2 h-4 w-4" />
          Upload Document
        </Button>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <div className="flex justify-between items-center mb-4">
          <TabsList>
            <TabsTrigger value="account">Account Documents</TabsTrigger>
            <TabsTrigger value="global">Global Optimizely Documents</TabsTrigger>
          </TabsList>
        </div>

        <div className="flex flex-wrap items-center gap-4 mb-6">
          <div className="relative flex-1 min-w-[200px]">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              type="search"
              placeholder="Search documents..."
              className="pl-8"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          {activeTab === "account" && (
            <Select value={selectedAccount} onValueChange={setSelectedAccount}>
              <SelectTrigger className="w-[200px]">
                <SelectValue placeholder="Select account" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Accounts</SelectItem>
                {mockAccounts.map((account) => (
                  <SelectItem key={account.id} value={account.id}>
                    {account.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          )}

          <Select value={sortBy} onValueChange={setSortBy}>
            <SelectTrigger className="w-[180px]">
              <SortAsc className="mr-2 h-4 w-4" />
              <SelectValue placeholder="Sort by" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="name">Name (A-Z)</SelectItem>
              <SelectItem value="date">Date (Newest)</SelectItem>
              <SelectItem value="size">Size (Largest)</SelectItem>
              <SelectItem value="relevance">AI Relevance</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <TabsContent value="account" className="space-y-4">
          <DocumentsList
            documents={filteredDocuments}
            onDelete={handleDocumentDelete}
            onUpdate={handleDocumentUpdate}
          />
        </TabsContent>

        <TabsContent value="global" className="space-y-4">
          <DocumentsList
            documents={filteredDocuments}
            onDelete={handleDocumentDelete}
            onUpdate={handleDocumentUpdate}
          />
        </TabsContent>
      </Tabs>

      <DocumentUploadDialog
        isOpen={isUploadDialogOpen}
        onClose={() => setIsUploadDialogOpen(false)}
        onUpload={handleDocumentUpload}
        activeTab={activeTab}
      />
    </div>
  )
}
