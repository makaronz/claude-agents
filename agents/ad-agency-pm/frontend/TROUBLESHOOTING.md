# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### ❌ "The requested module does not provide an export named..."

**Problem**: Vite module cache or browser cache issue

**Solution**:
```bash
# 1. Clear Vite cache
rm -rf node_modules/.vite

# 2. Clear browser cache (hard refresh)
# Chrome/Edge: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
# Firefox: Cmd+Shift+R (Mac) or Ctrl+F5 (Windows)

# 3. Restart dev server
npm run dev

# 4. If still fails, reinstall dependencies
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### ❌ "Cannot find module '@/...'"

**Problem**: Path alias not recognized

**Solutions**:
```bash
# 1. Restart TypeScript server in VS Code
# Cmd+Shift+P → "TypeScript: Restart TS Server"

# 2. Check vite.config.ts has:
resolve: {
  alias: {
    '@': path.resolve(__dirname, './src'),
  },
}

# 3. Check tsconfig.app.json has:
"baseUrl": ".",
"paths": {
  "@/*": ["./src/*"]
}

# 4. Restart dev server
npm run dev
```

### ❌ Tailwind styles not applying

**Problem**: PostCSS or Tailwind configuration

**Solutions**:
```bash
# 1. Check index.css has Tailwind directives
@tailwind base;
@tailwind components;
@tailwind utilities;

# 2. Check tailwind.config.js content paths:
content: [
  "./index.html",
  "./src/**/*.{js,ts,jsx,tsx}",
],

# 3. Restart dev server
npm run dev

# 4. If still fails, reinstall Tailwind
npm install -D tailwindcss@latest postcss@latest autoprefixer@latest
npx tailwindcss init -p
```

### ❌ Port 3000 already in use

**Problem**: Another process using port 3000

**Solutions**:
```bash
# Option 1: Kill process on port 3000
lsof -ti:3000 | xargs kill -9

# Option 2: Use different port
npm run dev -- --port 3001

# Option 3: Change port in vite.config.ts
server: {
  port: 3001,
}
```

### ❌ Module not found: socket.io-client

**Problem**: Dependency not installed

**Solution**:
```bash
npm install socket.io-client
```

### ❌ WebSocket connection failed

**Problem**: Backend not running or wrong URL

**Check**:
```bash
# 1. Verify backend is running
# Backend should be at http://localhost:8000

# 2. Check environment variables
# Create .env.local:
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000

# 3. This is EXPECTED if backend not started
# Frontend will show "Connecting..." badge
```

### ❌ Redux state not persisting

**Problem**: Normal behavior - no persistence configured yet

**Note**: This is expected in Phase 1. State resets on page refresh. Persistence will be added in Phase 2.

### ❌ "Cannot read property of undefined" in Redux

**Problem**: Accessing state before it's initialized

**Solution**:
```typescript
// Always provide default values
const { data: projects = [] } = useGetProjectsQuery();

// Or use optional chaining
const project = state.projects.selectedProject?.name;

// Check loading state
if (isLoading) return <Loading />;
```

### ❌ Build fails with TypeScript errors

**Problem**: Type errors in code

**Solutions**:
```bash
# 1. Run type check to see all errors
npm run type-check

# 2. Check for common issues:
# - Missing type imports
# - Incorrect prop types
# - Null/undefined handling

# 3. Fix errors one by one
# TypeScript will guide you with error messages
```

### ❌ ESLint errors preventing build

**Problem**: Code quality issues

**Solutions**:
```bash
# 1. Run lint to see errors
npm run lint

# 2. Auto-fix what's possible
npm run lint:fix

# 3. Manually fix remaining errors
# ESLint will show file and line number
```

## 🔍 Debugging Tips

### Check Dev Server Status
```bash
# See if server is running
ps aux | grep vite

# Check port
lsof -i:3000

# View full server logs
npm run dev
# (don't background it)
```

### Inspect Redux State
```typescript
// Add to any component for debugging
import { useAppSelector } from '@/store/hooks';

const Component = () => {
  const state = useAppSelector((state) => state);
  console.log('Full Redux state:', state);
  
  // Or specific slice
  const projects = useAppSelector((state) => state.projects);
  console.log('Projects state:', projects);
}
```

### Check WebSocket Connection
```typescript
// In browser console (F12)
// After page loads, check:
console.log('WebSocket:', window.socket); // Should show Socket object
```

### Verify Component Rendering
```typescript
// Add console.logs in components
const Component = (props) => {
  console.log('Component props:', props);
  console.log('Component rendering');
  
  useEffect(() => {
    console.log('Component mounted');
    return () => console.log('Component unmounted');
  }, []);
}
```

## 🛠️ Clean Slate (Nuclear Option)

If nothing works, start fresh:

```bash
# 1. Stop all processes
# Ctrl+C in all terminals

# 2. Clean everything
rm -rf node_modules
rm -rf node_modules/.vite
rm -rf dist
rm package-lock.json

# 3. Reinstall
npm install

# 4. Clear browser
# Clear cache + cookies for localhost

# 5. Restart
npm run dev

# 6. Hard refresh browser
# Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
```

## 📞 Still Having Issues?

### Check These Files

1. **package.json** - All dependencies present?
2. **vite.config.ts** - Path alias configured?
3. **tsconfig.app.json** - Paths configured?
4. **tailwind.config.js** - Content paths correct?
5. **src/main.tsx** - Redux Provider wrapping App?

### Verify Installation

```bash
# Check Node version (should be 18+)
node --version

# Check npm version
npm --version

# Verify dependencies installed
ls node_modules | wc -l
# Should show ~680+ packages
```

### Browser Console Errors

Open browser DevTools (F12) and check:
- **Console** - JavaScript errors
- **Network** - Failed requests (404, 500)
- **Redux DevTools** - State inspection

### Common Console Errors

**"Cannot find module"**
- Check import path
- Verify file exists
- Check file extension (.tsx vs .ts)

**"Unexpected token"**
- Syntax error in JSX
- Missing closing tag
- Invalid TypeScript

**"X is not a function"**
- Check import (named vs default)
- Verify export exists
- Check function is defined

## ✅ Health Check Commands

```bash
# All should pass:
npm run type-check     # TypeScript: should exit 0
npm run lint           # ESLint: should exit 0
npm run build          # Build: should succeed
npm run dev            # Server: should start on 3000

# Browser should open at http://localhost:3000
```

## 🎯 Expected Behavior

### Normal (Not Errors)
- ⚠️ WebSocket "Connecting..." badge (backend not running)
- ⚠️ Empty project/client lists (no data yet)
- ⚠️ API 404 errors in Network tab (backend not running)
- ⚠️ "0 projects" message on Projects page

### Actual Errors (Need Fixing)
- ❌ TypeScript compilation errors
- ❌ "Cannot find module" errors
- ❌ React rendering errors
- ❌ "X is not defined" errors
- ❌ Infinite render loops

## 📝 Reporting Issues

If you encounter an issue not covered here:

1. **Check browser console** (F12) for error message
2. **Check terminal** for build errors
3. **Note** the exact error message
4. **Try** clean slate procedure above
5. **Document** steps to reproduce

---

**Last Updated**: October 7, 2025  
**Applies To**: Phase 1 Implementation  
**Status**: Active Troubleshooting Guide

