"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import {
  BarChart3,
  FileText,
  Home,
  MessageSquare,
  Settings,
  Users,
  CheckSquare,
  Briefcase,
  Search,
  ChevronDown,
  LogOut,
  Mail,
  Send,
  AtSign,
  PenSquare,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarInput,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from "@/components/ui/sidebar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

interface Account {
  id: string
  name: string
  logo?: string
}

const accounts: Account[] = [
  {
    id: "1",
    name: "Acme Inc",
    logo: "/placeholder.svg?height=32&width=32",
  },
  {
    id: "2",
    name: "Globex Corporation",
    logo: "/placeholder.svg?height=32&width=32",
  },
  {
    id: "3",
    name: "Initech",
    logo: "/placeholder.svg?height=32&width=32",
  },
]

export function AppSidebar() {
  const pathname = usePathname()
  const [selectedAccount, setSelectedAccount] = useState<Account>(accounts[0])
  const [emailsOpen, setEmailsOpen] = useState(false)

  // Auto-expand emails section if on an email route
  useEffect(() => {
    if (pathname === "/emails" || pathname === "/emails/executive-generator" || pathname === "/emails/compose") {
      setEmailsOpen(true)
    }
  }, [pathname])

  // Check if any email route is active
  const isEmailRouteActive =
    pathname === "/emails" || pathname === "/emails/executive-generator" || pathname === "/emails/compose"

  return (
    <Sidebar>
      <SidebarHeader>
        <div className="flex items-center gap-2 px-2 py-3">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" className="flex items-center gap-2 w-full justify-start px-2">
                <Avatar className="h-6 w-6">
                  <AvatarImage src={selectedAccount.logo || "/placeholder.svg"} alt={selectedAccount.name} />
                  <AvatarFallback>{selectedAccount.name.charAt(0)}</AvatarFallback>
                </Avatar>
                <span className="font-medium truncate">{selectedAccount.name}</span>
                <ChevronDown className="ml-auto h-4 w-4 opacity-50" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="start" className="w-[--radix-dropdown-menu-trigger-width]">
              <DropdownMenuLabel>Switch Account</DropdownMenuLabel>
              <DropdownMenuSeparator />
              {accounts.map((account) => (
                <DropdownMenuItem
                  key={account.id}
                  onClick={() => setSelectedAccount(account)}
                  className="flex items-center gap-2"
                >
                  <Avatar className="h-6 w-6">
                    <AvatarImage src={account.logo || "/placeholder.svg"} alt={account.name} />
                    <AvatarFallback>{account.name.charAt(0)}</AvatarFallback>
                  </Avatar>
                  <span>{account.name}</span>
                </DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
        <div className="px-2 pb-2">
          <div className="relative">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <SidebarInput type="search" placeholder="Search..." className="pl-8" />
          </div>
        </div>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Navigation</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton asChild isActive={pathname === "/dashboard"}>
                  <Link href="/dashboard">
                    <Home className="h-4 w-4" />
                    <span>Dashboard</span>
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton asChild isActive={pathname === "/accounts" || pathname.startsWith("/accounts/")}>
                  <Link href="/accounts">
                    <Briefcase className="h-4 w-4" />
                    <span>Accounts</span>
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton asChild isActive={pathname === "/meetings"}>
                  <Link href="/meetings">
                    <MessageSquare className="h-4 w-4" />
                    <span>Meetings</span>
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>

              {/* Email Menu Item */}
              <div className="relative">
                {/* Email Button */}
                <div
                  className={`flex w-full cursor-pointer items-center gap-2 rounded-md p-2 text-sm text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground ${isEmailRouteActive ? "bg-sidebar-accent font-medium text-sidebar-accent-foreground" : ""}`}
                  onClick={() => setEmailsOpen(!emailsOpen)}
                >
                  <Mail className="h-4 w-4 shrink-0" />
                  <span className="truncate">Emails</span>
                  <ChevronDown
                    className={`ml-auto h-4 w-4 shrink-0 opacity-50 transition-transform duration-200 ${emailsOpen ? "rotate-180" : ""}`}
                  />
                </div>

                {/* Email Submenu */}
                <div
                  className={`ml-6 mt-1 space-y-1 border-l border-sidebar-border pl-2 ${emailsOpen ? "block" : "hidden"}`}
                >
                  <Link
                    href="/emails"
                    className={`flex items-center rounded-md px-2 py-1.5 text-sm hover:bg-sidebar-accent hover:text-sidebar-accent-foreground ${pathname === "/emails" ? "bg-sidebar-accent text-sidebar-accent-foreground font-medium" : ""}`}
                  >
                    <Send className="mr-2 h-4 w-4" />
                    Email Approvals
                  </Link>
                  <Link
                    href="/emails/executive-generator"
                    className={`flex items-center rounded-md px-2 py-1.5 text-sm hover:bg-sidebar-accent hover:text-sidebar-accent-foreground ${pathname === "/emails/executive-generator" ? "bg-sidebar-accent text-sidebar-accent-foreground font-medium" : ""}`}
                  >
                    <AtSign className="mr-2 h-4 w-4" />
                    Executive Email Generator
                  </Link>
                  <Link
                    href="/emails/compose"
                    className={`flex items-center rounded-md px-2 py-1.5 text-sm hover:bg-sidebar-accent hover:text-sidebar-accent-foreground ${pathname === "/emails/compose" ? "bg-sidebar-accent text-sidebar-accent-foreground font-medium" : ""}`}
                  >
                    <PenSquare className="mr-2 h-4 w-4" />
                    Compose Email
                  </Link>
                </div>
              </div>

              <SidebarMenuItem>
                <SidebarMenuButton asChild isActive={pathname === "/tasks"}>
                  <Link href="/tasks">
                    <CheckSquare className="h-4 w-4" />
                    <span>Tasks</span>
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton asChild isActive={pathname === "/documents"}>
                  <Link href="/documents">
                    <FileText className="h-4 w-4" />
                    <span>Documents</span>
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton asChild isActive={pathname === "/stakeholders"}>
                  <Link href="/stakeholders">
                    <Users className="h-4 w-4" />
                    <span>Stakeholders</span>
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton asChild isActive={pathname === "/analytics"}>
                  <Link href="/analytics">
                    <BarChart3 className="h-4 w-4" />
                    <span>Analytics</span>
                  </Link>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton asChild isActive={pathname === "/settings"}>
              <Link href="/settings">
                <Settings className="h-4 w-4" />
                <span>Settings</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
          <SidebarMenuItem>
            <SidebarMenuButton asChild>
              <Link href="/logout">
                <LogOut className="h-4 w-4" />
                <span>Logout</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
