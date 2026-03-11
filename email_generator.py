# email_generator.py
# This file contains ONE job: take LinkedIn profile → return cold email
# Think of it as the "chef" — you give ingredients, it cooks the email

from groq import Groq          # import our phone to call AI
import os                       # to read environment variables
from dotenv import load_dotenv  # to load our .env file

# Load the .env file so Python can read GROQ_API_KEY
load_dotenv()

# Create our Groq client (this is like turning on the phone)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_cold_email(
    linkedin_profile: str,   # the raw text pasted from LinkedIn
    sender_name: str,        # person sending the email e.g. "Neel"
    sender_product: str,     # what they're selling e.g. "AI chatbot for businesses"
    tone: str = "professional"  # "professional", "casual", "friendly"
) -> dict:
    """
    This function takes LinkedIn profile info and returns a cold email.
    
    INPUT:  LinkedIn profile text + sender details
    OUTPUT: A dictionary with subject line and email body
    """

    # THE PROMPT — this is where the magic happens
    # We are telling the AI exactly what to do, step by step
    prompt = f"""
    You are an expert cold email copywriter. Your emails get 40%+ reply rates.
    
    TASK: Write a personalized cold email based on the LinkedIn profile below.
    
    === LINKEDIN PROFILE ===
    {linkedin_profile}
    === END OF PROFILE ===
    
    === SENDER DETAILS ===
    Sender Name: {sender_name}
    What They're Offering: {sender_product}
    Tone: {tone}
    === END OF SENDER DETAILS ===
    
    RULES FOR THE EMAIL:
    1. Subject line must be specific to THIS person — not generic
    2. First line must mention something SPECIFIC from their profile (job, achievement, company)
    3. Connect their background to why your product/service is relevant to THEM
    4. Keep it SHORT — max 5 sentences in body. People don't read long cold emails.
    5. End with ONE clear call to action (e.g., "15-minute call this week?")
    6. Do NOT use clichés like "I hope this email finds you well"
    7. Sound like a human, not a robot
    8. Tone should be: {tone}
    
    OUTPUT FORMAT (return exactly this, nothing else):
    SUBJECT: [your subject line here]
    
    BODY:
    [your email body here]
    """

    # Call the Groq API
    # Think of this like sending a WhatsApp message to the AI and waiting for reply
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",   # Llama 3 70B — best free model available
        messages=[
            {
                "role": "user",      # we are the "user" talking to AI
                "content": prompt    # our message to the AI
            }
        ],
        max_tokens=500,    # max length of reply (500 tokens ≈ 375 words)
        temperature=0.8,   # creativity level: 0=robotic, 1=very creative, 0.8=balanced
    )

    # Extract the text from the response
    # response.choices[0].message.content → this is where AI's reply lives
    full_response = response.choices[0].message.content

    # Now split subject and body from the AI's response
    # AI will return text like:
    # SUBJECT: Hey John...
    # BODY: Hi John, I noticed...
    
    subject = ""
    body = ""

    if "SUBJECT:" in full_response and "BODY:" in full_response:
        # Split by BODY: to separate subject and body
        parts = full_response.split("BODY:")
        
        # Get subject line (remove "SUBJECT: " prefix)
        subject_part = parts[0].replace("SUBJECT:", "").strip()
        subject = subject_part
        
        # Get body (everything after BODY:)
        body = parts[1].strip()
    else:
        # If AI didn't follow format exactly, just return full response as body
        body = full_response
        subject = "Following up on a quick idea for you"

    return {
        "subject": subject,
        "body": body,
        "tone_used": tone
    }


# =============================================
# TEST THE FUNCTION RIGHT NOW
# Run: python email_generator.py
# =============================================
if __name__ == "__main__":
    
    # Fake LinkedIn profile for testing
    test_profile = """
    John Smith
    Founder & CEO at QuickSell India
    Mumbai, Maharashtra
    
    Building India's fastest B2B sales platform for SMEs.
    Previously: Sales Head at Razorpay (3 years), grew revenue 4x.
    Passionate about helping small businesses scale with technology.
    500+ connections | 12 posts | Actively posting about sales & startups
    """
    
    # Generate email
    result = generate_cold_email(
        linkedin_profile=test_profile,
        sender_name="Neel Deshmane",
        sender_product="AI-powered cold email tool that personalizes outreach at scale",
        tone="professional"
    )
    
    print("=" * 50)
    print("SUBJECT:", result["subject"])
    print("=" * 50)
    print("BODY:")
    print(result["body"])
    print("=" * 50)