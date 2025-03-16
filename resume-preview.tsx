"use client"

import { useState, useEffect } from "react"
import { Card } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { FileText } from "lucide-react"

interface ResumePreviewProps {
  file: File
}

export default function ResumePreview({ file }: ResumePreviewProps) {
  const [preview, setPreview] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!file) return

    setLoading(true)

    // For PDF files, we'd use a PDF viewer library
    // For simplicity in this demo, we'll just show image previews
    if (file.type.startsWith("image/")) {
      const reader = new FileReader()
      reader.onload = (e) => {
        setPreview(e.target?.result as string)
        setLoading(false)
      }
      reader.readAsDataURL(file)
    } else {
      // For non-image files, we'll just show a placeholder
      setTimeout(() => {
        setLoading(false)
      }, 1000)
    }
  }, [file])

  return (
    <div className="w-full">
      <h3 className="text-lg font-semibold mb-4">Resume Preview</h3>

      {loading ? (
        <div className="space-y-2">
          <Skeleton className="h-[400px] w-full" />
        </div>
      ) : preview ? (
        <div className="border rounded-lg overflow-hidden">
          <img
            src={preview || "/placeholder.svg"}
            alt="Resume preview"
            className="w-full h-auto max-h-[600px] object-contain bg-muted/30"
          />
        </div>
      ) : (
        <Card className="p-8 flex flex-col items-center justify-center h-[400px] bg-muted/10">
          <FileText className="h-16 w-16 text-muted-foreground mb-4" />
          <h4 className="text-lg font-medium mb-2">{file.name}</h4>
          <p className="text-sm text-muted-foreground">
            {file.type.includes("pdf") ? "PDF Document" : file.type.includes("word") ? "Word Document" : "Document"}
          </p>
        </Card>
      )}
    </div>
  )
}

