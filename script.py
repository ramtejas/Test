# Create the index.html file for the career journaling signup form
index_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Start Your Career Journey - Weekly Career Journaling</title>
    <meta name="description" content="Transform your career with weekly journaling. Track your professional growth, document achievements, and make data-driven career decisions.">
    <link rel="stylesheet" href="styles.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <!-- Header Section -->
        <header class="header">
            <div class="header-content">
                <h1 class="header-title">Weekly Career Journaling</h1>
                <p class="header-subtitle">Transform your career with data-driven insights</p>
            </div>
        </header>

        <!-- Main Form Section -->
        <main class="main-content">
            <div class="form-container" id="signupForm">
                <div class="form-header">
                    <h2>Start Your Career Journey</h2>
                    <p>Create your account in under 60 seconds</p>
                </div>

                <form id="authForm" class="auth-form" novalidate>
                    <!-- Error Display -->
                    <div id="errorMessage" class="error-message" role="alert" style="display: none;"></div>
                    
                    <!-- Success Message -->
                    <div id="successMessage" class="success-message" role="alert" style="display: none;"></div>

                    <!-- Name Field -->
                    <div class="form-group">
                        <label for="firstName" class="form-label">First Name</label>
                        <input 
                            type="text" 
                            id="firstName" 
                            name="firstName" 
                            class="form-input" 
                            required 
                            autocomplete="given-name"
                            aria-describedby="firstName-error"
                        >
                        <div id="firstName-error" class="field-error" role="alert"></div>
                    </div>

                    <!-- Email Field -->
                    <div class="form-group">
                        <label for="email" class="form-label">Work Email</label>
                        <input 
                            type="email" 
                            id="email" 
                            name="email" 
                            class="form-input" 
                            required 
                            autocomplete="email"
                            aria-describedby="email-error"
                        >
                        <div id="email-error" class="field-error" role="alert"></div>
                    </div>

                    <!-- Password Field -->
                    <div class="form-group">
                        <label for="password" class="form-label">Password</label>
                        <div class="password-container">
                            <input 
                                type="password" 
                                id="password" 
                                name="password" 
                                class="form-input" 
                                required 
                                autocomplete="new-password"
                                aria-describedby="password-error password-help"
                                minlength="6"
                            >
                            <button type="button" class="password-toggle" id="passwordToggle" aria-label="Show password">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                                    <circle cx="12" cy="12" r="3"></circle>
                                </svg>
                            </button>
                        </div>
                        <div id="password-help" class="form-help">At least 6 characters</div>
                        <div id="password-error" class="field-error" role="alert"></div>
                    </div>

                    <!-- Reminder Toggle -->
                    <div class="form-group">
                        <label class="checkbox-container">
                            <input type="checkbox" id="sendReminder" name="sendReminder" checked>
                            <span class="checkmark"></span>
                            <span class="checkbox-text">Send Monday reminder to fill my weekly journal</span>
                        </label>
                    </div>

                    <!-- Hidden UTM Source -->
                    <input type="hidden" id="utmSource" name="utmSource" value="">

                    <!-- Submit Button -->
                    <button type="submit" class="submit-btn" id="submitBtn">
                        <span class="btn-text">Create Account</span>
                        <span class="btn-loading" style="display: none;">Creating...</span>
                    </button>
                </form>

                <!-- Social Login Divider -->
                <div class="divider">
                    <span>or</span>
                </div>

                <!-- Social Login Buttons -->
                <div class="social-buttons">
                    <button type="button" class="social-btn google-btn" id="googleSignup">
                        <svg width="20" height="20" viewBox="0 0 24 24">
                            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                        </svg>
                        Continue with Google
                    </button>
                    <button type="button" class="social-btn linkedin-btn" id="linkedinSignup">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="#0077B5">
                            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                        </svg>
                        Continue with LinkedIn
                    </button>
                </div>
            </div>

            <!-- Progressive Onboarding Form (Hidden Initially) -->
            <div class="form-container" id="profileForm" style="display: none;">
                <div class="form-header">
                    <h2>Tell Us About Yourself</h2>
                    <p>Help us personalize your experience</p>
                </div>

                <form id="profileSetupForm" class="auth-form">
                    <div class="form-group">
                        <label for="jobTitle" class="form-label">Current Job Title</label>
                        <input 
                            type="text" 
                            id="jobTitle" 
                            name="jobTitle" 
                            class="form-input" 
                            placeholder="e.g., Marketing Manager, Data Analyst"
                            autocomplete="organization-title"
                        >
                    </div>

                    <div class="form-group">
                        <label for="careerGoal" class="form-label">Primary Career Goal</label>
                        <select id="careerGoal" name="careerGoal" class="form-input">
                            <option value="">Select your primary goal</option>
                            <option value="promotion">Get promoted</option>
                            <option value="skill-development">Develop new skills</option>
                            <option value="leadership">Build leadership skills</option>
                            <option value="career-change">Change career direction</option>
                            <option value="work-life-balance">Improve work-life balance</option>
                            <option value="salary-increase">Increase salary</option>
                            <option value="other">Other</option>
                        </select>
                    </div>

                    <button type="submit" class="submit-btn">
                        <span class="btn-text">Complete Setup</span>
                        <span class="btn-loading" style="display: none;">Saving...</span>
                    </button>

                    <button type="button" class="skip-btn" id="skipProfile">Skip for now</button>
                </form>
            </div>

            <!-- Success State -->
            <div class="success-container" id="successContainer" style="display: none;">
                <div class="success-content">
                    <div class="success-icon">
                        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2">
                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                            <polyline points="22,4 12,14.01 9,11.01"></polyline>
                        </svg>
                    </div>
                    <h2>Welcome to Your Career Journey!</h2>
                    <p>Your account has been created successfully. Start documenting your professional growth today.</p>
                    
                    <div class="success-actions">
                        <a href="#" class="primary-btn" id="addCalendarReminder">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                                <line x1="16" y1="2" x2="16" y2="6"></line>
                                <line x1="8" y1="2" x2="8" y2="6"></line>
                                <line x1="3" y1="10" x2="21" y2="10"></line>
                            </svg>
                            Add Weekly Reminder to Calendar
                        </a>
                        <a href="#" class="secondary-btn" id="startJournaling">Start My First Entry</a>
                    </div>
                </div>
            </div>
        </main>

        <!-- Footer -->
        <footer class="footer">
            <p>&copy; 2024 Weekly Career Journaling. Transform your career with data-driven insights.</p>
        </footer>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

# Save the HTML file
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print("✅ index.html created successfully!")
print(f"📄 File size: {len(index_html)} characters")