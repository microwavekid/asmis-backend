import { Header } from "@/components/layout/header"
import { DocumentsView } from "@/components/documents/documents-view"

export default function DocumentsPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header title="Documents" />
      <main className="flex-1 p-6">
        <DocumentsView />
      </main>
    </div>
  )
}
