import { Skeleton } from "@/components/ui/skeleton"
import { Header } from "@/components/layout/header"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

export default function AccountsLoading() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header title="Accounts" />
      <main className="flex-1 p-6">
        <div className="flex justify-between items-center mb-6">
          <Skeleton className="h-10 w-64" />
          <Skeleton className="h-10 w-36" />
        </div>

        <div className="flex flex-wrap gap-4 mb-6">
          <Skeleton className="h-10 flex-1 min-w-[200px]" />
          <Skeleton className="h-10 w-[180px]" />
          <Skeleton className="h-10 w-[180px]" />
        </div>

        <div className="rounded-md border overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                {Array(14)
                  .fill(0)
                  .map((_, i) => (
                    <TableHead key={i}>
                      <Skeleton className="h-5 w-full" />
                    </TableHead>
                  ))}
              </TableRow>
            </TableHeader>
            <TableBody>
              {Array(5)
                .fill(0)
                .map((_, i) => (
                  <TableRow key={i}>
                    {Array(14)
                      .fill(0)
                      .map((_, j) => (
                        <TableCell key={j}>
                          <Skeleton className="h-5 w-full" />
                        </TableCell>
                      ))}
                  </TableRow>
                ))}
            </TableBody>
          </Table>
        </div>
      </main>
    </div>
  )
}
