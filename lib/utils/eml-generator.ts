/**
 * Utility functions for generating .eml files (RFC 822 standard)
 */

// Generate a random boundary string for MIME multipart messages
function generateBoundary(): string {
  return `----=_NextPart_${Math.random().toString(36).substring(2)}`
}

// Format a date according to RFC 822 standard
function formatRFC822Date(date: Date): string {
  return date.toUTCString()
}

// Fold long lines according to RFC 822 standard (max 76 chars per line)
function foldLine(line: string, maxLength = 76): string {
  if (line.length <= maxLength) {
    return line
  }

  let result = ""
  for (let i = 0; i < line.length; i += maxLength) {
    result += line.substring(i, i + maxLength)
    if (i + maxLength < line.length) {
      result += "\r\n "
    }
  }
  return result
}

// Create a properly formatted email header
function createHeader(name: string, value: string): string {
  return `${name}: ${foldLine(value)}\r\n`
}

// Generate an .eml file from email data
export function generateEmlFile({
  from,
  to,
  subject,
  content,
  attachments = [],
}: {
  from: string
  to: string
  subject: string
  content: string
  attachments?: Array<{
    name: string
    type: string
    content: string // Base64 encoded content
  }>
}): string {
  const boundary = generateBoundary()
  const date = formatRFC822Date(new Date())
  const messageId = `<${Date.now()}.${Math.random().toString(36).substring(2)}@asmis.com>`

  // Create email headers
  let emlContent = ""
  emlContent += createHeader("From", from)
  emlContent += createHeader("To", to)
  emlContent += createHeader("Subject", subject)
  emlContent += createHeader("Date", date)
  emlContent += createHeader("Message-ID", messageId)
  emlContent += createHeader("MIME-Version", "1.0")

  // If there are attachments, create a multipart message
  if (attachments.length > 0) {
    emlContent += createHeader("Content-Type", `multipart/mixed; boundary="${boundary}"`)
    emlContent += "\r\n"

    // Add the email body as the first part
    emlContent += `--${boundary}\r\n`
    emlContent += createHeader("Content-Type", "text/plain; charset=utf-8")
    emlContent += createHeader("Content-Transfer-Encoding", "7bit")
    emlContent += "\r\n"
    emlContent += content.replace(/\n/g, "\r\n")
    emlContent += "\r\n\r\n"

    // Add each attachment
    for (const attachment of attachments) {
      emlContent += `--${boundary}\r\n`
      emlContent += createHeader("Content-Type", `${attachment.type}; name="${attachment.name}"`)
      emlContent += createHeader("Content-Disposition", `attachment; filename="${attachment.name}"`)
      emlContent += createHeader("Content-Transfer-Encoding", "base64")
      emlContent += "\r\n"

      // Add the base64 content with proper line breaks
      const base64Content = attachment.content
      for (let i = 0; i < base64Content.length; i += 76) {
        emlContent += base64Content.substring(i, i + 76) + "\r\n"
      }
      emlContent += "\r\n"
    }

    // Close the multipart message
    emlContent += `--${boundary}--\r\n`
  } else {
    // If there are no attachments, just add the email body
    emlContent += createHeader("Content-Type", "text/plain; charset=utf-8")
    emlContent += "\r\n"
    emlContent += content.replace(/\n/g, "\r\n")
  }

  return emlContent
}

// Create a data URL for downloading an .eml file
export function createEmlDataUrl(emlContent: string): string {
  const blob = new Blob([emlContent], { type: "message/rfc822" })
  return URL.createObjectURL(blob)
}
