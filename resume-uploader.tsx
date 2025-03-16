"use client"

import type React from "react"

import { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Upload, File, X } from "lucide-react"
import { toast } from "@/hooks/use-toast"

interface ResumeUploaderProps {
  onFileUpload: (file: File) => void
}

export default function ResumeUploader({ onFileUpload }: ResumeUploaderProps) {
  const [dragActive, setDragActive] = useState(false)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()

    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0])
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault()

    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0])
    }
  }

  const handleFile = async (file: File) => {
    // Check if file is PDF, Word, or image
    const validTypes = [
      "application/pdf",
      "application/msword",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "image/jpeg",
      "image/png",
      "text/plain",
    ]

    if (validTypes.includes(file.type)) {
      setIsUploading(true)

      try {
        // In a real app, you might want to upload the file to a server first
        // For this demo, we'll just simulate a delay
        await new Promise((resolve) => setTimeout(resolve, 1000))

        setSelectedFile(file)
        onFileUpload(file)
        toast({
          title: "Resume uploaded",
          description: "Your resume has been uploaded successfully.",
        })
      } catch (error) {
        console.error("Error uploading file:", error)
        toast({
          title: "Upload failed",
          description: "There was an error uploading your resume. Please try again.",
          variant: "destructive",
        })
      } finally {
        setIsUploading(false)
      }
    } else {
      toast({
        title: "Invalid file type",
        description: "Please upload a PDF, Word document, image file, or text file.",
        variant: "destructive",
      })
    }
  }

  const removeFile = () => {
    setSelectedFile(null)
    if (inputRef.current) {
      inputRef.current.value = ""
    }
  }

  const openFileDialog = () => {
    if (inputRef.current) {
      inputRef.current.click()
    }
  }

  return (
    <div className="w-full">
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center ${isUploading ? "opacity-70 pointer-events-none" : ""} ${dragActive ? "border-primary bg-primary/5" : "border-muted-foreground/20"}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        {selectedFile ? (
          <div className="flex flex-col items-center">
            <div className="bg-muted p-4 rounded-lg mb-4 flex items-center gap-3">
              <File className="h-8 w-8 text-primary" />
              <div className="text-left">
                <p className="font-medium truncate max-w-[200px]">{selectedFile.name}</p>
                <p className="text-sm text-muted-foreground">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
              </div>
              <Button variant="ghost" size="icon" className="ml-auto" onClick={removeFile}>
                <X className="h-4 w-4" />
              </Button>
            </div>
            <p className="text-sm text-muted-foreground">File uploaded successfully. Click below to change.</p>
            <Button variant="outline" size="sm" className="mt-4" onClick={openFileDialog}>
              Choose Another File
            </Button>
          </div>
        ) : (
          <>
            <Upload className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
            <h3 className="text-lg font-semibold mb-2">Upload Your Resume</h3>
            <p className="text-muted-foreground mb-6 max-w-md mx-auto">
              Drag and drop your resume file here, or click to browse. We support PDF, Word documents, images, and text
              files.
            </p>
            <Button onClick={openFileDialog} disabled={isUploading}>
              {isUploading ? "Uploading..." : "Browse Files"}
            </Button>
          </>
        )}
      </div>

      <input
        ref={inputRef}
        type="file"
        className="hidden"
        accept=".pdf,.doc,.docx,.jpg,.jpeg,.png,.txt"
        onChange={handleChange}
      />

      <div className="mt-6">
        <h4 className="font-medium mb-3">Supported Formats</h4>
        <div className="flex flex-wrap gap-2">
          <div className="bg-muted px-3 py-1 rounded text-sm">PDF</div>
          <div className="bg-muted px-3 py-1 rounded text-sm">Word (.doc, .docx)</div>
          <div className="bg-muted px-3 py-1 rounded text-sm">Images (.jpg, .png)</div>
          <div className="bg-muted px-3 py-1 rounded text-sm">Text (.txt)</div>
        </div>
      </div>
    </div>
  )
}

