"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Download, Check, Loader2 } from "lucide-react"
import { PDFDocument, rgb, StandardFonts } from "pdf-lib"

interface PDFExportProps {
  resumeData: {
    personalInfo?: {
      name: string
      email: string
      phone: string
      location: string
    }
    skills?: string[]
    experience?: {
      company: string
      title: string
      startDate: string
      endDate: string
      description: string[]
    }[]
    education?: {
      institution: string
      degree: string
      field: string
      graduationDate: string
    }[]
  }
  analysisResult: {
    score: number
    atsCompatibility: {
      score: number
      feedback: string
    }
    skillsMatch: {
      score: number
      feedback: string
    }
    formatStructure: {
      score: number
      feedback: string
    }
    contentQuality: {
      score: number
      feedback: string
    }
    suggestions: string[]
  }
}

export default function PDFExport({ resumeData, analysisResult }: PDFExportProps) {
  const [isGenerating, setIsGenerating] = useState(false)
  const [isGenerated, setIsGenerated] = useState(false)

  const generatePDF = async () => {
    try {
      setIsGenerating(true)
      setIsGenerated(false)

      // Create a new PDF document
      const pdfDoc = await PDFDocument.create()

      // Add a page to the document
      const page = pdfDoc.addPage([612, 792]) // Letter size
      const { width, height } = page.getSize()

      // Get the standard font
      const font = await pdfDoc.embedFont(StandardFonts.Helvetica)
      const boldFont = await pdfDoc.embedFont(StandardFonts.HelveticaBold)

      // Set up some variables for positioning
      const margin = 50
      let y = height - margin
      const lineHeight = 20

      // Add title
      page.drawText("Resume Analysis Report", {
        x: margin,
        y,
        size: 24,
        font: boldFont,
        color: rgb(0, 0, 0),
      })

      y -= lineHeight * 2

      // Add overall score
      page.drawText(`Overall Score: ${analysisResult.score}/100`, {
        x: margin,
        y,
        size: 18,
        font: boldFont,
        color: rgb(0, 0, 0),
      })

      y -= lineHeight * 2

      // Add section: ATS Compatibility
      page.drawText("ATS Compatibility", {
        x: margin,
        y,
        size: 16,
        font: boldFont,
        color: rgb(0, 0, 0),
      })

      y -= lineHeight

      page.drawText(`Score: ${analysisResult.atsCompatibility.score}/100`, {
        x: margin + 10,
        y,
        size: 12,
        font: font,
        color: rgb(0, 0, 0),
      })

      y -= lineHeight

      // Split feedback text to fit within page width
      const feedbackLines = splitTextToLines(
        analysisResult.atsCompatibility.feedback,
        font,
        12,
        width - 2 * margin - 10,
      )

      for (const line of feedbackLines) {
        page.drawText(line, {
          x: margin + 10,
          y,
          size: 12,
          font: font,
          color: rgb(0, 0, 0),
        })

        y -= lineHeight
      }

      y -= lineHeight

      // Add section: Skills Match
      page.drawText("Skills Match", {
        x: margin,
        y,
        size: 16,
        font: boldFont,
        color: rgb(0, 0, 0),
      })

      y -= lineHeight

      page.drawText(`Score: ${analysisResult.skillsMatch.score}/100`, {
        x: margin + 10,
        y,
        size: 12,
        font: font,
        color: rgb(0, 0, 0),
      })

      y -= lineHeight

      // Split feedback text to fit within page width
      const skillsLines = splitTextToLines(analysisResult.skillsMatch.feedback, font, 12, width - 2 * margin - 10)

      for (const line of skillsLines) {
        page.drawText(line, {
          x: margin + 10,
          y,
          size: 12,
          font: font,
          color: rgb(0, 0, 0),
        })

        y -= lineHeight
      }

      y -= lineHeight

      // Add section: Format & Structure
      page.drawText("Format & Structure", {
        x: margin,
        y,
        size: 16,
        font: boldFont,
        color: rgb(0, 0, 0),
      })

      y -= lineHeight

      page.drawText(`Score: ${analysisResult.formatStructure.score}/100`, {
        x: margin + 10,
        y,
        size: 12,
        font: font,
        color: rgb(0, 0, 0),
      })

      y -= lineHeight

      // Split feedback text to fit within page width
      const formatLines = splitTextToLines(analysisResult.formatStructure.feedback, font, 12, width - 2 * margin - 10)

      for (const line of formatLines) {
        page.drawText(line, {
          x: margin + 10,
          y,
          size: 12,
          font: font,
          color: rgb(0, 0, 0),
        })

        y -= lineHeight
      }

      y -= lineHeight

      // Add section: Content Quality
      page.drawText("Content Quality", {
        x: margin,
        y,
        size: 16,
        font: boldFont,
        color: rgb(0, 0, 0),
      })

      y -= lineHeight

      page.drawText(`Score: ${analysisResult.contentQuality.score}/100`, {
        x: margin + 10,
        y,
        size: 12,
        font: font,
        color: rgb(0, 0, 0),
      })

      y -= lineHeight

      // Split feedback text to fit within page width
      const contentLines = splitTextToLines(analysisResult.contentQuality.feedback, font, 12, width - 2 * margin - 10)

      for (const line of contentLines) {
        page.drawText(line, {
          x: margin + 10,
          y,
          size: 12,
          font: font,
          color: rgb(0, 0, 0),
        })

        y -= lineHeight
      }

      y -= lineHeight

      // Add section: Suggestions for Improvement
      page.drawText("Suggestions for Improvement", {
        x: margin,
        y,
        size: 16,
        font: boldFont,
        color: rgb(0, 0, 0),
      })

      y -= lineHeight

      // Add each suggestion as a bullet point
      for (const suggestion of analysisResult.suggestions) {
        // Split suggestion text to fit within page width
        const suggestionLines = splitTextToLines(`• ${suggestion}`, font, 12, width - 2 * margin - 10)

        for (const [index, line] of suggestionLines.entries()) {
          const lineText = index === 0 ? line : `  ${line}`

          page.drawText(lineText, {
            x: margin + 10,
            y,
            size: 12,
            font: font,
            color: rgb(0, 0, 0),
          })

          y -= lineHeight
        }
      }

      // Add a second page if needed for optimized resume
      if (
        resumeData &&
        (resumeData.personalInfo || resumeData.skills || resumeData.experience || resumeData.education)
      ) {
        const page2 = pdfDoc.addPage([612, 792]) // Letter size
        let y2 = height - margin

        // Add title
        page2.drawText("Optimized Resume", {
          x: margin,
          y: y2,
          size: 24,
          font: boldFont,
          color: rgb(0, 0, 0),
        })

        y2 -= lineHeight * 2

        // Add personal info
        if (resumeData.personalInfo) {
          page2.drawText(resumeData.personalInfo.name, {
            x: margin,
            y: y2,
            size: 18,
            font: boldFont,
            color: rgb(0, 0, 0),
          })

          y2 -= lineHeight

          page2.drawText(
            `${resumeData.personalInfo.email} | ${resumeData.personalInfo.phone} | ${resumeData.personalInfo.location}`,
            {
              x: margin,
              y: y2,
              size: 12,
              font: font,
              color: rgb(0, 0, 0),
            },
          )

          y2 -= lineHeight * 2
        }

        // Add skills
        if (resumeData.skills && resumeData.skills.length > 0) {
          page2.drawText("Skills", {
            x: margin,
            y: y2,
            size: 16,
            font: boldFont,
            color: rgb(0, 0, 0),
          })

          y2 -= lineHeight

          const skillsText = resumeData.skills.join(", ")
          const skillsLines = splitTextToLines(skillsText, font, 12, width - 2 * margin)

          for (const line of skillsLines) {
            page2.drawText(line, {
              x: margin,
              y: y2,
              size: 12,
              font: font,
              color: rgb(0, 0, 0),
            })

            y2 -= lineHeight
          }

          y2 -= lineHeight
        }

        // Add experience
        if (resumeData.experience && resumeData.experience.length > 0) {
          page2.drawText("Experience", {
            x: margin,
            y: y2,
            size: 16,
            font: boldFont,
            color: rgb(0, 0, 0),
          })

          y2 -= lineHeight

          for (const exp of resumeData.experience) {
            page2.drawText(`${exp.title}, ${exp.company}`, {
              x: margin,
              y: y2,
              size: 14,
              font: boldFont,
              color: rgb(0, 0, 0),
            })

            y2 -= lineHeight

            page2.drawText(`${exp.startDate} - ${exp.endDate}`, {
              x: margin,
              y: y2,
              size: 12,
              font: font,
              color: rgb(0, 0, 0),
            })

            y2 -= lineHeight

            for (const desc of exp.description) {
              const descLines = splitTextToLines(`• ${desc}`, font, 12, width - 2 * margin - 10)

              for (const [index, line] of descLines.entries()) {
                const lineText = index === 0 ? line : `  ${line}`

                page2.drawText(lineText, {
                  x: margin + 10,
                  y: y2,
                  size: 12,
                  font: font,
                  color: rgb(0, 0, 0),
                })

                y2 -= lineHeight
              }
            }

            y2 -= lineHeight
          }
        }

        // Add education
        if (resumeData.education && resumeData.education.length > 0) {
          page2.drawText("Education", {
            x: margin,
            y: y2,
            size: 16,
            font: boldFont,
            color: rgb(0, 0, 0),
          })

          y2 -= lineHeight

          for (const edu of resumeData.education) {
            page2.drawText(`${edu.degree} in ${edu.field}`, {
              x: margin,
              y: y2,
              size: 14,
              font: boldFont,
              color: rgb(0, 0, 0),
            })

            y2 -= lineHeight

            page2.drawText(`${edu.institution}, ${edu.graduationDate}`, {
              x: margin,
              y: y2,
              size: 12,
              font: font,
              color: rgb(0, 0, 0),
            })

            y2 -= lineHeight * 2
          }
        }
      }

      // Serialize the PDF to bytes
      const pdfBytes = await pdfDoc.save()

      // Create a blob from the PDF bytes
      const blob = new Blob([pdfBytes], { type: "application/pdf" })

      // Create a URL for the blob
      const url = URL.createObjectURL(blob)

      // Create a link element and trigger a download
      const link = document.createElement("a")
      link.href = url
      link.download = "resume-analysis.pdf"
      link.click()

      // Clean up
      URL.revokeObjectURL(url)

      setIsGenerated(true)
      setIsGenerating(false)
    } catch (error) {
      console.error("Error generating PDF:", error)
      setIsGenerating(false)
    }
  }

  // Helper function to split text into lines that fit within a given width
  const splitTextToLines = (text: string, font: any, fontSize: number, maxWidth: number): string[] => {
    const words = text.split(" ")
    const lines: string[] = []
    let currentLine = ""

    for (const word of words) {
      const testLine = currentLine ? `${currentLine} ${word}` : word
      const textWidth = font.widthOfTextAtSize(testLine, fontSize)

      if (textWidth <= maxWidth) {
        currentLine = testLine
      } else {
        lines.push(currentLine)
        currentLine = word
      }
    }

    if (currentLine) {
      lines.push(currentLine)
    }

    return lines
  }

  return (
    <Card>
      <CardContent className="pt-6">
        <div className="flex flex-col items-center justify-center py-6">
          <h3 className="text-xl font-semibold mb-4">Export Analysis Report</h3>
          <p className="text-muted-foreground mb-6 text-center max-w-md">
            Download a detailed PDF report of your resume analysis including scores, feedback, and suggestions for
            improvement.
          </p>

          <Button onClick={generatePDF} disabled={isGenerating} className="gap-2">
            {isGenerating ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Generating PDF...
              </>
            ) : isGenerated ? (
              <>
                <Check className="h-4 w-4" />
                Download Again
              </>
            ) : (
              <>
                <Download className="h-4 w-4" />
                Download PDF Report
              </>
            )}
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}

