# Flask Stock Market Webapp, one so called mini tradingview!

A web application that provides stock price predictions using machine learning models through historical patterns using technical tools such as RSI, SMI etc. Built with Flask, Dockerized for easy deployment, and backed by a MySQL database.

---

## Project Description

This app fetches historical stock data, trains machine learning models to predict future prices, and serves these predictions via a Flask web interface. It allows users to view current prices, predicted trends, and percentage changes for various stocks. Also it allows user to purchase his/her own stocks and see his/her personalized portfolio grow. Furthermore, you can add as much cash as possible - meaning that this app could be used as a demo account for paper trading etc.

- **Technologies used:**  
  - Python (Flask) for backend and web server  
  - MySQL for persistent data storage  
  - Docker & Docker Compose for containerized deployment  
  - scikit-learn for ML model training and predictions 
  - HTML, CSS and JavaScript for Frontend 

- **Challenges:**  
  - Learning new technologies for me personally
    - API implementation
    - REST
    - Docker
    - New languages
    - APIs
    - Machine-learning
  - Display stock prices through a graph visually in different types:
    - Bar
    - Line
    - Candlesticks
    - OHLC
  - Handling model training and prediction efficiently in a containerized environment  
  - Managing persistent data volumes in Docker for database and models 
  - Adding technical tools 

- **Features:**  
  - User authentication
  - User registration and deletion
  - Portfolio management
  - Stockmarket demo
  - Real-time stock updates and notifications  
  - Enhanced visualizations and interactive charts
  - AI assistent powered through machinelearning using historical patterns

---

## Table of Contents

- [Installation](#installation)  
- [Usage](#Usage)  
- [License](#license)  

---

## Installation

### Prerequisites

- Docker and Docker Compose installed on your machine

### Steps

1. Clone the repository  
   ```bash
   git clone https://github.com/GITGUOD/web-application_Project_stockMarket
````

2. Navigate into the project folder

   ```bash
   cd web-application_Project_stockMarket
   ```
3. Build and start the Docker containers

   ```bash
   docker-compose build
   docker-compose up
   ```
4. Open your browser and go to [http://localhost:5000](http://localhost:5000)

The MySQL database data and ML models are persisted in Docker volumes, so your data and models won’t be lost when restarting containers.

---

## Usage

* Browse to the home page to see stock prices.
    - Possible to select different stocks
    - Possible to select different graphs
    - Possible to select different historical data
    - Possible to select different timeframes
    - Possible to select and use different types of technical tools for an advanced investor.
* Press portfolio button to check your portfolio
* Press prediction button to check future price targets
    - Here it is also possible to check price targets next month, next day etc.
* Models are trained automatically during Docker build, so predictions are available on startup.
* If you want to retrain models, run the training script manually or rebuild the Docker images.

---

## Credits

* Developed by: [Tonny Huynh](https://github.com/GITGUOD)
* Thanks to the open-source communities of Flask, Docker, MySQL, and scikit-learn, and AI tools such as Gemini and ChatGPT for providing resources for research purposes and learning
* Inspired by tutorials and resources from \[TradingView, Youtube, free css sites, w3schools etc]

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---