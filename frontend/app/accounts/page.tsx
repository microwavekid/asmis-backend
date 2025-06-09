"use client"

import { useState, useMemo } from "react"
import { Header } from "@/components/layout/header"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { PlusCircle, Search, ArrowUpDown, ArrowUp, ArrowDown, ExternalLink, Lightbulb } from "lucide-react"
import Link from "next/link"
import { mockAccounts } from "@/lib/mock-data"
import { format, parseISO } from "date-fns"

export default function AccountsPage() {
  // State for sorting and filtering
  const [sortColumn, setSortColumn] = useState<string>("name")
  const [sortDirection, setSortDirection] = useState<"asc" | "desc">("asc")
  const [searchQuery, setSearchQuery] = useState("")
  const [customerTypeFilter, setCustomerTypeFilter] = useState("all")
  const [industryFilter, setIndustryFilter] = useState("all")

  // Get unique industries for filter dropdown
  const industries = useMemo(() => {
    const uniqueIndustries = new Set(mockAccounts.map((account) => account.industry))
    return Array.from(uniqueIndustries)
  }, [])

  // Filter accounts based on search query and filters
  const filteredAccounts = useMemo(() => {
    return mockAccounts.filter((account) => {
      // Filter by search query
      if (searchQuery && !account.name.toLowerCase().includes(searchQuery.toLowerCase())) {
        return false
      }

      // Filter by customer type
      if (customerTypeFilter !== "all" && account.customerType !== customerTypeFilter) {
        return false
      }

      // Filter by industry
      if (industryFilter !== "all" && account.industry !== industryFilter) {
        return false
      }

      return true
    })
  }, [searchQuery, customerTypeFilter, industryFilter])

  // Sort accounts based on sort column and direction
  const sortedAccounts = useMemo(() => {
    return [...filteredAccounts].sort((a, b) => {
      let aValue, bValue

      // Handle nested properties
      if (sortColumn === "arrBySolution.orchestrate") {
        aValue = a.arrBySolution.orchestrate
        bValue = b.arrBySolution.orchestrate
      } else if (sortColumn === "arrBySolution.digitalOptimization") {
        aValue = a.arrBySolution.digitalOptimization
        bValue = b.arrBySolution.digitalOptimization
      } else if (sortColumn === "arrBySolution.monetize") {
        aValue = a.arrBySolution.monetize
        bValue = b.arrBySolution.monetize
      } else if (sortColumn === "arrBySolution.opal") {
        aValue = a.arrBySolution.opal
        bValue = b.arrBySolution.opal
      } else if (sortColumn === "lastContact") {
        aValue = a.lastContact.date
        bValue = b.lastContact.date
      } else {
        // @ts-ignore
        aValue = a[sortColumn]
        // @ts-ignore
        bValue = b[sortColumn]
      }

      // Handle string comparison
      if (typeof aValue === "string" && typeof bValue === "string") {
        return sortDirection === "asc" ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue)
      }

      // Handle number comparison
      return sortDirection === "asc" ? aValue - bValue : bValue - aValue
    })
  }, [filteredAccounts, sortColumn, sortDirection])

  // Handle sort click
  const handleSort = (column: string) => {
    if (sortColumn === column) {
      // Toggle direction if same column
      setSortDirection(sortDirection === "asc" ? "desc" : "asc")
    } else {
      // Set new column and default to ascending
      setSortColumn(column)
      setSortDirection("asc")
    }
  }

  // Render sort indicator
  const renderSortIndicator = (column: string) => {
    if (sortColumn !== column) {
      return <ArrowUpDown className="ml-2 h-4 w-4" />
    }

    return sortDirection === "asc" ? <ArrowUp className="ml-2 h-4 w-4" /> : <ArrowDown className="ml-2 h-4 w-4" />
  }

  // Format currency
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: 0,
    }).format(amount)
  }

  // Get customer type badge color
  const getCustomerTypeBadge = (type: string) => {
    switch (type) {
      case "active":
        return <Badge className="bg-green-100 text-green-800 hover:bg-green-100">Active Customer</Badge>
      case "prospect":
        return <Badge className="bg-blue-100 text-blue-800 hover:bg-blue-100">Prospect</Badge>
      case "ex-customer":
        return <Badge className="bg-orange-100 text-orange-800 hover:bg-orange-100">Ex-Customer</Badge>
      default:
        return <Badge>{type}</Badge>
    }
  }

  return (
    <div className="flex flex-col min-h-screen">
      <Header title="Accounts" />
      <main className="flex-1 p-6">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">Accounts</h1>
          <Button>
            <PlusCircle className="mr-2 h-4 w-4" />
            Add Account
          </Button>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-4 mb-6">
          <div className="relative flex-1 min-w-[200px]">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              type="search"
              placeholder="Search accounts..."
              className="pl-8"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          <Select value={customerTypeFilter} onValueChange={setCustomerTypeFilter}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Customer Type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Types</SelectItem>
              <SelectItem value="active">Active Customers</SelectItem>
              <SelectItem value="prospect">Prospects</SelectItem>
              <SelectItem value="ex-customer">Ex-Customers</SelectItem>
            </SelectContent>
          </Select>

          <Select value={industryFilter} onValueChange={setIndustryFilter}>
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Industry" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Industries</SelectItem>
              {industries.map((industry) => (
                <SelectItem key={industry} value={industry}>
                  {industry}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Accounts Table */}
        <div className="rounded-md border overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="min-w-[200px]">
                  <button className="flex items-center font-semibold" onClick={() => handleSort("name")}>
                    Account Name {renderSortIndicator("name")}
                  </button>
                </TableHead>
                <TableHead>
                  <button className="flex items-center font-semibold" onClick={() => handleSort("aiSuggestions")}>
                    AI Suggestions {renderSortIndicator("aiSuggestions")}
                  </button>
                </TableHead>
                <TableHead>
                  <button className="flex items-center font-semibold" onClick={() => handleSort("customerType")}>
                    Customer Type {renderSortIndicator("customerType")}
                  </button>
                </TableHead>
                <TableHead className="text-right">
                  <button className="flex items-center font-semibold ml-auto" onClick={() => handleSort("totalARR")}>
                    Total ARR {renderSortIndicator("totalARR")}
                  </button>
                </TableHead>
                <TableHead className="text-right">
                  <button
                    className="flex items-center font-semibold ml-auto"
                    onClick={() => handleSort("arrBySolution.orchestrate")}
                  >
                    Orchestrate {renderSortIndicator("arrBySolution.orchestrate")}
                  </button>
                </TableHead>
                <TableHead className="text-right">
                  <button
                    className="flex items-center font-semibold ml-auto"
                    onClick={() => handleSort("arrBySolution.digitalOptimization")}
                  >
                    Digital Optimization {renderSortIndicator("arrBySolution.digitalOptimization")}
                  </button>
                </TableHead>
                <TableHead className="text-right">
                  <button
                    className="flex items-center font-semibold ml-auto"
                    onClick={() => handleSort("arrBySolution.monetize")}
                  >
                    Monetize {renderSortIndicator("arrBySolution.monetize")}
                  </button>
                </TableHead>
                <TableHead className="text-right">
                  <button
                    className="flex items-center font-semibold ml-auto"
                    onClick={() => handleSort("arrBySolution.opal")}
                  >
                    Opal ARR {renderSortIndicator("arrBySolution.opal")}
                  </button>
                </TableHead>
                <TableHead className="text-right">
                  <button
                    className="flex items-center font-semibold ml-auto"
                    onClick={() => handleSort("openOpportunities")}
                  >
                    Open Opps {renderSortIndicator("openOpportunities")}
                  </button>
                </TableHead>
                <TableHead className="text-right">
                  <button
                    className="flex items-center font-semibold ml-auto"
                    onClick={() => handleSort("buyingCenters")}
                  >
                    Buying Centers Engaged {renderSortIndicator("buyingCenters")}
                  </button>
                </TableHead>
                <TableHead className="text-right">
                  <button
                    className="flex items-center font-semibold ml-auto"
                    onClick={() => handleSort("contactsEngaged")}
                  >
                    Contacts {renderSortIndicator("contactsEngaged")}
                  </button>
                </TableHead>
                <TableHead className="text-right">
                  <button className="flex items-center font-semibold ml-auto" onClick={() => handleSort("mqls")}>
                    MQLs {renderSortIndicator("mqls")}
                  </button>
                </TableHead>
                <TableHead>
                  <button className="flex items-center font-semibold" onClick={() => handleSort("lastContact")}>
                    Last Contact {renderSortIndicator("lastContact")}
                  </button>
                </TableHead>
                <TableHead className="w-[50px]"></TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {sortedAccounts.map((account) => (
                <TableRow key={account.id} className="hover:bg-muted/50">
                  <TableCell className="font-medium">{account.name}</TableCell>
                  <TableCell>
                    {account.aiSuggestions > 0 ? (
                      <Link href={`/accounts/${account.id}/suggestions`}>
                        <Badge className="bg-purple-100 text-purple-800 hover:bg-purple-200 cursor-pointer">
                          <Lightbulb className="h-3 w-3 mr-1" />
                          {account.aiSuggestions}
                        </Badge>
                      </Link>
                    ) : (
                      <span className="text-muted-foreground">—</span>
                    )}
                  </TableCell>
                  <TableCell>{getCustomerTypeBadge(account.customerType)}</TableCell>
                  <TableCell className="text-right">{formatCurrency(account.totalARR)}</TableCell>
                  <TableCell className="text-right">{formatCurrency(account.arrBySolution.orchestrate)}</TableCell>
                  <TableCell className="text-right">
                    {formatCurrency(account.arrBySolution.digitalOptimization)}
                  </TableCell>
                  <TableCell className="text-right">{formatCurrency(account.arrBySolution.monetize)}</TableCell>
                  <TableCell className="text-right">{formatCurrency(account.arrBySolution.opal)}</TableCell>
                  <TableCell className="text-right">{account.openOpportunities}</TableCell>
                  <TableCell className="text-right">{account.buyingCenters}</TableCell>
                  <TableCell className="text-right">{account.contactsEngaged}</TableCell>
                  <TableCell className="text-right">{account.mqls}</TableCell>
                  <TableCell>
                    {format(parseISO(account.lastContact.date), "MMM d, yyyy")}
                    <span className="text-muted-foreground ml-1">({account.lastContact.type})</span>
                  </TableCell>
                  <TableCell>
                    <Button variant="ghost" size="icon" asChild>
                      <Link href={`/accounts/${account.id}`}>
                        <ExternalLink className="h-4 w-4" />
                        <span className="sr-only">View</span>
                      </Link>
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
              {sortedAccounts.length === 0 && (
                <TableRow>
                  <TableCell colSpan={14} className="text-center py-8 text-muted-foreground">
                    No accounts found matching your filters
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </div>
      </main>
    </div>
  )
}
