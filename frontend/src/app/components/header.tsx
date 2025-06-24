"use client"

import { useState, useEffect, useRef } from "react"
import { cn } from "../lib/utils"
import { Button } from "../../components/ui/button"
import { Menu, X, MessageCircle, LogIn, UserPlus, User, History, ChevronDown, Settings, LogOut } from "lucide-react"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { isAuthenticated, removeToken, getAuthUser } from "../lib/auth"

const Header = () => {
  const [scrolled, setScrolled] = useState(false)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [userDropdownOpen, setUserDropdownOpen] = useState(false)
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [userName, setUserName] = useState('')
  const [userEmail, setUserEmail] = useState('')
  const [userRole, setUserRole] = useState('')
  const pathname = usePathname()
  const dropdownRef = useRef<HTMLDivElement>(null)

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

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setUserDropdownOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [])
  
  // Check authentication status
  useEffect(() => {
    const isLoggedInNow = isAuthenticated();
    setIsLoggedIn(isLoggedInNow);
    
    if (isLoggedInNow) {
      const user = getAuthUser();
      console.log('User info from token:', user); // Debug log
      if (user) {
        setUserName(user.name || '');
        setUserEmail(user.email || '');
        setUserRole(user.role || '');
      }
    } else {
      setUserName('');
      setUserEmail('');
      setUserRole('');
    }
    
    // Listen for storage events (for when user logs in/out in another tab)
    const handleStorageChange = () => {
      const isLoggedInAfterChange = isAuthenticated();
      setIsLoggedIn(isLoggedInAfterChange);
      
      if (isLoggedInAfterChange) {
        const user = getAuthUser();
        if (user) {
          setUserName(user.name || '');
          setUserEmail(user.email || '');
          setUserRole(user.role || '');
        }
      } else {
        setUserName('');
        setUserEmail('');
        setUserRole('');
      }
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

  const handleSignOut = () => {
    removeToken();
    setIsLoggedIn(false);
    setUserName('');
    setUserEmail('');
    setUserRole('');
    setUserDropdownOpen(false);
    window.location.href = '/';
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
              <>
                <Link
                  href="/profile"
                  className="text-lg font-medium py-2 border-b border-gray-100 transition-colors text-foreground hover:text-primary flex items-center"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <User size={16} className="mr-2" />
                  <span className="font-medium">{userName || 'Profile'}</span>
                  {userRole && <span className="text-xs text-gray-500 ml-2">({userRole})</span>}
                </Link>
                <Link
                  href="/history"
                  className="text-lg font-medium py-2 border-b border-gray-100 transition-colors text-foreground hover:text-primary flex items-center"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  <History size={16} className="mr-2" />
                  Medical History
                </Link>
                <button
                  className="text-lg font-medium py-2 border-b border-gray-100 transition-colors text-foreground hover:text-primary flex items-center"
                  onClick={() => {
                    handleSignOut();
                    setMobileMenuOpen(false);
                  }}
                >
                  <LogOut size={16} className="mr-2" />
                  Sign Out
                </button>
              </>
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
              
              {/* User Dropdown */}
              <div className="relative" ref={dropdownRef}>
                <button
                  onClick={() => setUserDropdownOpen(!userDropdownOpen)}
                  className="flex items-center space-x-2 hover:bg-gray-100 rounded-lg px-3 py-2 transition-colors"
                >
                  <div className="h-8 w-8 rounded-full bg-primary text-white flex items-center justify-center">
                    {userName ? userName.charAt(0).toUpperCase() : 'U'}
                  </div>
                  <div className="flex flex-col items-start">
                    <span className="font-medium text-sm">{userName || 'User'}</span>
                    {userRole && <span className="text-xs text-gray-500">{userRole}</span>}
                  </div>
                  <ChevronDown 
                    size={16} 
                    className={cn(
                      "transition-transform duration-200",
                      userDropdownOpen ? "rotate-180" : ""
                    )}
                  />
                </button>

                {/* Dropdown Menu */}
                {userDropdownOpen && (
                  <div className="absolute right-0 mt-2 w-56 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50">
                    {/* User Info Header */}
                    <div className="px-4 py-3 border-b border-gray-100">
                      <div className="flex items-center space-x-3">
                        <div className="h-10 w-10 rounded-full bg-primary text-white flex items-center justify-center">
                          {userName ? userName.charAt(0).toUpperCase() : 'U'}
                        </div>
                        <div className="flex flex-col">
                          <span className="font-medium text-sm">{userName || 'User'}</span>
                          <span className="text-xs text-gray-500">{userEmail}</span>
                          {userRole && (
                            <span className="text-xs bg-primary/10 text-primary px-2 py-1 rounded-full mt-1 w-fit">
                              {userRole}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>

                    {/* Menu Items */}
                    <div className="py-1">
                      <Link
                        href="/profile"
                        className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                        onClick={() => setUserDropdownOpen(false)}
                      >
                        <User size={16} className="mr-3" />
                        Profile Settings
                      </Link>
                      
                      <Link
                        href="/history"
                        className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                        onClick={() => setUserDropdownOpen(false)}
                      >
                        <History size={16} className="mr-3" />
                        Medical History
                      </Link>
                      
                      <div className="border-t border-gray-100 my-1"></div>
                      
                      <button
                        onClick={handleSignOut}
                        className="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
                      >
                        <LogOut size={16} className="mr-3" />
                        Sign Out
                      </button>
                    </div>
                  </div>
                )}
              </div>
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
