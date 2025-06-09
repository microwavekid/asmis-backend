import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { GlobalTopicsChart } from "@/components/visualizations/global-topics-chart"
import { SentimentTrendList } from "@/components/dashboard/sentiment-trend-list"
import { opportunitySentimentData, accountSentimentData } from "@/lib/mock-sentiment-data"

export function GlobalInsightsSummary() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Global Insights Summary</CardTitle>
        <CardDescription>Overview of key insights across all accounts</CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="sentiment">
          <TabsList className="mb-4">
            <TabsTrigger value="sentiment">Sentiment Trends</TabsTrigger>
            <TabsTrigger value="topics">Key Topics</TabsTrigger>
          </TabsList>
          <TabsContent value="sentiment">
            <Tabs defaultValue="opportunities">
              <TabsList className="mb-4">
                <TabsTrigger value="opportunities">By Opportunity</TabsTrigger>
                <TabsTrigger value="accounts">By Account</TabsTrigger>
              </TabsList>

              <TabsContent value="opportunities">
                <SentimentTrendList items={opportunitySentimentData} title="Opportunity Sentiment Trends" />
              </TabsContent>

              <TabsContent value="accounts">
                <SentimentTrendList items={accountSentimentData} title="Account Sentiment Trends" />
              </TabsContent>
            </Tabs>
          </TabsContent>
          <TabsContent value="topics" className="h-[300px]">
            <GlobalTopicsChart />
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}
