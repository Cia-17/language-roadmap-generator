
import streamlit as st
import openai
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Language Learning Roadmap Generator",
    page_icon="🗺️",
    layout="wide"
)

# Initialize OpenAI
openai.api_key = st.secrets["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"]

# App header
st.title("🗺️ AI Language Learning Roadmap Generator")
st.markdown("### Get a personalized learning path with free resources!")

# Sidebar for inputs
with st.sidebar:
    st.header("📝 Your Learning Preferences")
    
    language = st.selectbox(
        "Select Language to Learn:",
        ["Spanish", "French", "German", "Japanese", "Chinese", 
         "Korean", "Italian", "Portuguese", "Arabic", "Russian",
         "Other (specify below)"]
    )
    
    if language == "Other (specify below)":
        language = st.text_input("Enter language:")
    
    level = st.select_slider(
        "Your Current Level:",
        options=["Complete Beginner", "Basic Knowledge", "Intermediate", "Advanced Beginner"]
    )
    
    goal = st.selectbox(
        "Learning Goal:",
        ["Travel Conversations", "Business Communication", "Academic Study", "Casual Fluency"]
    )
    
    weeks = st.slider("Weeks to Complete:", 4, 52, 12)
    
    hours_per_week = st.slider("Hours per Week:", 1, 20, 5)
    
    generate_button = st.button("🚀 Generate My Roadmap", type="primary", use_container_width=True)

# Main content area
if generate_button and language:
    with st.spinner("🤖 AI is crafting your personalized learning roadmap..."):
        try:
            # Create the prompt for OpenAI
            prompt = f'''
            Create a comprehensive {weeks}-week learning roadmap for a {level} learner wanting to learn {language} for {goal}.
            
            Total available time: {hours_per_week} hours per week.
            
            Format the response as follows:
            
            ## {language} Learning Roadmap ({weeks} weeks)
            
            ### Weekly Structure:
            
            Then create {weeks} sections, each titled "Week X: [Topic]"
            
            For each week, include:
            1. **Learning Objectives**: 3-4 specific goals
            2. **YouTube Resources**: 2-3 specific YouTube channels or video series with links
            3. **Websites/Articles**: 2-3 free websites with specific page recommendations
            4. **Practice Exercises**: 2-3 practical activities
            5. **Time Allocation**: How to split the {hours_per_week} hours
            6. **Weekend Project**: A small project to apply learning
            
            End with:
            ### 📚 Additional Free Resources
            ### 🎯 Final Assessment
            ### ✅ Next Steps After {weeks} Weeks
            
            Make it practical, motivational, and focused on FREE resources only.
            '''
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert language learning coach who specializes in creating structured learning paths using free online resources."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            # Display the roadmap
            roadmap = response.choices[0].message.content
            
            st.success("✅ Your personalized roadmap is ready!")
            
            # Display roadmap
            st.markdown(roadmap)
            
            # Download option
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{language.lower().replace(' ', '_')}_roadmap_{timestamp}.md"
            
            st.download_button(
                label="📥 Download Roadmap",
                data=roadmap,
                file_name=filename,
                mime="text/markdown"
            )
            
        except Exception as e:
            st.error(f"Error generating roadmap: {str(e)}")
            st.info("Please check your OpenAI API key and try again.")

elif generate_button and not language:
    st.warning("⚠️ Please select or enter a language to learn.")

else:
    # Default view before generation
    st.markdown('''
    ## Welcome to Your AI Language Learning Assistant! 🌍
    
    This tool creates a personalized learning roadmap using **100% free resources** from:
    
    - 📺 **YouTube** videos and channels
    - 🌐 **Websites** and articles
    - 📱 **Mobile apps** with free tiers
    - 💬 **Practice communities**
    
    ### How it works:
    1. **Select your language** and current level
    2. **Choose your goal** (travel, business, etc.)
    3. **Set your timeline** (weeks and hours per week)
    4. **Click "Generate My Roadmap"**
    
    ### You'll receive:
    ✅ Weekly learning objectives  
    ✅ Curated YouTube resources with links  
    ✅ Recommended websites and articles  
    ✅ Practice exercises and projects  
    ✅ Time management guidance  
    
    *Powered by AI and curated free resources*
    ''')

# Footer
st.markdown("---")
st.markdown("Built with ❤️ for the Buildathon | Uses OpenAI GPT-3.5 | All resources are free")
