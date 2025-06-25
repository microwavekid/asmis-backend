"use client"

import { usePathname } from "next/navigation"
import Link from "next/link"
import { cn } from "@/lib/utils"
import { 
  Building2, 
  Target, 
  FileText, 
  Brain, 
  Clock,
  Settings,
  HelpCircle
} from "lucide-react"

const navigationItems = [
  {
    title: "Accounts",
    href: "/accounts",
    icon: Building2,
  },
  {
    title: "Deals",
    href: "/deals",
    icon: Target,
  },
  {
    title: "Evidence",
    href: "/evidence",
    icon: FileText,
  },
  {
    title: "AI Insights",
    href: "/insights",
    icon: Brain,
  },
  {
    title: "Recent Activity",
    href: "/activity",
    icon: Clock,
  },
]

const bottomItems = [
  {
    title: "Settings",
    href: "/settings",
    icon: Settings,
  },
  {
    title: "Help",
    href: "/help",
    icon: HelpCircle,
  },
]

export function NavigationMenu() {
  const pathname = usePathname()

  return (
    <nav className="flex flex-col flex-1 py-4">
      <div className="space-y-1 px-3">
        {navigationItems.map((item) => {
          const Icon = item.icon
          const isActive = pathname.startsWith(item.href)
          
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                "hover:bg-[var(--bg-border)]",
                isActive
                  ? "bg-[var(--bg-border)] text-[var(--content-primary)]"
                  : "text-[var(--content-secondary)]"
              )}
            >
              <Icon className="h-4 w-4" />
              <span>{item.title}</span>
            </Link>
          )
        })}
      </div>
      
      <div className="mt-auto space-y-1 px-3">
        {bottomItems.map((item) => {
          const Icon = item.icon
          const isActive = pathname.startsWith(item.href)
          
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                "hover:bg-[var(--bg-border)]",
                isActive
                  ? "bg-[var(--bg-border)] text-[var(--content-primary)]"
                  : "text-[var(--content-secondary)]"
              )}
            >
              <Icon className="h-4 w-4" />
              <span>{item.title}</span>
            </Link>
          )
        })}
      </div>
    </nav>
  )
}