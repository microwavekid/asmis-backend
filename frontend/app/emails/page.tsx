import { Header } from "@/components/layout/header"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { AtSign, Calendar, ExternalLink, PlusCircle, User } from "lucide-react"
import Link from "next/link"
import { mockEmails } from "@/lib/mock-emails"
import { format } from "date-fns"

export default function EmailsPage() {
  const pendingEmails = mockEmails.filter((email) => email.status === "pending")
  const draftEmails = mockEmails.filter((email) => email.status === "draft")
  const approvedEmails = mockEmails.filter((email) => email.status === "approved" || email.status === "sent")

  return (
    <div className="flex flex-col min-h-screen">
      <Header title="Emails" />
      <main className="flex-1 p-6">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
          <div>
            <h1 className="text-3xl font-bold">Email Management</h1>
            <p className="text-muted-foreground mt-1">Manage and approve AI-generated emails</p>
          </div>
          <div className="flex flex-wrap gap-2">
            <Button asChild>
              <Link href="/emails/compose">
                <PlusCircle className="mr-2 h-4 w-4" />
                Compose Email
              </Link>
            </Button>
            <Button variant="outline" asChild>
              <Link href="/emails/executive-generator" className="flex items-center">
                <AtSign className="mr-2 h-4 w-4" />
                Executive Email Generator
              </Link>
            </Button>
            <Button variant="outline" asChild>
              <Link href="/emails/kanban" className="flex items-center">
                <ExternalLink className="mr-2 h-4 w-4" />
                Email Approvals Kanban
              </Link>
            </Button>
          </div>
        </div>

        <Tabs defaultValue="pending" className="space-y-4">
          <TabsList>
            <TabsTrigger value="pending">Pending Approval ({pendingEmails.length})</TabsTrigger>
            <TabsTrigger value="drafts">Drafts ({draftEmails.length})</TabsTrigger>
            <TabsTrigger value="approved">Approved & Sent ({approvedEmails.length})</TabsTrigger>
          </TabsList>

          <TabsContent value="pending">
            <EmailTable emails={pendingEmails} />
          </TabsContent>

          <TabsContent value="drafts">
            <EmailTable emails={draftEmails} />
          </TabsContent>

          <TabsContent value="approved">
            <EmailTable emails={approvedEmails} />
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}

function EmailTable({ emails }: { emails: any[] }) {
  if (emails.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-center">
        <h3 className="text-lg font-medium">No emails found</h3>
        <p className="text-muted-foreground mt-2">There are no emails in this category.</p>
      </div>
    )
  }

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[300px]">Subject</TableHead>
            <TableHead>Recipient</TableHead>
            <TableHead>Account</TableHead>
            <TableHead>Date</TableHead>
            <TableHead>Status</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {emails.map((email) => (
            <TableRow key={email.id} className="cursor-pointer hover:bg-muted/50">
              <TableCell>
                <Link href={`/emails/${email.id}`} className="block">
                  <div className="font-medium">{email.subject}</div>
                  <div className="text-xs text-muted-foreground line-clamp-1 mt-1">
                    {email.content?.substring(0, 100)}...
                  </div>
                </Link>
              </TableCell>
              <TableCell>
                <div className="flex items-center gap-2">
                  <User className="h-4 w-4 text-muted-foreground" />
                  <span>{email.to}</span>
                </div>
              </TableCell>
              <TableCell>
                {email.accountId ? (
                  <Link href={`/accounts/${email.accountId}`}>
                    <Badge variant="outline">
                      {email.accountId === "1"
                        ? "Acme Corp"
                        : email.accountId === "2"
                          ? "Globex Corporation"
                          : email.accountId === "3"
                            ? "Initech"
                            : `Account ${email.accountId}`}
                    </Badge>
                  </Link>
                ) : (
                  <span className="text-muted-foreground text-sm">—</span>
                )}
              </TableCell>
              <TableCell>
                <div className="flex items-center gap-2">
                  <Calendar className="h-4 w-4 text-muted-foreground" />
                  <span>{format(new Date(email.createdAt), "MMM d, yyyy")}</span>
                </div>
              </TableCell>
              <TableCell>
                <StatusBadge status={email.status} />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}

function StatusBadge({ status }: { status: string }) {
  switch (status) {
    case "pending":
      return (
        <Badge variant="outline" className="bg-amber-100 text-amber-800 hover:bg-amber-100">
          Pending
        </Badge>
      )
    case "draft":
      return (
        <Badge variant="outline" className="bg-blue-100 text-blue-800 hover:bg-blue-100">
          Draft
        </Badge>
      )
    case "approved":
      return (
        <Badge variant="outline" className="bg-green-100 text-green-800 hover:bg-green-100">
          Approved
        </Badge>
      )
    case "sent":
      return (
        <Badge variant="outline" className="bg-purple-100 text-purple-800 hover:bg-purple-100">
          Sent
        </Badge>
      )
    case "rejected":
      return (
        <Badge variant="outline" className="bg-red-100 text-red-800 hover:bg-red-100">
          Rejected
        </Badge>
      )
    default:
      return <Badge variant="outline">{status}</Badge>
  }
}
