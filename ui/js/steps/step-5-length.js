/**
 * Step 5: Book Length Component
 * Handles book length selection based on genre and market requirements
 */

function step5Length() {
    return {
        // Data
        selectedLength: '',
        isSubmitting: false,

        // Step data from API
        options: [],
        llmMessage: '',

        // UI state
        hoveredOption: null,
        showLengthDetails: false,

        // Computed
        get hasSelection() {
            return this.selectedLength !== '';
        },

        get canProceed() {
            return this.hasSelection;
        },

        // Methods
        async selectLength(lengthId) {
            this.selectedLength = lengthId;

            // Update store
            this.$store.wizard.updateFormData('length', lengthId);

            // Process length selection
            await this.processLengthSelection();
        },

        async processLengthSelection() {
            if (!this.selectedLength) return;

            this.isSubmitting = true;

            try {
                const success = await this.$store.wizard.processStep(
                    5, // Step number
                    this.selectedLength
                );

                if (success) {
                    await this.proceedToNextStep();
                }
            } catch (error) {
                console.error('Error processing length selection:', error);
            } finally {
                this.isSubmitting = false;
            }
        },

        async proceedToNextStep() {
            // Move to step 6 (story structure)
            this.$store.wizard.setCurrentStep(6);

            // Load step 6 data
            await this.loadStoryStructureData();
        },

        async loadStoryStructureData() {
            try {
                const success = await this.$store.wizard.processStep(6, null);
                // Step 6 data will be loaded in the wizard store
            } catch (error) {
                console.error('Error loading story structure data:', error);
            }
        },

        // UI Methods
        getOptionClasses(optionId) {
            const baseClasses = "border rounded-lg p-6 cursor-pointer transition-all duration-200 hover:shadow-md";
            const selectedClasses = "border-blue-500 bg-blue-50 ring-2 ring-blue-200";
            const defaultClasses = "border-gray-200 hover:border-gray-300";

            if (this.selectedLength === optionId) {
                return `${baseClasses} ${selectedClasses}`;
            }

            return `${baseClasses} ${defaultClasses}`;
        },

        getViabilityBadgeClasses(viability) {
            const baseClasses = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium";

            switch (viability?.toLowerCase()) {
                case 'high':
                    return `${baseClasses} bg-green-100 text-green-800`;
                case 'medium':
                    return `${baseClasses} bg-yellow-100 text-yellow-800`;
                case 'low':
                    return `${baseClasses} bg-red-100 text-red-800`;
                default:
                    return `${baseClasses} bg-gray-100 text-gray-600`;
            }
        },

        getTimeBadgeClasses(timeToWrite) {
            const baseClasses = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium";

            if (timeToWrite && timeToWrite.includes('month')) {
                return `${baseClasses} bg-blue-100 text-blue-800`;
            } else if (timeToWrite && timeToWrite.includes('year')) {
                return `${baseClasses} bg-purple-100 text-purple-800`;
            }

            return `${baseClasses} bg-gray-100 text-gray-600`;
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

            this.options = stepData.options || this.getSampleLengths();
            this.llmMessage = stepData.llmReasoning || this.getDefaultMessage();

            // Load any existing selection
            this.selectedLength = this.$store.wizard.formData.length || '';
        },

        getDefaultMessage() {
            const selectedGenre = this.$store.wizard.formData.genre;
            return `For commercial success in ${selectedGenre || 'your chosen genre'}, these lengths perform best:`;
        },

        // Lifecycle
        init() {
            this.loadStepData();

            // If we don't have step data, load it
            if (this.options.length === 0 || !this.options[0].id) {
                this.loadLengthOptions();
            }
        },

        async loadLengthOptions() {
            try {
                const success = await this.$store.wizard.processStep(5, null);
                if (success) {
                    this.loadStepData();
                }
            } catch (error) {
                console.error('Error loading length options:', error);
                // Fallback to sample data
                this.options = this.getSampleLengths();
            }
        },

        // Utility methods
        getOptionById(optionId) {
            return this.options.find(option => option.id === optionId);
        },

        getSelectedLengthInfo() {
            return this.getOptionById(this.selectedLength);
        },

        formatRecommendationScore(score) {
            if (!score) return null;
            return `${Math.round(score)}% Match`;
        },

        // Sample lengths for testing/fallback
        getSampleLengths() {
            const selectedGenre = this.$store.wizard.formData.genre;
            const selectedAudience = this.$store.wizard.formData.audience;

            const baseLengths = [
                {
                    id: 'novella',
                    name: 'Novella',
                    description: 'A shorter work perfect for focused storytelling and faster completion',
                    word_count: '20,000 - 40,000 words',
                    page_count: '80 - 160 pages',
                    time_to_write: '2-4 months',
                    publishing_viability: 'Medium',
                    market_appeal: 'Niche',
                    recommendation_score: this.calculateScore('novella', selectedGenre, selectedAudience),
                    advantages: ['Faster to write', 'Easy to read', 'Good for first books'],
                    considerations: ['Limited market', 'Shorter story arc', 'Pricing challenges']
                },
                {
                    id: 'standard_novel',
                    name: 'Standard Novel',
                    description: 'The industry standard length with broad market appeal and publishing support',
                    word_count: '70,000 - 90,000 words',
                    page_count: '280 - 360 pages',
                    time_to_write: '6-12 months',
                    publishing_viability: 'High',
                    market_appeal: 'High',
                    recommendation_score: this.calculateScore('standard_novel', selectedGenre, selectedAudience),
                    advantages: ['Market standard', 'Publishing friendly', 'Reader expectations'],
                    considerations: ['Substantial commitment', 'Complex plotting required', 'Longer development time']
                },
                {
                    id: 'short_novel',
                    name: 'Short Novel',
                    description: 'Compact storytelling that respects reader time while delivering full narrative',
                    word_count: '50,000 - 70,000 words',
                    page_count: '200 - 280 pages',
                    time_to_write: '4-8 months',
                    publishing_viability: 'High',
                    market_appeal: 'Medium',
                    recommendation_score: this.calculateScore('short_novel', selectedGenre, selectedAudience),
                    advantages: ['Manageable length', 'Good pacing', 'Reader friendly'],
                    considerations: ['Genre limitations', 'Tight plotting required', 'Less development space']
                },
                {
                    id: 'epic_novel',
                    name: 'Epic Novel',
                    description: 'Extended storytelling for complex narratives and deep world-building',
                    word_count: '100,000+ words',
                    page_count: '400+ pages',
                    time_to_write: '12-24 months',
                    publishing_viability: 'Medium',
                    market_appeal: 'High',
                    recommendation_score: this.calculateScore('epic_novel', selectedGenre, selectedAudience),
                    advantages: ['Deep development', 'Complex plots', 'Fan engagement'],
                    considerations: ['Major commitment', 'Publishing challenges', 'Reader investment required']
                }
            ];

            // Filter based on genre appropriateness
            return baseLengths.filter(length => this.isAppropriateForGenre(length.id, selectedGenre));
        },

        calculateScore(lengthId, genre, audience) {
            // Scoring based on genre and audience fit
            const scores = {
                novella: {
                    romance: 75,
                    mystery: 65,
                    fantasy: 45,
                    science_fiction: 50,
                    default: 60
                },
                short_novel: {
                    romance: 85,
                    mystery: 80,
                    young_adult: 85,
                    default: 75
                },
                standard_novel: {
                    all: 90, // Good for everything
                    default: 90
                },
                epic_novel: {
                    fantasy: 95,
                    science_fiction: 90,
                    adult: 85,
                    default: 70
                }
            };

            const lengthScores = scores[lengthId] || {};

            return lengthScores[genre] ||
                lengthScores[audience] ||
                lengthScores.all ||
                lengthScores.default ||
                70;
        },

        isAppropriateForGenre(lengthId, genre) {
            // Some length/genre combinations work better than others
            const inappropriate = {
                novella: ['epic_fantasy'],
                epic_novel: ['contemporary_romance']
            };

            const lengthRestrictions = inappropriate[lengthId] || [];
            return !lengthRestrictions.includes(genre);
        },

        // Length analysis and recommendations
        getLengthAnalysis(lengthId) {
            const length = this.getOptionById(lengthId);
            if (!length) return null;

            const selectedGenre = this.$store.wizard.formData.genre;
            const selectedAudience = this.$store.wizard.formData.audience;

            return {
                marketFit: this.getMarketFit(lengthId, selectedGenre, selectedAudience),
                writingConsiderations: this.getWritingConsiderations(lengthId),
                publishingAdvice: this.getPublishingAdvice(lengthId, selectedGenre)
            };
        },

        getMarketFit(lengthId, genre, audience) {
            const fits = {
                novella: 'Best for literary fiction and specialized markets',
                short_novel: 'Excellent for debut authors and specific genres',
                standard_novel: 'Optimal for most commercial fiction',
                epic_novel: 'Perfect for fantasy/sci-fi and series potential'
            };

            return fits[lengthId] || 'Good general market fit';
        },

        getWritingConsiderations(lengthId) {
            const considerations = {
                novella: ['Tight plotting essential', 'Every scene must count', 'Limited character development space'],
                short_novel: ['Efficient storytelling', 'Focus on main plot', 'Careful pacing required'],
                standard_novel: ['Balanced development', 'Multiple plot threads possible', 'Industry expectations'],
                epic_novel: ['Complex plotting required', 'Extensive world-building', 'Multiple character arcs']
            };

            return considerations[lengthId] || ['Standard writing considerations apply'];
        },

        getPublishingAdvice(lengthId, genre) {
            const advice = {
                novella: 'Consider digital-first publishing or literary magazines',
                short_novel: 'Great for debut novels, agents love manageable lengths',
                standard_novel: 'Perfect for traditional publishing, meets all expectations',
                epic_novel: 'Ensure exceptional quality, consider series potential'
            };

            return advice[lengthId] || 'Standard publishing approach recommended';
        },

        // Show detailed length information
        toggleLengthDetails(lengthId) {
            if (this.showLengthDetails === lengthId) {
                this.showLengthDetails = false;
            } else {
                this.showLengthDetails = lengthId;
            }
        },

        // Writing time calculator
        getWritingSchedule(lengthId) {
            const length = this.getOptionById(lengthId);
            if (!length) return null;

            const wordCounts = {
                novella: 30000,
                short_novel: 60000,
                standard_novel: 80000,
                epic_novel: 120000
            };

            const wordCount = wordCounts[lengthId] || 80000;
            const wordsPerDay = 500; // Conservative estimate
            const daysToWrite = Math.ceil(wordCount / wordsPerDay);
            const monthsToWrite = Math.ceil(daysToWrite / 30);

            return {
                totalWords: wordCount.toLocaleString(),
                wordsPerDay: wordsPerDay.toLocaleString(),
                estimatedDays: daysToWrite,
                estimatedMonths: monthsToWrite,
                schedule: this.generateWritingSchedule(daysToWrite)
            };
        },

        generateWritingSchedule(totalDays) {
            if (totalDays <= 60) {
                return 'Daily writing recommended';
            } else if (totalDays <= 180) {
                return 'Write 5 days per week';
            } else {
                return 'Consistent weekly schedule essential';
            }
        },

        // Navigation
        goBack() {
            this.$store.wizard.setCurrentStep(4);
        }
    };
}