const isBrowser = typeof window !== 'undefined';

// Use 127.0.0.1 instead of localhost to avoid IPv6 resolution issues on some systems
let defaultApiUrl = "http://127.0.0.1:8000";

if (isBrowser) {
  const hostname = window.location.hostname;
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    defaultApiUrl = `${window.location.protocol}//127.0.0.1:8000`;
  } else if (hostname.includes('.onrender.com')) {
    // Dynamically point to backend on Render (e.g. smartrx-frontend.onrender.com -> smartrx-backend.onrender.com)
    // Render apps on *.onrender.com are served over standard HTTPS (port 443), so no port suffix is needed.
    const backendHost = hostname.replace('-frontend', '-backend');
    defaultApiUrl = `${window.location.protocol}//${backendHost}`;
  } else {
    defaultApiUrl = `${window.location.protocol}//${hostname}:8000`;
  }
}

let API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || defaultApiUrl;

// Sanitize and dynamically correct API_BASE_URL at runtime in the browser
if (isBrowser) {
  // If the API URL points to the frontend Render domain (a common misconfiguration), dynamically map it to the backend domain
  if (API_BASE_URL.includes('smartrx-frontend.onrender.com')) {
    API_BASE_URL = API_BASE_URL.replace('smartrx-frontend.onrender.com', 'smartrx-backend.onrender.com');
  }
  
  // Render subdomains on *.onrender.com do not use port 8000 externally (they are served over HTTPS port 443)
  if (API_BASE_URL.includes('.onrender.com:8000')) {
    API_BASE_URL = API_BASE_URL.replace(':8000', '');
  }
}

export default API_BASE_URL;
