"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Check, Copy, X } from "lucide-react"

export default function UploadDocumentsPage() {
  const [uploadedFiles, setUploadedFiles] = useState<Record<string, string>>({})
  const [uploading, setUploading] = useState(false)
  const [copied, setCopied] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const documentTypes = [
    {
      id: "gartner-dxp",
      name: "Q1 2025 Gartner Magic Quadrant for Digital Experience Platforms (DXP)",
      filename: "Q1-2025-Gartner-Magic-Quadrant-DXP.pdf",
    },
    {
      id: "gartner-personalization",
      name: "Q1 2025 Gartner Magic Quadrant for Personalization Engines",
      filename: "Q1-2025-Gartner-Magic-Quadrant-Personalization.pdf",
    },
    {
      id: "gartner-cmp",
      name: "Q1 2025 Gartner Magic Quadrant for Content Marketing Platforms (CMP)",
      filename: "Q1-2025-Gartner-Magic-Quadrant-CMP.pdf",
    },
    {
      id: "forrester-cms",
      name: "Q1 2025 Forrester Wave for CMS",
      filename: "Q1-2025-Forrester-Wave-CMS.pdf",
    },
    {
      id: "forrester-optimization",
      name: "Q4 2024 Forrester Wave for Experience Optimization Solutions",
      filename: "Q4-2024-Forrester-Wave-Optimization.pdf",
    },
  ]

  const handleFileUpload = async (documentId: string, file: File) => {
    try {
      setUploading(true)
      setError(null)

      const formData = new FormData()
      formData.append("file", file)

      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || "Failed to upload file")
      }

      const data = await response.json()

      setUploadedFiles((prev) => ({
        ...prev,
        [documentId]: data.url,
      }))
    } catch (err) {
      console.error("Error uploading file:", err)
      setError((err as Error).message || "Failed to upload file")
    } finally {
      setUploading(false)
    }
  }

  const generateDocumentMap = () => {
    const documentMap: Record<string, { url: string; filename: string }> = {}

    for (const doc of documentTypes) {
      if (uploadedFiles[doc.id]) {
        documentMap[doc.id] = {
          url: uploadedFiles[doc.id],
          filename: doc.filename,
        }
      }
    }

    return JSON.stringify(documentMap, null, 2)
  }

  const copyToClipboard = () => {
    navigator.clipboard.writeText(generateDocumentMap())
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="container mx-auto py-10">
      <Card className="max-w-4xl mx-auto">
        <CardHeader>
          <CardTitle>Upload Document Library Files</CardTitle>
          <CardDescription>
            Upload your PDF files for the document library. These files will be stored in Vercel Blob and used for email
            attachments.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="upload">
            <TabsList className="mb-4">
              <TabsTrigger value="upload">Upload Files</TabsTrigger>
              <TabsTrigger value="code">Generated Code</TabsTrigger>
            </TabsList>
            <TabsContent value="upload">
              <div className="space-y-6">
                {error && (
                  <Alert variant="destructive">
                    <AlertTitle>Error</AlertTitle>
                    <AlertDescription>{error}</AlertDescription>
                  </Alert>
                )}

                {documentTypes.map((doc) => (
                  <div key={doc.id} className="border rounded-lg p-4">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h3 className="font-medium">{doc.name}</h3>
                        <p className="text-sm text-muted-foreground">{doc.filename}</p>
                      </div>
                      {uploadedFiles[doc.id] && (
                        <div className="flex items-center text-green-600">
                          <Check className="h-4 w-4 mr-1" />
                          <span className="text-sm">Uploaded</span>
                        </div>
                      )}
                    </div>

                    <div className="flex items-center gap-4">
                      <div className="grid w-full max-w-sm items-center gap-1.5">
                        <Label htmlFor={`file-${doc.id}`}>Select PDF file</Label>
                        <Input
                          id={`file-${doc.id}`}
                          type="file"
                          accept=".pdf"
                          disabled={uploading || !!uploadedFiles[doc.id]}
                          onChange={(e) => {
                            const file = e.target.files?.[0]
                            if (file) {
                              handleFileUpload(doc.id, file)
                            }
                          }}
                        />
                      </div>

                      {uploadedFiles[doc.id] && (
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => {
                            setUploadedFiles((prev) => {
                              const newFiles = { ...prev }
                              delete newFiles[doc.id]
                              return newFiles
                            })
                          }}
                        >
                          <X className="h-4 w-4 mr-1" />
                          Remove
                        </Button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </TabsContent>
            <TabsContent value="code">
              <div className="space-y-4">
                <div className="bg-muted p-4 rounded-md">
                  <div className="flex justify-between items-center mb-2">
                    <h3 className="font-medium">Document Map for document-actions.ts</h3>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={copyToClipboard}
                      disabled={Object.keys(uploadedFiles).length === 0}
                    >
                      {copied ? (
                        <>
                          <Check className="h-4 w-4 mr-1" />
                          Copied!
                        </>
                      ) : (
                        <>
                          <Copy className="h-4 w-4 mr-1" />
                          Copy
                        </>
                      )}
                    </Button>
                  </div>
                  <pre className="text-xs overflow-auto p-2 bg-background rounded border">{generateDocumentMap()}</pre>
                </div>

                <div className="bg-muted p-4 rounded-md">
                  <h3 className="font-medium mb-2">Instructions</h3>
                  <ol className="list-decimal list-inside space-y-2 text-sm">
                    <li>Upload all your PDF files using the "Upload Files" tab</li>
                    <li>Switch to this "Generated Code" tab</li>
                    <li>Copy the generated JSON object</li>
                    <li>
                      Replace the <code>documentMap</code> in <code>lib/actions/document-actions.ts</code>
                    </li>
                    <li>Deploy your changes to Vercel</li>
                  </ol>
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
        <CardFooter className="flex justify-between">
          <div className="text-sm text-muted-foreground">
            {Object.keys(uploadedFiles).length} of {documentTypes.length} files uploaded
          </div>
          <Button onClick={() => (window.location.href = "/emails/executive-generator")} variant="outline">
            Go to Email Generator
          </Button>
        </CardFooter>
      </Card>
    </div>
  )
}
