"use client";
import { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";

export default function Home() {
  const [question, setQuestion] = useState<string>("");
  const [answer, setAnswer] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const askQuestion = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setAnswer("");

    try {
      const response = await axios.post<{
        success: boolean;
        answer: string | null;
        error: string | null;
      }>(
        "http://127.0.0.1:8000/ask",
        { question },
        { headers: { "Content-Type": "application/json" } }
      );

      if (response.data.success) {
        setAnswer(response.data.answer || "No response available.");
      } else {
        setAnswer(`⚠️ Error: ${response.data.error}`);
      }
    } catch (error) {
      setAnswer("⚠️ Network error. Please try again.");
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-6 bg-black">
      <div className="bg-purple-900 p-6 rounded-lg shadow-lg w-full h-auto">
        <h1 className="text-2xl font-bold mb-4 text-center">
          Legal AI Query Engine
        </h1>
        <textarea
          className="w-full p-2 border rounded-md"
          rows={3}
          placeholder="Ask a legal or constitutional question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button
          className="w-full bg-black text-white py-2 rounded-md mt-4 hover:bg-purple-300 transition"
          onClick={askQuestion}
          disabled={loading}
        >
          {loading ? "Processing..." : "Ask Legal Consultant AI"}
        </button>
        {answer && (
          <div className="mt-4 p-3 bg-purple-900 rounded-md">
            <strong>Response:</strong>
            <ReactMarkdown>{answer}</ReactMarkdown>
          </div>
        )}
      </div>
    </main>
  );
}
