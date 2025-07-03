from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

class BERTSimilarity:
    def __init__(self, model_name='sentence-transformers/all-MiniLM-L6-v2'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()
        self.device = torch.device('cpu')
        self.model.to(self.device)

    def get_embedding(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Use the mean of the last hidden states as the sentence embedding
        return torch.mean(outputs.last_hidden_state, dim=1).squeeze().cpu().numpy()

    def calculate_similarity(self, text1, text2):
        emb1 = self.get_embedding(text1)
        emb2 = self.get_embedding(text2)
        return float(cosine_similarity([emb1], [emb2])[0][0])

if __name__ == '__main__':
    bert_sim = BERTSimilarity()

    text1 = "The quick brown fox jumps over the lazy dog."
    text2 = "A fast brown fox leaps over a sleepy canine."
    text3 = "The cat sat on the mat."

    similarity12 = bert_sim.calculate_similarity(text1, text2)
    similarity13 = bert_sim.calculate_similarity(text1, text3)

    print(f"Similarity between '{text1}' and '{text2}': {similarity12:.4f}")
    print(f"Similarity between '{text1}' and '{text3}': {similarity13:.4f}")


