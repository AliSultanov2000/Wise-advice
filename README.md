The goal of this project is to create ML model (Based on RNN) which will determine the tone of the text: positive or negative (thus the ML problem is a binary classification). The main scope of the project: chatbots
Project stages: 
- Problem statement, its translation into machine learning language  
- Choosing metrics  
- Text data parsing  
- Exploratory data analysis (EDA)  
- Text data preprocessing  
- Creating an RNN (exactly LSTM) model  
- Creating an ML Pipeline  
- Embedding the model in a Docker container (for further use in the application)  

The stack of technologies used: Python, Docker, Jupyter Notebook(Google Colab), Keras,  NumPy, Pandas  

Model limitations: The model can only process words in English  
Metrics: Precision (due to the objectivity)

There are various types of text representation in the form of a vector or matrix, for example:  
- Bag of words (N - grams). The text is represented as a vector   
- Numerical encoding of words. The text is represented as a vector  
- One-hot encoding. The text is represented as a vector  
- Dense vector representation of words. The text is represented as a matrix  

Within the framework of this project, a dense vector representation of words is used. To do this, we set the maximum number of words that will be represented as a vector, and also set the maximum number of words in one text. The numerical values in the vector to represent the word are set up during the training of a recurrent neural network and are trainable parameters

ML Pipeline: 
- Using our own tokenizer, we translate the text into tokens  
- Using the tokenizer dictionary, we match a number to each token. We get the sequence  
- Changing the size of the sequence (in our case it is 200 elements). If the numbers in the sequence are less than 200, then 0 are added to the beginning of the sequence. If the numbers in the sequence are more than 200, then the sequence is trimmed to the desired size  
- Passing the sequence model LSTM. As a result, we get an answer for this text  
