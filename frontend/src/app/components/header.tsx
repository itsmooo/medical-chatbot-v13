"use client"

import { useState, useEffect } from "react"
import { cn } from "../lib/utils"
import { Button } from "../../components/ui/button"
import { Menu, X, MessageCircle, LogIn, UserPlus } from "lucide-react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { isAuthenticated, removeToken } from "../lib/auth"

const Header = () => {
  const [scrolled, setScrolled] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const pathname = usePathname()

  useEffect(() => {
    const handleScroll = () => {
      const isScrolled = window.scrollY > 20
      if (isScrolled !== scrolled) {
        setScrolled(isScrolled)
      }
    }

    window.addEventListener("scroll", handleScroll)
    return () => {
      window.removeEventListener("scroll", handleScroll)
    }
  }, [scrolled])
  
  // Check authentication status
  useEffect(() => {
    setIsLoggedIn(isAuthenticated())
    
    // Listen for storage events (for when user logs in/out in another tab)
    const handleStorageChange = () => {
      setIsLoggedIn(isAuthenticated())
    }
    
    window.addEventListener('storage', handleStorageChange)
    return () => {
      window.removeEventListener('storage', handleStorageChange)
    }
  }, [])

  const navItems = [
    { name: "Home", path: "/" },
    { name: "About", path: "/#about" },
    { name: "Diseases", path: "/#diseases" },
    { name: "How It Works", path: "/#how-it-works" },
    { name: "Chat", path: "/chat" },
  ]

  const isActive = (path: string) => {
    if (path === "/") return pathname === "/"
    return pathname.includes(path.replace("/", ""))
  }

  return (
    <header
      className={cn(
        "fixed top-0 left-0 right-0 z-50 transition-all duration-300 px-6 md:px-10 py-4",
        scrolled ? "bg-white/80 backdrop-blur-md shadow-sm" : "bg-transparent",
      )}
    >
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <Link href="/" className="flex items-center">
          <h1 className="text-xl font-semibold text-foreground mr-2">
            <span className="text-primary">PredictaHealth</span>AI
          </h1>
          <div className="h-2 w-2 rounded-full bg-primary animate-pulse-soft"></div>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center space-x-8">
          {navItems.map((item) => (
            <Link
              key={item.name}
              href={item.path}
              className={cn(
                "text-sm font-medium transition-colors relative after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 after:bg-primary after:transition-all hover:after:w-full",
                isActive(item.path) ? "text-primary after:w-full" : "text-muted-foreground hover:text-primary",
              )}
            >
              {item.name}
            </Link>
          ))}
        </nav>

        {/* Mobile Menu Toggle */}
        <div className="md:hidden">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? <X size={20} /> : <Menu size={20} />}
          </Button>
        </div>

        {/* Mobile Navigation */}
        {mobileMenuOpen && (
          <div className="absolute top-full left-0 w-full bg-white/95 backdrop-blur-md shadow-lg p-5 flex flex-col gap-4 md:hidden animate-fade-in">
            {navItems.map((item) => (
              <Link
                key={item.name}
                href={item.path}
                className={cn(
                  "text-lg font-medium py-2 border-b border-gray-100 transition-colors",
                  isActive(item.path) ? "text-primary" : "text-foreground hover:text-primary",
                )}
                onClick={() => setMobileMenuOpen(false)}
              >
                {item.name}
              </Link>
            ))}
            
            {/* Auth links for mobile */}
            {isLoggedIn ? (
              <button
                className="text-lg font-medium py-2 border-b border-gray-100 transition-colors text-foreground hover:text-primary flex items-center"
                onClick={() => {
                  removeToken();
                  setIsLoggedIn(false);
                  setMobileMenuOpen(false);
                  window.location.href = '/';
                }}
              >
                <LogIn size={16} className="mr-2" />
                Sign Out
              </button>
            ) : (
              <>
                <Link
                  href="/signin"
                  className="text-lg font-medium py-2 border-b border-gray-100 transition-colors text-foreground hover:text-primary flex items-center"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <LogIn size={16} className="mr-2" />
                  Sign In
                </Link>
                <Link
                  href="/signup"
                  className="text-lg font-medium py-2 border-b border-gray-100 transition-colors text-primary flex items-center"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <UserPlus size={16} className="mr-2" />
                  Sign Up
                </Link>
              </>
            )}
          </div>
        )}

        {/* Auth Buttons - Desktop Only */}
        <div className="hidden md:flex items-center space-x-4">
          {isLoggedIn ? (
            <>
              <Link href="/chat">
                <Button className="bg-primary hover:bg-primary/90 text-white">
                  <MessageCircle size={16} className="mr-2" />
                  Chat Diagnosis
                </Button>
              </Link>
              <Button 
                variant="ghost" 
                onClick={() => {
                  removeToken();
                  setIsLoggedIn(false);
                  window.location.href = '/';
                }}
              >
                <LogIn size={16} className="mr-2" />
                Sign Out
              </Button>
            </>
          ) : (
            <>
              <Link href="/signin">
                <Button variant="outline">
                  <LogIn size={16} className="mr-2" />
                  Sign In
                </Button>
              </Link>
              <Link href="/signup">
                <Button className="bg-primary hover:bg-primary/90 text-white">
                  <UserPlus size={16} className="mr-2" />
                  Sign Up
                </Button>
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  )
}

export default Header
