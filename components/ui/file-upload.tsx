"use client"

import type React from "react"

import { useState, useRef } from "react"
import { Upload, X, FileIcon, Check, AlertCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { cn } from "@/lib/utils"

export interface UploadedFileInfo {
  id: string
  name: string
  type: string
  size: string
  url: string
}

export interface FileUploadProps {
  onFilesSelected: (files: UploadedFileInfo[]) => void
  maxFiles?: number
  maxSizeMB?: number
  acceptedFileTypes?: string[]
  className?: string
}

export function FileUpload({
  onFilesSelected,
  maxFiles = 5,
  maxSizeMB = 10,
  acceptedFileTypes = [".pdf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"],
  className,
}: FileUploadProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [uploadProgress, setUploadProgress] = useState<Record<string, number>>({})
  const [uploadErrors, setUploadErrors] = useState<Record<string, string>>({})
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFileInfo[]>([])
  const [isUploading, setIsUploading] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const maxSizeBytes = maxSizeMB * 1024 * 1024

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }

  const validateFile = (file: File): string | null => {
    // Check file size
    if (file.size > maxSizeBytes) {
      return `File size exceeds ${maxSizeMB}MB limit`
    }

    // Check file type
    const fileExtension = `.${file.name.split(".").pop()?.toLowerCase()}`
    if (acceptedFileTypes.length > 0 && !acceptedFileTypes.includes(fileExtension)) {
      return `File type not supported. Accepted types: ${acceptedFileTypes.join(", ")}`
    }

    return null
  }

  const simulateUpload = (file: File): Promise<UploadedFileInfo> => {
    return new Promise((resolve) => {
      let progress = 0
      const interval = setInterval(() => {
        progress += Math.floor(Math.random() * 10) + 5
        setUploadProgress((prev) => ({ ...prev, [file.name]: progress }))

        if (progress >= 100) {
          clearInterval(interval)

          // Create a placeholder URL for the file
          const fileType = file.name.split(".").pop()?.toLowerCase() || "file"
          const placeholderUrl = `/placeholder.svg?height=800&width=600&query=Uploaded ${fileType.toUpperCase()}: ${file.name}`

          resolve({
            id: `upload-${Date.now()}-${file.name.replace(/\s+/g, "-")}`,
            name: file.name,
            type: fileType.toUpperCase(),
            size: `${(file.size / (1024 * 1024)).toFixed(1)} MB`,
            url: placeholderUrl,
          })
        }
      }, 200)
    })
  }

  const processFiles = async (files: FileList | null) => {
    if (!files) return

    const newErrors: Record<string, string> = {}
    const newProgress: Record<string, number> = {}

    // Check if adding these files would exceed the max files limit
    if (uploadedFiles.length + files.length > maxFiles) {
      alert(`You can only upload a maximum of ${maxFiles} files`)
      return
    }

    setIsUploading(true)

    const filesToUpload: File[] = []
    Array.from(files).forEach((file) => {
      const error = validateFile(file)
      if (error) {
        newErrors[file.name] = error
      } else {
        filesToUpload.push(file)
        newProgress[file.name] = 0
      }
    })

    setUploadErrors({ ...uploadErrors, ...newErrors })
    setUploadProgress({ ...uploadProgress, ...newProgress })

    // Upload files one by one
    const uploadedFileInfos: UploadedFileInfo[] = []
    for (const file of filesToUpload) {
      try {
        const fileInfo = await simulateUpload(file)
        uploadedFileInfos.push(fileInfo)
      } catch (error) {
        console.error("Error uploading file:", error)
        newErrors[file.name] = "Failed to upload file"
      }
    }

    const updatedFiles = [...uploadedFiles, ...uploadedFileInfos]
    setUploadedFiles(updatedFiles)
    onFilesSelected(updatedFiles)
    setIsUploading(false)
  }

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
    processFiles(e.dataTransfer.files)
  }

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    processFiles(e.target.files)
    // Reset the input value so the same file can be uploaded again if removed
    if (fileInputRef.current) {
      fileInputRef.current.value = ""
    }
  }

  const handleRemoveFile = (file: UploadedFileInfo) => {
    const newUploadedFiles = uploadedFiles.filter((f) => f.id !== file.id)
    setUploadedFiles(newUploadedFiles)
    onFilesSelected(newUploadedFiles)

    // Clean up progress and errors
    const newProgress = { ...uploadProgress }
    delete newProgress[file.name]
    setUploadProgress(newProgress)

    const newErrors = { ...uploadErrors }
    delete newErrors[file.name]
    setUploadErrors(newErrors)
  }

  const getFileIcon = (fileName: string) => {
    const extension = fileName.split(".").pop()?.toLowerCase()

    switch (extension) {
      case "pdf":
        return <FileIcon className="h-4 w-4 text-red-500" />
      case "doc":
      case "docx":
        return <FileIcon className="h-4 w-4 text-blue-500" />
      case "ppt":
      case "pptx":
        return <FileIcon className="h-4 w-4 text-orange-500" />
      case "xls":
      case "xlsx":
        return <FileIcon className="h-4 w-4 text-green-500" />
      default:
        return <FileIcon className="h-4 w-4 text-gray-500" />
    }
  }

  return (
    <div className={cn("space-y-4", className)}>
      <div
        className={cn(
          "border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors",
          isDragging ? "border-primary bg-primary/5" : "border-muted-foreground/25 hover:border-primary/50",
          isUploading ? "opacity-50 pointer-events-none" : "",
          "focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2",
        )}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !isUploading && fileInputRef.current?.click()}
        tabIndex={0}
        role="button"
        aria-label="Upload files"
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileInputChange}
          className="hidden"
          multiple
          accept={acceptedFileTypes.join(",")}
          disabled={isUploading}
        />
        <div className="flex flex-col items-center justify-center space-y-2">
          <Upload className="h-8 w-8 text-muted-foreground" />
          <h3 className="text-lg font-medium">{isUploading ? "Uploading files..." : "Drag and drop files here"}</h3>
          <p className="text-sm text-muted-foreground">
            {isUploading ? (
              "Please wait..."
            ) : (
              <>
                or <span className="text-primary font-medium">click to browse</span>
              </>
            )}
          </p>
          <p className="text-xs text-muted-foreground mt-2">
            Accepted file types: {acceptedFileTypes.join(", ")} (Max {maxSizeMB}MB)
          </p>
          <p className="text-xs text-muted-foreground">Maximum {maxFiles} files</p>
        </div>
      </div>

      {uploadedFiles.length > 0 && (
        <div className="space-y-2">
          <h4 className="text-sm font-medium">
            Uploaded Files ({uploadedFiles.length}/{maxFiles})
          </h4>
          <ul className="space-y-2">
            {uploadedFiles.map((file) => (
              <li key={file.id} className="flex items-center justify-between p-2 border rounded-md bg-background">
                <div className="flex items-center space-x-2 overflow-hidden">
                  {getFileIcon(file.name)}
                  <span className="text-sm truncate max-w-[200px]" title={file.name}>
                    {file.name}
                  </span>
                  <span className="text-xs text-muted-foreground">{file.size}</span>
                </div>
                <div className="flex items-center space-x-2">
                  {uploadProgress[file.name] && uploadProgress[file.name] < 100 ? (
                    <div className="w-24">
                      <Progress value={uploadProgress[file.name]} className="h-2" />
                    </div>
                  ) : (
                    <Check className="h-4 w-4 text-green-500" />
                  )}
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-6 w-6 rounded-full"
                    onClick={(e) => {
                      e.stopPropagation()
                      handleRemoveFile(file)
                    }}
                    disabled={isUploading}
                  >
                    <X className="h-4 w-4" />
                    <span className="sr-only">Remove file</span>
                  </Button>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {Object.keys(uploadErrors).length > 0 && (
        <div className="space-y-2">
          <h4 className="text-sm font-medium text-destructive flex items-center gap-1">
            <AlertCircle className="h-4 w-4" />
            Errors
          </h4>
          <ul className="space-y-1">
            {Object.entries(uploadErrors).map(([fileName, error]) => (
              <li key={fileName} className="text-xs text-destructive flex items-center space-x-1">
                <X className="h-3 w-3" />
                <span>
                  {fileName}: {error}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
