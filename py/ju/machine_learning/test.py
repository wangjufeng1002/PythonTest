from transformers import pipeline

classifier = pipeline("sentiment-analysis")
result = classifier("I love you, 不想吃饭")
print(result)