/**
 * Step 3: Target Audience Component
 * Handles target audience selection based on genre
 */

function step3Audience() {
    return {
        // Data
        selectedAudience: '',
        isSubmitting: false,

        // Step data from API
        options: [],
        llmMessage: '',

        // UI state
        hoveredOption: null,

        // Computed
        get hasSelection() {
            return this.selectedAudience !== '';
        },

        get canProceed() {
            return this.hasSelection;
        },

        // Methods
        async selectAudience(audienceId) {
            this.selectedAudience = audienceId;

            // Update store
            this.$store.wizard.updateFormData('audience', audienceId);

            // Process audience selection
            await this.processAudienceSelection();
        },

        async processAudienceSelection() {
            if (!this.selectedAudience) return;

            this.isSubmitting = true;

            try {
                const success = await this.$store.wizard.processStep(
                    3, // Step number
                    this.selectedAudience
                );

                if (success) {
                    await this.proceedToNextStep();
                }
            } catch (error) {
                console.error('Error processing audience selection:', error);
            } finally {
                this.isSubmitting = false;
            }
        },

        async proceedToNextStep() {
            // Move to step 4 (writing style)
            this.$store.wizard.setCurrentStep(4);

            // Load step 4 data
            await this.loadWritingStyleData();
        },

        async loadWritingStyleData() {
            try {
                const success = await this.$store.wizard.processStep(4, null);
                // Step 4 data will be loaded in the wizard store
            } catch (error) {
                console.error('Error loading writing style data:', error);
            }
        },

        // UI Methods
        getOptionClasses(optionId) {
            const baseClasses = "border rounded-lg p-6 cursor-pointer transition-all duration-200 hover:shadow-md";
            const selectedClasses = "border-blue-500 bg-blue-50 ring-2 ring-blue-200";
            const defaultClasses = "border-gray-200 hover:border-gray-300";

            if (this.selectedAudience === optionId) {
                return `${baseClasses} ${selectedClasses}`;
            }

            return `${baseClasses} ${defaultClasses}`;
        },

        getMarketSizeBadgeClasses(marketSize) {
            const baseClasses = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium";

            switch (marketSize?.toLowerCase()) {
                case 'large':
                    return `${baseClasses} bg-green-100 text-green-800`;
                case 'medium':
                    return `${baseClasses} bg-yellow-100 text-yellow-800`;
                case 'small':
                    return `${baseClasses} bg-orange-100 text-orange-800`;
                case 'niche':
                    return `${baseClasses} bg-purple-100 text-purple-800`;
                default:
                    return `${baseClasses} bg-gray-100 text-gray-600`;
            }
        },

        onOptionHover(optionId) {
            this.hoveredOption = optionId;
        },

        onOptionLeave() {
            this.hoveredOption = null;
        },

        // Data loading
        loadStepData() {
            const stepData = this.$store.wizard.currentStepData;

            this.options = stepData.options || this.getSampleAudiences();
            this.llmMessage = stepData.llmReasoning || this.getDefaultMessage();

            // Load any existing selection
            this.selectedAudience = this.$store.wizard.formData.audience || '';
        },

        getDefaultMessage() {
            const selectedGenre = this.$store.wizard.formData.genre;
            return `For ${selectedGenre || 'your chosen genre'}, these audiences offer the best commercial potential:`;
        },

        // Lifecycle
        init() {
            this.loadStepData();

            // If we don't have step data, load it
            if (this.options.length === 0 || !this.options[0].id) {
                this.loadAudienceOptions();
            }
        },

        async loadAudienceOptions() {
            // Load options based on current selections
            try {
                const success = await this.$store.wizard.processStep(3, null);
                if (success) {
                    this.loadStepData();
                }
            } catch (error) {
                console.error('Error loading audience options:', error);
                // Fallback to sample data
                this.options = this.getSampleAudiences();
            }
        },

        // Utility methods
        getOptionById(optionId) {
            return this.options.find(option => option.id === optionId);
        },

        getSelectedAudienceInfo() {
            return this.getOptionById(this.selectedAudience);
        },

        formatRecommendationScore(score) {
            if (!score) return null;
            return `${Math.round(score)}% Match`;
        },

        // Sample audiences for testing/fallback
        getSampleAudiences() {
            const selectedGenre = this.$store.wizard.formData.genre;

            // Base audiences that work for most genres
            const baseAudiences = [
                {
                    id: 'adult',
                    name: 'Adult (18+)',
                    description: 'Mature readers seeking sophisticated narratives and complex themes',
                    market_size: 'Large',
                    age_range: '18-65+',
                    characteristics: ['Complex themes', 'Mature content', 'Sophisticated language'],
                    recommendation_score: 85
                },
                {
                    id: 'young_adult',
                    name: 'Young Adult (13-18)',
                    description: 'Teen readers navigating coming-of-age experiences and identity',
                    market_size: 'Large',
                    age_range: '13-18',
                    characteristics: ['Coming-of-age', 'Identity themes', 'Accessible language'],
                    recommendation_score: 78
                },
                {
                    id: 'new_adult',
                    name: 'New Adult (18-25)',
                    description: 'Young adults transitioning to independence with relatable struggles',
                    market_size: 'Medium',
                    age_range: '18-25',
                    characteristics: ['Independence themes', 'College/career', 'Modern issues'],
                    recommendation_score: 72
                }
            ];

            // Add middle grade for certain genres
            if (['fantasy', 'adventure', 'mystery'].includes(selectedGenre)) {
                baseAudiences.push({
                    id: 'middle_grade',
                    name: 'Middle Grade (8-12)',
                    description: 'Young readers discovering chapter books and adventure stories',
                    market_size: 'Medium',
                    age_range: '8-12',
                    characteristics: ['Age-appropriate content', 'Adventure focus', 'Clear moral lessons'],
                    recommendation_score: 65
                });
            }

            return baseAudiences;
        },

        // Navigation
        goBack() {
            this.$store.wizard.setCurrentStep(2);
        },

        // Audience insights
        getAudienceInsights(audienceId) {
            const insights = {
                adult: {
                    marketTrends: 'Strong market for literary fiction, thrillers, and romance',
                    publishingTips: 'Focus on complex characters and nuanced themes',
                    wordCount: '80,000-120,000 words typical'
                },
                young_adult: {
                    marketTrends: 'Huge market with crossover adult readership',
                    publishingTips: 'Authentic voice and contemporary issues crucial',
                    wordCount: '50,000-80,000 words typical'
                },
                new_adult: {
                    marketTrends: 'Growing segment, especially in romance and contemporary',
                    publishingTips: 'Bridge between YA and adult themes',
                    wordCount: '60,000-90,000 words typical'
                },
                middle_grade: {
                    marketTrends: 'Steady market with strong institutional sales',
                    publishingTips: 'Fast pacing and clear stakes essential',
                    wordCount: '20,000-50,000 words typical'
                }
            };

            return insights[audienceId] || {};
        },

        showAudienceDetails(audienceId) {
            const audience = this.getOptionById(audienceId);
            const insights = this.getAudienceInsights(audienceId);

            if (audience) {
                // You could implement a modal or expanded view here
                console.log('Audience details:', { audience, insights });
            }
        }
    };
}