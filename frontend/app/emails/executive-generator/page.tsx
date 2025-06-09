import type { Metadata } from "next"
import { Header } from "@/components/layout/header"
import { ExecutiveEmailGenerator } from "@/components/emails/executive-email-generator"

export const metadata: Metadata = {
  title: "Executive Email Generator | ASMIS",
  description: "Create professional emails from your executives to key stakeholders",
}

export default function ExecutiveGeneratorPage() {
  return (
    <>
      <Header title="Executive Email Generator" />
      <main className="flex-1 p-6">
        <ExecutiveEmailGenerator />
      </main>
    </>
  )
}
