import os
import json
import requests
from groq import Groq
from services.LLM import get_chat_response
from services.vector_db import vector_store
from evaluation_data import TEST_DATASET

# Configuration
API_URL = "http://127.0.0.1:5000"
FILE_PATH = "test.pdf" # The file you want to test
USER_ID = "eval_user_001"
GROQ_API_KEY = os.getenv("GROQ_KEY")

client = Groq(api_key=GROQ_API_KEY)

def upload_and_index():
    """Uploads the PDF to the Flask backend to ensure it is indexed."""
    print(f"📂 Uploading {FILE_PATH} for indexing...")
    try:
        with open(FILE_PATH, 'rb') as f:
            files = {'file': f}
            data = {'user_id': USER_ID}
            response = requests.post(f"{API_URL}/upload", files=files, data=data)
            
        if response.status_code == 200:
            print(f"✅ Upload Successful: {response.json()['message']}")
            return True
        else:
            print(f"❌ Upload Failed: {response.json().get('error')}")
            return False
    except Exception as e:
        print(f"❌ Connection Error: Ensure your Flask app is running at {API_URL}")
        return False

def judge_response(question, retrieved_context, ai_answer, ground_truth):
    """Uses Llama-3.3-70b to audit the RAG output."""
    prompt = f"""
    You are an Industry-Standard AI Quality Auditor. Grade the AI_ANSWER based on the PROVIDED_CONTEXT and GROUND_TRUTH.

    EVALUATION CRITERIA:
    1. FAITHFULNESS (Hallucination Check): Is the AI_ANSWER derived ONLY from the context? If it makes up info, it's a Hallucination.
    2. RELEVANCE: Does it actually answer the question?
    3. ACCURACY: Matches the GROUND_TRUTH?

    QUESTION: {question}
    GROUND_TRUTH: {ground_truth}
    PROVIDED_CONTEXT: {retrieved_context}
    AI_ANSWER: {ai_answer}

    Return ONLY a JSON object:
    {{
      "rating": "Not Hallucinated" | "Hallucinated" | "Neutral",
      "score": 0-10,
      "reason": "explanation"
    }}
    """
    
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        response_format={"type": "json_object"}
    )
    return json.loads(chat_completion.choices[0].message.content)

def run_automated_suite():
    # 1. First, upload the file
    if not upload_and_index():
        return

    # 2. Run the evaluation
    results = []
    print(f"\n🚀 Starting Evaluation on {len(TEST_DATASET)} questions...\n")

    for item in TEST_DATASET:
        q = item["question"]
        gt = item["ground_truth"]
        
        # Get response from the RAG system
        ai_resp = get_chat_response(USER_ID, q)
        
        # Get the context actually retrieved for the judge to verify faithfulness
        docs = vector_store.similarity_search(q, k=2)
        context = "\n".join([d.page_content for d in docs])
        
        # Evaluate
        evaluation = judge_response(q, context, ai_resp, gt)
        
        results.append({"question": q, "evaluation": evaluation})
        
        print(f"Q: {q}")
        print(f"Rating: {evaluation['rating']} | Score: {evaluation['score']}/10")
        print(f"Reason: {evaluation['reason']}\n" + "-"*30)

    # 3. Final Summary
    hallucinations = [r for r in results if r['evaluation']['rating'] == "Hallucinated"]
    avg_score = sum(r['evaluation']['score'] for r in results) / len(results)
    
    print(f"\n✅ Test Suite Complete!")
    print(f"Final Hallucination Rate: {(len(hallucinations)/len(TEST_DATASET))*100}%")
    print(f"Average System Score: {avg_score}/10")

if __name__ == "__main__":
    run_automated_suite()