# ⚽ Football Career Assistant

An AI-powered chatbot that provides personalized career guidance for aspiring professional footballers and coaches. Built with Streamlit and powered by Google's Gemini AI.

## 🌟 Features

- **Dual Career Paths**: Guidance for both players and coaches
- **Position-Specific Advice**: Tailored recommendations for different playing positions
- **Coaching Philosophy Analysis**: Support for various coaching styles and approaches
- **Historical References**: Learn from legendary players and coaches
- **Interactive Chat Interface**: Natural conversation flow with AI mentor
- **Career Development Roadmaps**: Step-by-step progression guidance
- **Real-time Responses**: Instant AI-powered career advice

## 🎯 What the Assistant Offers

### For Players:
- Position analysis (GK, CB, FB, CM, CAM, Winger, Striker, etc.)
- Training recommendations and skill development
- Career progression from amateur to professional
- References to legendary players in similar positions
- Physical and mental preparation guidance

### for Coaches:
- Coaching philosophy development (attacking, possession-based, counter-attacking, etc.)
- Management style analysis
- Tactical knowledge building
- Youth development strategies
- References to successful coaches and their methods

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Streamlit
- Google Gemini API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/odubajo/football-career-llm.git
   
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit requests
   ```

3. **Add your API Key**
   - Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Replace `YOUR_GEMINI_API_KEY_HERE` in the code with your actual API key

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the chatbot**
   - Open your browser to `http://localhost:8501`
   - Start chatting about your football career!

## 🌐 Deployment

### Streamlit Cloud (Recommended)
1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Add your API key as a secret in Streamlit Cloud settings
5. Deploy and get your public URL

### Other Deployment Options
- **Heroku**: Deploy as a web application
- **Railway**: Quick deployment with automatic HTTPS
- **Render**: Free tier available for small projects
- **Google Cloud Run**: Serverless deployment option

## 💬 How to Use

1. **Start the conversation**: The assistant will greet you and ask about your career aspirations
2. **Choose your path**: Tell the assistant if you want to be a player or coach
3. **Specify your focus**: 
   - Players: Share your preferred position
   - Coaches: Describe your coaching philosophy
4. **Get personalized advice**: Receive detailed guidance with historical examples
5. **Continue the conversation**: Ask follow-up questions about training, career steps, or specific challenges

## 🎮 Example Conversations

### For Players:
```
User: "I want to become a professional striker"
Assistant: Provides guidance on striker development, references players like Haaland, Kane, or Benzema, and offers specific training recommendations.
```

### For Coaches:
```
User: "I'm interested in possession-based coaching"
Assistant: Discusses tactical approaches, references coaches like Pep Guardiola or Xavi, and provides development pathways.
```


## 📋 Project Structure

```
football-career-assistant/
│
├── app.py                 # Main application file
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
└── .gitignore           # Git ignore file
```


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

⚽ **Start your football career journey today!** Whether you dream of scoring goals or developing the next generation of talent, this AI assistant is here to guide you every step of the way.
