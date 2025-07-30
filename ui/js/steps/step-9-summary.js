/**
 * Step 9: Final Summary Component
 * Displays complete book definition and handles wizard completion
 * NOTE: Step 8 is actually the final API step, Step 9 just displays the summary
 */

function step9Summary() {
    return {
        // Data
        isGenerating: false,
        summaryData: null,
        showValidation: false,

        // Step data from API (loaded from step 8 response)
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

        get currentStepData() {
            return this.$store.wizard.currentStepData;
        },

        get formData() {
            return this.$store.wizard.formData;
        },

        // Methods - NO API CALLS TO STEP 9!
        async finishWizard() {
            if (!this.canFinish) return;

            try {
                // Update store with completion
                // this.$store.wizard.setComplete(true); // If this method exists

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

        // Data loading - NO API CALLS, just use data from step 8
        loadSummaryData() {
            console.log('📥 Step9Summary - loadSummaryData called');

            const stepData = this.currentStepData;
            const formData = this.formData;

            console.log('📥 Step9Summary - stepData:', stepData);
            console.log('📥 Step9Summary - formData:', formData);

            // Load data from step 8 response or generate from form data
            this.llmMessage = stepData?.llmReasoning || stepData?.llm_reasoning || 'Here\'s your commercial book blueprint:';
            this.bookDefinition = stepData?.bookDefinition || stepData?.book_definition || this.generateSummaryFromFormData();
            this.researchPlan = stepData?.researchPlan || stepData?.research_plan || null;

            console.log('📥 Step9Summary - Loaded llmMessage:', this.llmMessage);
            console.log('📥 Step9Summary - Loaded bookDefinition:', this.bookDefinition);
            console.log('📥 Step9Summary - Loaded researchPlan:', this.researchPlan);
        },

        generateSummaryFromFormData() {
            console.log('🔧 Step9Summary - generateSummaryFromFormData called');

            const formData = this.formData;

            const summary = {
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

            console.log('🔧 Step9Summary - Generated summary:', summary);
            return summary;
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
            const audience = formData.audience === 'young_adult' ? ' for young adults' : '';
            return `${base}${audience}`;
        },

        estimateWritingTime(formData) {
            const lengthMap = {
                'short_story': '1-2 weeks',
                'novella': '1-2 months',
                'novel': '3-6 months',
                'epic': '6-12 months'
            };
            return lengthMap[formData.length] || '3-6 months';
        },

        assessCommercialViability(formData) {
            // Simple scoring based on popular combinations
            let score = 5; // Base score

            // Popular genres get bonus points
            const popularGenres = ['romance', 'fantasy', 'mystery', 'thriller'];
            if (popularGenres.includes(formData.genre)) {
                score += 2;
            }

            // Adult and YA audiences are commercially strong
            if (['adult', 'young_adult'].includes(formData.audience)) {
                score += 1;
            }

            // Novel length is most commercial
            if (formData.length === 'novel') {
                score += 1;
            }

            return {
                score: Math.min(10, score),
                rating: score >= 7 ? 'High' : score >= 5 ? 'Medium' : 'Developing',
                factors: this.getViabilityFactors(formData)
            };
        },

        getViabilityFactors(formData) {
            const factors = [];

            const popularGenres = ['romance', 'fantasy', 'mystery', 'thriller'];
            if (popularGenres.includes(formData.genre)) {
                factors.push('Popular genre with strong market demand');
            }

            if (['adult', 'young_adult'].includes(formData.audience)) {
                factors.push('Target audience with high reading engagement');
            }

            if (formData.length === 'novel') {
                factors.push('Optimal length for commercial publishing');
            }

            return factors;
        },

        // Research plan utilities
        getResearchCategories() {
            if (!this.researchPlan) return [];

            return [
                {
                    name: 'Genre Research',
                    items: this.researchPlan.genre_research || [],
                    description: 'Understanding market expectations and reader preferences'
                },
                {
                    name: 'Character Development',
                    items: this.researchPlan.character_research || [],
                    description: 'Creating authentic, relatable characters'
                },
                {
                    name: 'World Building',
                    items: this.researchPlan.world_research || [],
                    description: 'Developing your story\'s setting and atmosphere'
                },
                {
                    name: 'Story Structure',
                    items: this.researchPlan.structure_research || [],
                    description: 'Understanding your chosen story structure and pacing'
                }
            ];
        },

        // Lifecycle - NO API CALLS!
        init() {
            console.log('🚀 Step9Summary - INIT STARTED');
            console.log('🚀 Step9Summary - Current step:', this.$store.wizard.currentStep);
            console.log('🚀 Step9Summary - Session ID:', this.$store.wizard.sessionId);

            // Load summary data from step 8 response (no API calls)
            this.loadSummaryData();

            console.log('🏁 Step9Summary - INIT COMPLETED (no API calls made)');
        },

        // Export functionality
        exportSummary() {
            const data = {
                bookDefinition: this.bookDefinition,
                formData: this.formData,
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
        },

        // Debug helper
        logDebugInfo() {
            console.log('🔧 Step9Summary - DEBUG INFO:');
            console.log('🔧 Current Step:', this.$store.wizard.currentStep);
            console.log('🔧 Session ID:', this.$store.wizard.sessionId);
            console.log('🔧 Current Step Data:', this.currentStepData);
            console.log('🔧 Form Data:', this.formData);
            console.log('🔧 Book Definition:', this.bookDefinition);
            console.log('🔧 Research Plan:', this.researchPlan);
            console.log('🔧 LLM Message:', this.llmMessage);
            console.log('🔧 Is Complete:', this.isComplete);
            console.log('🔧 Can Finish:', this.canFinish);
        }
    };
}