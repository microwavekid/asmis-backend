"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Checkbox } from "@/components/ui/checkbox"
import { Loader2 } from "lucide-react"

interface EmailGeneratorFormProps {
  onGenerate: (formData: any) => void
  isGenerating: boolean
}

export function EmailGeneratorForm({ onGenerate, isGenerating }: EmailGeneratorFormProps) {
  const [formData, setFormData] = useState({
    executiveSender: "",
    recipientEmail: "",
    relationshipSummary: "",
    actionAsk: "",
    specialConsiderations: "",
    attachments: {
      ebook: false,
      gartnerDXP: false,
      gartnerPersonalization: false,
    },
  })

  const handleChange = (field: string, value: any) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }))
  }

  const handleAttachmentChange = (attachment: string, checked: boolean) => {
    setFormData((prev) => ({
      ...prev,
      attachments: {
        ...prev.attachments,
        [attachment]: checked,
      },
    }))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onGenerate(formData)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-4">
        <h2 className="text-lg font-semibold">Email Details</h2>
        <p className="text-sm text-muted-foreground">Provide information to generate your executive email</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-2">
          <Label htmlFor="executive-sender">Executive Sender</Label>
          <Select value={formData.executiveSender} onValueChange={(value) => handleChange("executiveSender", value)}>
            <SelectTrigger id="executive-sender">
              <SelectValue placeholder="Select executive role" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="ceo">Sarah Johnson - CEO</SelectItem>
              <SelectItem value="cto">Michael Chen - CTO</SelectItem>
              <SelectItem value="cfo">David Wilson - CFO</SelectItem>
              <SelectItem value="coo">Alex Rodriguez - COO</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="recipient-email">Recipient Email</Label>
          <Input
            id="recipient-email"
            placeholder="john.doe@example.com"
            value={formData.recipientEmail}
            onChange={(e) => handleChange("recipientEmail", e.target.value)}
          />
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="relationship-summary">Relationship/Opportunity Summary</Label>
        <Textarea
          id="relationship-summary"
          placeholder="Describe the current state of the relationship or opportunity..."
          rows={4}
          value={formData.relationshipSummary}
          onChange={(e) => handleChange("relationshipSummary", e.target.value)}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="action-ask">Action/Ask</Label>
        <Textarea
          id="action-ask"
          placeholder="What action do you want the recipient to take?"
          rows={4}
          value={formData.actionAsk}
          onChange={(e) => handleChange("actionAsk", e.target.value)}
        />
      </div>

      <div className="space-y-2">
        <Label htmlFor="special-considerations">Special Considerations (Optional)</Label>
        <Textarea
          id="special-considerations"
          placeholder="Any special details the sender should consider..."
          rows={4}
          value={formData.specialConsiderations}
          onChange={(e) => handleChange("specialConsiderations", e.target.value)}
        />
      </div>

      <div className="space-y-2">
        <Label>Attachments & Resources</Label>
        <div className="space-y-2">
          <div className="flex items-start space-x-2">
            <Checkbox
              id="attachment-ebook"
              checked={formData.attachments.ebook}
              onCheckedChange={(checked) => handleAttachmentChange("ebook", checked as boolean)}
            />
            <div className="grid gap-1.5 leading-none">
              <label
                htmlFor="attachment-ebook"
                className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
              >
                Free Ebook: "Experimentation Works" by Stefan Thomke
              </label>
              <p className="text-xs text-muted-foreground">Link will be inserted in the email</p>
            </div>
          </div>

          <div className="flex items-start space-x-2">
            <Checkbox
              id="attachment-gartner-dxp"
              checked={formData.attachments.gartnerDXP}
              onCheckedChange={(checked) => handleAttachmentChange("gartnerDXP", checked as boolean)}
            />
            <div className="grid gap-1.5 leading-none">
              <label
                htmlFor="attachment-gartner-dxp"
                className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
              >
                Gartner Magic Quadrant for Digital Experience Platforms (Q1 2025)
              </label>
              <p className="text-xs text-muted-foreground">PDF attachment</p>
            </div>
          </div>

          <div className="flex items-start space-x-2">
            <Checkbox
              id="attachment-gartner-personalization"
              checked={formData.attachments.gartnerPersonalization}
              onCheckedChange={(checked) => handleAttachmentChange("gartnerPersonalization", checked as boolean)}
            />
            <div className="grid gap-1.5 leading-none">
              <label
                htmlFor="attachment-gartner-personalization"
                className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
              >
                Gartner Magic Quadrant for Personalization Engines (Q1 2025)
              </label>
              <p className="text-xs text-muted-foreground">PDF attachment</p>
            </div>
          </div>
        </div>
      </div>

      <Button
        type="submit"
        className="w-full"
        disabled={
          isGenerating ||
          !formData.executiveSender ||
          !formData.recipientEmail ||
          !formData.relationshipSummary ||
          !formData.actionAsk
        }
      >
        {isGenerating ? (
          <>
            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            Generating...
          </>
        ) : (
          "Generate Executive Email"
        )}
      </Button>
    </form>
  )
}
