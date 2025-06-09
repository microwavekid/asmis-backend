"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { DocumentDetailDialog } from "./document-detail-dialog"
import { mockAccounts } from "@/lib/mock-data"
import { Download, Eye, FileText, MoreHorizontal, Trash2 } from "lucide-react"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { formatDistanceToNow } from "date-fns"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

interface DocumentsListProps {
  documents: any[]
  onDelete: (documentId: string) => void
  onUpdate: (updatedDocument: any) => void
}

export function DocumentsList({ documents, onDelete, onUpdate }: DocumentsListProps) {
  const [selectedDocument, setSelectedDocument] = useState<any | null>(null)
  const [isDetailOpen, setIsDetailOpen] = useState(false)

  const handleViewDocument = (document: any) => {
    setSelectedDocument(document)
    setIsDetailOpen(true)
  }

  const handleDownload = (document: any) => {
    // In a real app, this would download the actual file
    alert(`Downloading ${document.name}`)
  }

  const getFileIcon = (fileType: string) => {
    switch (fileType.toLowerCase()) {
      case "pdf":
        return <FileText className="h-5 w-5 text-red-500" />
      case "doc":
      case "docx":
        return <FileText className="h-5 w-5 text-blue-500" />
      case "xls":
      case "xlsx":
        return <FileText className="h-5 w-5 text-green-500" />
      case "ppt":
      case "pptx":
        return <FileText className="h-5 w-5 text-orange-500" />
      default:
        return <FileText className="h-5 w-5 text-gray-500" />
    }
  }

  const getAccountName = (accountId: string) => {
    const account = mockAccounts.find((a) => a.id === accountId)
    return account ? account.name : "Unknown Account"
  }

  if (documents.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-center">
        <FileText className="h-12 w-12 text-muted-foreground mb-4" />
        <h3 className="text-lg font-medium">No documents found</h3>
        <p className="text-muted-foreground mt-2">Upload documents to provide context to the AI agent system.</p>
      </div>
    )
  }

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[300px]">Document</TableHead>
            <TableHead>Category</TableHead>
            <TableHead>AI Relevance</TableHead>
            {!documents.some((doc) => doc.isGlobal) && <TableHead>Account</TableHead>}
            <TableHead>Uploaded</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {documents.map((document) => (
            <TableRow key={document.id}>
              <TableCell>
                <div className="flex items-center gap-2">
                  {getFileIcon(document.fileType)}
                  <div>
                    <div className="font-medium">{document.name}</div>
                    <div className="text-xs text-muted-foreground truncate max-w-[250px]">{document.description}</div>
                    <div className="text-xs text-muted-foreground mt-1">
                      {document.fileType.toUpperCase()} · {(document.fileSize / 1024 / 1024).toFixed(2)} MB
                    </div>
                  </div>
                </div>
              </TableCell>
              <TableCell>
                <Badge variant="outline">{document.category}</Badge>
              </TableCell>
              <TableCell>
                <Badge
                  className={
                    document.aiRelevance === "high"
                      ? "bg-green-100 text-green-800 hover:bg-green-100"
                      : document.aiRelevance === "medium"
                        ? "bg-blue-100 text-blue-800 hover:bg-blue-100"
                        : "bg-gray-100 text-gray-800 hover:bg-gray-100"
                  }
                >
                  {document.aiRelevance}
                </Badge>
              </TableCell>
              {!documents.some((doc) => doc.isGlobal) && (
                <TableCell>{document.isGlobal ? "Global" : getAccountName(document.accountId)}</TableCell>
              )}
              <TableCell>
                <div className="text-sm">{formatDistanceToNow(new Date(document.uploadedAt), { addSuffix: true })}</div>
                <div className="text-xs text-muted-foreground">by {document.uploadedBy}</div>
              </TableCell>
              <TableCell className="text-right">
                <div className="flex justify-end gap-2">
                  <Button variant="ghost" size="icon" onClick={() => handleViewDocument(document)}>
                    <Eye className="h-4 w-4" />
                    <span className="sr-only">View</span>
                  </Button>
                  <Button variant="ghost" size="icon" onClick={() => handleDownload(document)}>
                    <Download className="h-4 w-4" />
                    <span className="sr-only">Download</span>
                  </Button>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" size="icon">
                        <MoreHorizontal className="h-4 w-4" />
                        <span className="sr-only">More options</span>
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem onClick={() => handleViewDocument(document)}>
                        <Eye className="mr-2 h-4 w-4" />
                        View Details
                      </DropdownMenuItem>
                      <DropdownMenuItem onClick={() => handleDownload(document)}>
                        <Download className="mr-2 h-4 w-4" />
                        Download
                      </DropdownMenuItem>
                      <DropdownMenuItem onClick={() => onDelete(document.id)} className="text-destructive">
                        <Trash2 className="mr-2 h-4 w-4" />
                        Delete
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      {selectedDocument && (
        <DocumentDetailDialog
          document={selectedDocument}
          isOpen={isDetailOpen}
          onClose={() => setIsDetailOpen(false)}
          onUpdate={onUpdate}
        />
      )}
    </div>
  )
}
