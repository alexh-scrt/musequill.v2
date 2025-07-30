/**
 * Step 9: Final Summary Component
 * Displays complete book definition and handles wizard completion
 */

function step9Summary() {
    return {
        // Data
        isGenerating: false,
        summaryData: null,
        showValidation: false,

        // Step data from API
        llmMessage: '',
        bookDefinition: null,
        researchPlan: null,

        // UI state
        activeTab: 'overview',

        // Computed
        get isComplete() {
            return this.bookDefinition !== null;
        },

        get canFinish() {
            return this.isComplete && !this.isGenerating;
        },

        // Methods
        async generateBookDefinition() {
            this.isGenerating = true;

            try {
                const success = await this.$store.wizard.processStep(
                    9, // Step number
                    'generate_final' // Signal to generate complete definition
                );

                if (success) {
                    this.loadSummaryData();
                }
            } catch (error) {
                console.error('Error generating book definition:', error);
            } finally {
                this.isGenerating = false;
            }
        },

        async finishWizard() {
            if (!this.canFinish) return;

            try {
                // Update store with completion
                this.$store.wizard.setComplete(true);

                // You could navigate to a new page or show completion state
                console.log('Wizard completed!', this.bookDefinition);

                // For now, just show an alert
                alert('Book definition complete! Ready to start writing.');

            } catch (error) {
                console.error('Error finishing wizard:', error);
            }
        },

        // Navigation
        goBack() {
            // Go back to step 8 (content preferences)
            this.$store.wizard.setCurrentStep(8);
        },

        editStep(stepNumber) {
            // Navigate back to a specific step for editing
            this.$store.wizard.setCurrentStep(stepNumber);
        },

        // Data loading
        loadSummaryData() {
            const stepData = this.$store.wizard.currentStepData;
            const formData = this.$store.wizard.formData;

            this.llmMessage = stepData.llmReasoning || 'Here\'s your commercial book blueprint:';
            this.bookDefinition = stepData.bookDefinition || this.generateSummaryFromFormData();
            this.researchPlan = stepData.researchPlan || null;
        },

        generateSummaryFromFormData() {
            const formData = this.$store.wizard.formData;

            return {
                concept: formData.concept,
                genre: {
                    primary: formData.genre,
                    subgenre: formData.subgenre
                },
                targetAudience: formData.audience,
                writingStyle: formData.style,
                bookLength: formData.length,
                storyStructure: formData.structure,
                worldType: formData.world,
                contentPreferences: formData.contentPreferences || 'No specific restrictions',
                marketingTagline: this.generateTagline(formData),
                estimatedWritingTime: this.estimateWritingTime(formData),
                commercialViability: this.assessCommercialViability(formData)
            };
        },

        // Tab management
        setActiveTab(tab) {
            this.activeTab = tab;
        },

        // Utility methods
        generateTagline(formData) {
            const genreMap = {
                'romance': 'A heartwarming romance',
                'fantasy': 'An epic fantasy adventure',
                'mystery': 'A gripping mystery',
                'science_fiction': 'A thought-provoking sci-fi story',
                'thriller': 'A heart-pounding thriller',
                'literary_fiction': 'A compelling literary story'
            };

            const base = genreMap[formData.genre] || 'An engaging story';
            const audience = formData.audience === 'young_adult' ? ' for young readers' : '';

            return `${base}${audience} that explores themes of growth and discovery.`;
        },

        estimateWritingTime(formData) {
            const lengthMap = {
                'novella': '2-4 months',
                'short_novel': '4-6 months',
                'standard_novel': '6-9 months',
                'long_novel': '9-12 months',
                'epic_length': '12+ months'
            };

            return lengthMap[formData.length] || '6-9 months';
        },

        assessCommercialViability(formData) {
            // Simple scoring based on popular combinations
            let score = 70; // Base score

            // Genre popularity adjustments
            const genreBonus = {
                'romance': 15,
                'fantasy': 10,
                'mystery': 8,
                'thriller': 8,
                'science_fiction': 5
            };
            score += genreBonus[formData.genre] || 0;

            // Audience size adjustments
            if (formData.audience === 'adult') score += 10;
            if (formData.audience === 'young_adult') score += 8;

            // Length optimization
            if (formData.length === 'standard_novel') score += 5;

            return Math.min(score, 95); // Cap at 95%
        },

        // Validation helpers
        validateBookDefinition() {
            const required = ['concept', 'genre', 'audience', 'style', 'length', 'structure', 'world'];
            const formData = this.$store.wizard.formData;

            const missing = required.filter(field => !formData[field] || formData[field].trim() === '');

            if (missing.length > 0) {
                return {
                    isValid: false,
                    missing: missing,
                    message: `Missing required fields: ${missing.join(', ')}`
                };
            }

            return { isValid: true, message: 'All required fields complete' };
        },

        // Formatting helpers
        formatFieldName(fieldName) {
            const nameMap = {
                'concept': 'Book Concept',
                'genre': 'Primary Genre',
                'subgenre': 'Subgenre',
                'audience': 'Target Audience',
                'style': 'Writing Style',
                'length': 'Book Length',
                'structure': 'Story Structure',
                'world': 'World/Setting',
                'contentPreferences': 'Content Preferences'
            };
            return nameMap[fieldName] || fieldName;
        },

        formatValue(value) {
            if (!value) return 'Not specified';
            if (typeof value === 'string') {
                return value.charAt(0).toUpperCase() + value.slice(1).replace(/_/g, ' ');
            }
            return String(value);
        },

        // Research plan helpers
        getResearchCategories() {
            if (!this.researchPlan) return [];

            return [
                {
                    name: 'Genre Research',
                    items: this.researchPlan.genre_research || [],
                    description: 'Understanding your genre\'s conventions and reader expectations'
                },
                {
                    name: 'World Building',
                    items: this.researchPlan.world_research || [],
                    description: 'Research needed for your chosen setting and world'
                },
                {
                    name: 'Character Development',
                    items: this.researchPlan.character_research || [],
                    description: 'Research to create authentic, compelling characters'
                },
                {
                    name: 'Plot & Structure',
                    items: this.researchPlan.structure_research || [],
                    description: 'Understanding your chosen story structure and pacing'
                }
            ];
        },

        // Lifecycle
        init() {
            this.loadSummaryData();

            // If we don't have a complete definition, generate it
            if (!this.bookDefinition && !this.isGenerating) {
                this.generateBookDefinition();
            }
        },

        // Export functionality
        exportSummary() {
            const data = {
                bookDefinition: this.bookDefinition,
                formData: this.$store.wizard.formData,
                researchPlan: this.researchPlan,
                generatedAt: new Date().toISOString()
            };

            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'musequill-book-definition.json';
            a.click();
            URL.revokeObjectURL(url);
        },

        // Share functionality
        shareDefinition() {
            if (navigator.share) {
                navigator.share({
                    title: 'My Book Definition',
                    text: `I just created a book definition with Musequill: ${this.bookDefinition.concept}`,
                    url: window.location.href
                });
            } else {
                // Fallback: copy to clipboard
                const text = `My Book Definition:\n${this.bookDefinition.concept}\nGenre: ${this.bookDefinition.genre.primary}\nTarget: ${this.bookDefinition.targetAudience}`;
                navigator.clipboard.writeText(text).then(() => {
                    alert('Book definition copied to clipboard!');
                });
            }
        }
    };
}