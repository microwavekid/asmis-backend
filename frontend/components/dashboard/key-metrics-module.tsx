"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Slider } from "@/components/ui/slider"
import { Badge } from "@/components/ui/badge"
import {
  CalendarDays,
  FileText,
  Mail,
  Users,
  MessageSquare,
  Calendar,
  UserCheck,
  Target,
  DollarSign,
  Award,
  RefreshCw,
  TrendingDown,
  AlertTriangle,
  CheckCircle2,
} from "lucide-react"
import { defaultUserGoals, industryBenchmarks } from "@/lib/mock-metrics"

export function KeyMetricsModule() {
  const [userGoals, setUserGoals] = useState(defaultUserGoals)
  const [isEditingGoals, setIsEditingGoals] = useState(false)
  const [weeklyMetrics, setWeeklyMetrics] = useState([])
  const [monthlyMetrics, setMonthlyMetrics] = useState({})
  const [quarterlyMetrics, setQuarterlyMetrics] = useState({})

  // Calculate all metrics based on user goals
  useEffect(() => {
    // Calculate weekly metrics
    const calculatedWeeklyMetrics = calculateWeeklyMetrics(userGoals)
    setWeeklyMetrics(calculatedWeeklyMetrics)

    // Calculate monthly metrics
    const calculatedMonthlyMetrics = calculateMonthlyMetrics(userGoals)
    setMonthlyMetrics(calculatedMonthlyMetrics)

    // Calculate quarterly metrics
    const calculatedQuarterlyMetrics = calculateQuarterlyMetrics(userGoals)
    setQuarterlyMetrics(calculatedQuarterlyMetrics)
  }, [userGoals])

  // Calculate weekly metrics based on user goals
  const calculateWeeklyMetrics = (goals) => {
    // Base weekly targets as specified
    const baseWeeklyTargets = {
      externalMeetings: 7,
      filesShared: 10,
      emailsSent: 50,
      newStakeholders: 2,
      prospectsEngaged: 5,
      amplifyPosts: 5,
    }

    // Calculate scaling factor based on annual target
    // This allows the targets to scale proportionally when the annual target changes
    const scalingFactor = goals.annualTarget / defaultUserGoals.annualTarget

    // Calculate metrics for the next 3 weeks
    return [
      {
        weekName: "This Week",
        externalMeetings: {
          target: Math.round(baseWeeklyTargets.externalMeetings * scalingFactor),
          actual: Math.round(baseWeeklyTargets.externalMeetings * scalingFactor * 0.7 * Math.random()),
        },
        filesShared: {
          target: Math.round(baseWeeklyTargets.filesShared * scalingFactor),
          actual: Math.round(baseWeeklyTargets.filesShared * scalingFactor * 0.8 * Math.random()),
        },
        emailsSent: {
          target: Math.round(baseWeeklyTargets.emailsSent * scalingFactor),
          actual: Math.round(baseWeeklyTargets.emailsSent * scalingFactor * 0.75 * Math.random()),
        },
        prospectsEngaged: {
          target: Math.round(baseWeeklyTargets.prospectsEngaged * scalingFactor),
          actual: Math.round(baseWeeklyTargets.prospectsEngaged * scalingFactor * 0.6 * Math.random()),
        },
        amplifyPosts: {
          target: Math.round(baseWeeklyTargets.amplifyPosts * scalingFactor),
          actual: Math.round(baseWeeklyTargets.amplifyPosts * scalingFactor * 0.6 * Math.random()),
        },
        newStakeholders: {
          target: Math.round(baseWeeklyTargets.newStakeholders * scalingFactor),
          actual: Math.round(baseWeeklyTargets.newStakeholders * scalingFactor * 0.5 * Math.random()),
        },
      },
      {
        weekName: "Next Week",
        externalMeetings: {
          target: Math.round(baseWeeklyTargets.externalMeetings * scalingFactor * 1.1),
          actual: 0,
        },
        filesShared: {
          target: Math.round(baseWeeklyTargets.filesShared * scalingFactor * 1.1),
          actual: 0,
        },
        emailsSent: {
          target: Math.round(baseWeeklyTargets.emailsSent * scalingFactor * 1.1),
          actual: 0,
        },
        prospectsEngaged: {
          target: Math.round(baseWeeklyTargets.prospectsEngaged * scalingFactor * 1.1),
          actual: 0,
        },
        amplifyPosts: {
          target: Math.round(baseWeeklyTargets.amplifyPosts * scalingFactor * 1.1),
          actual: 0,
        },
        newStakeholders: {
          target: Math.round(baseWeeklyTargets.newStakeholders * scalingFactor * 1.1),
          actual: 0,
        },
      },
      {
        weekName: "Week 3",
        externalMeetings: {
          target: Math.round(baseWeeklyTargets.externalMeetings * scalingFactor * 1.2),
          actual: 0,
        },
        filesShared: {
          target: Math.round(baseWeeklyTargets.filesShared * scalingFactor * 1.2),
          actual: 0,
        },
        emailsSent: {
          target: Math.round(baseWeeklyTargets.emailsSent * scalingFactor * 1.2),
          actual: 0,
        },
        prospectsEngaged: {
          target: Math.round(baseWeeklyTargets.prospectsEngaged * scalingFactor * 1.2),
          actual: 0,
        },
        amplifyPosts: {
          target: Math.round(baseWeeklyTargets.amplifyPosts * scalingFactor * 1.2),
          actual: 0,
        },
        newStakeholders: {
          target: Math.round(baseWeeklyTargets.newStakeholders * scalingFactor * 1.2),
          actual: 0,
        },
      },
    ]
  }

  // Calculate monthly metrics based on user goals
  const calculateMonthlyMetrics = (goals) => {
    // Calculate monthly target based on annual goal
    const annualTarget = goals.annualTarget
    const monthlyTargetBase = annualTarget / 12

    return {
      qbrsScheduled: {
        target: Math.round(monthlyTargetBase / industryBenchmarks.averageDealSize / 10) + 2,
        actual: Math.round((monthlyTargetBase / industryBenchmarks.averageDealSize / 10 + 2) * 0.5 * Math.random()),
      },
      inPersonMeetings: {
        target: Math.round((monthlyTargetBase / industryBenchmarks.averageDealSize) * 0.5),
        actual: Math.round((monthlyTargetBase / industryBenchmarks.averageDealSize) * 0.5 * 0.6 * Math.random()),
      },
      pipelineGenerated: {
        dollars: {
          target: Math.round(monthlyTargetBase * 3),
          actual: Math.round(monthlyTargetBase * 3 * 0.7 * Math.random()),
        },
        count: {
          target: Math.round((monthlyTargetBase / industryBenchmarks.averageDealSize) * 1.5),
          actual: Math.round((monthlyTargetBase / industryBenchmarks.averageDealSize) * 1.5 * 0.65 * Math.random()),
        },
      },
      buyingProcessAdvances: {
        discovery: {
          target: Math.round((monthlyTargetBase / industryBenchmarks.averageDealSize) * 2),
          actual: Math.round((monthlyTargetBase / industryBenchmarks.averageDealSize) * 2 * 0.7 * Math.random()),
        },
        proof: {
          target: Math.round((monthlyTargetBase / industryBenchmarks.averageDealSize) * 1.5),
          actual: Math.round((monthlyTargetBase / industryBenchmarks.averageDealSize) * 1.5 * 0.65 * Math.random()),
        },
        proposal: {
          target: Math.round((monthlyTargetBase / industryBenchmarks.averageDealSize) * 1.2),
          actual: Math.round((monthlyTargetBase / industryBenchmarks.averageDealSize) * 1.2 * 0.5 * Math.random()),
        },
        contracts: {
          target: Math.round(monthlyTargetBase / industryBenchmarks.averageDealSize),
          actual: Math.round((monthlyTargetBase / industryBenchmarks.averageDealSize) * 0.3 * Math.random()),
        },
      },
      newStakeholderBuyingWindows: {
        target: Math.round(
          ((monthlyTargetBase / industryBenchmarks.averageDealSize) * industryBenchmarks.stakeholdersPerDeal) / 3,
        ),
        actual: Math.round(
          (((monthlyTargetBase / industryBenchmarks.averageDealSize) * industryBenchmarks.stakeholdersPerDeal) / 3) *
            0.6 *
            Math.random(),
        ),
      },
    }
  }

  // Calculate quarterly metrics based on user goals
  const calculateQuarterlyMetrics = (goals) => {
    // Use the first quarter goal as the current quarter target
    const currentQuarterTarget = goals.quarterlyGoals[0].target

    return {
      closedWonDollars: {
        target: currentQuarterTarget,
        actual: Math.round(currentQuarterTarget * 0.75 * Math.random()),
      },
      closedWonDeals: {
        target: Math.round(currentQuarterTarget / industryBenchmarks.averageDealSize),
        actual: Math.round((currentQuarterTarget / industryBenchmarks.averageDealSize) * 0.6 * Math.random()),
      },
      winRate: {
        target: industryBenchmarks.opportunityToWinRate,
        actual: industryBenchmarks.opportunityToWinRate * (0.7 + 0.3 * Math.random()),
      },
    }
  }

  // Format currency
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: 0,
    }).format(amount)
  }

  // Format percentage
  const formatPercent = (value) => {
    return new Intl.NumberFormat("en-US", {
      style: "percent",
      minimumFractionDigits: 0,
      maximumFractionDigits: 1,
    }).format(value)
  }

  // Calculate progress percentage (capped at 100%)
  const calculateProgress = (actual, target) => {
    return Math.min(Math.round((actual / target) * 100), 100)
  }

  // Get progress color based on percentage
  const getProgressColor = (percentage) => {
    if (percentage < 40) return "bg-red-500"
    if (percentage < 70) return "bg-amber-500"
    return "bg-emerald-500"
  }

  // Get status badge based on percentage
  const getStatusBadge = (percentage) => {
    if (percentage < 40) {
      return (
        <Badge variant="outline" className="bg-red-50 text-red-700 border-red-200 flex items-center gap-1">
          <TrendingDown className="h-3 w-3" /> At Risk
        </Badge>
      )
    }
    if (percentage < 70) {
      return (
        <Badge variant="outline" className="bg-amber-50 text-amber-700 border-amber-200 flex items-center gap-1">
          <AlertTriangle className="h-3 w-3" /> Needs Attention
        </Badge>
      )
    }
    return (
      <Badge variant="outline" className="bg-emerald-50 text-emerald-700 border-emerald-200 flex items-center gap-1">
        <CheckCircle2 className="h-3 w-3" /> On Track
      </Badge>
    )
  }

  // Handle user goal updates
  const handleGoalUpdate = () => {
    // In a real app, this would save the goals to a database
    setIsEditingGoals(false)
  }

  return (
    <Card className="w-full">
      <CardHeader className="bg-gradient-to-r from-slate-50 to-blue-50 dark:from-slate-900 dark:to-blue-950 border-b">
        <div className="flex justify-between items-center">
          <div>
            <CardTitle className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-700 to-indigo-700 dark:from-blue-400 dark:to-indigo-400">
              Key Performance Metrics
            </CardTitle>
            <CardDescription>Track your progress against weekly, monthly, and quarterly targets</CardDescription>
          </div>
          <Button
            variant={isEditingGoals ? "secondary" : "default"}
            size="sm"
            onClick={() => setIsEditingGoals(!isEditingGoals)}
            className={
              isEditingGoals
                ? ""
                : "bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700"
            }
          >
            {isEditingGoals ? "Cancel" : "Configure Goals"}
          </Button>
        </div>
      </CardHeader>
      <CardContent className="p-4 md:p-6">
        {isEditingGoals ? (
          <div className="space-y-6 animate-in fade-in duration-300">
            <h3 className="text-lg font-medium text-blue-700 dark:text-blue-400">Configure Your Sales Goals</h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4 p-4 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
                <div>
                  <Label htmlFor="annualTarget" className="text-sm font-medium">
                    Annual Target ($)
                  </Label>
                  <Input
                    id="annualTarget"
                    type="number"
                    value={userGoals.annualTarget}
                    onChange={(e) => setUserGoals({ ...userGoals, annualTarget: Number(e.target.value) })}
                    className="mt-1"
                  />
                </div>

                <div>
                  <Label htmlFor="annualQuota" className="text-sm font-medium">
                    Annual Quota ($)
                  </Label>
                  <Input
                    id="annualQuota"
                    type="number"
                    value={userGoals.annualQuota}
                    onChange={(e) => setUserGoals({ ...userGoals, annualQuota: Number(e.target.value) })}
                    className="mt-1"
                  />
                </div>

                <div>
                  <Label className="text-sm font-medium">Fiscal Year Split (H1/H2)</Label>
                  <div className="flex items-center gap-4 mt-2">
                    <span className="text-sm font-medium w-8 text-blue-700 dark:text-blue-400">
                      {Math.round(userGoals.fyh1Split * 100)}%
                    </span>
                    <Slider
                      value={[userGoals.fyh1Split * 100]}
                      max={100}
                      step={5}
                      onValueChange={(value) => {
                        const h1 = value[0] / 100
                        setUserGoals({
                          ...userGoals,
                          fyh1Split: h1,
                          fyh2Split: 1 - h1,
                        })
                      }}
                      className="flex-1"
                    />
                    <span className="text-sm font-medium w-8 text-indigo-700 dark:text-indigo-400">
                      {Math.round(userGoals.fyh2Split * 100)}%
                    </span>
                  </div>
                </div>
              </div>

              <div className="space-y-4 p-4 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
                <Label className="text-sm font-medium">Quarterly ARR Goals</Label>
                {userGoals.quarterlyGoals.map((quarter, index) => (
                  <div key={quarter.quarter} className="flex items-center gap-3">
                    <span
                      className={`text-sm font-medium w-8 ${
                        index === 0
                          ? "text-blue-700 dark:text-blue-400"
                          : index === 1
                            ? "text-indigo-700 dark:text-indigo-400"
                            : index === 2
                              ? "text-violet-700 dark:text-violet-400"
                              : "text-purple-700 dark:text-purple-400"
                      }`}
                    >
                      {quarter.quarter}
                    </span>
                    <Input
                      type="number"
                      value={quarter.target}
                      onChange={(e) => {
                        const newQuarterlyGoals = [...userGoals.quarterlyGoals]
                        newQuarterlyGoals[index].target = Number(e.target.value)
                        setUserGoals({ ...userGoals, quarterlyGoals: newQuarterlyGoals })
                      }}
                    />
                  </div>
                ))}
              </div>
            </div>

            <div className="flex justify-end gap-3 mt-4">
              <Button variant="outline" onClick={() => setIsEditingGoals(false)}>
                Cancel
              </Button>
              <Button
                onClick={handleGoalUpdate}
                className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700"
              >
                Update Goals
              </Button>
            </div>
          </div>
        ) : (
          <Tabs defaultValue="weekly" className="animate-in fade-in duration-300">
            <TabsList className="grid w-full grid-cols-3 mb-6">
              <TabsTrigger
                value="weekly"
                className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-blue-600 data-[state=active]:to-indigo-600 data-[state=active]:text-white"
              >
                Weekly
              </TabsTrigger>
              <TabsTrigger
                value="monthly"
                className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-blue-600 data-[state=active]:to-indigo-600 data-[state=active]:text-white"
              >
                Monthly
              </TabsTrigger>
              <TabsTrigger
                value="quarterly"
                className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-blue-600 data-[state=active]:to-indigo-600 data-[state=active]:text-white"
              >
                Quarterly
              </TabsTrigger>
            </TabsList>

            {/* Weekly Metrics Tab */}
            <TabsContent value="weekly" className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-4">
                {weeklyMetrics.map((week, index) => {
                  // Calculate overall progress for the week
                  const metrics = [
                    calculateProgress(week.externalMeetings.actual, week.externalMeetings.target),
                    calculateProgress(week.filesShared.actual, week.filesShared.target),
                    calculateProgress(week.emailsSent.actual, week.emailsSent.target),
                    calculateProgress(week.prospectsEngaged.actual, week.prospectsEngaged.target),
                    calculateProgress(week.amplifyPosts.actual, week.amplifyPosts.target),
                    calculateProgress(week.newStakeholders?.actual || 0, week.newStakeholders?.target || 1),
                  ]
                  const avgProgress = metrics.reduce((a, b) => a + b, 0) / metrics.length

                  return (
                    <Card
                      key={index}
                      className={`overflow-hidden border ${
                        index === 0 ? "border-blue-200 dark:border-blue-800" : "border-slate-200 dark:border-slate-800"
                      }`}
                    >
                      <CardHeader
                        className={`pb-2 ${
                          index === 0 ? "bg-blue-50 dark:bg-blue-950" : "bg-slate-50 dark:bg-slate-900"
                        }`}
                      >
                        <div className="flex justify-between items-center">
                          <CardTitle className="text-lg">{week.weekName}</CardTitle>
                          {index === 0 && getStatusBadge(avgProgress)}
                        </div>
                      </CardHeader>
                      <CardContent className="space-y-4 p-4">
                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center">
                              <CalendarDays className="h-4 w-4 mr-2 text-blue-600 dark:text-blue-400" />
                              <span className="text-sm">External Meetings</span>
                            </div>
                            <span className="text-sm font-medium">
                              {week.externalMeetings.actual}/{week.externalMeetings.target}
                            </span>
                          </div>
                          <Progress
                            value={calculateProgress(week.externalMeetings.actual, week.externalMeetings.target)}
                            className="h-2"
                            indicatorClassName={getProgressColor(
                              calculateProgress(week.externalMeetings.actual, week.externalMeetings.target),
                            )}
                          />
                        </div>

                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center">
                              <FileText className="h-4 w-4 mr-2 text-indigo-600 dark:text-indigo-400" />
                              <span className="text-sm">Files Shared</span>
                            </div>
                            <span className="text-sm font-medium">
                              {week.filesShared.actual}/{week.filesShared.target}
                            </span>
                          </div>
                          <Progress
                            value={calculateProgress(week.filesShared.actual, week.filesShared.target)}
                            className="h-2"
                            indicatorClassName={getProgressColor(
                              calculateProgress(week.filesShared.actual, week.filesShared.target),
                            )}
                          />
                        </div>

                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center">
                              <Mail className="h-4 w-4 mr-2 text-violet-600 dark:text-violet-400" />
                              <span className="text-sm">Emails Sent</span>
                            </div>
                            <span className="text-sm font-medium">
                              {week.emailsSent.actual}/{week.emailsSent.target}
                            </span>
                          </div>
                          <Progress
                            value={calculateProgress(week.emailsSent.actual, week.emailsSent.target)}
                            className="h-2"
                            indicatorClassName={getProgressColor(
                              calculateProgress(week.emailsSent.actual, week.emailsSent.target),
                            )}
                          />
                        </div>

                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center">
                              <Users className="h-4 w-4 mr-2 text-purple-600 dark:text-purple-400" />
                              <span className="text-sm">Prospects Engaged</span>
                            </div>
                            <span className="text-sm font-medium">
                              {week.prospectsEngaged.actual}/{week.prospectsEngaged.target}
                            </span>
                          </div>
                          <Progress
                            value={calculateProgress(week.prospectsEngaged.actual, week.prospectsEngaged.target)}
                            className="h-2"
                            indicatorClassName={getProgressColor(
                              calculateProgress(week.prospectsEngaged.actual, week.prospectsEngaged.target),
                            )}
                          />
                        </div>

                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center">
                              <UserCheck className="h-4 w-4 mr-2 text-teal-600 dark:text-teal-400" />
                              <span className="text-sm">New Stakeholders</span>
                            </div>
                            <span className="text-sm font-medium">
                              {week.newStakeholders?.actual || 0}/{week.newStakeholders?.target || 0}
                            </span>
                          </div>
                          <Progress
                            value={calculateProgress(
                              week.newStakeholders?.actual || 0,
                              week.newStakeholders?.target || 1,
                            )}
                            className="h-2"
                            indicatorClassName={getProgressColor(
                              calculateProgress(week.newStakeholders?.actual || 0, week.newStakeholders?.target || 1),
                            )}
                          />
                        </div>

                        <div className="space-y-2">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center">
                              <MessageSquare className="h-4 w-4 mr-2 text-pink-600 dark:text-pink-400" />
                              <span className="text-sm">Amplify Posts</span>
                            </div>
                            <span className="text-sm font-medium">
                              {week.amplifyPosts.actual}/{week.amplifyPosts.target}
                            </span>
                          </div>
                          <Progress
                            value={calculateProgress(week.amplifyPosts.actual, week.amplifyPosts.target)}
                            className="h-2"
                            indicatorClassName={getProgressColor(
                              calculateProgress(week.amplifyPosts.actual, week.amplifyPosts.target),
                            )}
                          />
                        </div>
                      </CardContent>
                    </Card>
                  )
                })}
              </div>

              <div className="text-sm text-muted-foreground bg-slate-50 dark:bg-slate-900 p-3 rounded-lg border border-slate-200 dark:border-slate-800">
                <p className="flex items-center">
                  <RefreshCw className="h-4 w-4 mr-2 text-blue-600 dark:text-blue-400" />
                  Targets are automatically calculated based on your annual goals and industry benchmarks
                </p>
              </div>
            </TabsContent>

            {/* Monthly Metrics Tab */}
            <TabsContent value="monthly" className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-4">
                <Card className="border-blue-200 dark:border-blue-800 overflow-hidden">
                  <CardHeader className="pb-2 bg-blue-50 dark:bg-blue-950">
                    <CardTitle className="text-lg">Meeting Metrics</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4 p-4">
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center">
                          <Calendar className="h-4 w-4 mr-2 text-blue-600 dark:text-blue-400" />
                          <span className="text-sm">QBRs Scheduled</span>
                        </div>
                        <span className="text-sm font-medium">
                          {monthlyMetrics.qbrsScheduled?.actual}/{monthlyMetrics.qbrsScheduled?.target}
                        </span>
                      </div>
                      <Progress
                        value={calculateProgress(
                          monthlyMetrics.qbrsScheduled?.actual || 0,
                          monthlyMetrics.qbrsScheduled?.target || 1,
                        )}
                        className="h-2"
                        indicatorClassName={getProgressColor(
                          calculateProgress(
                            monthlyMetrics.qbrsScheduled?.actual || 0,
                            monthlyMetrics.qbrsScheduled?.target || 1,
                          ),
                        )}
                      />
                      {getStatusBadge(
                        calculateProgress(
                          monthlyMetrics.qbrsScheduled?.actual || 0,
                          monthlyMetrics.qbrsScheduled?.target || 1,
                        ),
                      )}
                    </div>

                    <div className="space-y-2 mt-6">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center">
                          <Users className="h-4 w-4 mr-2 text-indigo-600 dark:text-indigo-400" />
                          <span className="text-sm">In-Person Meetings</span>
                        </div>
                        <span className="text-sm font-medium">
                          {monthlyMetrics.inPersonMeetings?.actual}/{monthlyMetrics.inPersonMeetings?.target}
                        </span>
                      </div>
                      <Progress
                        value={calculateProgress(
                          monthlyMetrics.inPersonMeetings?.actual || 0,
                          monthlyMetrics.inPersonMeetings?.target || 1,
                        )}
                        className="h-2"
                        indicatorClassName={getProgressColor(
                          calculateProgress(
                            monthlyMetrics.inPersonMeetings?.actual || 0,
                            monthlyMetrics.inPersonMeetings?.target || 1,
                          ),
                        )}
                      />
                      {getStatusBadge(
                        calculateProgress(
                          monthlyMetrics.inPersonMeetings?.actual || 0,
                          monthlyMetrics.inPersonMeetings?.target || 1,
                        ),
                      )}
                    </div>
                  </CardContent>
                </Card>

                <Card className="border-indigo-200 dark:border-indigo-800 overflow-hidden">
                  <CardHeader className="pb-2 bg-indigo-50 dark:bg-indigo-950">
                    <CardTitle className="text-lg">Pipeline Generation</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4 p-4">
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center">
                          <DollarSign className="h-4 w-4 mr-2 text-indigo-600 dark:text-indigo-400" />
                          <span className="text-sm">Pipeline $ Generated</span>
                        </div>
                        <span className="text-sm font-medium">
                          {formatCurrency(monthlyMetrics.pipelineGenerated?.dollars?.actual || 0)}/
                          {formatCurrency(monthlyMetrics.pipelineGenerated?.dollars?.target || 0)}
                        </span>
                      </div>
                      <Progress
                        value={calculateProgress(
                          monthlyMetrics.pipelineGenerated?.dollars?.actual || 0,
                          monthlyMetrics.pipelineGenerated?.dollars?.target || 1,
                        )}
                        className="h-2"
                        indicatorClassName={getProgressColor(
                          calculateProgress(
                            monthlyMetrics.pipelineGenerated?.dollars?.actual || 0,
                            monthlyMetrics.pipelineGenerated?.dollars?.target || 1,
                          ),
                        )}
                      />
                      {getStatusBadge(
                        calculateProgress(
                          monthlyMetrics.pipelineGenerated?.dollars?.actual || 0,
                          monthlyMetrics.pipelineGenerated?.dollars?.target || 1,
                        ),
                      )}
                    </div>

                    <div className="space-y-2 mt-6">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center">
                          <Target className="h-4 w-4 mr-2 text-violet-600 dark:text-violet-400" />
                          <span className="text-sm">Pipeline # Generated</span>
                        </div>
                        <span className="text-sm font-medium">
                          {monthlyMetrics.pipelineGenerated?.count?.actual || 0}/
                          {monthlyMetrics.pipelineGenerated?.count?.target || 0}
                        </span>
                      </div>
                      <Progress
                        value={calculateProgress(
                          monthlyMetrics.pipelineGenerated?.count?.actual || 0,
                          monthlyMetrics.pipelineGenerated?.count?.target || 1,
                        )}
                        className="h-2"
                        indicatorClassName={getProgressColor(
                          calculateProgress(
                            monthlyMetrics.pipelineGenerated?.count?.actual || 0,
                            monthlyMetrics.pipelineGenerated?.count?.target || 1,
                          ),
                        )}
                      />
                      {getStatusBadge(
                        calculateProgress(
                          monthlyMetrics.pipelineGenerated?.count?.actual || 0,
                          monthlyMetrics.pipelineGenerated?.count?.target || 1,
                        ),
                      )}
                    </div>
                  </CardContent>
                </Card>

                <Card className="border-violet-200 dark:border-violet-800 overflow-hidden">
                  <CardHeader className="pb-2 bg-violet-50 dark:bg-violet-950">
                    <CardTitle className="text-lg">Buying Process Advances</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4 p-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center">
                            <span className="text-sm font-medium text-blue-600 dark:text-blue-400">Discovery</span>
                          </div>
                          <span className="text-sm">
                            {monthlyMetrics.buyingProcessAdvances?.discovery?.actual || 0}/
                            {monthlyMetrics.buyingProcessAdvances?.discovery?.target || 0}
                          </span>
                        </div>
                        <Progress
                          value={calculateProgress(
                            monthlyMetrics.buyingProcessAdvances?.discovery?.actual || 0,
                            monthlyMetrics.buyingProcessAdvances?.discovery?.target || 1,
                          )}
                          className="h-2"
                          indicatorClassName={getProgressColor(
                            calculateProgress(
                              monthlyMetrics.buyingProcessAdvances?.discovery?.actual || 0,
                              monthlyMetrics.buyingProcessAdvances?.discovery?.target || 1,
                            ),
                          )}
                        />
                      </div>

                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center">
                            <span className="text-sm font-medium text-indigo-600 dark:text-indigo-400">Proof</span>
                          </div>
                          <span className="text-sm">
                            {monthlyMetrics.buyingProcessAdvances?.proof?.actual || 0}/
                            {monthlyMetrics.buyingProcessAdvances?.proof?.target || 0}
                          </span>
                        </div>
                        <Progress
                          value={calculateProgress(
                            monthlyMetrics.buyingProcessAdvances?.proof?.actual || 0,
                            monthlyMetrics.buyingProcessAdvances?.proof?.target || 1,
                          )}
                          className="h-2"
                          indicatorClassName={getProgressColor(
                            calculateProgress(
                              monthlyMetrics.buyingProcessAdvances?.proof?.actual || 0,
                              monthlyMetrics.buyingProcessAdvances?.proof?.target || 1,
                            ),
                          )}
                        />
                      </div>

                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center">
                            <span className="text-sm font-medium text-violet-600 dark:text-violet-400">Proposal</span>
                          </div>
                          <span className="text-sm">
                            {monthlyMetrics.buyingProcessAdvances?.proposal?.actual || 0}/
                            {monthlyMetrics.buyingProcessAdvances?.proposal?.target || 0}
                          </span>
                        </div>
                        <Progress
                          value={calculateProgress(
                            monthlyMetrics.buyingProcessAdvances?.proposal?.actual || 0,
                            monthlyMetrics.buyingProcessAdvances?.proposal?.target || 1,
                          )}
                          className="h-2"
                          indicatorClassName={getProgressColor(
                            calculateProgress(
                              monthlyMetrics.buyingProcessAdvances?.proposal?.actual || 0,
                              monthlyMetrics.buyingProcessAdvances?.proposal?.target || 1,
                            ),
                          )}
                        />
                      </div>

                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center">
                            <span className="text-sm font-medium text-purple-600 dark:text-purple-400">Contracts</span>
                          </div>
                          <span className="text-sm">
                            {monthlyMetrics.buyingProcessAdvances?.contracts?.actual || 0}/
                            {monthlyMetrics.buyingProcessAdvances?.contracts?.target || 0}
                          </span>
                        </div>
                        <Progress
                          value={calculateProgress(
                            monthlyMetrics.buyingProcessAdvances?.contracts?.actual || 0,
                            monthlyMetrics.buyingProcessAdvances?.contracts?.target || 1,
                          )}
                          className="h-2"
                          indicatorClassName={getProgressColor(
                            calculateProgress(
                              monthlyMetrics.buyingProcessAdvances?.contracts?.actual || 0,
                              monthlyMetrics.buyingProcessAdvances?.contracts?.target || 1,
                            ),
                          )}
                        />
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="border-purple-200 dark:border-purple-800 overflow-hidden">
                  <CardHeader className="pb-2 bg-purple-50 dark:bg-purple-950">
                    <CardTitle className="text-lg">Stakeholder Engagement</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4 p-4">
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center">
                          <UserCheck className="h-4 w-4 mr-2 text-purple-600 dark:text-purple-400" />
                          <span className="text-sm">New Stakeholder Buying Windows</span>
                        </div>
                        <span className="text-sm font-medium">
                          {monthlyMetrics.newStakeholderBuyingWindows?.actual || 0}/
                          {monthlyMetrics.newStakeholderBuyingWindows?.target || 0}
                        </span>
                      </div>
                      <Progress
                        value={calculateProgress(
                          monthlyMetrics.newStakeholderBuyingWindows?.actual || 0,
                          monthlyMetrics.newStakeholderBuyingWindows?.target || 1,
                        )}
                        className="h-2"
                        indicatorClassName={getProgressColor(
                          calculateProgress(
                            monthlyMetrics.newStakeholderBuyingWindows?.actual || 0,
                            monthlyMetrics.newStakeholderBuyingWindows?.target || 1,
                          ),
                        )}
                      />
                      {getStatusBadge(
                        calculateProgress(
                          monthlyMetrics.newStakeholderBuyingWindows?.actual || 0,
                          monthlyMetrics.newStakeholderBuyingWindows?.target || 1,
                        ),
                      )}
                    </div>
                  </CardContent>
                </Card>
              </div>

              <div className="text-sm text-muted-foreground bg-slate-50 dark:bg-slate-900 p-3 rounded-lg border border-slate-200 dark:border-slate-800">
                <p className="flex items-center">
                  <RefreshCw className="h-4 w-4 mr-2 text-indigo-600 dark:text-indigo-400" />
                  Monthly targets are derived from your quarterly goals and adjusted based on historical performance
                </p>
              </div>
            </TabsContent>

            {/* Quarterly Metrics Tab */}
            <TabsContent value="quarterly" className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-4">
                <Card className="border-blue-200 dark:border-blue-800 overflow-hidden">
                  <CardHeader className="pb-2 bg-blue-50 dark:bg-blue-950">
                    <CardTitle className="text-lg">Closed Won $</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4 p-4">
                    <div className="flex flex-col items-center justify-center py-4">
                      <div className="text-3xl font-bold text-blue-700 dark:text-blue-400">
                        {formatCurrency(quarterlyMetrics.closedWonDollars?.actual || 0)}
                      </div>
                      <div className="text-sm text-muted-foreground mt-1">
                        of {formatCurrency(quarterlyMetrics.closedWonDollars?.target || 0)} target
                      </div>
                      <div className="w-full mt-4">
                        <Progress
                          value={calculateProgress(
                            quarterlyMetrics.closedWonDollars?.actual || 0,
                            quarterlyMetrics.closedWonDollars?.target || 1,
                          )}
                          className="h-3"
                          indicatorClassName={getProgressColor(
                            calculateProgress(
                              quarterlyMetrics.closedWonDollars?.actual || 0,
                              quarterlyMetrics.closedWonDollars?.target || 1,
                            ),
                          )}
                        />
                      </div>
                      <div className="text-sm font-medium mt-2">
                        {formatPercent(
                          (quarterlyMetrics.closedWonDollars?.actual || 0) /
                            (quarterlyMetrics.closedWonDollars?.target || 1),
                        )}{" "}
                        of goal
                      </div>
                      <div className="mt-2">
                        {getStatusBadge(
                          calculateProgress(
                            quarterlyMetrics.closedWonDollars?.actual || 0,
                            quarterlyMetrics.closedWonDollars?.target || 1,
                          ),
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="border-indigo-200 dark:border-indigo-800 overflow-hidden">
                  <CardHeader className="pb-2 bg-indigo-50 dark:bg-indigo-950">
                    <CardTitle className="text-lg">Closed Won Deals</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4 p-4">
                    <div className="flex flex-col items-center justify-center py-4">
                      <div className="text-3xl font-bold text-indigo-700 dark:text-indigo-400">
                        {quarterlyMetrics.closedWonDeals?.actual || 0}
                      </div>
                      <div className="text-sm text-muted-foreground mt-1">
                        of {quarterlyMetrics.closedWonDeals?.target || 0} target
                      </div>
                      <div className="w-full mt-4">
                        <Progress
                          value={calculateProgress(
                            quarterlyMetrics.closedWonDeals?.actual || 0,
                            quarterlyMetrics.closedWonDeals?.target || 1,
                          )}
                          className="h-3"
                          indicatorClassName={getProgressColor(
                            calculateProgress(
                              quarterlyMetrics.closedWonDeals?.actual || 0,
                              quarterlyMetrics.closedWonDeals?.target || 1,
                            ),
                          )}
                        />
                      </div>
                      <div className="text-sm font-medium mt-2">
                        {formatPercent(
                          (quarterlyMetrics.closedWonDeals?.actual || 0) /
                            (quarterlyMetrics.closedWonDeals?.target || 1),
                        )}{" "}
                        of goal
                      </div>
                      <div className="mt-2">
                        {getStatusBadge(
                          calculateProgress(
                            quarterlyMetrics.closedWonDeals?.actual || 0,
                            quarterlyMetrics.closedWonDeals?.target || 1,
                          ),
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>

                <Card className="border-violet-200 dark:border-violet-800 overflow-hidden">
                  <CardHeader className="pb-2 bg-violet-50 dark:bg-violet-950">
                    <CardTitle className="text-lg">Win Rate</CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4 p-4">
                    <div className="flex flex-col items-center justify-center py-4">
                      <div className="text-3xl font-bold text-violet-700 dark:text-violet-400">
                        {formatPercent(quarterlyMetrics.winRate?.actual || 0)}
                      </div>
                      <div className="text-sm text-muted-foreground mt-1">
                        of {formatPercent(quarterlyMetrics.winRate?.target || 0)} target
                      </div>
                      <div className="w-full mt-4">
                        <Progress
                          value={calculateProgress(
                            quarterlyMetrics.winRate?.actual || 0,
                            quarterlyMetrics.winRate?.target || 1,
                          )}
                          className="h-3"
                          indicatorClassName={getProgressColor(
                            calculateProgress(
                              quarterlyMetrics.winRate?.actual || 0,
                              quarterlyMetrics.winRate?.target || 1,
                            ),
                          )}
                        />
                      </div>
                      <div className="text-sm font-medium mt-2">
                        {formatPercent(
                          (quarterlyMetrics.winRate?.actual || 0) / (quarterlyMetrics.winRate?.target || 1),
                        )}{" "}
                        of goal
                      </div>
                      <div className="mt-2">
                        {getStatusBadge(
                          calculateProgress(
                            quarterlyMetrics.winRate?.actual || 0,
                            quarterlyMetrics.winRate?.target || 1,
                          ),
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>

              <Card className="border-purple-200 dark:border-purple-800 overflow-hidden">
                <CardHeader className="pb-2 bg-purple-50 dark:bg-purple-950">
                  <CardTitle className="text-lg">Annual Goal Progress</CardTitle>
                </CardHeader>
                <CardContent className="p-4">
                  <div className="space-y-6">
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center">
                          <Target className="h-4 w-4 mr-2 text-blue-600 dark:text-blue-400" />
                          <span className="text-sm">Annual Target ({formatCurrency(userGoals.annualTarget)})</span>
                        </div>
                        <span className="text-sm font-medium">
                          {formatCurrency(quarterlyMetrics.closedWonDollars?.actual || 0)} /{" "}
                          {formatCurrency(userGoals.annualTarget)}
                        </span>
                      </div>
                      <Progress
                        value={calculateProgress(
                          quarterlyMetrics.closedWonDollars?.actual || 0,
                          userGoals.annualTarget,
                        )}
                        className="h-2"
                        indicatorClassName={getProgressColor(
                          calculateProgress(quarterlyMetrics.closedWonDollars?.actual || 0, userGoals.annualTarget),
                        )}
                      />
                    </div>

                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center">
                          <Award className="h-4 w-4 mr-2 text-indigo-600 dark:text-indigo-400" />
                          <span className="text-sm">Annual Quota ({formatCurrency(userGoals.annualQuota)})</span>
                        </div>
                        <span className="text-sm font-medium">
                          {formatCurrency(quarterlyMetrics.closedWonDollars?.actual || 0)} /{" "}
                          {formatCurrency(userGoals.annualQuota)}
                        </span>
                      </div>
                      <Progress
                        value={calculateProgress(quarterlyMetrics.closedWonDollars?.actual || 0, userGoals.annualQuota)}
                        className="h-2"
                        indicatorClassName={getProgressColor(
                          calculateProgress(quarterlyMetrics.closedWonDollars?.actual || 0, userGoals.annualQuota),
                        )}
                      />
                    </div>

                    <div className="grid grid-cols-4 gap-4">
                      {userGoals.quarterlyGoals.map((quarter, index) => (
                        <div key={quarter.quarter} className="space-y-2">
                          <div className="flex items-center justify-between">
                            <span
                              className={`text-sm font-medium ${
                                index === 0
                                  ? "text-blue-700 dark:text-blue-400"
                                  : index === 1
                                    ? "text-indigo-700 dark:text-indigo-400"
                                    : index === 2
                                      ? "text-violet-700 dark:text-violet-400"
                                      : "text-purple-700 dark:text-purple-400"
                              }`}
                            >
                              {quarter.quarter}
                            </span>
                            <span className="text-sm text-muted-foreground">{formatCurrency(quarter.target)}</span>
                          </div>
                          <Progress
                            value={
                              quarter.quarter === "Q1"
                                ? calculateProgress(quarterlyMetrics.closedWonDollars?.actual || 0, quarter.target)
                                : 0
                            }
                            className="h-2"
                            indicatorClassName={
                              quarter.quarter === "Q1"
                                ? getProgressColor(
                                    calculateProgress(quarterlyMetrics.closedWonDollars?.actual || 0, quarter.target),
                                  )
                                : ""
                            }
                          />
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>

              <div className="text-sm text-muted-foreground bg-slate-50 dark:bg-slate-900 p-3 rounded-lg border border-slate-200 dark:border-slate-800">
                <p className="flex items-center">
                  <RefreshCw className="h-4 w-4 mr-2 text-violet-600 dark:text-violet-400" />
                  Quarterly targets are based on your annual goals and fiscal year split
                </p>
              </div>
            </TabsContent>
          </Tabs>
        )}
      </CardContent>
    </Card>
  )
}
