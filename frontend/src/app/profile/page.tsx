"use client";

import { useEffect, useState } from 'react';
import { getAuthUser, isAuthenticated } from '../lib/auth';
import { useRouter } from 'next/navigation';
import { UserProfile } from '../../components/UserProfile';

export default function ProfilePage() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  
  useEffect(() => {
    // Check if user is authenticated
    if (!isAuthenticated()) {
      router.push('/signin');
      return;
    }
    
    // Get user information from token
    const authUser = getAuthUser();
    setUser(authUser);
  }, [router]);
  
  if (!user) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
      </div>
    );
  }
  
  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-md mx-auto bg-white rounded-lg shadow-md overflow-hidden">
        <div className="bg-primary text-white px-6 py-4">
          <h1 className="text-2xl font-bold">User Profile</h1>
        </div>
        <div className="p-6">
          <div className="flex justify-center mb-6">
            <div className="h-24 w-24 rounded-full bg-primary text-white flex items-center justify-center text-4xl">
              {user.name ? user.name.charAt(0).toUpperCase() : 'U'}
            </div>
          </div>
          
          <div className="space-y-4">
            <div>
              <h2 className="text-lg font-semibold">Name</h2>
              <p className="text-gray-700">{user.name}</p>
            </div>
            
            <div>
              <h2 className="text-lg font-semibold">Email</h2>
              <p className="text-gray-700">{user.email}</p>
            </div>
            
            <div>
              <h2 className="text-lg font-semibold">Role</h2>
              <p className="text-gray-700 capitalize">{user.role}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
