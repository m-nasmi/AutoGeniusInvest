AutoGenius Invest: AI-Based Investment Portfolio Optimizer

- Introduction to the System:
AutoGenius Invest is a multi-agent AI-based financial decision-making assistant designed to help users make smart investment decisions. It leverages OpenAI’s GPT-4 through AutoGen framework, real-time stock data from Yahoo Finance, and custom-trained models to provide stock insights, investment advice, and market trends — all accessible through an intuitive mobile chat interface.

-----------------------------------------
- User Requirements:
▪ Stable Internet Connection  
▪ Smartphone 

-----------------------------------------
- Backend Requirements:
▪ Node.js  
▪ MongoDB  
▪ Flask (Python)  
▪ AutoGen (Multi-agent AI Framework)  
▪ yFinance, Pandas  
▪ dotenv, Flask-CORS, Axios

-----------------------------------------
- Software Requirements:
▪ Operating System: Windows/macOS/Linux  
▪ Programming Languages: JavaScript (Node.js), Python 3.x  
▪ Libraries/Frameworks:  
  - Flask  
  - Express.js  
  - OpenAI (GPT-4 via API)  
  - AutoGen  
  - yFinance  
  - Pandas  
  - Axios  
  - JWT for Authentication

-----------------------------------------
- System Installation:

PART 1 – Node.js Backend Setup
▪ Install Node.js and MongoDB  
▪ Navigate to the `/backend` directory  
▪ Run `npm install`  
▪ Set environment variables for DB and JWT_SECRET in `.env`  
▪ Run the backend server using `node index.js`

PART 2 – Flask (AutoGen AI) Setup
▪ Create a Python virtual environment  
▪ Install requirements:
  - `pip install flask flask-cors python-dotenv openai autogen pandas yfinance matplotlib duckduckgo_search`  
▪ Set `OPENAI_API_KEY_MAIN` in `.env`  
▪ Place `stock_data.csv` in the same directory  
▪ Run `python app.py`

PART 3 – Mobile App Setup (React Native)
▪ Install Expo CLI  
▪ Navigate to `/frontend`  
▪ Run `npm install`  
▪ Start the app using `npm start` or `expo start`
▪ or Can use Android Studio.

-----------------------------------------
- Features:

▪ Real-time Chat-Based Investment Assistant  
▪ GPT-4 powered multi-agent AI with stock-specific logic  
▪ Stock trend and performance analysis
▪ Investment Suggestion with accurate ratings.
▪ Authentication (JWT)  
▪ Profile view and account management  
▪ AutoGen Agent integrated for accurate reasoning  
▪ React Native mobile app frontend

-----------------------------------------
- API Endpoints (Backend):
POST `/api/auth/signup` – Register user  
POST `/api/auth/login` – Login & get token  
GET `/api/user/profile` – Get user profile  
DELETE `/api/user/delete` – Delete user account  
POST `/chat` – AutoGen AI Query (Flask endpoint)

-----------------------------------------
- Usage Instructions:

▪ Signup using the credentials to app and log in to receive JWT token  
▪ Access chat assistant to ask stock-related questions like:  
  “Should I invest in Apple?”  
  “What is the closing price of Tesla?”  
  “Give me a stock rates of Microsoft.”    
▪ Sign out or delete account anytime

-----------------------------------------
- Future Improvements:
▪ Integrate DeepSeek AI agent for multi-model financial processing  
▪ Extend support for more international stock exchanges and currencies  
▪ Add advanced investment chart visualizations and dashboards  
▪ Support multilingual input and accessibility features

-----------------------------------------
Developed by: Sirajudeen Muhammed Nasmi
Supervisor: Dr. Y.D. Jayaweera  
SLIIT – BSc (Hons) in Computer Science – Final Year UnderGraduate Project
