"use client"

import { useEffect, useState } from "react"
import Header from "../components/header"
import Footer from "../components/footer"
import ChatInterface from "../components/chat-interface"
import { Activity, Globe } from "lucide-react"
import { languages, Language } from "../lib/languages"

export default function ChatPage() {
  const [language, setLanguage] = useState<Language>('en')

  // Add animation effect when the page loads
  useEffect(() => {
    const elements = document.querySelectorAll(".reveal")
    elements.forEach((element) => {
      element.classList.add("active")
    })
  }, [])

  const currentLang = languages[language]

  return (
    <div className="min-h-screen bg-white flex flex-col">
      <Header />

      <main className="flex-grow pt-24 pb-16 px-6 md:px-10">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-10 reveal">
            <div className="inline-block mb-4 pill bg-red-100 text-red-600">{currentLang.pageTitle}</div>
            <h1 className="text-3xl md:text-4xl font-bold mb-4">{currentLang.pageHeading}</h1>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              {currentLang.pageDescription}
            </p>
            
            {/* Language Toggle */}
            <div className="mt-6 flex justify-center">
              <div className="flex items-center gap-2 bg-slate-100 rounded-full p-1 shadow-sm">
                <Globe className="w-4 h-4 text-slate-600" />
                <button
                  onClick={() => setLanguage('en')}
                  className={`text-sm px-4 py-2 rounded-full transition-all duration-200 ${
                    language === 'en' 
                      ? 'bg-white text-blue-600 shadow-md font-medium' 
                      : 'text-slate-600 hover:text-slate-800'
                  }`}
                >
                  {languages.en.english}
                </button>
                <button
                  onClick={() => setLanguage('so')}
                  className={`text-sm px-4 py-2 rounded-full transition-all duration-200 ${
                    language === 'so' 
                      ? 'bg-white text-blue-600 shadow-md font-medium' 
                      : 'text-slate-600 hover:text-slate-800'
                  }`}
                >
                  {languages.so.somali}
                </button>
              </div>
            </div>
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
                    <h3 className="font-medium">{currentLang.aiAssistant}</h3>
                    <p className="text-xs text-muted-foreground">{currentLang.aiPowered}</p>
                  </div>
                </div>
                <div className="pill bg-red-50 text-red-600 flex items-center">
                  <span className="w-2 h-2 rounded-full bg-red-500 mr-1"></span>
                  <span className="text-xs">{currentLang.online}</span>
                </div>
              </div>

              <ChatInterface language={language} />
            </div>

            <div className="mt-8 text-center text-sm text-muted-foreground">
              <p className="mb-2 font-medium">
                {language === 'en' ? 'Important Disclaimer' : 'Digniin Muhiim ah'}
              </p>
              <p>
                {language === 'en' 
                  ? 'HealthAI is not a replacement for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.'
                  : 'HealthAI ma aha mid ku beddelaya talo caafimaad oo professional ah, diagnosis, ama daaweyn. Mar walba raadi talada dhakhaatiirkaaga ama caafimaad kale oo u qaloon ah oo aad ku doon lahayd su\'aalo aad ka qabtid ku saabsan xaalad caafimaad.'
                }
              </p>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}