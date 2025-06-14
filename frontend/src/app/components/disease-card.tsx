"use client"

import type React from "react"

import { useState } from "react"
import { ChevronRight } from "lucide-react"
import { cn } from "../lib/utils"

interface DiseaseCardProps {
  title: string
  description: string
  icon: React.ReactNode
  color: string
  index: number
}

const DiseaseCard = ({ title, description, icon, color, index }: DiseaseCardProps) => {
  const [isHovered, setIsHovered] = useState(false)

  return (
    <div
      className={cn("glass-card p-6 transition-all duration-500 group", isHovered ? "translate-y-[-8px]" : "")}
      style={{
        transitionDelay: `${index * 50}ms`,
        animationDelay: `${index * 100}ms`,
      }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="mb-4">
        <div
          className={cn(
            "w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-300",
            isHovered ? `${color} text-white` : `${color}/20 text-slate-700`,
          )}
        >
          {icon}
        </div>
      </div>
      <h3 className="text-lg font-semibold mb-2">{title}</h3>
      <p className="text-muted-foreground text-sm mb-4">{description}</p>
      <div className="flex items-center text-primary text-sm font-medium group cursor-pointer">
        <span>Learn more</span>
        <ChevronRight
          size={16}
          className={cn("ml-1 transform transition-transform duration-300", isHovered ? "translate-x-1" : "")}
        />
      </div>
    </div>
  )
}

export default DiseaseCard
