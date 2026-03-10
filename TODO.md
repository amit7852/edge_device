# TOzzzzzzzzzzzzzzzzzz  ///////////////////////////////////////////////////DO: Remove Login/Authentication from EdgeVision Guard

## Plan Summary
Remove all login/authentication functionality from the backend and web dashboard to make the application publicly accessible.

## Backend Changes

### 1. backend/main.py ✅
- [x] Remove auth router inclusion (`app.include_router(auth_router)`)
- [x] Remove default admin user creation function
- [x] Remove `get_current_user_or_api_key` dependency
- [x] Make `/api/events` endpoint public (remove authentication requirement)
- [x] Remove JWT-related imports (jwt, JWTError)
- [x] Remove EDGE_DEVICE_API_KEY and related logic
- [x] Clean up unused imports

### 2. backend/auth.py
- [x] File kept but not used (no changes needed)

## Frontend Changes

### 3. web_dashboard/script.js ✅
- [x] Remove login/register form UI (`showLogin()` function)
- [x] Remove token management functions (`getToken()`, `setToken()`, `removeToken()`)
- [x] Remove `isAuthenticated()` function
- [x] Remove `handleLogin()` function
- [x] Remove `handleRegister()` function
- [x] Remove `handleLogout()` function
- [x] Remove Authorization headers from `fetchEvents()` API calls
- [x] Directly call `showApp()` and `fetchEvents()` on page load
- [x] Keep auto-refresh interval (every 30 seconds)

### 4. web_dashboard/index.html ✅
- [x] Remove auth-container div
- [x] Remove logout button from nav
- [x] Remove authentication check in inline script
- [x] Directly show main-content

### 5. web_dashboard/dashboard.html ✅
- [x] Apply same changes as index.html
- [x] Remove authentication checks

### 6. web_dashboard/analytics.html ✅
- [x] Apply same changes as index.html
- [x] Remove authentication checks

## Edge Device Changes

### 7. edge_device/uplink_client.py ✅
- [x] Remove API key header from requests

## Database
- No changes needed - User table can remain but won't be used

