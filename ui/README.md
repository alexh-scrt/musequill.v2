# Musequill UI Wizard

A modular, lightweight book creation wizard built with Alpine.js and Tailwind CSS.

## 🏗️ Architecture

### Directory Structure
```
ui/
├── index.html                 # Main entry point
├── css/
│   └── wizard.css            # Custom styles and enhancements
├── js/
│   ├── stores/
│   │   └── wizard-store.js   # Alpine.js global state management
│   ├── utils/
│   │   └── api-client.js     # API communication layer
│   ├── components/
│   │   ├── progress-bar.js   # Progress indicator component
│   │   ├── step-container.js # Step content container
│   │   └── navigation.js     # Wizard navigation controls
│   └── steps/
│       ├── step-1-concept.js     # Book concept input
│       ├── step-2-genre.js       # Genre selection
│       ├── step-3-audience.js    # Target audience
│       ├── step-4-style.js       # Writing style
│       ├── step-5-length.js      # Book length
│       ├── step-6-structure.js   # Story structure
│       ├── step-7-world.js       # World building
│       ├── step-8-content.js     # Content preferences
│       └── step-9-summary.js     # Final summary
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- FastAPI backend running on `http://localhost:8000`
- Modern web browser with JavaScript enabled

### Running the Wizard
1. Open `index.html` in a web browser
2. Or serve via a local server:
   ```bash
   # Using Python
   python -m http.server 8080
   
   # Using Node.js
   npx serve .
   
   # Using PHP
   php -S localhost:8080
   ```

3. Navigate to `http://localhost:8080`

## 🧩 Component Architecture

### State Management (Alpine.js Store)
The wizard uses Alpine.js global store for centralized state management:

```javascript
// Access the wizard store
$store.wizard.currentStep        // Current step number (1-9)
$store.wizard.formData          // All collected form data
$store.wizard.sessionId         // Backend session ID
$store.wizard.isLoading         // Loading state
$store.wizard.error             // Error messages
```

### API Communication
All backend communication goes through the `apiClient`:

```javascript
// Start wizard with concept
await window.apiClient.startWizard({
    concept: "Book concept text",
    additional_notes: "Optional notes"
});

// Process a step
await window.apiClient.processStep(stepNumber, {
    session_id: sessionId,
    selection: userSelection,
    additional_input: optionalInput
});
```

### Component Pattern
Each step follows a consistent pattern:

```javascript
function stepXComponent() {
    return {
        // Data properties
        selectedOption: '',
        isSubmitting: false,
        options: [],
        
        // Computed properties
        get canProceed() {
            return this.selectedOption !== '';
        },
        
        // Methods
        async selectOption(optionId) {
            this.selectedOption = optionId;
            await this.processSelection();
        },
        
        // Lifecycle
        init() {
            this.loadStepData();
        }
    };
}
```

## 📋 Step-by-Step Flow

### Step 1: Book Concept
- **Input**: 2-3 sentence book description
- **Validation**: 10-1000 characters
- **Output**: Creates wizard session, moves to genre selection

### Step 2: Genre Selection
- **Input**: Genre choice from LLM recommendations
- **Process**: May show subgenre options
- **Output**: Selected genre/subgenre, moves to audience

### Step 3: Target Audience
- **Input**: Audience selection (Adult, YA, etc.)
- **Process**: Shows market size and commercial appeal
- **Output**: Target audience, moves to writing style

### Step 4: Writing Style
- **Input**: Writing style selection
- **Process**: Style recommendations based on genre/audience
- **Output**: Writing style, moves to book length

### Step 5: Book Length
- **Input**: Book length category
- **Process**: Commercial viability indicators
- **Output**: Target length, moves to story structure

### Step 6: Story Structure
- **Input**: Narrative structure choice
- **Process**: Structure recommendations for genre
- **Output**: Story structure, moves to world building

### Step 7: World Building
- **Input**: World/setting type
- **Process**: Setting options matching genre
- **Output**: World type, moves to content preferences

### Step 8: Content Preferences
- **Input**: Free text content preferences/restrictions
- **Process**: Captures user content guidelines
- **Output**: Content preferences, moves to summary

### Step 9: Final Summary
- **Display**: Complete book definition
- **Action**: Wizard completion
- **Output**: Ready for book creation phase

## 🎨 Styling and Theming

### CSS Custom Properties
The wizard uses CSS custom properties for consistent theming:

```css
:root {
    --wizard-primary: #3b82f6;
    --wizard-secondary: #6366f1;
    --wizard-success: #10b981;
    --wizard-error: #ef4444;
    /* ... more variables */
}
```

### Responsive Design
- Mobile-first approach
- Breakpoints: 480px, 768px, 1024px
- Adaptive layouts for different screen sizes

### Accessibility Features
- Keyboard navigation support
- Focus management
- Screen reader friendly
- High contrast mode support
- Reduced motion support

## 🔌 API Integration

### Backend Endpoints
The wizard communicates with these FastAPI endpoints:

```
POST /wizard/start           # Start new session
POST /wizard/step/{step}     # Process step
GET  /wizard/session/{id}    # Get session state
GET  /health                 # Health check
GET  /models/info           # Model information
```

### Error Handling
- Network errors are caught and displayed
- Validation errors show contextual messages
- Retry mechanisms for failed requests
- Graceful degradation when backend unavailable

## 🧪 Testing

### Manual Testing Checklist
- [ ] All 9 steps load correctly
- [ ] Form validation works
- [ ] Navigation between steps
- [ ] Error states display properly
- [ ] Loading states show during API calls
- [ ] Responsive design on mobile
- [ ] Keyboard navigation works
- [ ] Backend integration functions

### Browser Compatibility
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 🔧 Configuration

### API Base URL
Update the API base URL in `js/utils/api-client.js`:

```javascript
class ApiClient {
    constructor(baseUrl = 'http://localhost:8000') {
        // Change this URL for production
    }
}
```

### Step Configuration
Modify step configuration in `js/stores/wizard-store.js`:

```javascript
steps: [
    { number: 1, name: 'Book Concept', shortName: 'Concept', key: 'concept' },
    // Add, remove, or modify steps
]
```

## 🐛 Troubleshooting

### Common Issues

**"Failed to start wizard" Error**
- Check if FastAPI backend is running
- Verify API URL is correct
- Check browser console for network errors

**Steps not loading**
- Ensure all JavaScript files are loaded
- Check for console errors
- Verify Alpine.js is loaded correctly

**Styling issues**
- Ensure Tailwind CSS is loaded
- Check custom CSS file is included
- Verify no CSS conflicts

### Debug Mode
Enable debug logging by adding to console:

```javascript
// Enable debug mode
Alpine.store('wizard').debug = true;

// Check current state
console.log(Alpine.store('wizard').formData);
```

## 📈 Performance Optimization

### Loading Strategy
- CSS and JavaScript are loaded via CDN
- Components load on-demand
- Minimal external dependencies

### Bundle Size
- Alpine.js: ~15KB gzipped
- Tailwind CSS: ~30KB compressed
- Custom code: ~10KB total

### Caching Strategy
- Static assets can be cached
- API responses include cache headers
- Progressive loading for images

## 🚀 Deployment

### Static Hosting
The wizard can be deployed to any static hosting service:

```bash
# Build for production (if using build tools)
npm run build

# Deploy to Netlify, Vercel, etc.
# Just upload the ui/ directory
```

### Environment Variables
For production, consider:
- API_BASE_URL configuration
- Error tracking integration
- Analytics integration

## 🤝 Contributing

### Adding New Steps
1. Create new step component in `js/steps/`
2. Add step configuration to wizard store
3. Update navigation logic
4. Add corresponding backend endpoint
5. Update tests and documentation

### Code Style
- Use meaningful variable names
- Add JSDoc comments for functions
- Follow Alpine.js conventions
- Keep components small and focused

## 📝 License

This project is part of the Musequill book creation platform.