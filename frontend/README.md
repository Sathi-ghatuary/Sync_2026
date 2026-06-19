# TitleVerify - Frontend

Beautiful and responsive React + Tailwind CSS frontend for the **PRGI Title Verification & Compliance System**.

## 🎨 Features

✨ **Modern Design**
- Responsive layout that works on all devices
- Smooth animations and transitions
- Beautiful gradient backgrounds
- Dark mode compatible

🚀 **User-Friendly Interface**
- Real-time title verification
- Quick application submission
- Live database statistics dashboard
- Visual feedback with progress indicators

📊 **Real-time Analytics**
- System statistics dashboard
- Verification metrics
- Application tracking
- Database capacity visualization

🔗 **Seamless Integration**
- Real-time connection with FastAPI backend
- Instant verification results
- Error handling and user feedback
- CORS-enabled communication

## 📋 Tech Stack

- **React 18** - UI framework
- **Vite** - Fast build tool & dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **Lucide React** - Beautiful icons

## 🚀 Quick Start

### 1. Prerequisites

- Node.js 16+ installed
- Backend API running at `http://127.0.0.1:8000`

### 2. Install Dependencies

```bash
cd frontend
npm install
```

### 3. Configure Backend URL (Optional)

Create `.env` file:
```
VITE_API_URL=http://127.0.0.1:8000
```

Or use default (already configured in [src/api.js](src/api.js))

### 4. Start Development Server

```bash
npm run dev
```

Frontend opens at: **`http://localhost:3000`**

### 5. Build for Production

```bash
npm run build
```

Optimized files in `dist/` folder

## 📁 Project Structure

```
frontend/
├── public/           # Static assets
├── src/
│   ├── components/   # React components
│   │   ├── Header.jsx              # Navigation header
│   │   ├── Hero.jsx                # Hero section
│   │   ├── VerificationForm.jsx    # Title verification form
│   │   ├── ResultsDisplay.jsx      # Results visualization
│   │   ├── Dashboard.jsx           # Statistics dashboard
│   │   └── Footer.jsx              # Footer section
│   ├── App.jsx                     # Main app component
│   ├── main.jsx                    # Entry point
│   ├── index.css                   # Global styles & Tailwind
│   └── api.js                      # API client (axios)
├── index.html        # HTML template
├── vite.config.js    # Vite configuration
├── tailwind.config.js # Tailwind CSS config
├── postcss.config.js # PostCSS config
└── package.json      # Dependencies
```

## 🎯 Key Components

### VerificationForm
- Input field for publication title
- Two modes: Quick Verify & Submit Application
- Email input for application submission
- Real-time error handling

### ResultsDisplay
- Similarity score visualization
- Verification probability gauge
- List of similar existing titles
- Rule violation details
- Approval recommendations

### Dashboard
- Real-time statistics
- Database capacity meter
- Application status breakdown
- Compliance rules overview

### Header
- Logo and branding
- Navigation menu
- Mobile responsive menu
- Sticky positioning

## 🔌 API Integration

All API calls are handled in [src/api.js](src/api.js) using Axios:

```javascript
// Verify a title
const result = await titleApi.verify("My Title");

// Submit an application
const app = await titleApi.submitApplication("My Title", "email@example.com");

// Get statistics
const stats = await titleApi.getStats();

// Upload CSV
const response = await titleApi.uploadCSV(file);
```

## 🎨 Customization

### Colors and Theme

Edit `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: "#0f172a",
      secondary: "#1e293b",
      accent: "#3b82f6",
      // ... add your colors
    }
  }
}
```

### Animations

```css
/* In src/index.css */
@keyframes slideIn {
  0% { transform: translateY(-10px); opacity: 0; }
  100% { transform: translateY(0); opacity: 1; }
}
```

## 📱 Responsive Design

All components are mobile-first and responsive:
- **Mobile**: 320px+
- **Tablet**: 768px+
- **Desktop**: 1024px+
- **Large**: 1280px+

## 🧪 Testing

Run the test suite:
```bash
npm run test
```

## 🐛 Troubleshooting

### Backend Connection Failed

```
⚠️ Backend not connected. Make sure the API server is running (check VITE_API_URL in your .env)
```

**Solution:**
1. Check if backend is running: `python -m uvicorn app.main:app --reload`
2. Verify URL in `.env` file
3. Check CORS is enabled in backend

### Verification not working

1. Ensure backend database is populated
2. Check API response in browser DevTools
3. Verify title is not empty

### Styling issues

1. Run `npm install tailwindcss -D` to ensure Tailwind is installed
2. Rebuild: `npm run dev`
3. Clear browser cache

## 🚀 Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Connect to Vercel
3. Set environment variable:
   ```
   VITE_API_URL=https://your-api-domain.com
   ```
4. Deploy!

### Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "dev"]
```

### Static Hosting

```bash
npm run build
# Upload dist/ folder to hosting provider
```

## 📞 Support

For issues or feature requests:
- Backend issues: See [../backend/README.md](../backend/README.md)
- Frontend issues: Check browser console and network tab
- API docs: http://127.0.0.1:8000/docs

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/amazing-feature`
2. Commit changes: `git commit -m 'Add amazing feature'`
3. Push to branch: `git push origin feature/amazing-feature`
4. Open a Pull Request

## 📄 License

© 2026 Press Registrar General of India (PRGI). All rights reserved.

## 🙏 Acknowledgments

- React team for excellent framework
- Tailwind CSS for utility-first CSS
- Lucide for beautiful icons
- Vite for blazing fast dev experience

---

**Made with ❤️ for the PRGI Title Verification System**
