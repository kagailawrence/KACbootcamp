import google.generativeai as genai

# Your API key here
API_KEY = "AIzaSyBIyXXXXXXXXXXXXXXX"  # Replace with your actual API key

def setup_gemini():
    # Configure the Gemini API with the provided key
    genai.configure(api_key=API_KEY)
    return genai.GenerativeModel('gemini-2.5-flash')

def generate_joke(model, topic=None):
    prompt = "Tell me a funny joke"
    if topic:
        prompt += f" about {topic}"
    prompt += ". Make it family-friendly and keep it short."
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating joke: {str(e)}"

def main():
    model = setup_gemini()
    
    print("🎭 Welcome to the Gemini Joke Generator! 🎭")
    print("(Press Ctrl+C to exit)")
    
    while True:
        try:
            topic = input("\nEnter a topic for the joke (or press Enter for a random joke): ").strip()
            print("\nGenerating joke... 🤔")
            joke = generate_joke(model, topic if topic else None)
            print("\n" + joke)
            print("\n" + "="*50)
        except KeyboardInterrupt:
            print("\n\nThanks for using the Joke Generator! Goodbye! 👋")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()
