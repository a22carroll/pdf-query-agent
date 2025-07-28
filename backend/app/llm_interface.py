from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

#Preconditions: Takes in user question and Context Chunks
#Post: returns Generated Anwser
def generate_answer(question, context_chunks):
    context = "\n\n".join(context_chunks)
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    
    #Output parameters
    outputs = generator(
        prompt,
        max_length=512,
        temperature=0.8,
        top_p=0.95,
        repetition_penalty=1.2,
        do_sample=True,
        num_return_sequences=1,
        pad_token_id=50256  # prevent warning from GPT-2 lacking a pad token
    )

    # Only return the part of the output that comes after "Answer:"
    generated_text = outputs[0]['generated_text']
    answer = generated_text.split("Answer:")[-1].strip()
    return answer