from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)

# Dictionary to hold Selenium instances for each user
user_sessions = {}

def create_selenium_driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run headless
    driver = webdriver.Chrome(service=service, options=options)
    return driver

@app.route('/start-scraping', methods=['POST'])
def start_scraping():
    user_id = request.json.get('user_id')
    if user_id in user_sessions:
        return jsonify({'error': 'User already has a session running'}), 400
    
    # Create a new Selenium instance for the user
    driver = create_selenium_driver()
    user_sessions[user_id] = driver

    # Start scraping in a separate thread
    def scrape_logic():
        try:
            # Perform scraping tasks (simplified for example)
            driver.get("https://example.com/login")
            # Perform login actions
            time.sleep(5)  # Simulate some work
            driver.get("https://example.com/dashboard")
            # Extract data
            # driver.find_element(By.CSS_SELECTOR, 'some_selector')
            print(f"Scraping done for user {user_id}")
        finally:
            # Clean up once scraping is done
            user_sessions.pop(user_id, None)
            driver.quit()

    # Run the scraping logic in a background thread
    threading.Thread(target=scrape_logic).start()

    return jsonify({'message': 'Scraping started for user {}'.format(user_id)}), 200

@app.route('/get-scraping-status', methods=['GET'])
def get_status():
    user_id = request.args.get('user_id')
    if user_id not in user_sessions:
        return jsonify({'error': 'No active session for this user'}), 404

    return jsonify({'status': 'Scraping in progress', 'user_id': user_id}), 200

if __name__ == '__main__':
    app.run(debug=True)
