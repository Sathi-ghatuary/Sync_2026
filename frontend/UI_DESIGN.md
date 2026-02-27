# 🎨 Frontend UI Preview

This document describes the visual design and layout of the TitleVerify frontend.

## Color Scheme

```
Primary Dark:     #0f172a (slate-900)
Secondary Dark:   #1e293b (slate-800)
Light Background: #f8fafc (slate-50)
Accent Blue:      #3b82f6 (blue-600)
Success Green:    #10b981 (green-600)
Warning Yellow:   #f59e0b (amber-500)
Danger Red:       #ef4444 (red-600)
```

## Layout Sections

### 1. Header Navigation
- Fixed sticky header at top
- Logo with icon (checkmark in blue box)
- Navigation links: Verify, Applications, Dashboard, About
- Mobile hamburger menu
- 16px padding top (below header)

### 2. Hero Section
- Full-screen background gradient (dark blue to slate)
- Large headline: "Verify Your Publication Title"
- Gradient text accent
- Feature bullets with checkmarks
- "Start Verification" CTA button
- Right side: Statistics card with glassmorphism effect

### 3. Verification Form Section
- Blue gradient background
- "Verify Your Publication Title" heading
- Two toggle buttons: "Quick Verify" & "Submit Application"
- Title input field with search icon
- Email field (appears only in Submit mode)
- Large blue submit button
- Info box with instructions

### 4. Results Display Section
- Shows when user submits a title
- Large title display
- Color-coded verdict badge (green/yellow/red)
- Two main score cards:
  - Similarity Score (orange progress bar)
  - Verification Probability (blue progress bar)
- Similar titles box (amber background)
- Violations list (red background)
- Recommendations section

### 5. Dashboard Section
- 5 stat cards in responsive grid:
  - Total Titles (blue)
  - Applications (purple)
  - Pending (yellow)
  - Approved (green)
  - Rejected (red)
- Summary section with 3 metric cards
- How to Use guide
- Compliance Rules list

### 6. Footer
- Dark slate background
- 4-column layout:
  - Brand/logo
  - Support links
  - Resources links
  - Contact info
- Divider with copyright
- Social media icons (GitHub, LinkedIn, Twitter)

## Component Hierarchy

```
App
├── Header
│   └── Mobile menu
├── Hero
│   ├── Headline + CTA
│   └── Stats card (right)
├── VerificationForm
│   ├── Mode selector buttons
│   ├── Title input
│   ├── Email input (conditional)
│   └── Submit button
├── ResultsDisplay
│   ├── Title display
│   ├── Verdict badge
│   ├── Score cards (2)
│   ├── Similar titles
│   ├── Violations list
│   └── Recommendations
├── Dashboard
│   ├── Stat cards (5)
│   ├── Summary section (3)
│   └── Info cards (2)
└── Footer
    ├── Links section (4 cols)
    ├── Copyright
    └── Social links
```

## Responsive Breakpoints

- **Mobile**: 320px - 640px (full-width, stacked)
- **Tablet**: 641px - 1024px (2 columns, optimized spacing)
- **Desktop**: 1025px+ (full layout, side-by-side)

## Interactive States

### Buttons
- **Idle**: Full color, shadow
- **Hover**: Lighter shade, enhanced shadow
- **Active**: Darker shade
- **Disabled**: 50% opacity, no cursor

### Input Fields
- **Idle**: Border color (grey)
- **Focus**: Blue ring (ring-2), border transparent
- **Disabled**: Grey background, reduced opacity

### Result Cards
- **Hover**: Enhanced shadow, slight lift
- **Loading**: Skeleton shimmer animation

## Animations

### Page Load
- Fade in (0.5s ease-in)
- Slide in for content (0.3s from top)

### User Interactions
- Button clicks: 200ms transition
- Results appear: Slide in animation
- Hover effects: 300ms duration
- Progress bars: Linear animation fill

### Loading States
- Spinner rotation (infinite)
- Skeleton shimmer effect
- Pulsing badges

## Typography

**Font:** Inter (Google Fonts)

**Sizes:**
- Hero H1: 48px (desktop), 36px (mobile)
- Section H2: 32px
- Card H3: 20px
- Body: 16px
- Small: 14px
- Extra Small: 12px

**Weights:**
- Regular: 400
- Semibold: 600
- Bold: 700
- Extra Bold: 800
- Black: 900

## Spacing System

- **xs**: 4px
- **sm**: 8px
- **md**: 16px
- **lg**: 24px
- **xl**: 32px
- **2xl**: 48px

## Shadow System

- **sm**: 0 1px 2px (#00000010)
- **md**: 0 4px 6px (#00000015)
- **lg**: 0 10px 15px (#00000020)
- **xl**: 0 20px 25px (#00000030)

## Accessibility

- All buttons have focus states
- High contrast colors (WCAG AA compliant)
- Semantic HTML structure
- ARIA labels on interactive elements
- Keyboard navigation support
- Screen reader friendly

## Cards & Containers

### Main Card (.card)
```css
background: white;
border-radius: 0.75rem;
box-shadow: 0 4px 6px rgba(0,0,0,0.15);
padding: 1.5rem;
transition: box-shadow 300ms;
```

### Badge Variants
- **Success**: Green background, dark green text
- **Warning**: Yellow background, dark yellow text
- **Danger**: Red background, dark red text

## Form Elements

### Input Fields
```css
width: 100%;
padding: 0.75rem 1rem;
border: 1px solid #e2e8f0;
border-radius: 0.5rem;
focus: ring 2px blue-500;
```

### Buttons
```css
padding: 0.75rem 1.5rem;
border-radius: 0.5rem;
font-weight: 600;
transition: all 300ms;
display: flex;
align-items: center;
gap: 0.5rem;
```

## Responsive Images

- Logo: SVG icon (24px desktop, 20px mobile)
- Placeholders: Gradient backgrounds
- Icons: 16px-32px Lucide React

## Dark Mode Ready

All components support dark mode with Tailwind's `dark:` prefix:
- Background inverses
- Text color inverses
- Border colors adjust
- Shadow intensity changes

## Performance

- CSS-in-JS for dynamic styles
- Lazy loading for off-screen components
- Optimized animations (GPU-accelerated)
- Minimal repaints/reflows
- No unnecessary keyframe animations

---

**The UI is:✨ Modern ✨ Clean ✨ Responsive ✨ Accessible ✨ Fast**
