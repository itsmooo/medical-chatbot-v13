"use client";

import { useEffect, useState } from 'react';
import { getAuthUser, isAuthenticated, authFetch } from '../lib/auth';
import { useRouter } from 'next/navigation';
import { UserProfile } from '../../components/UserProfile';
import Header from '../components/header';
import Footer from '../components/footer';
import { Camera, Upload } from 'lucide-react';

export default function ProfilePage() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [profileImage, setProfileImage] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  
  useEffect(() => {
    // Check if user is authenticated
    if (!isAuthenticated()) {
      router.push('/signin');
      return;
    }
    
    // Get user information from token
    const authUser = getAuthUser();
    console.log('Auth user from token:', authUser);
    setUser(authUser);
    
    // Load profile image if exists
    if (authUser && authUser.id) {
      loadProfileImage(authUser.id);
    }
  }, [router]);

  const loadProfileImage = async (userId: string) => {
    try {
      const nestjsBackendUrl = 'http://localhost:4000';
      const response = await authFetch(`${nestjsBackendUrl}/api/auth/profile-image/${userId}`);
      
      if (response.ok) {
        const blob = await response.blob();
        if (blob.size > 0) {
          const imageUrl = URL.createObjectURL(blob);
          setProfileImage(imageUrl);
        }
      }
    } catch (error) {
      console.log('No profile image found or error loading image');
    }
  };

  const handleImageUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('image/')) {
      setUploadError('Please select a valid image file');
      return;
    }

    // Validate file size (5MB max)
    if (file.size > 5 * 1024 * 1024) {
      setUploadError('Image size should be less than 5MB');
      return;
    }

    setUploading(true);
    setUploadError(null);

    try {
      const formData = new FormData();
      formData.append('profileImage', file);
      
      const token = localStorage.getItem('auth_token');
      console.log('Upload token:', token ? 'Token exists' : 'No token found');
      
      const nestjsBackendUrl = 'http://localhost:4000';
      const response = await fetch(`${nestjsBackendUrl}/api/auth/upload-profile-image`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });
      
      console.log('Upload response status:', response.status, response.statusText);

      if (response.ok) {
        const result = await response.json();
        // Update profile image display
        setProfileImage(URL.createObjectURL(file));
        console.log('Profile image uploaded successfully:', result);
      } else {
        const error = await response.json();
        setUploadError(error.message || 'Failed to upload image');
      }
    } catch (error) {
      console.error('Error uploading image:', error);
      setUploadError('Failed to upload image. Please try again.');
    } finally {
      setUploading(false);
    }
  };

  if (!user) {
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
  
  return (
    <>
      <Header />
      <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-teal-50 pt-20">
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-md mx-auto bg-white rounded-lg shadow-md overflow-hidden">
            <div className="bg-primary text-white px-6 py-4">
              <h1 className="text-2xl font-bold">User Profile</h1>
            </div>
            
            <div className="p-6">
              <div className="flex justify-center mb-6">
                <div className="relative">
                  {profileImage ? (
                    <img
                      src={profileImage}
                      alt="Profile"
                      className="h-24 w-24 rounded-full object-cover border-4 border-primary"
                    />
                  ) : (
                    <div className="h-24 w-24 rounded-full bg-primary text-white flex items-center justify-center text-4xl border-4 border-primary">
                      {user.name ? user.name.charAt(0).toUpperCase() : 'U'}
                    </div>
                  )}
                  
                  {/* Upload button overlay */}
                  <label className="absolute bottom-0 right-0 bg-white rounded-full p-2 shadow-lg cursor-pointer hover:bg-gray-50 transition-colors">
                    <Camera size={16} className="text-primary" />
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImageUpload}
                      className="hidden"
                    />
                  </label>
                  
                  {uploading && (
                    <div className="absolute inset-0 bg-black bg-opacity-50 rounded-full flex items-center justify-center">
                      <div className="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-white"></div>
                    </div>
                  )}
                </div>
              </div>

              {uploadError && (
                <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
                  {uploadError}
                </div>
              )}
              
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

                <div className="pt-4 border-t">
                  <label className="flex items-center justify-center w-full p-4 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:border-primary hover:bg-gray-50 transition-colors">
                    <Upload size={20} className="mr-2 text-gray-400" />
                    <span className="text-gray-600">Click to upload profile image</span>
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImageUpload}
                      className="hidden"
                    />
                  </label>
                  <p className="text-xs text-gray-500 mt-2 text-center">
                    Maximum file size: 5MB. Supported formats: JPG, PNG, GIF
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </>
  );
}
