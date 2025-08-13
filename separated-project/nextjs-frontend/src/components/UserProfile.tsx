"use client";

import { useEffect, useState } from 'react';
import { getAuthUser } from '../app/lib/auth';

export const UserProfile = () => {
  const [user, setUser] = useState<{ name: string; email: string; role: string } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Get the authenticated user from the token
    const authUser = getAuthUser();
    if (authUser) {
      setUser({
        name: authUser.name || 'Unknown',
        email: authUser.email || '',
        role: authUser.role || 'patient'
      });
    }
    setLoading(false);
  }, []);

  if (loading) {
    return <div>Loading user information...</div>;
  }

  if (!user) {
    return <div>Not logged in</div>;
  }

  return (
    <div className="flex items-center space-x-2">
      <div className="h-8 w-8 rounded-full bg-primary text-white flex items-center justify-center">
        {user.name.charAt(0).toUpperCase()}
      </div>
      <div>
        <p className="font-medium">{user.name}</p>
        <p className="text-xs text-gray-500">{user.role}</p>
      </div>
    </div>
  );
};

export default UserProfile;
