/**
 * Step 3: Target Audience Component
 * Enhanced with LLM data access and comprehensive debug logging
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
        showAnalysisDetails: false,

        // Computed properties to access wizard store data (with logging)
        get conceptAnalysis() {
            const analysis = this.$store.wizard.conceptAnalysis;
            console.log('🔍 Step3Audience - Accessing conceptAnalysis:', analysis);
            return analysis;
        },

        get hasConceptAnalysis() {
            const hasAnalysis = this.conceptAnalysis && this.conceptAnalysis.analysis_successful;
            console.log('✅ Step3Audience - hasConceptAnalysis:', hasAnalysis);
            return hasAnalysis;
        },

        get currentStepData() {
            const stepData = this.$store.wizard.currentStepData;
            console.log('📊 Step3Audience - currentStepData:', stepData);
            return stepData;
        },

        get userConcept() {
            const concept = this.$store.wizard.formData.concept;
            console.log('💭 Step3Audience - userConcept:', concept);
            return concept;
        },

        get selectedGenre() {
            const genre = this.$store.wizard.formData.genre;
            console.log('🎭 Step3Audience - selectedGenre:', genre);
            return genre;
        },

        get selectedSubgenre() {
            const subgenre = this.$store.wizard.formData.subgenre;
            console.log('🎪 Step3Audience - selectedSubgenre:', subgenre);
            return subgenre;
        },

        // Enhanced options that combine API data with analysis context (with logging)
        get enhancedOptions() {
            console.log('🚀 Step3Audience - Building enhancedOptions...');
            console.log('🚀 Step3Audience - hasConceptAnalysis:', this.hasConceptAnalysis);
            console.log('🚀 Step3Audience - currentStepData.options:', this.currentStepData?.options?.length || 0);

            let baseOptions = [];

            // Use API data if available
            if (this.currentStepData?.options && this.currentStepData.options.length > 0) {
                console.log('✨ Step3Audience - Using API options');
                baseOptions = this.currentStepData.options;
            } else if (this.options.length > 0) {
                console.log('⚡ Step3Audience - Using component options');
                baseOptions = this.options;
            } else {
                console.log('⚠️ Step3Audience - Using fallback sample options');
                baseOptions = this.getSampleAudiences();
            }

            // Enhance options with analysis context
            const enhancedOptions = baseOptions.map(option => {
                console.log('🎯 Step3Audience - Processing option:', option);

                const enhanced = {
                    ...option,
                    // Add analysis-based enhancements
                    analysis_context: this.getAnalysisContext(option.id),
                    genre_compatibility: this.getGenreCompatibility(option.id),
                    market_insights: this.getMarketInsights(option.id),
                    source: this.currentStepData?.options ? 'api_data' : 'component_fallback'
                };

                console.log('🎯 Step3Audience - Enhanced option:', enhanced);
                return enhanced;
            });

            console.log('✨ Step3Audience - Final enhanced options:', enhancedOptions);
            return enhancedOptions;
        },

        // Computed
        get hasSelection() {
            const hasSelection = this.selectedAudience !== '';
            console.log('🎯 Step3Audience - hasSelection:', hasSelection);
            return hasSelection;
        },

        get canProceed() {
            const canProceed = this.hasSelection;
            console.log('✅ Step3Audience - canProceed:', canProceed);
            return canProceed;
        },

        // Methods (with enhanced logging)
        async selectAudience(audienceId) {
            console.log('🎬 Step3Audience - selectAudience called with:', audienceId);

            this.selectedAudience = audienceId;
            console.log('🎬 Step3Audience - Set selectedAudience:', this.selectedAudience);

            // Update store
            this.$store.wizard.updateFormData('audience', audienceId);
            console.log('🎬 Step3Audience - Updated wizard store formData');
            console.log('🎬 Step3Audience - Current formData:', this.$store.wizard.formData);

            // Process audience selection
            await this.processAudienceSelection();
        },

        async processAudienceSelection() {
            console.log('🔥 Step3Audience - processAudienceSelection called');

            if (!this.selectedAudience) {
                console.log('❌ Step3Audience - No audience selected, aborting');
                return;
            }

            this.isSubmitting = true;
            console.log('🔥 Step3Audience - Set isSubmitting to true');

            try {
                const stepData = {
                    session_id: this.$store.wizard.sessionId,
                    selection: this.selectedAudience,
                    additional_input: this.getSelectionContext()
                };

                console.log('🔥 Step3Audience - Calling processStep with:', stepData);

                const success = await this.$store.wizard.processStep(
                    3, // Step number
                    this.selectedAudience,
                    this.getSelectionContext()
                );

                console.log('🔥 Step3Audience - processStep result:', success);

                if (success) {
                    console.log('🔥 Step3Audience - Processing successful, proceeding to next step');
                    await this.proceedToNextStep();
                } else {
                    console.error('❌ Step3Audience - processStep failed');
                }
            } catch (error) {
                console.error('💥 Step3Audience - Error in processAudienceSelection:', error);
            } finally {
                this.isSubmitting = false;
                console.log('🔥 Step3Audience - processAudienceSelection finished');
            }
        },

        async proceedToNextStep() {
            console.log('➡️ Step3Audience - proceedToNextStep called');

            // Move to step 4 (writing style)
            this.$store.wizard.setCurrentStep(4);
            console.log('➡️ Step3Audience - Set current step to 4');

            // Load step 4 data
            await this.loadWritingStyleData();
        },

        async loadWritingStyleData() {
            console.log('🌐 Step3Audience - loadWritingStyleData called');

            try {
                const success = await this.$store.wizard.processStep(4, null);
                console.log('🌐 Step3Audience - loadWritingStyleData result:', success);
                // Step 4 data will be loaded in the wizard store
            } catch (error) {
                console.error('💥 Step3Audience - Error loading writing style data:', error);
            }
        },

        // Enhanced context methods
        getSelectionContext() {
            const context = {
                selected_genre: this.selectedGenre,
                selected_subgenre: this.selectedSubgenre,
                concept_summary: this.userConcept?.substring(0, 100),
                has_analysis: this.hasConceptAnalysis
            };

            console.log('📝 Step3Audience - getSelectionContext:', context);
            return JSON.stringify(context);
        },

        getAnalysisContext(audienceId) {
            if (!this.hasConceptAnalysis) {
                console.log('📝 Step3Audience - No analysis context for:', audienceId);
                return null;
            }

            // Extract relevant analysis information for this audience
            const context = {
                genre_compatibility: this.getGenreCompatibility(audienceId),
                concept_themes: this.extractThemesFromConcept(),
                tone_indicators: this.conceptAnalysis.tone_signals || []
            };

            console.log('📝 Step3Audience - Analysis context for', audienceId, ':', context);
            return context;
        },

        getGenreCompatibility(audienceId) {
            const compatibilityMap = {
                adult: {
                    high: ['literary_fiction', 'thriller', 'mystery', 'romance', 'science_fiction', 'fantasy'],
                    medium: ['young_adult', 'new_adult'],
                    low: ['middle_grade', 'children']
                },
                young_adult: {
                    high: ['young_adult', 'fantasy', 'romance', 'dystopian', 'contemporary'],
                    medium: ['science_fiction', 'mystery', 'thriller'],
                    low: ['literary_fiction', 'middle_grade']
                },
                new_adult: {
                    high: ['romance', 'contemporary', 'fantasy', 'new_adult'],
                    medium: ['young_adult', 'science_fiction'],
                    low: ['middle_grade', 'literary_fiction']
                },
                middle_grade: {
                    high: ['middle_grade', 'fantasy', 'adventure', 'mystery'],
                    medium: ['science_fiction'],
                    low: ['romance', 'thriller', 'adult']
                }
            };

            const compatibility = compatibilityMap[audienceId];
            if (!compatibility) return 'medium';

            const selectedGenre = this.selectedGenre?.toLowerCase();
            if (compatibility.high.includes(selectedGenre)) return 'high';
            if (compatibility.medium.includes(selectedGenre)) return 'medium';
            return 'low';
        },

        getMarketInsights(audienceId) {
            const insights = {
                adult: {
                    market_size: 'Large',
                    growth_trend: 'Stable',
                    key_platforms: ['Traditional publishers', 'Amazon KDP', 'Bookstores'],
                    avg_word_count: '80,000-120,000',
                    price_range: '$12-25'
                },
                young_adult: {
                    market_size: 'Very Large',
                    growth_trend: 'Growing',
                    key_platforms: ['Social media marketing', 'BookTok', 'YA publishers'],
                    avg_word_count: '50,000-80,000',
                    price_range: '$10-18'
                },
                new_adult: {
                    market_size: 'Medium',
                    growth_trend: 'Rapidly Growing',
                    key_platforms: ['Digital-first publishers', 'Romance platforms'],
                    avg_word_count: '60,000-90,000',
                    price_range: '$8-15'
                },
                middle_grade: {
                    market_size: 'Medium',
                    growth_trend: 'Stable',
                    key_platforms: ['School libraries', 'Educational markets'],
                    avg_word_count: '20,000-50,000',
                    price_range: '$8-15'
                }
            };

            const insight = insights[audienceId] || {};
            console.log('💡 Step3Audience - Market insights for', audienceId, ':', insight);
            return insight;
        },

        extractThemesFromConcept() {
            if (!this.userConcept) return [];

            const concept = this.userConcept.toLowerCase();
            const themes = [];

            // Simple theme detection based on keywords
            if (concept.includes('love') || concept.includes('romance')) themes.push('Romance');
            if (concept.includes('adventure') || concept.includes('journey')) themes.push('Adventure');
            if (concept.includes('mystery') || concept.includes('detective')) themes.push('Mystery');
            if (concept.includes('magic') || concept.includes('fantasy')) themes.push('Fantasy');
            if (concept.includes('future') || concept.includes('technology')) themes.push('Science Fiction');
            if (concept.includes('child') || concept.includes('young')) themes.push('Coming of Age');
            if (concept.includes('family') || concept.includes('relationship')) themes.push('Family');

            console.log('🎨 Step3Audience - Extracted themes:', themes);
            return themes;
        },

        // UI Methods (with logging)
        getOptionClasses(optionId) {
            const baseClasses = "border rounded-lg p-4 cursor-pointer transition-all duration-200 hover:shadow-md";
            const selectedClasses = "border-blue-500 bg-blue-50 ring-2 ring-blue-200";
            const compatibleClasses = "border-green-400 bg-green-50";
            const defaultClasses = "border-gray-200 hover:border-gray-300";

            const option = this.getOptionById(optionId);
            const isSelected = this.selectedAudience === optionId;
            const compatibility = this.getGenreCompatibility(optionId);

            console.log('🎨 Step3Audience - getOptionClasses for', optionId, '- selected:', isSelected, 'compatibility:', compatibility);

            if (isSelected) {
                return `${baseClasses} ${selectedClasses}`;
            }

            if (compatibility === 'high') {
                return `${baseClasses} ${compatibleClasses}`;
            }

            return `${baseClasses} ${defaultClasses}`;
        },

        getMarketSizeBadgeClasses(marketSize) {
            const baseClasses = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium";

            switch (marketSize?.toLowerCase()) {
                case 'very large':
                    return `${baseClasses} bg-green-100 text-green-800`;
                case 'large':
                    return `${baseClasses} bg-blue-100 text-blue-800`;
                case 'medium':
                    return `${baseClasses} bg-yellow-100 text-yellow-800`;
                case 'small':
                    return `${baseClasses} bg-gray-100 text-gray-800`;
                default:
                    return `${baseClasses} bg-gray-100 text-gray-600`;
            }
        },

        getCompatibilityBadge(audienceId) {
            const compatibility = this.getGenreCompatibility(audienceId);

            const badges = {
                high: { text: 'Perfect Match', classes: 'bg-green-100 text-green-800' },
                medium: { text: 'Good Match', classes: 'bg-yellow-100 text-yellow-800' },
                low: { text: 'Consider Carefully', classes: 'bg-red-100 text-red-800' }
            };

            const badge = badges[compatibility] || badges.medium;
            console.log('🏷️ Step3Audience - getCompatibilityBadge for', audienceId, ':', badge);
            return badge;
        },

        onOptionHover(optionId) {
            console.log('🖱️ Step3Audience - onOptionHover:', optionId);
            this.hoveredOption = optionId;
        },

        onOptionLeave() {
            console.log('🖱️ Step3Audience - onOptionLeave');
            this.hoveredOption = null;
        },

        toggleAnalysisDetails() {
            console.log('🔍 Step3Audience - toggleAnalysisDetails');
            this.showAnalysisDetails = !this.showAnalysisDetails;
        },

        // Data loading (with enhanced logging)
        loadStepData() {
            console.log('📥 Step3Audience - loadStepData called');

            const stepData = this.currentStepData;
            console.log('📥 Step3Audience - Retrieved currentStepData:', stepData);

            // Load options from step data
            this.options = stepData.options || [];
            console.log('📥 Step3Audience - Set this.options:', this.options);

            // Set LLM message with context
            this.llmMessage = stepData.llmReasoning || this.getDefaultMessage();
            console.log('📥 Step3Audience - Set llmMessage:', this.llmMessage);

            // Load any existing selection
            this.selectedAudience = this.$store.wizard.formData.audience || '';
            console.log('📥 Step3Audience - Loaded selectedAudience:', this.selectedAudience);
            console.log('📥 Step3Audience - loadStepData completed');
        },

        getDefaultMessage() {
            const selectedGenre = this.selectedGenre;
            const message = `For ${selectedGenre || 'your chosen genre'}, these audiences offer the best commercial potential:`;
            console.log('💬 Step3Audience - getDefaultMessage:', message);
            return message;
        },

        // Lifecycle (with comprehensive logging) - FIXED to prevent premature API calls
        init() {
            console.log('🏁 Step3Audience - INIT STARTING');
            console.log('🏁 Step3Audience - Component initialization...');

            // Log wizard store state
            console.log('🏪 Step3Audience - Wizard Store State:');
            console.log('🏪 Step3Audience - currentStep:', this.$store.wizard.currentStep);
            console.log('🏪 Step3Audience - sessionId:', this.$store.wizard.sessionId);

            // IMPORTANT: Never make API calls during init()
            // Components are initialized for ALL steps when page loads
            console.log('⚠️ Step3Audience - Init should never make API calls');

            // Only load existing data from store
            this.selectedAudience = this.$store.wizard.formData.audience || '';
            console.log('📥 Step3Audience - Loaded existing selection:', this.selectedAudience);

            // Set up fallback data immediately (no API calls)
            this.options = this.getSampleAudiences();
            this.llmMessage = this.getDefaultMessage();
            console.log('📋 Step3Audience - Set fallback data');

            // Set up a watcher to load data when we actually reach Step 3
            this.$watch('$store.wizard.currentStep', (newStep, oldStep) => {
                console.log('👀 Step3Audience - Step changed from', oldStep, 'to', newStep);
                if (newStep === 3 && oldStep !== 3) {
                    console.log('🎯 Step3Audience - Now entering Step 3, loading data...');
                    this.onEnterStep3();
                }
            });

            console.log('🏁 Step3Audience - INIT COMPLETED (no API calls)');
        },

        // New method called only when actually entering Step 3
        async onEnterStep3() {
            console.log('🚀 Step3Audience - onEnterStep3 called');

            // Check if we have a valid session
            if (!this.$store.wizard.sessionId) {
                console.log('❌ Step3Audience - No session ID, keeping fallback data');
                return;
            }

            // Check concept analysis availability
            console.log('🔍 Step3Audience - Checking concept analysis...');
            console.log('🔍 Step3Audience - Has concept analysis:', this.hasConceptAnalysis);

            // Load current step data from wizard store
            console.log('📥 Step3Audience - Loading step data from store...');
            this.loadStepData();

            // Check if we have step data from previous navigation
            if (this.currentStepData?.options && this.currentStepData.options.length > 0) {
                console.log('✅ Step3Audience - Found existing step data, using it');
                this.options = this.currentStepData.options;
                this.llmMessage = this.currentStepData.llmReasoning || this.getDefaultMessage();
                return;
            }

            // Only make API call if we don't have options
            console.log('🌐 Step3Audience - No step data found, loading from API...');
            await this.loadAudienceOptions();
        },

        async loadAudienceOptions() {
            console.log('🌐 Step3Audience - loadAudienceOptions called');

            // Final safety checks
            if (this.$store.wizard.currentStep !== 3) {
                console.log('❌ Step3Audience - Not on Step 3, aborting API call');
                return;
            }

            if (!this.$store.wizard.sessionId) {
                console.log('❌ Step3Audience - No session ID, aborting API call');
                return;
            }

            // Load options based on current selections
            try {
                console.log('🌐 Step3Audience - Making API call to load options...');
                const success = await this.$store.wizard.processStep(3, null);
                console.log('🌐 Step3Audience - API call result:', success);

                if (success) {
                    console.log('🌐 Step3Audience - Reloading step data after successful API call');
                    this.loadStepData();
                } else {
                    console.log('⚠️ Step3Audience - API call returned false, keeping fallback data');
                }
            } catch (error) {
                console.error('💥 Step3Audience - Error loading audience options:', error);
                console.log('⚠️ Step3Audience - Keeping fallback sample data due to error');
                // Keep existing fallback data, don't overwrite
            }
        },

        // Utility methods (with logging)
        getOptionById(optionId) {
            const option = this.enhancedOptions.find(option => option.id === optionId);
            console.log('🔍 Step3Audience - getOptionById called with:', optionId);
            console.log('🔍 Step3Audience - Found option:', option);
            return option;
        },

        getSelectedAudienceInfo() {
            const info = this.getOptionById(this.selectedAudience);
            console.log('ℹ️ Step3Audience - getSelectedAudienceInfo:', info);
            return info;
        },

        formatRecommendationScore(score) {
            const formatted = !score ? null : `${Math.round(score)}% Match`;
            console.log('📊 Step3Audience - formatRecommendationScore:', score, '->', formatted);
            return formatted;
        },

        // Sample audiences for testing/fallback
        getSampleAudiences() {
            console.log('📋 Step3Audience - getSampleAudiences called (fallback data)');
            const selectedGenre = this.selectedGenre;

            // Base audiences that work for most genres
            const baseAudiences = [
                {
                    id: 'adult',
                    name: 'Adult (18+)',
                    description: 'Mature readers seeking sophisticated narratives and complex themes',
                    market_size: 'Large',
                    age_range: '18-65+',
                    characteristics: ['Complex themes', 'Mature content', 'Sophisticated language'],
                    recommendation_score: 85,
                    source: 'fallback'
                },
                {
                    id: 'young_adult',
                    name: 'Young Adult (13-18)',
                    description: 'Teen readers navigating coming-of-age experiences and identity',
                    market_size: 'Large',
                    age_range: '13-18',
                    characteristics: ['Coming-of-age', 'Identity themes', 'Accessible language'],
                    recommendation_score: 78,
                    source: 'fallback'
                },
                {
                    id: 'new_adult',
                    name: 'New Adult (18-25)',
                    description: 'Young adults transitioning to independence with relatable struggles',
                    market_size: 'Medium',
                    age_range: '18-25',
                    characteristics: ['Independence themes', 'College/career', 'Modern issues'],
                    recommendation_score: 72,
                    source: 'fallback'
                }
            ];

            // Add middle grade for certain genres
            if (['fantasy', 'adventure', 'mystery', 'coming_of_age'].includes(selectedGenre)) {
                baseAudiences.push({
                    id: 'middle_grade',
                    name: 'Middle Grade (8-12)',
                    description: 'Young readers discovering chapter books and adventure stories',
                    market_size: 'Medium',
                    age_range: '8-12',
                    characteristics: ['Age-appropriate content', 'Adventure focus', 'Clear moral lessons'],
                    recommendation_score: 88, // High for bunny story
                    source: 'fallback'
                });
            }

            console.log('📋 Step3Audience - Returning sample audiences:', baseAudiences);
            return baseAudiences;
        },

        // Navigation
        goBack() {
            console.log('⬅️ Step3Audience - goBack called');
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

            const insight = insights[audienceId] || {};
            console.log('💡 Step3Audience - getAudienceInsights for', audienceId, ':', insight);
            return insight;
        },

        showAudienceDetails(audienceId) {
            console.log('📖 Step3Audience - showAudienceDetails called for:', audienceId);

            const audience = this.getOptionById(audienceId);
            const insights = this.getAudienceInsights(audienceId);

            if (audience) {
                // You could implement a modal or expanded view here
                console.log('📖 Step3Audience - Audience details:', { audience, insights });
            }
        },

        // Debug helpers (enhanced)
        logAnalysisData() {
            console.log('🔧 Step3Audience - DEBUG ANALYSIS DATA:');
            console.log('🔧 Concept Analysis:', this.conceptAnalysis);
            console.log('🔧 Current Step Data:', this.currentStepData);
            console.log('🔧 Enhanced Options:', this.enhancedOptions);
            console.log('🔧 Selected Genre:', this.selectedGenre);
            console.log('🔧 Selected Subgenre:', this.selectedSubgenre);
            console.log('🔧 Wizard Store Full State:', this.$store.wizard);
        },

        logWizardState() {
            console.log('🔧 Step3Audience - FULL WIZARD STATE:');
            console.log('🔧 Current Step:', this.$store.wizard.currentStep);
            console.log('🔧 Session ID:', this.$store.wizard.sessionId);
            console.log('🔧 Form Data:', this.$store.wizard.formData);
            console.log('🔧 Concept Analysis:', this.$store.wizard.conceptAnalysis);
            console.log('🔧 Current Step Data:', this.$store.wizard.currentStepData);
            console.log('🔧 Is Loading:', this.$store.wizard.isLoading);
            console.log('🔧 Error:', this.$store.wizard.error);
        }
    };
}