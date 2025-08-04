# Create the Supabase database schema
supabase_schema = """-- Career Journaling Platform Database Schema
-- Supabase PostgreSQL Schema for User Management and Journal Settings
-- Version: 1.0
-- Created: 2024

-- Enable Row Level Security
ALTER DATABASE postgres SET "app.jwt_secret" TO 'your-super-secret-jwt-token-with-at-least-32-characters-long';

-- Create custom types
CREATE TYPE auth_provider_type AS ENUM ('email', 'google', 'linkedin');
CREATE TYPE career_goal_type AS ENUM ('promotion', 'skill-development', 'leadership', 'career-change', 'work-life-balance', 'salary-increase', 'other');
CREATE TYPE reminder_day_type AS ENUM ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday');

-- Users table (extends Supabase auth.users)
CREATE TABLE public.users (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    first_name TEXT NOT NULL CHECK (length(first_name) >= 2 AND length(first_name) <= 50),
    email TEXT NOT NULL UNIQUE CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'),
    auth_provider auth_provider_type NOT NULL DEFAULT 'email',
    utm_source TEXT DEFAULT 'direct',
    onboarding_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Journal settings table
CREATE TABLE public.journal_settings (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    send_reminder BOOLEAN DEFAULT TRUE,
    reminder_day reminder_day_type DEFAULT 'friday',
    reminder_time TIME DEFAULT '16:00:00', -- 4 PM default
    career_goal career_goal_type,
    job_title TEXT CHECK (length(job_title) <= 100),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Ensure one settings record per user
    UNIQUE(user_id)
);

-- Journal entries table (for future analytics)
CREATE TABLE public.journal_entries (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    week_start_date DATE NOT NULL,
    week_end_date DATE NOT NULL,
    
    -- Weekly goals and focus
    weekly_goals JSONB,
    primary_skill_focus TEXT,
    relationship_focus TEXT,
    
    -- Daily entries (stored as JSONB for flexibility)
    daily_entries JSONB DEFAULT '{}',
    
    -- Weekly reflection
    accomplishments JSONB,
    insights_learned JSONB,
    challenges_faced JSONB,
    skills_applied JSONB,
    
    -- Performance metrics
    productivity_score INTEGER CHECK (productivity_score >= 1 AND productivity_score <= 10),
    learning_score INTEGER CHECK (learning_score >= 1 AND learning_score <= 10),
    collaboration_score INTEGER CHECK (collaboration_score >= 1 AND collaboration_score <= 10),
    goal_progress_score INTEGER CHECK (goal_progress_score >= 1 AND goal_progress_score <= 10),
    satisfaction_score INTEGER CHECK (satisfaction_score >= 1 AND satisfaction_score <= 10),
    
    -- Metadata
    completion_status TEXT DEFAULT 'draft' CHECK (completion_status IN ('draft', 'completed')),
    completion_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Ensure one entry per user per week
    UNIQUE(user_id, week_start_date)
);

-- User analytics summary (for future ML/AI insights)
CREATE TABLE public.user_analytics (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE NOT NULL,
    
    -- Computed metrics
    total_entries INTEGER DEFAULT 0,
    consistency_score DECIMAL(3,2), -- 0.00 to 1.00
    average_productivity DECIMAL(3,2),
    average_satisfaction DECIMAL(3,2),
    growth_trend JSONB, -- Store trend data as JSON
    
    -- Key insights
    top_skills JSONB,
    collaboration_patterns JSONB,
    achievement_patterns JSONB,
    
    -- Computed at
    last_computed_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(user_id)
);

-- Create indexes for performance
CREATE INDEX idx_users_email ON public.users(email);
CREATE INDEX idx_users_created_at on public.users(created_at);
CREATE INDEX idx_journal_entries_user_id ON public.journal_entries(user_id);
CREATE INDEX idx_journal_entries_week_start ON public.journal_entries(week_start_date);
CREATE INDEX idx_journal_entries_completion ON public.journal_entries(completion_status);
CREATE INDEX idx_user_analytics_user_id ON public.user_analytics(user_id);

-- Enable Row Level Security (RLS)
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.journal_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.journal_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_analytics ENABLE ROW LEVEL SECURITY;

-- RLS Policies

-- Users can only see and update their own profile
CREATE POLICY "Users can view own profile" ON public.users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.users
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" ON public.users
    FOR INSERT WITH CHECK (auth.uid() = id);

-- Journal settings policies
CREATE POLICY "Users can manage own journal settings" ON public.journal_settings
    FOR ALL USING (auth.uid() = user_id);

-- Journal entries policies
CREATE POLICY "Users can manage own journal entries" ON public.journal_entries
    FOR ALL USING (auth.uid() = user_id);

-- User analytics policies (read-only for users)
CREATE POLICY "Users can view own analytics" ON public.user_analytics
    FOR SELECT USING (auth.uid() = user_id);

-- Functions for automatic timestamp updates
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for updated_at
CREATE TRIGGER users_updated_at BEFORE UPDATE ON public.users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER journal_settings_updated_at BEFORE UPDATE ON public.journal_settings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER journal_entries_updated_at BEFORE UPDATE ON public.journal_entries
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER user_analytics_updated_at BEFORE UPDATE ON public.user_analytics
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Function to create user profile after signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.users (id, email, first_name, auth_provider)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'first_name', split_part(NEW.email, '@', 1)),
        COALESCE(NEW.raw_user_meta_data->>'provider', 'email')
    );
    
    -- Create default journal settings
    INSERT INTO public.journal_settings (user_id)
    VALUES (NEW.id);
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger for new user creation
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Function to calculate user analytics (runs periodically)
CREATE OR REPLACE FUNCTION public.update_user_analytics(target_user_id UUID)
RETURNS VOID AS $$
DECLARE
    entry_count INTEGER;
    avg_productivity DECIMAL;
    avg_satisfaction DECIMAL;
    consistency DECIMAL;
BEGIN
    -- Calculate metrics from journal entries
    SELECT 
        COUNT(*),
        AVG(productivity_score),
        AVG(satisfaction_score)
    INTO entry_count, avg_productivity, avg_satisfaction
    FROM public.journal_entries 
    WHERE user_id = target_user_id AND completion_status = 'completed';
    
    -- Calculate consistency (entries per week over time)
    SELECT 
        CASE 
            WHEN EXTRACT(WEEK FROM MAX(created_at)) - EXTRACT(WEEK FROM MIN(created_at)) + 1 > 0
            THEN entry_count::DECIMAL / (EXTRACT(WEEK FROM MAX(created_at)) - EXTRACT(WEEK FROM MIN(created_at)) + 1)
            ELSE 0
        END
    INTO consistency
    FROM public.journal_entries 
    WHERE user_id = target_user_id AND completion_status = 'completed';
    
    -- Upsert analytics record
    INSERT INTO public.user_analytics (
        user_id, 
        total_entries, 
        consistency_score, 
        average_productivity, 
        average_satisfaction,
        last_computed_at
    )
    VALUES (
        target_user_id,
        entry_count,
        LEAST(consistency, 1.0), -- Cap at 1.0
        avg_productivity,
        avg_satisfaction,
        NOW()
    )
    ON CONFLICT (user_id) 
    DO UPDATE SET
        total_entries = EXCLUDED.total_entries,
        consistency_score = EXCLUDED.consistency_score,
        average_productivity = EXCLUDED.average_productivity,
        average_satisfaction = EXCLUDED.average_satisfaction,
        last_computed_at = EXCLUDED.last_computed_at,
        updated_at = NOW();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create sample data for testing (remove in production)
-- This is helpful for development and testing

-- Sample user (will be created via Supabase Auth in real usage)
-- INSERT INTO auth.users (id, email, encrypted_password, email_confirmed_at, created_at, updated_at)
-- VALUES (
--     gen_random_uuid(),
--     'demo@example.com',
--     crypt('password123', gen_salt('bf')),
--     NOW(),
--     NOW(),
--     NOW()
-- );

COMMENT ON TABLE public.users IS 'User profiles extending Supabase auth.users';
COMMENT ON TABLE public.journal_settings IS 'User preferences for journaling reminders and settings';
COMMENT ON TABLE public.journal_entries IS 'Weekly journal entries with structured reflection data';
COMMENT ON TABLE public.user_analytics IS 'Computed analytics and insights for users';

COMMENT ON COLUMN public.journal_entries.daily_entries IS 'JSONB structure: {"monday": {"energy": 5, "win": "...", "learning": "..."}, ...}';
COMMENT ON COLUMN public.journal_entries.accomplishments IS 'JSONB array of weekly accomplishments';
COMMENT ON COLUMN public.journal_entries.skills_applied IS 'JSONB array of skills used during the week';
COMMENT ON COLUMN public.user_analytics.growth_trend IS 'JSONB with trend data for ML/AI processing';"""

# Save the SQL schema file
with open('supabase_schema.sql', 'w', encoding='utf-8') as f:
    f.write(supabase_schema)

print("✅ supabase_schema.sql created successfully!")
print(f"📄 File size: {len(supabase_schema)} characters")
print("\n🗄️ DATABASE FEATURES:")
print("• Future-proof schema for analytics and ML")
print("• Row Level Security (RLS) for data protection")
print("• JSONB fields for flexible data storage")
print("• Automatic timestamp management")
print("• Comprehensive indexing for performance")
print("• Built-in data validation and constraints")
print("• Analytics-ready structure for insights generation")
print("• Supabase Auth integration")