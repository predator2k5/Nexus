import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()

    // Forward the request to the Python backend
    const pythonApiUrl = process.env.PYTHON_API_URL || "http://localhost:5000/api/analyze-resume"

    const response = await fetch(pythonApiUrl, {
      method: "POST",
      body: formData,
    })

    if (!response.ok) {
      const errorData = await response.json()
      return NextResponse.json({ error: errorData.error || "Failed to analyze resume" }, { status: response.status })
    }

    const analysisResult = await response.json()
    return NextResponse.json(analysisResult)
  } catch (error) {
    console.error("Error analyzing resume:", error)
    return NextResponse.json({ error: "Failed to analyze resume" }, { status: 500 })
  }
}

