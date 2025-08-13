// Authentication utility functions

// Store token in localStorage
export const setToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('auth_token', token);
  }
};

// Get token from localStorage
export const getToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('auth_token');
  }
  return null;
};

// Remove token from localStorage
export const removeToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('auth_token');
  }
};

// Check if user is authenticated
export const isAuthenticated = (): boolean => {
  const token = getToken();
  return !!token;
};

// Get authenticated user from token
export const getAuthUser = (): any => {
  const token = getToken();
  if (!token) return null;
  
  try {
    // Decode JWT token (simple decode, not verification)
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    
    const payload = JSON.parse(jsonPayload);
    console.log('Decoded JWT payload:', payload); // Debug log to see the actual payload structure
    
    // Return user object with consistent structure for frontend components
    // Try different possible locations for the name field
    const userName = payload.name || payload.username || payload.displayName || '';
    console.log('Extracted user name:', userName);
    
    return {
      id: payload.sub,
      name: userName || 'Unknown',
      email: payload.email,
      role: payload.role
    };
  } catch (error) {
    console.error('Error decoding token:', error);
    removeToken(); // Remove invalid token
    return null;
  }
};

// Create authenticated fetch function that includes the token
export const authFetch = async (url: string, options: RequestInit = {}): Promise<Response> => {
  const token = getToken();
  
  // Create a proper Headers object
  const headers = new Headers(options.headers);
  
  // Only set Content-Type to JSON if it's not already set and not a multipart request
  if (!headers.has('Content-Type') && !(options.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json');
  }
  
  if (token) {
    headers.set('Authorization', `Bearer ${token}`);
  }
  
  return fetch(url, {
    ...options,
    headers,
  });
};
