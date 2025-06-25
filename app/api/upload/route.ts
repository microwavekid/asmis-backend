import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const file = formData.get("file") as File

    if (!file) {
      return NextResponse.json({ error: "File is required" }, { status: 400 })
    }

    // Generate a unique ID for the file
    const fileId = `file-${Date.now()}-${file.name.replace(/\s+/g, "-")}`

    // Create a placeholder URL for the file
    const fileType = file.name.split(".").pop()?.toLowerCase() || "file"
    const placeholderUrl = `/placeholder.svg?height=800&width=600&query=Uploaded ${fileType.toUpperCase()}: ${file.name}`

    // Return success with the placeholder URL
    return NextResponse.json({
      url: placeholderUrl,
      name: file.name,
      id: fileId,
      size: `${(file.size / (1024 * 1024)).toFixed(1)} MB`,
      type: fileType.toUpperCase(),
    })
  } catch (error) {
    console.error("Error handling upload:", error)
    return NextResponse.json({ error: "Failed to process upload" }, { status: 500 })
  }
}

export const runtime = "nodejs"
