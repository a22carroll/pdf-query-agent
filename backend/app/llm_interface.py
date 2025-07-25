from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

def generate_answer(question, context_chunks):
    context = "\n\n".join(context_chunks)
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    outputs = generator(prompt, max_length=512, do_sample=True, temperature=0.7)
    return outputs[0]['generated_text']
