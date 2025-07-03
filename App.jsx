import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Loader2, FileText, CheckCircle, AlertCircle } from 'lucide-react'
import './App.css'

function App() {
  const [essayText, setEssayText] = useState('')
  const [keyPoints, setKeyPoints] = useState([])
  const [newKeyPoint, setNewKeyPoint] = useState('')
  const [topic, setTopic] = useState('')
  const [isGrading, setIsGrading] = useState(false)
  const [gradingResults, setGradingResults] = useState(null)

  const addKeyPoint = () => {
    if (newKeyPoint.trim()) {
      setKeyPoints([...keyPoints, newKeyPoint.trim()])
      setNewKeyPoint('')
    }
  }

  const removeKeyPoint = (index) => {
    setKeyPoints(keyPoints.filter((_, i) => i !== index))
  }

  const loadSampleData = async () => {
    try {
      const rubricResponse = await fetch('/api/sample-rubric')
      const keypointsResponse = await fetch('/api/sample-keypoints')
      
      if (rubricResponse.ok && keypointsResponse.ok) {
        const keypointsData = await keypointsResponse.json()
        setTopic(keypointsData.topic)
        setKeyPoints(keypointsData.points)
        
        // Sample essay
        setEssayText("Renewable energy is crucial for our future. It helps us move away from fossil fuels, which are harmful to the environment. Solar and wind energy are great examples of how we can generate clean power. By using these sources, we can significantly reduce our carbon footprint and combat climate change. Furthermore, the renewable energy sector is a growing industry, providing many new jobs and boosting the economy.")
      }
    } catch (error) {
      console.error('Error loading sample data:', error)
    }
  }

  const gradeEssay = async () => {
    if (!essayText.trim() || keyPoints.length === 0) {
      alert('Please provide essay text and at least one key point.')
      return
    }

    setIsGrading(true)
    setGradingResults(null)

    try {
      const response = await fetch('/api/grade', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          essay_text: essayText,
          key_points: {
            topic: topic || 'Essay Topic',
            points: keyPoints
          },
          rubric: {
            name: "Essay Quality Rubric",
            criteria: [
              {
                name: "Content Accuracy",
                weight: 0.4,
                scores: {
                  1: "Content is largely inaccurate or irrelevant.",
                  2: "Some content is accurate, but significant inaccuracies exist.",
                  3: "Content is mostly accurate with minor inaccuracies.",
                  4: "Content is highly accurate and relevant."
                }
              },
              {
                name: "Clarity and Cohesion",
                weight: 0.3,
                scores: {
                  1: "Ideas are unclear and disorganized.",
                  2: "Ideas are somewhat clear but lack cohesion.",
                  3: "Ideas are generally clear and cohesive.",
                  4: "Ideas are exceptionally clear, well-organized, and cohesive."
                }
              },
              {
                name: "Use of Evidence",
                weight: 0.3,
                scores: {
                  1: "Little to no relevant evidence provided.",
                  2: "Some evidence provided, but not well-integrated or explained.",
                  3: "Evidence is mostly relevant and adequately explained.",
                  4: "Evidence is highly relevant, well-integrated, and insightful."
                }
              }
            ]
          }
        })
      })

      if (response.ok) {
        const data = await response.json()
        setGradingResults(data.results)
      } else {
        const errorData = await response.json()
        alert('Error grading essay: ' + (errorData.error || 'Unknown error'))
      }
    } catch (error) {
      console.error('Error grading essay:', error)
      alert('Error grading essay: ' + error.message)
    } finally {
      setIsGrading(false)
    }
  }

  const getScoreColor = (score) => {
    if (score >= 3.5) return 'bg-green-100 text-green-800'
    if (score >= 2.5) return 'bg-yellow-100 text-yellow-800'
    return 'bg-red-100 text-red-800'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2 flex items-center justify-center gap-2">
            <FileText className="h-8 w-8 text-blue-600" />
            Automatic Essay Grading System
          </h1>
          <p className="text-gray-600">Grade essays using BERT similarity and custom rubrics</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Input Section */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Essay Input</CardTitle>
                <CardDescription>Enter the student's essay to be graded</CardDescription>
              </CardHeader>
              <CardContent>
                <Textarea
                  placeholder="Paste the student's essay here..."
                  value={essayText}
                  onChange={(e) => setEssayText(e.target.value)}
                  className="min-h-[200px]"
                />
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Key Points Setup</CardTitle>
                <CardDescription>Define the key points that should be covered in the essay</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <Label htmlFor="topic">Essay Topic</Label>
                  <Input
                    id="topic"
                    placeholder="Enter the essay topic..."
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                  />
                </div>
                
                <div>
                  <Label htmlFor="keypoint">Add Key Point</Label>
                  <div className="flex gap-2">
                    <Input
                      id="keypoint"
                      placeholder="Enter a key point..."
                      value={newKeyPoint}
                      onChange={(e) => setNewKeyPoint(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && addKeyPoint()}
                    />
                    <Button onClick={addKeyPoint}>Add</Button>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label>Key Points ({keyPoints.length})</Label>
                  <div className="flex flex-wrap gap-2">
                    {keyPoints.map((point, index) => (
                      <Badge
                        key={index}
                        variant="secondary"
                        className="cursor-pointer hover:bg-red-100"
                        onClick={() => removeKeyPoint(index)}
                      >
                        {point} ×
                      </Badge>
                    ))}
                  </div>
                </div>

                <div className="flex gap-2">
                  <Button onClick={loadSampleData} variant="outline">
                    Load Sample Data
                  </Button>
                  <Button 
                    onClick={gradeEssay} 
                    disabled={isGrading || !essayText.trim() || keyPoints.length === 0}
                    className="flex-1"
                  >
                    {isGrading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Grading...
                      </>
                    ) : (
                      'Grade Essay'
                    )}
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Results Section */}
          <div>
            {gradingResults ? (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <CheckCircle className="h-5 w-5 text-green-600" />
                    Grading Results
                  </CardTitle>
                  <CardDescription>
                    Total Score: <span className={`px-2 py-1 rounded text-sm font-medium ${getScoreColor(gradingResults.total_score)}`}>
                      {gradingResults.total_score.toFixed(2)}/4.0
                    </span>
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h4 className="font-semibold mb-2">Detailed Feedback:</h4>
                    <div className="bg-gray-50 p-3 rounded-md">
                      <pre className="whitespace-pre-wrap text-sm text-gray-700">
                        {gradingResults.feedback}
                      </pre>
                    </div>
                  </div>

                  <div>
                    <h4 className="font-semibold mb-2">Criterion Breakdown:</h4>
                    <div className="space-y-2">
                      {Object.entries(gradingResults).map(([key, value]) => {
                        if (key !== 'total_score' && key !== 'feedback' && typeof value === 'object') {
                          return (
                            <div key={key} className="flex justify-between items-center p-2 bg-white rounded border">
                              <span className="font-medium">{key}</span>
                              <div className="flex items-center gap-2">
                                <span className="text-sm text-gray-600">
                                  Similarity: {(value.avg_similarity * 100).toFixed(1)}%
                                </span>
                                <Badge className={getScoreColor(value.score)}>
                                  {value.score}/4
                                </Badge>
                              </div>
                            </div>
                          )
                        }
                        return null
                      })}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ) : (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <AlertCircle className="h-5 w-5 text-gray-400" />
                    Grading Results
                  </CardTitle>
                  <CardDescription>Results will appear here after grading</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-center py-8 text-gray-500">
                    <FileText className="h-12 w-12 mx-auto mb-2 opacity-50" />
                    <p>Submit an essay to see grading results</p>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

