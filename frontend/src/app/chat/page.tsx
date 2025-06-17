"use client"

import { useEffect } from "react"
import Header from "../components/header"
import Footer from "../components/footer"
import ChatInterface from "../components/chat-interface"
import { Activity } from "lucide-react"

export default function ChatPage() {
  // Add animation effect when the page loads
  useEffect(() => {
    const elements = document.querySelectorAll(".reveal")
    elements.forEach((element) => {
      element.classList.add("active")
    })
  }, [])

  return (
    <div className="min-h-screen bg-white flex flex-col">
      <Header />

      <main className="flex-grow pt-24 pb-16 px-6 md:px-10">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-10 reveal">
            <div className="inline-block mb-4 pill bg-red-100 text-red-600">AI Health Assistant</div>
            <h1 className="text-3xl md:text-4xl font-bold mb-4">Chat with HealthAI</h1>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Describe your symptoms in a natural conversation and our AI system will analyze patterns to help predict
              potential health conditions.
            </p>
          </div>

          <div className="max-w-3xl mx-auto reveal">
            <div className="glass-morphism p-6 md:p-8 relative overflow-hidden">
              <div className="absolute -top-10 -right-10 w-32 h-32 bg-red-100 rounded-full blur-3xl"></div>

              <div className="flex items-center justify-between mb-6 pb-4 border-b">
                <div className="flex items-center">
                  <div className="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center mr-3">
                    <Activity size={20} className="text-red-600" />
                  </div>
                  <div>
                    <h3 className="font-medium">HealthAI Assistant</h3>
                    <p className="text-xs text-muted-foreground">AI-powered diagnosis</p>
                  </div>
                </div>
                <div className="pill bg-red-50 text-red-600 flex items-center">
                  <span className="w-2 h-2 rounded-full bg-red-500 mr-1"></span>
                  <span className="text-xs">Online</span>
                </div>
              </div>

              <ChatInterface />
            </div>

            <div className="mt-8 text-center text-sm text-muted-foreground">
              <p className="mb-2 font-medium">Important Disclaimer</p>
              <p>
                HealthAI is not a replacement for professional medical advice, diagnosis, or treatment. Always seek the
                advice of your physician or other qualified health provider with any questions you may have regarding a
                medical condition.
              </p>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}