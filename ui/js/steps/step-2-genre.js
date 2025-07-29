/**
 * Step 2: Genre Selection Component
 * Handles genre and subgenre selection with LLM recommendations
 */

function step2Genre() {
    return {
        // Data
        selectedGenre: '',
        selectedSubgenre: '',
        showSubgenres: false,
        isSubmitting: false,

        // Step data from API
        options: [],
        subgenreOptions: [],
        llmMessage: '',

        // UI state
        hoveredOption: null,

        // Computed
        get hasGenreSelection() {
            return this.selectedGenre !== '';
        },

        get hasSubgenreSelection() {
            return this.selectedSubgenre !== '';
        },

        get canProceed() {
            return this.hasGenreSelection && (!this.showSubgenres || this.hasSubgenreSelection);
        },

        get currentSelection() {
            if (this.showSubgenres && this.hasSubgenreSelection) {
                return this.selectedSubgenre;
            }
            return this.selectedGenre;
        },

        // Methods
        async selectGenre(genreId) {
            this.selectedGenre = genreId;
            this.selectedSubgenre = ''; // Reset subgenre when genre changes

            // Update store
            this.$store.wizard.updateFormData('genre', genreId);

            // Process genre selection and get subgenres
            await this.processGenreSelection();
        },

        async processGenreSelection() {
            if (!this.selectedGenre) return;

            this.isSubmitting = true;

            try {
                const success = await this.$store.wizard.processStep(
                    2, // Step number
                    this.selectedGenre
                );

                if (success) {
                    // Check if we got subgenre options
                    const stepData = this.$store.wizard.currentStepData;

                    if (stepData.options && stepData.options.length > 0) {
                        // We have subgenres to show
                        this.subgenreOptions = stepData.options;
                        this.showSubgenres = true;
                        this.llmMessage = stepData.llmReasoning || 'Great! Now let\'s get more specific with subgenres:';
                    } else {
                        // No subgenres, proceed to next step
                        await this.proceedToNextStep();
                    }
                }
            } catch (error) {
                console.error('Error processing genre selection:', error);
            } finally {
                this.isSubmitting = false;
            }
        },

        async selectSubgenre(subgenreId) {
            this.selectedSubgenre = subgenreId;

            // Update store
            this.$store.wizard.updateFormData('subgenre', subgenreId);

            // Process subgenre selection
            await this.processSubgenreSelection();
        },

        async processSubgenreSelection() {
            if (!this.selectedSubgenre) return;

            this.isSubmitting = true;

            try {
                const success = await this.$store.wizard.processStep(
                    2, // Still step 2, but with subgenre
                    this.selectedSubgenre
                );

                if (success) {
                    await this.proceedToNextStep();
                }
            } catch (error) {
                console.error('Error processing subgenre selection:', error);
            } finally {
                this.isSubmitting = false;
            }
        },

        async proceedToNextStep() {
            // Move to step 3 (target audience)
            this.$store.wizard.setCurrentStep(3);

            // Load step 3 data
            await this.loadTargetAudienceData();
        },

        async loadTargetAudienceData() {
            try {
                const success = await this.$store.wizard.processStep(3, null);
                // Step 3 data will be loaded in the wizard store
            } catch (error) {
                console.error('Error loading target audience data:', error);
            }
        },

        // UI Methods
        getOptionClasses(optionId) {
            const baseClasses = "border rounded-lg p-4 cursor-pointer transition-all duration-200 hover:shadow-md";
            const selectedClasses = "border-blue-500 bg-blue-50 ring-2 ring-blue-200";
            const defaultClasses = "border-gray-200 hover:border-gray-300";

            if (this.selectedGenre === optionId || this.selectedSubgenre === optionId) {
                return `${baseClasses} ${selectedClasses}`;
            }

            return `${baseClasses} ${defaultClasses}`;
        },

        getMarketAppealBadgeClasses(appeal) {
            const baseClasses = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium";

            switch (appeal?.toLowerCase()) {
                case 'high':
                    return `${baseClasses} bg-green-100 text-green-800`;
                case 'medium':
                    return `${baseClasses} bg-yellow-100 text-yellow-800`;
                case 'low':
                    return `${baseClasses} bg-gray-100 text-gray-800`;
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

        // Navigation
        goBack() {
            if (this.showSubgenres) {
                // Go back to genre selection
                this.showSubgenres = false;
                this.selectedSubgenre = '';
                this.$store.wizard.updateFormData('subgenre', '');
            } else {
                // Go back to step 1
                this.$store.wizard.setCurrentStep(1);
            }
        },

        // Data loading
        loadStepData() {
            const stepData = this.$store.wizard.currentStepData;

            this.options = stepData.options || [];
            this.llmMessage = stepData.llmReasoning || 'Based on your concept, I recommend these commercial genres:';

            // Load any existing selections
            this.selectedGenre = this.$store.wizard.formData.genre || '';
            this.selectedSubgenre = this.$store.wizard.formData.subgenre || '';
        },

        // Lifecycle
        init() {
            this.loadStepData();

            // If we don't have options, load them
            if (this.options.length === 0) {
                this.loadGenreOptions();
            }
        },

        async loadGenreOptions() {
            // This would typically be called when step data is loaded
            // For now, we'll use the data from the wizard store
            console.log('Loading genre options...');
        },

        // Utility methods
        getOptionById(optionId, optionsList = null) {
            const list = optionsList || this.options;
            return list.find(option => option.id === optionId);
        },

        getSelectedGenreInfo() {
            return this.getOptionById(this.selectedGenre);
        },

        getSelectedSubgenreInfo() {
            return this.getOptionById(this.selectedSubgenre, this.subgenreOptions);
        },

        // Format recommendation score for display
        formatRecommendationScore(score) {
            if (!score) return null;
            return `${Math.round(score)}% Match`;
        },

        // Sample genres for testing (fallback data)
        getSampleGenres() {
            return [
                {
                    id: 'fantasy',
                    name: 'Fantasy',
                    description: 'Stories with magical elements, mythical creatures, and imaginary worlds',
                    market_appeal: 'High',
                    recommendation_score: 92
                },
                {
                    id: 'romance',
                    name: 'Romance',
                    description: 'Stories focused on romantic relationships and emotional connections',
                    market_appeal: 'High',
                    recommendation_score: 78
                },
                {
                    id: 'mystery',
                    name: 'Mystery',
                    description: 'Stories involving puzzles, crimes, and detective work',
                    market_appeal: 'Medium',
                    recommendation_score: 85
                },
                {
                    id: 'science_fiction',
                    name: 'Science Fiction',
                    description: 'Stories featuring futuristic technology, space travel, and scientific concepts',
                    market_appeal: 'Medium',
                    recommendation_score: 71
                }
            ];
        }
    };
}