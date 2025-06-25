import { Header } from "@/components/layout/header"
import { KeyMetricsModule } from "@/components/dashboard/key-metrics-module"
import { GlobalInsightsSummary } from "@/components/dashboard/global-insights-summary"
import { GlobalRecommendations } from "@/components/dashboard/global-recommendations"
import { GlobalTasksOverview } from "@/components/dashboard/global-tasks-overview"
import { AccountsOverview } from "@/components/dashboard/accounts-overview"
import { PendingEmailsApproval } from "@/components/dashboard/pending-emails-approval"
import { SentimentTrendList } from "@/components/dashboard/sentiment-trend-list"
import { accountSentimentData, opportunitySentimentData } from "@/lib/mock-sentiment-data"

export default function DashboardPage() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header title="Dashboard" />
      <main className="flex-1 p-6">
        <h1 className="text-3xl font-bold mb-6">Global Dashboard</h1>

        <div className="grid gap-6">
          {/* Key Metrics Module - Full Width */}
          <div className="col-span-full">
            <KeyMetricsModule />
          </div>

          {/* Global Insights Summary - Full Width */}
          <div className="col-span-full">
            <GlobalInsightsSummary />
          </div>

          {/* Pending Email Approvals - Full Width */}
          <div className="col-span-full">
            <PendingEmailsApproval />
          </div>

          {/* Accounts Overview - 2/3 Width */}
          <div className="grid gap-6 grid-cols-1 lg:grid-cols-3">
            <div className="lg:col-span-2">
              <AccountsOverview />
            </div>

            {/* Tasks Overview - 1/3 Width */}
            <div className="lg:col-span-1">
              <GlobalTasksOverview />
            </div>
          </div>

          {/* Sentiment Trends - Full Width */}
          <div className="col-span-full grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow p-4">
              <SentimentTrendList items={accountSentimentData} title="Account Sentiment Trends" />
            </div>
            <div className="bg-white rounded-lg shadow p-4">
              <SentimentTrendList items={opportunitySentimentData} title="Opportunity Sentiment Trends" />
            </div>
          </div>

          {/* Recommendations - Full Width */}
          <div className="col-span-full">
            <GlobalRecommendations />
          </div>
        </div>
      </main>
    </div>
  )
}
