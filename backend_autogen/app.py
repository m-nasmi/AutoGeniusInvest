import os
import autogen
import pandas as pd
from dotenv import load_dotenv
import yfinance as yf
from flask import Flask, request, jsonify
from flask_cors import CORS
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from duckduckgo_search import DDGS
import matplotlib.pyplot as plt
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY_MAIN")
if not api_key:
    raise ValueError("ERROR: OPENAI_API_KEY environment variable is not set.")

# Initialize Flask app
app = Flask(__name__)
CORS(app)

print("✅ API Key Loaded!")

# Load CSV file
csv_path = "stock_data.csv"
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"❌ CSV file not found at path: {csv_path}")

df = pd.read_csv(csv_path)
df["Date"] = pd.to_datetime(df["Date"], utc=True)  # Fixing FutureWarning

print("✅ CSV Loaded Successfully!")

# AutoGen AI Configuration
config_list = [{"model": "gpt-4", "api_key": api_key}]
llm_config = {"seed": 42, "config_list": config_list, "temperature": 0}

def fetch_stock_data(stock_symbol, period="5d", interval="1d"):
    """
    Fetch historical closing prices for a given stock symbol from Yahoo Finance.
    """
    try:
        stock = yf.Ticker(stock_symbol)
        hist = stock.history(period=period, interval=interval)

        if hist.empty:
            return f"No data found for {stock_symbol}."

        closing_prices = hist["Close"].tolist()
        dates = hist.index.strftime("%Y-%m-%d").tolist()

        result = "\n".join([f"- {date}: ${price:.2f}" for date, price in zip(dates, closing_prices)])
        return f"Here are the closing prices for {stock_symbol} in the last {period}:\n{result}"
    
    except Exception as e:
        return f"Error fetching data: {str(e)}"

def plot_stock_data(stock_symbol, period="auto"):
    """Fetch stock data and plot the closing prices."""
    stock_data = fetch_stock_data(stock_symbol, period)  # Fetch stock prices
    if stock_data is None or stock_data.empty:
        return "No data available to plot."

    # Convert Date column to datetime (if not already done)
    stock_data["Date"] = pd.to_datetime(stock_data["Date"])

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(stock_data["Date"], stock_data["Close"], label=f"{stock_symbol} Closing Prices")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.title(f"{stock_symbol} Stock Price Trend")
    plt.legend()
    plt.grid()
    plt.show()

# Initialize Assistant
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    system_message="""
    You are a stock data and investment assistant. Your job is to answer stock-related questions using data and provide general investment advice.

    **Behavior Rules:**
    1️⃣ **Stock Data Requests:** 
       - If the user asks about stock prices, closing rates, or trends, check the provided CSV.
       - If missing, extract the stock symbol & time period, then call `fetch_stock_data(stock_symbol, period="auto")` to get real-time data.

    2️⃣ **Investment Advice Requests:**  
   - If the user asks "Should I invest in X?" or "Can I invest in X?"  
   - **First, fetch the latest stock data for X (if not available in CSV).**  
     - Example: `fetch_stock_data("X", period="5d")`  
   - Then, provide investment advice **with stock price trends**.  

   - **Response Format:**  
     - Fetch the last 5 days of stock data for the requested company.  
     - Display the stock data in a tabular format.  
     - Explain the meaning of each column:  
       - **Open:** Price at the start of the trading day.  
       - **High:** The highest price of the stock on that trading day.  
       - **Low:** The lowest price of the stock on that trading day.  
       - **Close:** The final price of the stock at the end of the trading day.  
       - **Volume:** Number of shares traded during the day.  
       - **Dividends & Stock Splits:** If applicable.  
     - Provide an overall trend summary based on the data.  
     - Conclude with a disclaimer advising users to do thorough research or consult a financial expert before investing. 

       **Example Response:**  
       ```
       Here is the latest Tesla (TSLA) stock data from the past 5 days:

       | Date       | Open    | High    | Low     | Close   | Volume  |
       |-----------|--------|--------|--------|--------|---------|
       | 2025-03-17 | 245.06  | 245.40  | 242.10  | 243.50  | 10M     |
       | 2025-03-18 | 228.16  | 230.10  | 225.50  | 229.00  | 12M     |
       | 2025-03-19 | 231.61  | 241.41  | 230.20  | 238.00  | 15M     |
       | 2025-03-20 | 233.35  | 238.00  | 231.50  | 236.50  | 11M     |
       | 2025-03-21 | 234.99  | 249.52  | 233.00  | 248.00  | 14M     |

       **Stock Data Explanation:**
       - **Open:** The stock price at the beginning of the trading day.
       - **High:** The highest price of the stock during the day.
       - **Low:** The lowest price of the stock during the day.
       - **Close:** The final stock price when the market closed.
       - **Volume:** The number of shares traded that day.

       Based on the last 5 days, Tesla's stock shows an **upward trend** with increasing closing prices.  
       However, investing in stocks involves risks. Always conduct thorough research or consult a financial advisor before making investment decisions.
       ```

    3️⃣ **Stock Data Visualization:**
       - If the user requests a **graph** of stock prices, call `plot_stock_data(stock_symbol, period="auto")`.
       - Example: "Can you show me the price trend of Apple?" → Call `plot_stock_data("AAPL", period="auto")`
       - Example: "Show me Puma's stock graph" → Call `plot_stock_data("PMMAF", period="auto")`

    **Examples:**
    - "What is Puma’s closing price for the last 5 days?" ✅ Fetch stock data.
    - "Should I invest in Puma?" ✅ Fetch stock data **first**, then provide investment guidance.
    - "Can you plot Apple's stock prices?" ✅ Fetch data & generate graph.

    Always provide clear and structured responses.
    """,
    function_map={
        "fetch_stock_data": fetch_stock_data,
        "plot_stock_data": plot_stock_data  # 🔹 Added function to generate stock price graphs
    }
)

print("✅ AI Assistant Initialized!")

# UserProxyAgent Configuration (with Docker disabled)
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=6,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"use_docker": False},  # Disable Docker for code execution
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction. 
    Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

@app.route("/", methods=["GET"])
def home():
    return "Flask server is running!", 200

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Message is required."}), 400

        # Extract the relevant stock data or any other information from the CSV
        stock_data = df.head()  # For example, the first few rows of the stock data

        # Convert the stock data into a string that the assistant can process
        stock_data_str = stock_data.to_string()

        # Create a message to send to the assistant, including the stock data
        task_message = f"Here is some stock data:\n{stock_data_str}\n\n{user_message}"

        # Reset chat history for each new request
        user_proxy.chat_messages[assistant] = []

        # Initiate chat with the assistant, including the CSV data
        user_proxy.initiate_chat(
            assistant,
            message=task_message
        )

        # Extract all messages from the chat history
        chat_history = user_proxy.chat_messages[assistant]

        # Format the messages for the frontend
        formatted_messages = []
        for msg in chat_history:
            if isinstance(msg, dict) and "role" in msg and "content" in msg:
                content = msg["content"]
                is_code = "```" in content  # Check if the message contains a code block
                formatted_messages.append({
                    "sender": msg["role"],
                    "content": content,
                    "isCode": is_code  # Explicitly mark code blocks
                })
            else:
                # Handle unexpected message format
                formatted_messages.append({
                    "sender": "system",
                    "content": str(msg),  # Convert unexpected messages to string
                    "isCode": False
                })

        return jsonify({"messages": formatted_messages})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🚀 Starting Flask Server...")
    app.run(host="0.0.0.0", port=5000, debug=True)

# Initial Task for Testing
task = """
Write the python code to display numbers 1 to 10
"""

user_proxy.initiate_chat(
    assistant,
    message=task
)





#OPENAI_API_KEY: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
#OPENAI_API_KEY_TWO=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
#OPENAI_API_KEY_MAIN=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

