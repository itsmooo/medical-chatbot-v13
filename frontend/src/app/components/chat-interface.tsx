'use client';

import type React from 'react';
import { useState, useRef, useEffect } from 'react';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { Send, Activity, User, Loader2, AlertCircle } from 'lucide-react';
import { cn } from '../lib/utils';
import axios from 'axios';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

interface Disease {
  name: string;
  probability: number;
  description?: string;
  recommendations?: string[];
  precautions?: string[];
}

interface ApiResponse {
  disease: string;
  confidence: number;
  precautions: string[];
  lang: string;
  debug_info?: {
    detected_language: string;
    original_disease: string;
    precautions_count: number;
  };
  prediction_id?: string | null;
  translated_text?: string[];
  translation_method?: string;
}

const ChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: "Hello, I'm HealthAI. Please describe any symptoms you're experiencing, and I'll help predict potential conditions.",
      sender: 'ai',
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [language, setLanguage] = useState<'en' | 'so'>('so'); // Default to Somali
  const [predictions, setPredictions] = useState<Record<string, ApiResponse>>({}); // Store raw API responses by message ID
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  // Effect to update message content when language changes
  useEffect(() => {
    if (Object.keys(predictions).length === 0) return;
    
    setMessages(prevMessages => {
      return prevMessages.map(msg => {
        // Only update AI messages that have prediction data
        if (msg.sender === 'ai' && predictions[msg.id]) {
          return {
            ...msg,
            text: formatPredictionResponse(predictions[msg.id], language)
          };
        }
        return msg;
      });
    });
  }, [language]);

  const formatPredictionResponse = (data: ApiResponse, lang: 'en' | 'so' = 'en'): string => {
    if (!data.disease || data.confidence <= 0) {
      return "I couldn't make a confident prediction based on your symptoms.";
    }

    let response = '';
    const confidencePercent = Math.round(data.confidence * 100);

    // Disease with confidence
    response = `Based on your symptoms, you might be experiencing **${data.disease}** (${confidencePercent}% confidence).\n\n`;

    // Add precautions based on selected language
    const useSomali = lang === 'so' && data.translated_text && data.translated_text.length > 0;
    const precautionsList = useSomali ? data.translated_text : data.precautions;
    
    if (precautionsList && precautionsList.length > 0) {
      response += `**${useSomali ? 'Taxaddarrada:' : 'Precautions:'}**\n`;
      precautionsList.forEach((prec) => {
        response += `• ${prec}\n`;
      });
      response += '\n';
    }

    response +=
      '⚠️ **Important:** This is not a medical diagnosis. Please consult a healthcare professional for proper evaluation and treatment.';

    return response;
  };

  const handleSend = async () => {
    if (inputValue.trim() === '') return;

    const userInput = inputValue.trim();

    // Add user message
    const newUserMessage: Message = {
      id: Date.now().toString(),
      text: userInput,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, newUserMessage]);
    setInputValue('');
    setIsTyping(true);

    try {
      console.log('Sending request to backend...');

      const response = await axios.post<ApiResponse>(
        'http://localhost:5000/predict',
        {
          symptoms: userInput,
        },
        {
          // timeout: 30000, // 30 second timeout
          headers: {
            'Content-Type': 'application/json',
          },
        },
      );

      console.log('Backend response:', response.data);

      let finalResponse = '';
      
      if (response.data.disease) {
        // We have a valid prediction
        finalResponse = formatPredictionResponse(response.data, language);
        
        // Store the raw API response for language switching
        const messageId = (Date.now() + 1).toString();
        setPredictions(prev => ({
          ...prev,
          [messageId]: response.data
        }));
        
        // Log debug info if available
        if (response.data.debug_info) {
          console.log('Debug info:', response.data.debug_info);
        }
      } else {
        // Handle error case
        finalResponse = "I couldn't analyze your symptoms properly.";
        console.error('Unexpected response format:', response.data);
      }

      const newAiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: finalResponse,
        sender: 'ai',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, newAiMessage]);
    } catch (error) {
      console.error('Error in prediction:', error);

      let errorMessage =
        "I apologize, but I'm having trouble analyzing your symptoms right now.";

      if (axios.isAxiosError(error)) {
        if (error.code === 'ECONNREFUSED') {
          errorMessage =
            'Cannot connect to the prediction service. Please make sure the backend server is running.';
        } else if (error.response?.status === 500) {
          errorMessage =
            'The prediction service encountered an error. Please try again with different symptoms.';
        } else if (error.response?.status === 400) {
          errorMessage = 'Please provide valid symptom information.';
        }
      }

      const errorAiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: errorMessage,
        sender: 'ai',
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorAiMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const formatMessageText = (text: string) => {
    // Simple markdown-like formatting
    return text.split('\n').map((line, index) => {
      if (line.startsWith('**') && line.endsWith('**')) {
        return (
          <div key={index} className="font-semibold text-slate-800 mt-2 mb-1">
            {line.slice(2, -2)}
          </div>
        );
      }
      if (line.startsWith('• ')) {
        return (
          <div key={index} className="ml-4 text-slate-700">
            {line}
          </div>
        );
      }
      if (line.includes('⚠️')) {
        return (
          <div
            key={index}
            className="mt-3 p-2 bg-amber-50 border-l-4 border-amber-400 text-amber-800 text-xs"
          >
            <AlertCircle className="inline w-4 h-4 mr-1" />
            {line}
          </div>
        );
      }
      return line ? (
        <div key={index} className="text-slate-700">
          {line}
        </div>
      ) : (
        <div key={index} className="h-2" />
      );
    });
  };

  return (
    <div className="w-full h-[600px] flex flex-col bg-white rounded-lg shadow-sm border">
      {/* Header */}
      <div className="p-4 border-b bg-slate-50 rounded-t-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Activity className="w-5 h-5 text-blue-600" />
            <h2 className="font-semibold text-slate-800">HealthAI Assistant</h2>
          </div>
          
          {/* Language Toggle */}
          <div className="flex items-center gap-1 bg-slate-200 rounded-full p-1">
            <button
              onClick={() => setLanguage('en')}
              className={`text-xs px-3 py-1 rounded-full transition-colors ${language === 'en' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600'}`}
            >
              English
            </button>
            <button
              onClick={() => setLanguage('so')}
              className={`text-xs px-3 py-1 rounded-full transition-colors ${language === 'so' ? 'bg-white text-blue-600 shadow-sm' : 'text-slate-600'}`}
            >
              Somali
            </button>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={cn(
              'flex items-start gap-3 animate-in slide-in-from-bottom-2 duration-300',
              message.sender === 'user' ? 'justify-end' : '',
            )}
          >
            {message.sender === 'ai' && (
              <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center flex-shrink-0">
                <Activity size={16} className="text-blue-600" />
              </div>
            )}

            <div
              className={cn(
                'rounded-2xl p-3 max-w-[85%] text-sm',
                message.sender === 'ai'
                  ? 'bg-slate-50 rounded-tl-none border'
                  : 'bg-blue-600 text-white rounded-tr-none',
              )}
            >
              <div className="space-y-1">
                {message.sender === 'ai' ? (
                  formatMessageText(message.text)
                ) : (
                  <p>{message.text}</p>
                )}
              </div>
              <div
                className={cn(
                  'text-xs mt-2 opacity-70',
                  message.sender === 'ai' ? 'text-slate-500' : 'text-blue-100',
                )}
              >
                {message.timestamp.toLocaleTimeString([], {
                  hour: '2-digit',
                  minute: '2-digit',
                })}
              </div>
            </div>

            {message.sender === 'user' && (
              <div className="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center flex-shrink-0">
                <User size={16} className="text-slate-600" />
              </div>
            )}
          </div>
        ))}

        {isTyping && (
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center">
              <Activity size={16} className="text-blue-600" />
            </div>
            <div className="bg-slate-50 rounded-2xl rounded-tl-none p-3 border">
              <div className="flex gap-1">
                <div className="w-2 h-2 rounded-full bg-slate-400 animate-pulse"></div>
                <div
                  className="w-2 h-2 rounded-full bg-slate-400 animate-pulse"
                  style={{ animationDelay: '0.2s' }}
                ></div>
                <div
                  className="w-2 h-2 rounded-full bg-slate-400 animate-pulse"
                  style={{ animationDelay: '0.4s' }}
                ></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t bg-slate-50 rounded-b-lg">
        <div className="relative">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Describe your symptoms (e.g., headache, fever, nausea)..."
            className="pr-14 focus-visible:ring-blue-500 border-slate-300"
            disabled={isTyping}
          />
          <Button
            onClick={handleSend}
            disabled={inputValue.trim() === '' || isTyping}
            className="absolute right-1 top-1 h-8 w-8 p-0 rounded-full bg-blue-600 hover:bg-blue-700"
          >
            {isTyping ? (
              <Loader2 size={16} className="animate-spin" />
            ) : (
              <Send size={16} />
            )}
          </Button>
        </div>
        <p className="text-xs text-slate-500 mt-2 text-center">
          HealthAI is not a replacement for professional medical advice. Always
          consult a healthcare provider.
        </p>
      </div>
    </div>
  );
};

export default ChatInterface;
