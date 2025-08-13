"use client";

import { useEffect, useState } from 'react';
import { getAuthUser, isAuthenticated, authFetch } from '../lib/auth';
import { useRouter } from 'next/navigation';
import { UserProfile } from '../../components/UserProfile';
import Header from '../components/header';
import Footer from '../components/footer';
import { Camera, Upload, User, Mail, Shield, Calendar, Edit3, CheckCircle, AlertCircle, Settings, Activity, Heart, Brain } from 'lucide-react';

export default function ProfilePage() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [profileImage, setProfileImage] = useState<string | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editedName, setEditedName] = useState('');
  
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
    setEditedName(authUser?.name || '');
    
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
    setUploadSuccess(false);

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
        setUploadSuccess(true);
        console.log('Profile image uploaded successfully:', result);
        
        // Hide success message after 3 seconds
        setTimeout(() => setUploadSuccess(false), 3000);
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

  const handleSaveName = () => {
    // Here you would typically make an API call to update the name
    setUser({ ...user, name: editedName });
    setIsEditing(false);
  };

  if (!user) {
    return (
      <>
        <Header />
        <div className="min-h-screen bg-gradient-to-br from-red-50 via-pink-50 to-rose-50 pt-20 flex justify-center items-center">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-red-600"></div>
        </div>
        <Footer />
      </>
    );
  }
  
  return (
    <>
      <Header />
      <div className="min-h-screen bg-gradient-to-br from-red-50 via-pink-50 to-rose-50 pt-20">
        <div className="container mx-auto px-4 py-8">
          {/* Profile Header */}
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
              {/* Hero Section */}
              <div className="relative h-48 bg-gradient-to-r from-red-600 via-pink-600 to-rose-600">
                <div className="absolute inset-0 bg-black bg-opacity-20"></div>
                <div className="absolute bottom-0 left-0 right-0 p-8">
                  <div className="flex items-end space-x-6">
                    {/* Profile Image */}
                    <div className="relative">
                      {profileImage ? (
                        <img
                          src={profileImage}
                          alt="Profile"
                          className="h-32 w-32 rounded-full object-cover border-4 border-white shadow-lg"
                        />
                      ) : (
                        <div className="h-32 w-32 rounded-full bg-white bg-opacity-20 text-white flex items-center justify-center text-6xl font-bold border-4 border-white shadow-lg backdrop-blur-sm">
                          {user.name ? user.name.charAt(0).toUpperCase() : 'U'}
                        </div>
                      )}
                      
                      {/* Upload button overlay */}
                      <label className="absolute bottom-2 right-2 bg-white rounded-full p-3 shadow-lg cursor-pointer hover:bg-gray-50 transition-all duration-200 hover:scale-110">
                        <Camera size={20} className="text-red-600" />
                        <input
                          type="file"
                          accept="image/*"
                          onChange={handleImageUpload}
                          className="hidden"
                        />
                      </label>
                      
                      {uploading && (
                        <div className="absolute inset-0 bg-black bg-opacity-50 rounded-full flex items-center justify-center">
                          <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-white"></div>
                        </div>
                      )}
                    </div>
                    
                    {/* User Info */}
                    <div className="flex-1 text-white">
                      <div className="flex items-center space-x-4 mb-2">
                        {isEditing ? (
                          <div className="flex items-center space-x-2">
                            <input
                              type="text"
                              value={editedName}
                              onChange={(e) => setEditedName(e.target.value)}
                              className="text-3xl font-bold bg-white bg-opacity-20 rounded px-3 py-1 text-white placeholder-white placeholder-opacity-70 focus:outline-none focus:ring-2 focus:ring-white"
                            />
                            <button
                              onClick={handleSaveName}
                              className="p-1 bg-white bg-opacity-20 rounded hover:bg-opacity-30 transition-colors"
                            >
                              <CheckCircle size={20} />
                            </button>
                          </div>
                        ) : (
                          <h1 className="text-3xl font-bold">{user.name}</h1>
                        )}
                        <button
                          onClick={() => setIsEditing(true)}
                          className="p-2 bg-white bg-opacity-20 rounded-full hover:bg-opacity-30 transition-colors"
                        >
                          <Edit3 size={16} />
                        </button>
                      </div>
                      <p className="text-xl opacity-90 capitalize">{user.role}</p>
                      <p className="text-lg opacity-80">{user.email}</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Content Section */}
              <div className="p-8">
                {/* Status Messages */}
                {uploadError && (
                  <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg flex items-center space-x-2">
                    <AlertCircle size={20} />
                    <span>{uploadError}</span>
                  </div>
                )}

                {uploadSuccess && (
                  <div className="mb-6 p-4 bg-green-50 border border-green-200 text-green-700 rounded-lg flex items-center space-x-2">
                    <CheckCircle size={20} />
                    <span>Profile image uploaded successfully!</span>
                  </div>
                )}

                {/* Profile Statistics */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                  <div className="bg-gradient-to-br from-red-50 to-red-100 p-6 rounded-xl border border-red-200">
                    <div className="flex items-center space-x-3">
                      <div className="p-3 bg-red-500 rounded-lg">
                        <Activity size={24} className="text-white" />
                      </div>
                      <div>
                        <p className="text-sm text-red-600 font-medium">Predictions Made</p>
                        <p className="text-2xl font-bold text-red-800">12</p>
                      </div>
                    </div>
                  </div>

                  <div className="bg-gradient-to-br from-pink-50 to-pink-100 p-6 rounded-xl border border-pink-200">
                    <div className="flex items-center space-x-3">
                      <div className="p-3 bg-pink-500 rounded-lg">
                        <Heart size={24} className="text-white" />
                      </div>
                      <div>
                        <p className="text-sm text-pink-600 font-medium">Health Score</p>
                        <p className="text-2xl font-bold text-pink-800">85%</p>
                      </div>
                    </div>
                  </div>

                  <div className="bg-gradient-to-br from-rose-50 to-rose-100 p-6 rounded-xl border border-rose-200">
                    <div className="flex items-center space-x-3">
                      <div className="p-3 bg-rose-500 rounded-lg">
                        <Brain size={24} className="text-white" />
                      </div>
                      <div>
                        <p className="text-sm text-rose-600 font-medium">AI Accuracy</p>
                        <p className="text-2xl font-bold text-rose-800">94%</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Profile Details */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  {/* Personal Information */}
                  <div className="bg-gray-50 rounded-xl p-6">
                    <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center space-x-2">
                      <User size={20} className="text-red-600" />
                      <span>Personal Information</span>
                    </h2>
                    
                    <div className="space-y-4">
                      <div className="flex items-center space-x-3 p-3 bg-white rounded-lg">
                        <User size={18} className="text-gray-400" />
                        <div>
                          <p className="text-sm text-gray-500">Full Name</p>
                          <p className="font-medium text-gray-800">{user.name}</p>
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-3 p-3 bg-white rounded-lg">
                        <Mail size={18} className="text-gray-400" />
                        <div>
                          <p className="text-sm text-gray-500">Email Address</p>
                          <p className="font-medium text-gray-800">{user.email}</p>
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-3 p-3 bg-white rounded-lg">
                        <Shield size={18} className="text-gray-400" />
                        <div>
                          <p className="text-sm text-gray-500">Account Role</p>
                          <p className="font-medium text-gray-800 capitalize">{user.role}</p>
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-3 p-3 bg-white rounded-lg">
                        <Calendar size={18} className="text-gray-400" />
                        <div>
                          <p className="text-sm text-gray-500">Member Since</p>
                          <p className="font-medium text-gray-800">January 2024</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Image Upload Section */}
                  <div className="bg-gray-50 rounded-xl p-6">
                    <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center space-x-2">
                      <Camera size={20} className="text-red-600" />
                      <span>Profile Photo</span>
                    </h2>
                    
                    <div className="space-y-4">
                      <div className="bg-white rounded-lg p-6 border-2 border-dashed border-gray-300 hover:border-red-400 transition-colors">
                        <label className="flex flex-col items-center justify-center cursor-pointer space-y-3">
                          <div className="p-4 bg-red-100 rounded-full">
                            <Upload size={24} className="text-red-600" />
                          </div>
                          <div className="text-center">
                            <p className="text-sm font-medium text-gray-700">
                              {profileImage ? 'Change Profile Photo' : 'Upload Profile Photo'}
                            </p>
                            <p className="text-xs text-gray-500 mt-1">
                              JPG, PNG, GIF up to 5MB
                            </p>
                          </div>
                          <input
                            type="file"
                            accept="image/*"
                            onChange={handleImageUpload}
                            className="hidden"
                          />
                        </label>
                      </div>
                      
                      {profileImage && (
                        <div className="bg-white rounded-lg p-4">
                          <p className="text-sm text-gray-600 mb-2">Current Photo:</p>
                          <img
                            src={profileImage}
                            alt="Current Profile"
                            className="h-20 w-20 rounded-full object-cover border-2 border-gray-200"
                          />
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                {/* Quick Actions */}
                <div className="mt-8 bg-white rounded-xl p-6 border border-gray-200">
                  <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center space-x-2">
                    <Settings size={20} className="text-red-600" />
                    <span>Quick Actions</span>
                  </h2>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <button className="flex items-center justify-center space-x-2 p-4 bg-red-50 hover:bg-red-100 rounded-lg transition-colors">
                      <Activity size={18} className="text-red-600" />
                      <span className="text-red-700 font-medium">View History</span>
                    </button>
                    
                    <button className="flex items-center justify-center space-x-2 p-4 bg-pink-50 hover:bg-pink-100 rounded-lg transition-colors">
                      <Heart size={18} className="text-pink-600" />
                      <span className="text-pink-700 font-medium">Health Report</span>
                    </button>
                    
                    <button className="flex items-center justify-center space-x-2 p-4 bg-rose-50 hover:bg-rose-100 rounded-lg transition-colors">
                      <Brain size={18} className="text-rose-600" />
                      <span className="text-rose-700 font-medium">New Prediction</span>
                    </button>
                  </div>
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
