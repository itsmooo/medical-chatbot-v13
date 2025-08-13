"use client";

import { useEffect, useState } from 'react';
import { getAuthUser, isAuthenticated, authFetch } from '../lib/auth';
import { useRouter } from 'next/navigation';
// @ts-ignore - Ignore missing type declarations for react-pdf
import { PDFDownloadLink, Document, Page, Text, View, StyleSheet, Font } from '@react-pdf/renderer';
import Header from '../components/header';
import Footer from '../components/footer';

// Register fonts for PDF
Font.register({
  family: 'Roboto',
  fonts: [
    { src: 'https://cdnjs.cloudflare.com/ajax/libs/ink/3.1.10/fonts/Roboto/roboto-regular-webfont.ttf', fontWeight: 'normal' },
    { src: 'https://cdnjs.cloudflare.com/ajax/libs/ink/3.1.10/fonts/Roboto/roboto-bold-webfont.ttf', fontWeight: 'bold' },
  ]
});

// PDF styles
const styles = StyleSheet.create({
  page: {
    flexDirection: 'column',
    backgroundColor: '#FFFFFF',
    padding: 30,
    fontFamily: 'Roboto',
  },
  header: {
    fontSize: 24,
    marginBottom: 20,
    textAlign: 'center',
    color: '#4F46E5', // Primary color
    fontWeight: 'bold',
  },
  subheader: {
    fontSize: 18,
    marginBottom: 10,
    color: '#4F46E5',
    fontWeight: 'bold',
  },
  section: {
    margin: 10,
    padding: 10,
    borderRadius: 5,
    backgroundColor: '#F3F4F6',
  },
  predictionItem: {
    marginBottom: 15,
    padding: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#E5E7EB',
    borderBottomStyle: 'solid',
  },
  label: {
    fontSize: 12,
    color: '#6B7280',
    marginBottom: 3,
  },
  value: {
    fontSize: 14,
    marginBottom: 5,
  },
  precautionItem: {
    fontSize: 12,
    marginBottom: 3,
  },
  footer: {
    position: 'absolute',
    bottom: 30,
    left: 30,
    right: 30,
    textAlign: 'center',
    color: '#6B7280',
    fontSize: 10,
  },
  userInfo: {
    marginBottom: 20,
    padding: 10,
    borderRadius: 5,
    backgroundColor: '#EEF2FF',
  },
});

// Define types for our data
interface User {
  id: string;
  name: string;
  email: string;
  role: string;
}

interface Prediction {
  _id: string;
  user_id: string;
  symptoms_original: string;
  prediction_displayed: string;
  prediction_actual_en: string;
  probability: number;
  confidence_percentage?: string;
  precautions: string[];
  timestamp: string;
  formatted_date?: string;
  language_original: string;
}

// PDF Document component
const MedicalHistoryPDF = ({ user, predictions }: { user: User | null, predictions: Prediction[] }) => (
  <Document>
    <Page size="A4" style={styles.page}>
      <Text style={styles.header}>Medical History Report</Text>
      
      <View style={styles.userInfo}>
        <Text style={styles.subheader}>Patient Information</Text>
        <Text style={styles.label}>Name:</Text>
        <Text style={styles.value}>{user?.name || 'Unknown'}</Text>
        <Text style={styles.label}>Email:</Text>
        <Text style={styles.value}>{user?.email || 'Unknown'}</Text>
      </View>
      
      <Text style={styles.subheader}>Prediction History</Text>
      
      {predictions.length === 0 ? (
        <Text>No prediction history available.</Text>
      ) : (
        predictions.map((prediction, index) => (
          <View key={index} style={styles.predictionItem}>
            <Text style={styles.label}>Date:</Text>
            <Text style={styles.value}>
              {new Date(prediction.timestamp).toLocaleString()}
            </Text>
            
            <Text style={styles.label}>Symptoms:</Text>
            <Text style={styles.value}>{prediction.symptoms_original}</Text>
            
            <Text style={styles.label}>Diagnosis:</Text>
            <Text style={styles.value}>{prediction.prediction_displayed}</Text>
            
            <Text style={styles.label}>Confidence:</Text>
            <Text style={styles.value}>{(prediction.probability * 100).toFixed(2)}%</Text>
            
            <Text style={styles.label}>Precautions:</Text>
            {prediction.precautions.map((precaution, i) => (
              <Text key={i} style={styles.precautionItem}>• {precaution}</Text>
            ))}
          </View>
        ))
      )}
      
      <Text style={styles.footer}>
        Generated on {new Date().toLocaleString()} | Medical Prediction System
      </Text>
    </Page>
  </Document>
);

// History page component
export default function HistoryPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isPdfReady, setIsPdfReady] = useState(false);

  useEffect(() => {
    // Check if user is authenticated
    if (!isAuthenticated()) {
      router.push('/signin');
      return;
    }
    
    // Get user information from token
    const authUser = getAuthUser();
    setUser(authUser);
    
    // Fetch user's prediction history
    const fetchHistory = async () => {
      try {
        // Use the correct API URL (no /api prefix since we're calling the backend directly)
        const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:5000';
        const response = await authFetch(`${backendUrl}/history?user_id=${authUser.id}`);
        
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error((errorData as any).message || 'Failed to fetch history');
        }
        
        const data = await response.json();
        
        // Check if the response has the new format with predictions array
        if (data.status === 'success' && Array.isArray(data.predictions)) {
          setPredictions(data.predictions);
        } else if (Array.isArray(data)) {
          // Handle old format for backward compatibility
          setPredictions(data);
        } else {
          setPredictions([]);
          console.warn('Unexpected data format from history API:', data);
        }
        
        setIsPdfReady(true);
      } catch (err) {
        console.error('Error fetching history:', err);
        setError(err instanceof Error ? err.message : 'An unknown error occurred');
      } finally {
        setLoading(false);
      }
    };
    
    fetchHistory();
  }, [router]);
  
  // Format date for display
  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  if (loading) {
    return (
      <>
        <Header />
        <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-teal-50 pt-20 flex justify-center items-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
        </div>
        <Footer />
      </>
    );
  }

  if (error) {
    return (
      <>
        <Header />
        <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-teal-50 pt-20">
          <div className="container mx-auto px-4 py-8">
            <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-md overflow-hidden">
              <div className="bg-red-500 text-white px-6 py-4">
                <h1 className="text-2xl font-bold">Error</h1>
              </div>
              <div className="p-6">
                <p className="text-red-500">{error}</p>
                <button 
                  onClick={() => router.push('/')}
                  className="mt-4 px-4 py-2 bg-primary text-white rounded hover:bg-primary-dark"
                >
                  Return to Home
                </button>
              </div>
            </div>
          </div>
        </div>
        <Footer />
      </>
    );
  }
  
  return (
    <>
      <Header />
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-teal-50 pt-20">
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-md overflow-hidden">
            <div className="bg-primary text-white px-6 py-4 flex justify-between items-center">
              <h1 className="text-2xl font-bold">Medical History</h1>
              
              {isPdfReady && predictions.length > 0 && (
                <PDFDownloadLink 
                  document={<MedicalHistoryPDF user={user} predictions={predictions} />} 
                  fileName={`medical-history-${user?.name || 'patient'}.pdf`}
                  className="px-4 py-2 bg-white text-primary rounded hover:bg-gray-100 transition"
                >
                  {({ blob, url, loading, error }: { 
                    blob: Blob | null; 
                    url: string | null; 
                    loading: boolean; 
                    error: Error | null 
                  }) => 
                    loading ? 'Preparing PDF...' : 'Download PDF'
                  }
                </PDFDownloadLink>
              )}
            </div>
            
            <div className="p-6">
              <div className="mb-8 p-4 bg-gray-50 rounded-lg">
                <h2 className="text-xl font-semibold mb-2">Patient Information</h2>
                <p><span className="font-medium">Name:</span> {user?.name || 'Unknown'}</p>
                <p><span className="font-medium">Email:</span> {user?.email}</p>
              </div>
              
              <h2 className="text-xl font-semibold mb-4">Prediction History</h2>
              
              {predictions.length === 0 ? (
                <div className="text-center py-8">
                  <p className="text-gray-500">No prediction history available.</p>
                  <button 
                    onClick={() => router.push('/')}
                    className="mt-4 px-4 py-2 bg-primary text-white rounded hover:bg-primary-dark"
                  >
                    Make a Prediction
                  </button>
                </div>
              ) : (
                <div className="space-y-6">
                  {predictions.map((prediction, index) => (
                    <div key={index} className="border rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow duration-200">
                      <div className="bg-gradient-to-r from-primary/90 to-primary px-4 py-3 border-b text-white">
                        <div className="flex justify-between items-center">
                          <span className="font-medium flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                            {formatDate(prediction.timestamp)}
                          </span>
                          <span className="bg-white text-primary px-3 py-1 rounded-full text-sm font-bold">
                            {prediction.confidence_percentage || (prediction.probability * 100).toFixed(2) + '%'}
                          </span>
                        </div>
                      </div>
                      
                      <div className="p-5 space-y-4">
                        <div className="bg-gray-50 p-3 rounded-md">
                          <h3 className="text-sm text-gray-500 mb-1 flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                            </svg>
                            Symptoms
                          </h3>
                          <p className="text-gray-700">{prediction.symptoms_original}</p>
                        </div>
                        
                        <div className="bg-primary/5 p-3 rounded-md border-l-4 border-primary">
                          <h3 className="text-sm text-gray-500 mb-1 flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                            </svg>
                            Diagnosis
                          </h3>
                          <p className="font-medium text-lg text-primary">{prediction.prediction_displayed}</p>
                        </div>
                        
                        <div>
                          <h3 className="text-sm text-gray-500 mb-2 flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            Precautions
                          </h3>
                          <ul className="list-disc list-inside space-y-1 text-gray-700">
                            {Array.isArray(prediction.precautions) && prediction.precautions.length > 0 ? (
                              prediction.precautions.map((precaution, i) => (
                                <li key={i} className="pl-2">{precaution}</li>
                              ))
                            ) : (
                              <li className="text-gray-500 italic">No specific precautions available</li>
                            )}
                          </ul>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </>
  );
} 