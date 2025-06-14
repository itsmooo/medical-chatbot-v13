import { Heart } from "lucide-react"

const Footer = () => {
  return (
    <footer className="bg-white border-t border-slate-100 py-12 px-6 md:px-10">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="md:col-span-1">
            <div className="mb-4">
              <h1 className="text-xl font-semibold text-foreground">
                <span className="text-primary">Health</span>AI
              </h1>
            </div>
            <p className="text-muted-foreground text-sm mb-4">
              AI-powered disease prediction system for early detection and prevention.
            </p>
            <div className="flex items-center text-sm text-muted-foreground">
              <Heart size={14} className="text-primary mr-1" />
              <span>Made with care for better health</span>
            </div>
          </div>

          <div>
            <h3 className="font-medium mb-4">Explore</h3>
            <ul className="space-y-2">
              {["Home", "About", "Diseases", "How It Works", "Contact"].map((item) => (
                <li key={item}>
                  <a href="#" className="text-muted-foreground hover:text-primary transition-colors text-sm">
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-medium mb-4">Resources</h3>
            <ul className="space-y-2">
              {["Documentation", "Research", "Help Center", "Privacy Policy", "Terms of Service"].map((item) => (
                <li key={item}>
                  <a href="#" className="text-muted-foreground hover:text-primary transition-colors text-sm">
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-medium mb-4">Connect</h3>
            <ul className="space-y-2">
              {["Twitter", "LinkedIn", "Instagram", "Email", "Support"].map((item) => (
                <li key={item}>
                  <a href="#" className="text-muted-foreground hover:text-primary transition-colors text-sm">
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="border-t border-slate-100 mt-10 pt-6 flex flex-col md:flex-row justify-between items-center">
          <p className="text-sm text-muted-foreground">
            &copy; {new Date().getFullYear()} HealthAI. All rights reserved.
          </p>
          <div className="flex items-center space-x-4 mt-4 md:mt-0">
            <a href="#" className="text-sm text-muted-foreground hover:text-primary transition-colors">
              Privacy Policy
            </a>
            <a href="#" className="text-sm text-muted-foreground hover:text-primary transition-colors">
              Terms of Service
            </a>
            <a href="#" className="text-sm text-muted-foreground hover:text-primary transition-colors">
              Cookie Policy
            </a>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
