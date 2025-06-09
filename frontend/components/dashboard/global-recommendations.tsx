import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ScrollArea } from "@/components/ui/scroll-area"

export function GlobalRecommendations() {
  // Mock data for recommendations
  const recommendations = [
    {
      id: 1,
      title: "Schedule follow-up with Acme Corp",
      description: "CEO mentioned interest in expanding the contract during last call",
      priority: "high",
      category: "follow-up",
    },
    {
      id: 2,
      title: "Share case study with TechGiant",
      description: "Their team requested ROI examples from similar implementations",
      priority: "medium",
      category: "content",
    },
    {
      id: 3,
      title: "Prepare technical demo for NextGen",
      description: "Focus on integration capabilities as discussed in last meeting",
      priority: "high",
      category: "preparation",
    },
    {
      id: 4,
      title: "Update proposal for Finance Solutions Inc",
      description: "Incorporate new pricing structure based on feedback",
      priority: "medium",
      category: "proposal",
    },
  ]

  return (
    <Card className="h-[400px]">
      <CardHeader>
        <CardTitle>Strategic Recommendations</CardTitle>
        <CardDescription>AI-generated recommendations based on recent activities</CardDescription>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[300px] pr-4">
          <div className="space-y-4">
            {recommendations.map((rec) => (
              <div key={rec.id} className="rounded-lg border p-3">
                <div className="flex items-center justify-between">
                  <h4 className="font-medium">{rec.title}</h4>
                  <Badge variant={rec.priority === "high" ? "destructive" : "outline"}>{rec.priority}</Badge>
                </div>
                <p className="mt-1 text-sm text-muted-foreground">{rec.description}</p>
                <div className="mt-2">
                  <Badge variant="secondary" className="text-xs">
                    {rec.category}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  )
}
