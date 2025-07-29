/**
 * Step 4: Writing Style Component
 * Handles writing style selection based on genre and audience
 */

function step4Style() {
    return {
        // Data
        selectedStyle: '',
        isSubmitting: false,

        // Step data from API
        options: [],
        llmMessage: '',

        // UI state
        hoveredOption: null,
        showStyleDetails: false,

        // Computed
        get hasSelection() {
            return this.selectedStyle !== '';
        },

        get canProceed() {
            return this.hasSelection;
        },

        // Methods
        async selectStyle(styleId) {
            this.selectedStyle = styleId;

            // Update store
            this.$store.wizard.updateFormData('style', styleId);

            // Process style selection
            await this.processStyleSelection();
        },

        async processStyleSelection() {
            if (!this.selectedStyle) return;

            this.isSubmitting = true;

            try {
                const success = await this.$store.wizard.processStep(
                    4, // Step number
                    this.selectedStyle
                );

                if (success) {
                    await this.proceedToNextStep();
                }
            } catch (error) {
                console.error('Error processing style selection:', error);
            } finally {
                this.isSubmitting = false;
            }
        },

        async proceedToNextStep() {
            // Move to step 5 (book length)
            this.$store.wizard.setCurrentStep(5);

            // Load step 5 data
            await this.loadBookLengthData();
        },

        async loadBookLengthData() {
            try {
                const success = await this.$store.wizard.processStep(5, null);
                // Step 5 data will be loaded in the wizard store
            } catch (error) {
                console.error('Error loading book length data:', error);
            }
        },

        // UI Methods
        getOptionClasses(optionId) {
            const baseClasses = "border rounded-lg p-6 cursor-pointer transition-all duration-200 hover:shadow-md";
            const selectedClasses = "border-blue-500 bg-blue-50 ring-2 ring-blue-200";
            const defaultClasses = "border-gray-200 hover:border-gray-300";

            if (this.selectedStyle === optionId) {
                return `${baseClasses} ${selectedClasses}`;
            }

            return `${baseClasses} ${defaultClasses}`;
        },

        getComplexityBadgeClasses(complexity) {
            const baseClasses = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium";

            switch (complexity?.toLowerCase()) {
                case 'simple':
                    return `${baseClasses} bg-green-100 text-green-800`;
                case 'moderate':
                    return `${baseClasses} bg-yellow-100 text-yellow-800`;
                case 'complex':
                    return `${baseClasses} bg-red-100 text-red-800`;
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

            this.options = stepData.options || this.getSampleStyles();
            this.llmMessage = stepData.llmReasoning || this.getDefaultMessage();

            // Load any existing selection
            this.selectedStyle = this.$store.wizard.formData.style || '';
        },

        getDefaultMessage() {
            const selectedGenre = this.$store.wizard.formData.genre;
            const selectedAudience = this.$store.wizard.formData.audience;
            return `For commercial ${selectedGenre || 'your chosen genre'} targeting ${selectedAudience || 'your audience'}, these styles work best:`;
        },

        // Lifecycle
        init() {
            this.loadStepData();

            // If we don't have step data, load it
            if (this.options.length === 0 || !this.options[0].id) {
                this.loadStyleOptions();
            }
        },

        async loadStyleOptions() {
            try {
                const success = await this.$store.wizard.processStep(4, null);
                if (success) {
                    this.loadStepData();
                }
            } catch (error) {
                console.error('Error loading style options:', error);
                // Fallback to sample data
                this.options = this.getSampleStyles();
            }
        },

        // Utility methods
        getOptionById(optionId) {
            return this.options.find(option => option.id === optionId);
        },

        getSelectedStyleInfo() {
            return this.getOptionById(this.selectedStyle);
        },

        formatRecommendationScore(score) {
            if (!score) return null;
            return `${Math.round(score)}% Match`;
        },

        // Sample styles for testing/fallback
        getSampleStyles() {
            const selectedGenre = this.$store.wizard.formData.genre;
            const selectedAudience = this.$store.wizard.formData.audience;

            // Base styles that work for most combinations
            const styles = [
                {
                    id: 'accessible_contemporary',
                    name: 'Accessible Contemporary',
                    description: 'Clear, modern prose that\'s easy to read and commercially appealing',
                    characteristics: ['Clear language', 'Modern voice', 'Broad appeal'],
                    complexity: 'Simple',
                    market_appeal: 'High',
                    recommendation_score: 88,
                    example: '"Sarah stepped into the coffee shop, the familiar aroma of espresso wrapping around her like a warm hug."'
                },
                {
                    id: 'literary_commercial',
                    name: 'Literary Commercial',
                    description: 'Elevated prose with commercial appeal, balancing artistry with readability',
                    characteristics: ['Sophisticated language', 'Character-driven', 'Literary merit'],
                    complexity: 'Moderate',
                    market_appeal: 'High',
                    recommendation_score: 75,
                    example: '"The city breathed around her, its pulse a symphony of car horns and distant conversations."'
                },
                {
                    id: 'genre_specific',
                    name: 'Genre-Specific',
                    description: 'Style tailored to genre conventions and reader expectations',
                    characteristics: ['Genre conventions', 'Reader expectations', 'Market-tested'],
                    complexity: 'Moderate',
                    market_appeal: 'High',
                    recommendation_score: 82,
                    example: this.getGenreExample(selectedGenre)
                },
                {
                    id: 'minimalist',
                    name: 'Minimalist',
                    description: 'Spare, direct prose that lets the story speak for itself',
                    characteristics: ['Concise sentences', 'Direct approach', 'Strong impact'],
                    complexity: 'Simple',
                    market_appeal: 'Medium',
                    recommendation_score: 65,
                    example: '"She left. The door closed. Everything changed."'
                }
            ];

            // Add voice-specific style for YA
            if (selectedAudience === 'young_adult') {
                styles.push({
                    id: 'authentic_ya_voice',
                    name: 'Authentic YA Voice',
                    description: 'Contemporary voice that resonates with teen readers',
                    characteristics: ['Authentic dialogue', 'Teen perspective', 'Emotional honesty'],
                    complexity: 'Simple',
                    market_appeal: 'High',
                    recommendation_score: 92,
                    example: '"I stared at my phone, waiting for a text that would probably never come. Story of my life."'
                });
            }

            // Add immersive style for fantasy/sci-fi
            if (['fantasy', 'science_fiction'].includes(selectedGenre)) {
                styles.push({
                    id: 'immersive_world_building',
                    name: 'Immersive World-Building',
                    description: 'Rich, descriptive prose that brings imaginary worlds to life',
                    characteristics: ['Detailed descriptions', 'World immersion', 'Atmospheric'],
                    complexity: 'Complex',
                    market_appeal: 'Medium',
                    recommendation_score: 78,
                    example: '"The crystalline towers of Aethermoor caught the twin suns\' light, casting rainbow shadows across the floating gardens below."'
                });
            }

            return styles;
        },

        getGenreExample(genre) {
            const examples = {
                fantasy: '"Magic crackled between her fingers as she faced the ancient dragon."',
                romance: '"His eyes met hers across the crowded room, and time seemed to stop."',
                mystery: '"The evidence pointed to only one conclusion—someone was lying."',
                science_fiction: '"The ship\'s AI spoke with unsettling calm: \'Hull breach detected.\'"',
                thriller: '"She heard footsteps behind her, matching her pace exactly."'
            };

            return examples[genre] || '"The story unfolded with compelling clarity."';
        },

        // Style analysis and recommendations
        getStyleAnalysis(styleId) {
            const style = this.getOptionById(styleId);
            if (!style) return null;

            const selectedGenre = this.$store.wizard.formData.genre;
            const selectedAudience = this.$store.wizard.formData.audience;

            return {
                strengths: this.getStyleStrengths(styleId, selectedGenre, selectedAudience),
                considerations: this.getStyleConsiderations(styleId, selectedGenre, selectedAudience),
                marketFit: this.getMarketFit(styleId, selectedGenre, selectedAudience)
            };
        },

        getStyleStrengths(styleId, genre, audience) {
            const strengths = {
                accessible_contemporary: ['Broad market appeal', 'Easy to read', 'Strong commercial potential'],
                literary_commercial: ['Critical respect', 'Award potential', 'Crossover appeal'],
                genre_specific: ['Reader expectations met', 'Strong genre appeal', 'Publisher friendly'],
                minimalist: ['Powerful impact', 'Modern appeal', 'Easy to write'],
                authentic_ya_voice: ['Teen authenticity', 'Strong emotional connection', 'Series potential'],
                immersive_world_building: ['Fan engagement', 'World expansion possibilities', 'Memorable settings']
            };

            return strengths[styleId] || ['Clear communication', 'Reader engagement'];
        },

        getStyleConsiderations(styleId, genre, audience) {
            const considerations = {
                accessible_contemporary: ['May lack distinctiveness', 'High competition'],
                literary_commercial: ['Longer writing time', 'Smaller initial audience'],
                genre_specific: ['Genre limitations', 'Reader expectations pressure'],
                minimalist: ['May seem too simple', 'Limited description'],
                authentic_ya_voice: ['Age-specific appeal', 'Trend dependency'],
                immersive_world_building: ['Longer books required', 'Complex plotting needed']
            };

            return considerations[styleId] || ['Style learning curve'];
        },

        getMarketFit(styleId, genre, audience) {
            // This would be calculated based on genre/audience combinations
            const fits = {
                accessible_contemporary: 'Excellent for most genres and audiences',
                literary_commercial: 'Best for adult fiction and literary genres',
                genre_specific: 'Perfect match for established genre readers',
                minimalist: 'Great for literary fiction and short works',
                authentic_ya_voice: 'Essential for YA contemporary and romance',
                immersive_world_building: 'Ideal for fantasy and science fiction'
            };

            return fits[styleId] || 'Good general fit';
        },

        // Show detailed style information
        toggleStyleDetails(styleId) {
            if (this.showStyleDetails === styleId) {
                this.showStyleDetails = false;
            } else {
                this.showStyleDetails = styleId;
            }
        },

        // Navigation
        goBack() {
            this.$store.wizard.setCurrentStep(3);
        }
    };
}