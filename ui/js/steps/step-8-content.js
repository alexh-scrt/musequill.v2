/**
 * Step 8: Content Preferences Component
 * Handles free-text content preferences and restrictions
 */

function step8Content() {
    return {
        // Data
        contentPreferences: '',
        isSubmitting: false,

        // Step data from API
        llmMessage: '',
        suggestions: [],

        // UI state
        showSuggestions: false,
        characterCount: 0,

        // Computed
        get canProceed() {
            // Content preferences are optional, so always allow proceeding
            return true;
        },

        get isValid() {
            return this.contentPreferences.length <= 1000;
        },

        get characterCountClass() {
            if (this.characterCount > 1000) return 'text-red-500';
            if (this.characterCount > 800) return 'text-yellow-500';
            return 'text-gray-500';
        },

        // Methods
        updateContentPreferences() {
            this.characterCount = this.contentPreferences.length;

            // Update store
            this.$store.wizard.updateFormData('contentPreferences', this.contentPreferences);
        },

        async proceedToSummary() {
            this.isSubmitting = true;

            try {
                const success = await this.$store.wizard.processStep(
                    8, // Step number
                    null, // No selection for this step
                    this.contentPreferences // Additional input
                );

                if (success) {
                    await this.proceedToNextStep();
                }
            } catch (error) {
                console.error('Error processing content preferences:', error);
            } finally {
                this.isSubmitting = false;
            }
        },

        async proceedToNextStep() {
            // Move to step 9 (final summary)
            this.$store.wizard.setCurrentStep(9);

            // Load step 9 data (final summary)
            await this.loadSummaryData();
        },

        async loadSummaryData() {
            try {
                const success = await this.$store.wizard.processStep(9, null);
                // Step 9 data will be loaded automatically through the store
            } catch (error) {
                console.error('Error loading summary data:', error);
            }
        },

        // Suggestion handling
        applySuggestion(suggestion) {
            if (this.contentPreferences) {
                this.contentPreferences += '\n' + suggestion;
            } else {
                this.contentPreferences = suggestion;
            }
            this.updateContentPreferences();
        },

        toggleSuggestions() {
            this.showSuggestions = !this.showSuggestions;
        },

        // Data loading
        loadStepData() {
            const stepData = this.$store.wizard.currentStepData;

            this.llmMessage = stepData.llmReasoning || this.getDefaultMessage();
            this.suggestions = stepData.suggestions || this.getDefaultSuggestions();

            // Load any existing content preferences
            this.contentPreferences = this.$store.wizard.formData.contentPreferences || '';
            this.updateContentPreferences();
        },

        getDefaultMessage() {
            return "Please specify any content preferences, themes you'd like to explore, or restrictions you'd like to set for your book:";
        },

        // Navigation
        goBack() {
            // Go back to step 7 (world building)
            this.$store.wizard.setCurrentStep(7);
        },

        // Lifecycle
        init() {
            this.loadStepData();
        },

        // Default suggestions based on genre and choices
        getDefaultSuggestions() {
            const selectedGenre = this.$store.wizard.formData.genre;
            const selectedAudience = this.$store.wizard.formData.audience;

            let suggestions = [
                "Family-friendly content appropriate for all ages",
                "Moderate romantic tension without explicit content",
                "Violence limited to necessary plot advancement",
                "Focus on character growth and positive themes",
                "Avoid controversial political topics"
            ];

            // Genre-specific suggestions
            if (selectedGenre === 'romance') {
                suggestions = [
                    "Sweet romance with minimal explicit content",
                    "Focus on emotional connection and character development",
                    "Include diverse representation",
                    "Avoid love triangles or excessive drama",
                    "Happy ending required"
                ];
            } else if (selectedGenre === 'fantasy') {
                suggestions = [
                    "Magic system with clear rules and limitations",
                    "Diverse fantasy races and cultures",
                    "Avoid graphic violence despite fantasy setting",
                    "Environmental themes woven into worldbuilding",
                    "Coming-of-age elements"
                ];
            } else if (selectedGenre === 'mystery') {
                suggestions = [
                    "Cozy mystery style - no graphic violence",
                    "Focus on puzzle-solving rather than gore",
                    "Amateur detective protagonist",
                    "Small-town or community setting",
                    "Justice served but not through vigilantism"
                ];
            } else if (selectedGenre === 'science_fiction') {
                suggestions = [
                    "Hard science fiction with realistic technology",
                    "Explore ethical implications of advancement",
                    "Diverse representation in future society",
                    "Environmental consciousness themes",
                    "Optimistic view of humanity's future"
                ];
            } else if (selectedGenre === 'thriller') {
                suggestions = [
                    "Psychological tension over graphic violence",
                    "Strong, capable protagonist",
                    "Justice-focused rather than revenge-driven",
                    "Avoid excessive gore or torture scenes",
                    "Satisfying resolution with consequences"
                ];
            }

            // Audience-specific modifications
            if (selectedAudience === 'young_adult') {
                suggestions = suggestions.map(suggestion =>
                    suggestion.replace('Family-friendly', 'Age-appropriate for teens')
                );
                suggestions.push("Relatable teenage concerns and experiences");
                suggestions.push("Avoid excessive adult themes");
            } else if (selectedAudience === 'new_adult') {
                suggestions.push("College-age or early career themes");
                suggestions.push("Coming-into-adulthood challenges");
            }

            return suggestions;
        },

        // Content level helpers
        getContentLevelSuggestions() {
            return {
                'clean': {
                    label: 'Clean/Family-Friendly',
                    description: 'No profanity, minimal violence, sweet romance only',
                    examples: ['No strong language', 'Minimal conflict violence', 'Fade-to-black romance']
                },
                'moderate': {
                    label: 'Moderate Content',
                    description: 'Some mature themes but nothing graphic',
                    examples: ['Occasional mild language', 'Action violence without gore', 'Romantic tension with tasteful scenes']
                },
                'mature': {
                    label: 'Mature Themes',
                    description: 'Adult content appropriate for intended audience',
                    examples: ['Complex moral situations', 'Realistic violence when plot-relevant', 'Adult relationships treated maturely']
                }
            };
        },

        // Theme suggestions
        getThemeSuggestions() {
            return [
                'Personal growth and self-discovery',
                'Friendship and loyalty',
                'Overcoming adversity',
                'Family relationships and dynamics',
                'Love and relationships',
                'Justice and moral choices',
                'Redemption and second chances',
                'Good vs. evil',
                'Finding one\'s purpose',
                'Community and belonging',
                'Environmental consciousness',
                'Social justice and equality',
                'Mental health awareness',
                'Cultural diversity and inclusion'
            ];
        },

        // Restriction helpers
        getCommonRestrictions() {
            return [
                'No graphic violence or gore',
                'No explicit sexual content',
                'No strong profanity',
                'No animal cruelty',
                'No substance abuse glorification',
                'No suicide or self-harm themes',
                'No religious or political controversies',
                'No stereotypical representations'
            ];
        }
    };
}