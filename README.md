# Medical Data Chatbot with W&B 📚🤖💬

This project implements a chatbot that can answer questions based on the content of a provided PDF document. The chatbot uses LangChain, Google Generative AI, FAISS for natural language processing and vector-based similarity search, and Weights and Biases for logging and tracking.

## Google Colab

You can also run this project directly in Google Colab. Click the link below to open the Colab notebook:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1fxGYD8SbcK7eSNRtDP2GSz84XdWiYhuq?usp=sharing)

## Features

- Extracts text from PDF files
- Splits text into manageable chunks
- Creates and saves a vector store for text chunks
- Answers questions based on the context provided in the PDF
- Logs metadata and results with Weights and Biases

## Requirements

- Python 3.10 or later
- Google Generative AI API Key
- Weights and Biases API Key

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/sidrasaleem296/medical-data-chatbot.git
    cd medical-data-chatbot
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

    The `requirements.txt` file should include the following packages:
    ```text
    faiss-gpu
    PyPDF2
    langchain
    google-generativeai
    python-dotenv
    langchain-community
    langchain_google_genai
    wandb
    ```

## Environment Variables

You need to set up environment variables to configure the Google Generative AI API and Weights and Biases. Create a `.env` file in the root directory of your project with the following content:

Replace `your_google_api_key` and `your_wandb_api_key` with your actual API keys. You can obtain the API keys by following these steps:

### Google Generative AI API Key
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing project.
3. Enable the Google Generative AI API for your project.
4. Go to the Credentials page and create a new API key.
5. Copy the API key and add it to your `.env` file.

### Weights and Biases API Key
1. Go to the [Weights and Biases website](https://wandb.ai/).
2. Sign up for an account or log in if you already have one.
3. Go to your profile and find the API key.
4. Copy the API key and add it to your `.env` file.

## How to Run

1. Ensure you have your PDF file ready and placed in the correct directory.

2. Run the `app.py` file:
    ```bash
    python app.py
    ```

## Usage

The main function in `app.py` extracts text from the provided PDF, creates vector stores, and processes the input question to return the relevant answer based on the context in the PDF.

Here is an example of how to use the application:

1. Place your PDF file in the project directory, for example: `/content/L1- Introduction To Orthopedics.pdf`.

2. Modify the `pdf_path` and `question` variables in the `main()` function within `app.py` as needed:
    ```python
    pdf_path = "/content/L1- Introduction To Orthopedics.pdf"  # Change this to your actual PDF file path
    question = "What are the diseases discussed and their treatment?"
    main(question, pdf_path)
    ```

3. Execute the script:
    ```bash
    python app.py
    ```

4. The script will output the answer to the question based on the content of the provided PDF and log the details to Weights and Biases.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under a Proprietary License. All rights are reserved. For more information, please refer to the [LICENSE](./LICENSE) file.



