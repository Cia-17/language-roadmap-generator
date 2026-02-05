import streamlit as st
import openai
import os
from datetime import datetime

# ==============================
# SECURE API KEY MANAGEMENT
# ==============================
def initialize_openai():
    """
    Safely initialize OpenAI API key from multiple sources
    Priority: Streamlit Secrets > Environment Variable > Demo Mode
    """
    api_key = None
    
    # Try to get key from Streamlit Secrets
    try:
        if "OPENAI_API_KEY" in st.secrets:
            api_key = st.secrets["OPENAI_API_KEY"]
    except:
        pass
    
    # Try environment variable
    if not api_key:
        api_key = os.environ.get("OPENAI_API_KEY")
    
    # Set the API key if we have it
    if api_key and api_key.startswith("sk-"):
        openai.api_key = api_key
        return True  # AI mode enabled
    else:
        # Demo mode - no valid key
        return False  # Demo mode

# ==============================
# DEMO MODE FUNCTIONS
# ==============================
def generate_demo_roadmap(language, level, goal, weeks, hours_per_week):
    """Generate a demo roadmap when API key is not available"""
    return f"""
# 🌍 {language} Learning Roadmap ({weeks} weeks)

## 🎯 Your Learning Profile
- **Current Level**: {level}
- **Primary Goal**: {goal}
- **Time Commitment**: {weeks} weeks × {hours_per_week} hours/week = {weeks*hours_per_week} total hours
- **Target**: {goal.lower()} proficiency in {language}

## 📋 Overview
This personalized roadmap structures free resources to maximize your learning efficiency. 
Each week builds upon the previous, with practical exercises to reinforce skills.

## 📅 Weekly Breakdown

### Week 1: Foundation & Basics
**Learning Objectives:**
1. Master basic greetings and introductions
2. Learn the {language} alphabet and pronunciation rules
3. Build a 50-word vocabulary foundation
4. Practice simple sentence structures

**Free Resources:**
- 📺 **YouTube**: Search "Learn {language} for absolute beginners"
- 🌐 **Websites**: Duolingo ({language} course) - Complete Units 1-3
- 📱 **Apps**: HelloTalk (language exchange)

**Practice Exercises:**
1. Record yourself introducing yourself in {language}
2. Label 10 items in your home with {language} words

**Weekend Project:** Create a 1-minute self-introduction video

---

### Week 2: Daily Conversations
**Learning Objectives:**
1. Learn common phrases for shopping, dining, and directions
2. Practice present tense conjugations
3. Build vocabulary to 150 words

**Free Resources:**
- 📺 **YouTube**: "{language} daily conversations" playlists
- 🌐 **Websites**: BBC Languages ({language} section)

**Weekend Project:** Have a 5-minute conversation with a language partner

---

### Weeks 3-{weeks}: Progressive Mastery
*(Add OpenAI API key to Streamlit Secrets for complete AI-generated roadmap)*

## 🔑 Enable AI Generation
For personalized AI recommendations with specific YouTube links and websites:

1. **Get API Key**: Visit platform.openai.com
2. **Add to Streamlit Cloud**: Deploy this app and add your key to Secrets
3. **Regenerate**: Click the generate button

---
*This demo shows the structure. Add API key for AI-powered personalized roadmap.*
"""

# ==============================
# MAIN APP
# ==============================
def main():
    # Page configuration
    st.set_page_config(
        page_title="Language Learning Roadmap Generator",
        page_icon="🗺️",
        layout="wide"
    )
    
    # Initialize OpenAI (returns True if AI mode, False if demo)
    ai_enabled = initialize_openai()
    
    # App header
    st.title("🗺️ Language Learning Roadmap Generator")
    st.markdown("### Get a personalized learning path with free resources!")
    
    # API Key status indicator
    with st.sidebar:
        st.header("🔧 Configuration")
        if ai_enabled:
            st.success("✅ AI Mode Active")
            st.info("Using secure API key from Streamlit Secrets")
        else:
            st.warning("🔒 Demo Mode")
            st.markdown("""
            **To enable AI:**
            1. Get OpenAI key
            2. Add to Streamlit Secrets
            3. Redeploy app
            """)
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("📝 Your Preferences")
        
        language = st.selectbox(
            "Language to Learn:",
            ["Spanish", "French", "German", "Japanese", "Chinese", 
             "Korean", "Italian", "Portuguese", "Arabic", "Russian",
             "Other"]
        )
        
        if language == "Other":
            language = st.text_input("Enter language:")
        
        level = st.select_slider(
            "Your Level:",
            options=["Beginner", "Basic", "Intermediate"]
        )
        
        goal = st.selectbox(
            "Goal:",
            ["Travel", "Business", "Academic", "Casual"]
        )
        
        weeks = st.slider("Weeks:", 4, 24, 8)
        
        hours_per_week = st.slider("Hours/Week:", 1, 10, 3)
        
        generate_button = st.button("🚀 Generate Roadmap", type="primary")
    
    # Main content area
    if generate_button and language:
        if ai_enabled:
            # AI MODE - Real OpenAI API call
            with st.spinner("🤖 AI is generating your roadmap..."):
                try:
                    prompt = f"Create a {weeks}-week roadmap for learning {language} for {goal}. Level: {level}. Hours/week: {hours_per_week}. Include specific free YouTube channels, websites, and practice exercises. Format clearly with weekly breakdowns."
                    
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Create structured language learning roadmaps with free resources."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=1500
                    )
                    
                    roadmap = response.choices[0].message.content
                    st.success("✅ AI Roadmap Generated!")
                    
                except Exception as e:
                    st.error(f"API Error. Using demo mode.")
                    roadmap = generate_demo_roadmap(language, level, goal, weeks, hours_per_week)
        else:
            # DEMO MODE
            roadmap = generate_demo_roadmap(language, level, goal, weeks, hours_per_week)
            st.info("Showing demo. Add API key for AI generation.")
        
        # Display roadmap
        st.markdown(roadmap)
        
        # Download option
        st.download_button(
            label="📥 Download",
            data=roadmap,
            file_name=f"{language}_roadmap.md",
            mime="text/markdown"
        )
    
    elif generate_button and not language:
        st.warning("Please select a language.")
    
    else:
        # Default view
        st.markdown("""
        ## Welcome! 🌍
        
        This tool creates **personalized language learning roadmaps**.
        
        ### How it works:
        1. Select your language and level
        2. Choose your goal and timeline
        3. Click "Generate Roadmap"
        4. Follow the weekly plan
        
        ### Features:
        ✅ Weekly structured plans  
        ✅ Free YouTube resources  
        ✅ Recommended websites  
        ✅ Practice exercises  
        ✅ Time management guidance  
        
        *Add OpenAI API key for AI-powered personalization*
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("Built for Buildathon | Secure API Management")

# Run the app
if __name__ == "__main__":
    main()