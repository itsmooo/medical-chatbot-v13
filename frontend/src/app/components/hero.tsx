"use client"

import { Button } from "../../components/ui/button"
import { ChevronRight, Activity, Shield } from "lucide-react"
import { useEffect, useRef } from "react"
import Link from "next/link"

const Hero = () => {
  const elementsRef = useRef<HTMLDivElement[]>([])

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("active")
            observer.unobserve(entry.target)
          }
        })
      },
      { threshold: 0.1 },
    )

    const currentElements = elementsRef.current

    currentElements.forEach((el) => {
      if (el) observer.observe(el)
    })

    return () => {
      currentElements.forEach((el) => {
        if (el) observer.unobserve(el)
      })
    }
  }, [])

  const addToRefs = (el: HTMLDivElement) => {
    if (el && !elementsRef.current.includes(el)) {
      elementsRef.current.push(el)
    }
  }

  return (
    <div className="relative min-h-screen flex flex-col items-center justify-center px-6 md:px-10 overflow-hidden">
      <div className="hero-gradient absolute inset-0 z-0"></div>

      {/* Abstract shapes */}
      <div className="absolute top-1/4 -left-20 h-64 w-64 rounded-full bg-primary/5 blur-3xl"></div>
      <div className="absolute bottom-1/4 -right-20 h-72 w-72 rounded-full bg-primary/5 blur-3xl"></div>

      <div className="max-w-6xl mx-auto z-10 pt-20">
        <div className="text-center mb-16 mt-16">
          <div ref={addToRefs} className="reveal inline-block mb-4 pill bg-primary/10 text-primary">
            AI-Powered Health Diagnosis
          </div>

          <h1 ref={addToRefs} className="reveal text-4xl md:text-5xl lg:text-6xl font-bold mb-6 leading-tight">
            Advanced Disease Prediction
            <br />
            <span className="text-primary">Powered by AI</span>
          </h1>

          <p ref={addToRefs} className="reveal text-muted-foreground max-w-2xl mx-auto mb-10 text-lg">
            Describe your symptoms in a natural conversation and our AI system will analyze patterns to help predict
            potential health conditions.
          </p>

          <div ref={addToRefs} className="reveal flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="/chat">
              <Button size="lg" className="bg-primary hover:bg-primary/90 text-white">
                Start Diagnosis
                <ChevronRight size={16} className="ml-1" />
              </Button>
            </Link>
            <Link href="/#how-it-works">
              <Button size="lg" variant="outline">
                Learn More
              </Button>
            </Link>
          </div>
        </div>

        <div
          ref={addToRefs}
          className="reveal glass-morphism rounded-3xl p-6 md:p-8 max-w-4xl mx-auto overflow-hidden animate-float"
        >
          <div className="flex flex-col items-center">
            <div className="absolute -top-10 -right-10 w-32 h-32 bg-primary/10 rounded-full blur-3xl"></div>
            <div className="mb-4 text-center">
              <h3 className="text-xl font-semibold mb-2">Chat with HealthAI</h3>
              <p className="text-muted-foreground text-sm">Describe your symptoms for an AI-powered analysis</p>
            </div>

            <div className="w-full h-[300px] md:h-[350px] rounded-2xl bg-slate-50 p-4 overflow-hidden relative">
              <div className="chat-container h-full overflow-y-auto pb-16">
                <div className="space-y-4">
                  {/* AI Message */}
                  <div className="flex items-start gap-3 animate-fade-in">
                    <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center">
                      <Activity size={16} className="text-primary" />
                    </div>
                    <div className="bg-slate-100 rounded-2xl rounded-tl-none p-3 max-w-[80%]">
                      <p className="text-sm">
                        Hello, I'm HealthAI. How can I help you today? Please describe any symptoms you're experiencing.
                      </p>
                    </div>
                  </div>

                  {/* User Message */}
                  <div className="flex items-start gap-3 justify-end animate-fade-in animation-delay-200">
                    <div className="bg-primary/10 rounded-2xl rounded-tr-none p-3 max-w-[80%]">
                      <p className="text-sm">
                        I've been having a headache for the past 3 days, with some fever and fatigue.
                      </p>
                    </div>
                    <div className="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center">
                      <Shield size={16} className="text-slate-500" />
                    </div>
                  </div>

                  {/* AI Message */}
                  <div className="flex items-start gap-3 animate-fade-in animation-delay-400">
                    <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center">
                      <Activity size={16} className="text-primary" />
                    </div>
                    <div className="bg-slate-100 rounded-2xl rounded-tl-none p-3 max-w-[80%]">
                      <p className="text-sm">
                        I understand you're experiencing headaches, fever, and fatigue. Could you tell me if you have
                        any other symptoms like muscle aches, sore throat, or congestion?
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="absolute bottom-0 left-0 right-0 p-3 bg-white border-t border-slate-100">
                <div className="relative">
                  <input
                    type="text"
                    placeholder="Describe your symptoms..."
                    className="w-full rounded-full py-2 px-4 pr-10 border border-slate-200 focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary text-sm"
                  />
                  <Button
                    size="sm"
                    className="absolute right-1 top-[2px] rounded-full w-8 h-8 p-0 bg-primary hover:bg-primary/90"
                  >
                    <ChevronRight size={16} className="text-white" />
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Hero
