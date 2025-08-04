// Weekly Career Journaling - Signup Form JavaScript
class SignupFlow {
    constructor() {
        this.currentStep = 1;
        this.userData = {};
        this.init();
    }

    init() {
        this.bindEvents();
        this.setupValidation();
        this.trackUTMParameters();
        this.showCurrentStep();
    }

    bindEvents() {
        // Form submissions
        const signupForm = document.getElementById('signup-form');
        const profileForm = document.getElementById('profile-form');
        
        if (signupForm) {
            signupForm.addEventListener('submit', (e) => this.handleSignup(e));
        }
        
        if (profileForm) {
            profileForm.addEventListener('submit', (e) => this.handleProfile(e));
        }
        
        // Social login buttons
        const googleBtn = document.getElementById('google-btn');
        const linkedinBtn = document.getElementById('linkedin-btn');
        
        if (googleBtn) {
            googleBtn.addEventListener('click', () => this.handleSocialLogin('google'));
        }
        
        if (linkedinBtn) {
            linkedinBtn.addEventListener('click', () => this.handleSocialLogin('linkedin'));
        }
        
        // Profile step buttons
        const skipBtn = document.getElementById('skip-profile-btn');
        if (skipBtn) {
            skipBtn.addEventListener('click', () => this.skipProfile());
        }
        
        // Success step buttons
        const calendarBtn = document.getElementById('add-calendar-btn');
        const journalingBtn = document.getElementById('start-journaling-btn');
        
        if (calendarBtn) {
            calendarBtn.addEventListener('click', () => this.addCalendarReminder());
        }
        
        if (journalingBtn) {
            journalingBtn.addEventListener('click', () => this.startJournaling());
        }
        
        // Password toggle
        const passwordToggle = document.getElementById('password-toggle-btn');
        if (passwordToggle) {
            passwordToggle.addEventListener('click', (e) => this.togglePassword(e));
        }
        
        // Real-time validation
        this.setupRealtimeValidation();
    }

    showCurrentStep() {
        // Hide all steps
        const steps = document.querySelectorAll('.step');
        steps.forEach((step, index) => {
            step.classList.remove('active');
        });
        
        // Show current step
        const currentStepElement = document.getElementById(`step-${this.currentStep}`);
        if (currentStepElement) {
            currentStepElement.classList.add('active');
        }
        
        // Update progress bar
        this.updateProgress();
    }

    setupRealtimeValidation() {
        const form = document.getElementById('signup-form');
        if (!form) return;
        
        const inputs = form.querySelectorAll('input[required]');
        
        inputs.forEach(input => {
            // Validate on blur for better UX
            input.addEventListener('blur', () => this.validateField(input));
            
            // For email, also validate on input for immediate feedback
            if (input.type === 'email') {
                let timeout;
                input.addEventListener('input', () => {
                    clearTimeout(timeout);
                    timeout = setTimeout(() => this.validateField(input), 500);
                });
            }
            
            // For password, validate on input
            if (input.type === 'password') {
                input.addEventListener('input', () => this.validateField(input));
            }
        });
    }

    validateField(field) {
        const fieldName = field.name;
        const value = field.value.trim();
        const errorElement = document.getElementById(`${fieldName}-error`);
        
        let isValid = true;
        let errorMessage = '';
        
        // Required field validation
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = `${this.getFieldLabel(fieldName)} is required`;
        }
        
        // Email validation
        else if (fieldName === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                errorMessage = 'Please enter a valid email address';
            }
        }
        
        // Password validation
        else if (fieldName === 'password' && value) {
            if (value.length < 6) {
                isValid = false;
                errorMessage = 'Password must be at least 6 characters';
            }
        }
        
        // First name validation
        else if (fieldName === 'firstName' && value) {
            if (value.length < 2) {
                isValid = false;
                errorMessage = 'First name must be at least 2 characters';
            }
        }

        // Update UI
        this.updateFieldValidation(field, errorElement, isValid, errorMessage);
        
        return isValid;
    }

    updateFieldValidation(field, errorElement, isValid, errorMessage) {
        field.classList.remove('error', 'success');
        
        if (errorMessage) {
            field.classList.add('error');
            if (errorElement) {
                errorElement.textContent = errorMessage;
                errorElement.setAttribute('aria-live', 'polite');
            }
        } else if (field.value.trim()) {
            field.classList.add('success');
            if (errorElement) {
                errorElement.textContent = '';
            }
        } else {
            if (errorElement) {
                errorElement.textContent = '';
            }
        }
    }

    getFieldLabel(fieldName) {
        const labels = {
            firstName: 'First name',
            email: 'Email',
            password: 'Password'
        };
        return labels[fieldName] || fieldName;
    }

    validateForm(formElement) {
        const inputs = formElement.querySelectorAll('input[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!this.validateField(input)) {
                isValid = false;
            }
        });
        
        return isValid;
    }

    async handleSignup(e) {
        e.preventDefault();
        
        const form = e.target;
        const formData = new FormData(form);
        
        // Validate form
        if (!this.validateForm(form)) {
            this.focusFirstError(form);
            return;
        }
        
        // Show loading state
        this.setButtonLoading('create-account-btn', true);
        
        try {
            // Collect form data
            this.userData = {
                firstName: formData.get('firstName').trim(),
                email: formData.get('email').trim().toLowerCase(),
                password: formData.get('password'),
                sendReminder: formData.has('sendReminder'),
                utmSource: window.utmData?.utm_source || 'direct',
                utmMedium: window.utmData?.utm_medium,
                utmCampaign: window.utmData?.utm_campaign,
                utmContent: window.utmData?.utm_content,
                utmTerm: window.utmData?.utm_term,
                signupMethod: 'email',
                createdAt: new Date().toISOString()
            };
            
            // Simulate API call
            await this.createAccount(this.userData);
            
            // Success - move to next step
            this.nextStep();
            
        } catch (error) {
            console.error('Signup error:', error);
            this.showError('An error occurred during signup. Please try again.');
        } finally {
            this.setButtonLoading('create-account-btn', false);
        }
    }

    async handleSocialLogin(provider) {
        try {
            this.setButtonLoading(`${provider}-btn`, true);
            
            // Track social login attempt
            this.trackEvent('social_login_attempt', { provider });
            
            // In a real app, this would integrate with OAuth
            console.log(`Social login with ${provider}`);
            
            // Simulate social login success
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            this.userData = {
                firstName: 'John', // Would come from social provider
                email: 'john@example.com', // Would come from social provider
                sendReminder: true,
                utmSource: window.utmData?.utm_source || 'direct',
                signupMethod: provider,
                createdAt: new Date().toISOString()
            };
            
            this.trackEvent('social_login_success', { provider });
            this.nextStep();
            
        } catch (error) {
            console.error(`${provider} login error:`, error);
            this.showError(`${provider} login failed. Please try again.`);
        } finally {
            this.setButtonLoading(`${provider}-btn`, false);
        }
    }

    async handleProfile(e) {
        e.preventDefault();
        
        const form = e.target;
        const formData = new FormData(form);
        
        this.setButtonLoading('save-profile-btn', true);
        
        try {
            // Add profile data to user data
            this.userData.jobTitle = formData.get('jobTitle')?.trim() || null;
            this.userData.careerGoal = formData.get('careerGoal') || null;
            
            // Simulate API call to update profile
            await this.updateProfile(this.userData);
            
            this.trackEvent('profile_completed');
            this.nextStep();
            
        } catch (error) {
            console.error('Profile update error:', error);
            this.showError('Failed to save profile. Please try again.');
        } finally {
            this.setButtonLoading('save-profile-btn', false);
        }
    }

    skipProfile() {
        this.trackEvent('profile_skipped');
        this.nextStep();
    }

    nextStep() {
        // Hide current step
        const currentStepElement = document.getElementById(`step-${this.currentStep}`);
        if (currentStepElement) {
            currentStepElement.classList.remove('active');
        }
        
        // Update progress
        this.currentStep++;
        
        // Show next step
        this.showCurrentStep();
        
        // Focus management for accessibility
        const nextStepElement = document.getElementById(`step-${this.currentStep}`);
        if (nextStepElement) {
            const heading = nextStepElement.querySelector('h1');
            if (heading) {
                heading.focus();
            }
        }
    }

    updateProgress() {
        const steps = document.querySelectorAll('.progress-step');
        steps.forEach((step, index) => {
            if (index < this.currentStep) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });
    }

    togglePassword(e) {
        e.preventDefault();
        
        const passwordInput = document.getElementById('password');
        const toggleButton = e.target.closest('.password-toggle');
        const toggleText = toggleButton.querySelector('.password-toggle-text');
        
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            toggleText.textContent = 'Hide';
            toggleButton.setAttribute('aria-label', 'Hide password');
        } else {
            passwordInput.type = 'password';
            toggleText.textContent = 'Show';
            toggleButton.setAttribute('aria-label', 'Show password');
        }
    }

    setButtonLoading(buttonId, loading) {
        const button = document.getElementById(buttonId);
        if (!button) return;
        
        const textElement = button.querySelector('.btn-text');
        const loadingElement = button.querySelector('.btn-loading');
        
        if (loading) {
            button.disabled = true;
            button.classList.add('loading');
            if (textElement) textElement.style.opacity = '0';
            if (loadingElement) loadingElement.style.display = 'inline-block';
        } else {
            button.disabled = false;
            button.classList.remove('loading');
            if (textElement) textElement.style.opacity = '1';
            if (loadingElement) loadingElement.style.display = 'none';
        }
    }

    focusFirstError(form) {
        const firstError = form.querySelector('.form-control.error');
        if (firstError) {
            firstError.focus();
        }
    }

    showError(message) {
        // Create or update error notification
        let errorNotification = document.getElementById('error-notification');
        
        if (!errorNotification) {
            errorNotification = document.createElement('div');
            errorNotification.id = 'error-notification';
            errorNotification.className = 'error-notification';
            errorNotification.setAttribute('role', 'alert');
            errorNotification.setAttribute('aria-live', 'polite');
            document.body.appendChild(errorNotification);
        }
        
        errorNotification.textContent = message;
        errorNotification.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (errorNotification) {
                errorNotification.style.display = 'none';
            }
        }, 5000);
    }

    async addCalendarReminder() {
        try {
            this.trackEvent('calendar_reminder_clicked');
            
            // Create calendar event data
            const event = {
                title: 'Weekly Career Journal',
                description: 'Take 15 minutes to reflect on your career progress, wins, challenges, and learnings.',
                startTime: this.getNextFridayAt5PM(),
                duration: 15, // minutes
                recurrence: 'weekly'
            };
            
            // Generate calendar links
            const calendarUrl = this.generateCalendarUrl(event);
            
            // Open calendar application
            window.open(calendarUrl, '_blank');
            
            this.trackEvent('calendar_reminder_added');
            
        } catch (error) {
            console.error('Calendar error:', error);
            this.showError('Unable to add calendar reminder. Please add it manually.');
        }
    }

    generateCalendarUrl(event) {
        const startDate = new Date(event.startTime);
        const endDate = new Date(startDate.getTime() + event.duration * 60000);
        
        // Format dates for Google Calendar
        const formatDate = (date) => {
            return date.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
        };
        
        const params = new URLSearchParams({
            action: 'TEMPLATE',
            text: event.title,
            details: event.description,
            dates: `${formatDate(startDate)}/${formatDate(endDate)}`,
            recur: 'RRULE:FREQ=WEEKLY;BYDAY=FR'
        });
        
        return `https://calendar.google.com/calendar/render?${params.toString()}`;
    }

    getNextFridayAt5PM() {
        const now = new Date();
        const friday = new Date();
        
        // Find next Friday
        const daysUntilFriday = (5 - now.getDay() + 7) % 7 || 7;
        friday.setDate(now.getDate() + daysUntilFriday);
        
        // Set to 5 PM
        friday.setHours(17, 0, 0, 0);
        
        return friday;
    }

    startJournaling() {
        this.trackEvent('start_journaling_clicked');
        
        // In a real app, this would redirect to the journaling interface
        console.log('Redirecting to journaling interface...');
        
        // Show success message
        alert('Welcome to your journaling dashboard! (This would be a real redirect in production)');
    }

    // API simulation methods
    async createAccount(userData) {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        console.log('Account created:', userData);
        
        this.trackEvent('account_created', {
            method: userData.signupMethod,
            utm_source: userData.utmSource
        });
    }

    async updateProfile(userData) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        console.log('Profile updated:', {
            jobTitle: userData.jobTitle,
            careerGoal: userData.careerGoal
        });
    }

    setupValidation() {
        // Add custom validation styles and behavior
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.noValidate = true; // Disable browser validation to use custom
        });
    }

    trackUTMParameters() {
        // UTM parameters are already captured in the HTML script tag
        // Log for debugging
        if (window.utmData) {
            console.log('UTM Parameters:', window.utmData);
        }
    }

    trackEvent(eventName, properties = {}) {
        // Analytics tracking
        console.log('Event tracked:', eventName, properties);
    }
}

// Initialize the signup flow when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SignupFlow();
});

// Performance monitoring
window.addEventListener('load', () => {
    // Track page load time
    const loadTime = performance.now();
    console.log(`Page loaded in ${Math.round(loadTime)}ms`);
});

// Error boundary for unhandled errors
window.addEventListener('error', (event) => {
    console.error('Unhandled error:', event.error);
});

// Accessibility: Skip link functionality
document.addEventListener('keydown', (e) => {
    if (e.key === 'Tab' && !e.shiftKey) {
        // Ensure proper tab order and focus management
        const activeElement = document.activeElement;
        if (activeElement && activeElement.classList.contains('sr-only')) {
            e.preventDefault();
            const firstInput = document.querySelector('.step.active input:not([type="hidden"])');
            if (firstInput) {
                firstInput.focus();
            }
        }
    }
});