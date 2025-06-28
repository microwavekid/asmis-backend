import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ArrowUpRight } from "lucide-react"
import Link from "next/link"

export function AccountsOverview() {
  // Mock data for accounts
  const accounts = [
    {
      id: "acme-corp",
      name: "Acme Corporation",
      status: "active",
      lastActivity: "2 days ago",
      nextMeeting: "Tomorrow, 2:00 PM",
      health: "healthy",
    },
    {
      id: "tech-giant",
      name: "TechGiant Inc",
      status: "active",
      lastActivity: "Yesterday",
      nextMeeting: "Next week",
      health: "at-risk",
    },
    {
      id: "next-gen",
      name: "NextGen Solutions",
      status: "active",
      lastActivity: "1 week ago",
      nextMeeting: "Today, 4:30 PM",
      health: "healthy",
    },
    {
      id: "finance-solutions",
      name: "Finance Solutions Inc",
      status: "inactive",
      lastActivity: "3 weeks ago",
      nextMeeting: "Not scheduled",
      health: "critical",
    },
    {
      id: "global-media",
      name: "Global Media Group",
      status: "active",
      lastActivity: "4 days ago",
      nextMeeting: "Friday, 10:00 AM",
      health: "healthy",
    },
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle>Accounts Overview</CardTitle>
        <CardDescription>Summary of all active accounts and their current status</CardDescription>
      </CardHeader>
      <CardContent>
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Account</TableHead>
              <TableHead>Status</TableHead>
              <TableHead>Last Activity</TableHead>
              <TableHead>Next Meeting</TableHead>
              <TableHead>Health</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {accounts.map((account) => (
              <TableRow key={account.id}>
                <TableCell className="font-medium">{account.name}</TableCell>
                <TableCell>
                  <Badge variant={account.status === "active" ? "outline" : "secondary"}>{account.status}</Badge>
                </TableCell>
                <TableCell>{account.lastActivity}</TableCell>
                <TableCell>{account.nextMeeting}</TableCell>
                <TableCell>
                  <Badge
                    variant={
                      account.health === "healthy"
                        ? "outline"
                        : account.health === "at-risk"
                          ? "secondary"
                          : "destructive"
                    }
                  >
                    {account.health}
                  </Badge>
                </TableCell>
                <TableCell className="text-right">
                  <Button variant="ghost" size="sm" asChild>
                    <Link href={`/accounts/${account.id}`}>
                      <ArrowUpRight className="mr-2 h-4 w-4" />
                      View
                    </Link>
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}
