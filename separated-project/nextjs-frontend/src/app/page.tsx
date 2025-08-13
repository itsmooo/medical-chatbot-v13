'use client';

import { useEffect, useRef } from 'react';
import Header from './components/header';
import Hero from './components/hero';
import ChatInterface from './components/chat-interface';
import DiseaseCard from './components/disease-card';
import Footer from './components/footer';
import {
  Globe,
  Brain,
  Heart,
  Activity,
  Pill,
  Microscope,
  Thermometer,
  Stethoscope,
  ArrowRight,
  CheckCircle,
  Search,
  ShieldCheck,
  MessageCircle,
} from 'lucide-react';
import { Button } from '../components/ui/button';

export default function Home() {
  const sectionsRef = useRef<HTMLDivElement[]>([]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('active');
          }
        });
      },
      { threshold: 0.1 },
    );

    const currentSections = sectionsRef.current;

    currentSections.forEach((section) => {
      if (section) observer.observe(section);
    });

    return () => {
      currentSections.forEach((section) => {
        if (section) observer.unobserve(section);
      });
    };
  }, []);

  const addToRefs = (el: HTMLDivElement) => {
    if (el && !sectionsRef.current.includes(el)) {
      sectionsRef.current.push(el);
    }
  };

  const diseases = [
    {
      title: 'Diabetes',
      description:
        'AI analysis of symptoms related to glucose levels and metabolic factors.',
      icon: <Pill size={24} />,
      color: 'bg-red-500',
    },
    {
      title: 'Heart Disease',
      description:
        'Detection of cardiovascular conditions based on reported symptoms.',
      icon: <Heart size={24} />,
      color: 'bg-rose-600',
    },
    {
      title: 'Pneumonia',
      description:
        'Respiratory infection identification from breathing and cough patterns.',
      icon: <Activity size={24} />,
      color: 'bg-red-400',
    },
    {
      title: 'Neurological Disorders',
      description: 'Analysis of brain and nervous system related symptoms.',
      icon: <Brain size={24} />,
      color: 'bg-red-700',
    },
    {
      title: 'Infectious Diseases',
      description: 'Detection of bacterial and viral infection symptoms.',
      icon: <Globe size={24} />,
      color: 'bg-red-600',
    },
    {
      title: 'Cancer Screening',
      description: 'Early warning system for potential cancer indicators.',
      icon: <Microscope size={24} />,
      color: 'bg-rose-500',
    },
    {
      title: 'Thyroid Conditions',
      description:
        'Analysis of hormone-related symptoms and metabolic markers.',
      icon: <Thermometer size={24} />,
      color: 'bg-red-300',
    },
    {
      title: 'Autoimmune Diseases',
      description:
        'Detection of immune system dysfunction and related symptoms.',
      icon: <ShieldCheck size={24} />,
      color: 'bg-rose-400',
    },
  ];

  const features = [
    {
      title: 'AI-Powered Analysis',
      description:
        'Advanced machine learning algorithms analyze your symptoms in real-time.',
      icon: <Brain size={24} className="text-primary" />,
    },
    {
      title: 'Conversational Interface',
      description:
        'Natural chat experience makes describing symptoms simple and intuitive.',
      icon: <MessageCircle size={24} className="text-primary" />,
    },
    {
      title: 'Multi-Disease Detection',
      description:
        'System trained to identify patterns across 8 different disease categories.',
      icon: <Search size={24} className="text-primary" />,
    },
    {
      title: 'Privacy Focused',
      description:
        'Your health information is encrypted and never shared with third parties.',
      icon: <ShieldCheck size={24} className="text-primary" />,
    },
  ];

  return (
    <div className="min-h-screen bg-white">
      <Header />

      {/* Hero Section */}
      <Hero />

      {/* Diseases Section */}
      <section id="diseases" className="py-20 px-6 md:px-10 relative">
        <div className="max-w-7xl mx-auto">
          <div ref={addToRefs} className="text-center mb-16 reveal">
            <div className="inline-block mb-4 pill bg-primary/10 text-primary">
              Disease Prediction
            </div>
            <h2 className="text-3xl md:text-4xl font-bold mb-6">
              Our AI Can Help Identify 8 Major Diseases
            </h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Our machine learning system is trained to recognize patterns
              associated with these conditions based on reported symptoms.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {diseases.map((disease, index) => (
              <div
                key={disease.title}
                ref={addToRefs}
                className="reveal animate-scale-in"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <DiseaseCard
                  title={disease.title}
                  description={disease.description}
                  icon={disease.icon} 
                  color={disease.color}
                  index={index}
                />
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Chat Interface Section */}
      <section
        id="how-it-works"
        className="py-20 px-6 md:px-10 bg-slate-50 relative"
      >
        <div className="absolute top-0 left-0 right-0 h-20 bg-gradient-to-b from-white to-transparent"></div>
        <div ref={addToRefs} className="max-w-7xl mx-auto reveal">
          <div className="text-center mb-16">
            <div className="inline-block mb-4 pill bg-primary/10 text-primary">
              How It Works
            </div>
            <h2 className="text-3xl md:text-4xl font-bold mb-6">
              Describe Your Symptoms
            </h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Our AI-powered chat interface makes it easy to describe what
              you're feeling, just like you would to a doctor.
            </p>
          </div>

          <ChatInterface />

          <div className="mt-16 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div
                key={feature.title}
                className="text-center p-6 glass-card animate-fade-in"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="w-12 h-12 mx-auto rounded-full bg-primary/10 flex items-center justify-center mb-4">
                  {feature.icon}
                </div>
                <h3 className="font-semibold mb-2">{feature.title}</h3>
                <p className="text-muted-foreground text-sm">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* About Section */}
      <section
        id="about"
        className="py-20 px-6 md:px-10 relative overflow-hidden"
      >
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary/5 rounded-full blur-3xl"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-primary/5 rounded-full blur-3xl"></div>

        <div ref={addToRefs} className="max-w-7xl mx-auto reveal">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <div className="inline-block mb-4 pill bg-primary/10 text-primary">
                About Our Technology
              </div>
              <h2 className="text-3xl md:text-4xl font-bold mb-6">
                Advanced Machine Learning for Health
              </h2>
              <p className="text-muted-foreground mb-6">
                Our AI system uses sophisticated machine learning algorithms
                trained on vast datasets of medical information to identify
                patterns associated with various diseases.
              </p>

              <div className="space-y-4 mb-8">
                {[
                  'Natural language processing to understand symptoms',
                  'Pattern recognition across multiple disease indicators',
                  'Continuous learning from medical databases',
                  'High accuracy prediction models',
                ].map((item, i) => (
                  <div key={i} className="flex items-start">
                    <CheckCircle
                      size={20}
                      className="text-primary mr-2 flex-shrink-0 mt-0.5"
                    />
                    <p className="text-sm text-muted-foreground">{item}</p>
                  </div>
                ))}
              </div>

              <Button className="bg-primary hover:bg-primary/90 text-white">
                Learn More About Our Technology
                <ArrowRight size={16} className="ml-2" />
              </Button>
            </div>

            <div className="relative">
              <div className="w-full h-96 glass-card overflow-hidden relative">
                <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent z-0"></div>
                <div className="relative z-10 h-full flex items-center justify-center p-8">
                  <div className="text-center">
                    <Stethoscope
                      size={48}
                      className="text-primary mx-auto mb-6"
                    />
                    <h3 className="text-xl font-semibold mb-4">
                      Not A Replacement For Doctors
                    </h3>
                    <p className="text-muted-foreground text-sm">
                      Our AI system is designed to be a preliminary screening
                      tool. Always consult with healthcare professionals for
                      proper diagnosis and treatment.
                    </p>
                  </div>
                </div>
              </div>

              <div className="absolute -top-4 -left-4 w-20 h-20 rounded-full bg-primary/20 blur-xl"></div>
              <div className="absolute -bottom-6 -right-6 w-32 h-32 rounded-full bg-blue-500/10 blur-xl"></div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section
        ref={addToRefs}
        className="py-20 px-6 md:px-10 bg-gradient-to-r from-primary/10 to-primary/5 reveal"
      >
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Start Your Health Assessment Today
          </h2>
          <p className="text-muted-foreground mb-8 max-w-2xl mx-auto">
            Our AI-powered system is ready to help you understand your symptoms
            and guide you toward appropriate healthcare decisions.
          </p>
          <Button
            size="lg"
            className="bg-primary hover:bg-primary/90 text-white"
          >
            Begin Diagnosis
          </Button>
        </div>
      </section>

      {/* Footer */}
      <Footer />
    </div>
  );
}
