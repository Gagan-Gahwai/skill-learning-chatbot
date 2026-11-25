
import ollama


MODEL_NAME = "qwen2.5:1.5b-instruct"


# --------------------------------
# SYSTEM PROMPT
# --------------------------------


SYSTEM_PROMPT = """
You are the official AI assistant of Skill Learning Academy.

Your job is to help website visitors with:
- Course information
- Course fees
- Course duration
- Curriculum
- Certifications
- Placement assistance
- Admissions and counselling

IMPORTANT RULES:

1. Answer using the supplied website context.
2. Be friendly, natural and professional.
3. Use simple English.
4. Never invent course fees, phone numbers,
   email addresses or placement guarantees.
5. If the requested information is missing,
   do not simply say "I don't know".
6. Politely explain that the information is
   not currently available.
7. Guide the visitor to contact the academy
   for more information.
8. Provide the official contact page:
   https://www.skilllearningacademy.com/contact-us
9. If a verified phone number or email address
   is present in the supplied context, include it.
10. Never make up contact details.
11. Keep answers conversational and concise.

EXAMPLE FALLBACK:

If someone asks about course fees and the
context does not contain the fees, respond:

"The course fee isn't currently available
in the information I have. No worries!

You can contact our counselling team for
the latest fee details and available batches.

Contact us:
https://www.skilllearningacademy.com/contact-us

They will help you with the details!"

Remember:
Your priority is helpfulness and accuracy.
"""



# --------------------------------
# GENERATE ANSWER
# --------------------------------

def generate_answer(question, context):

    user_prompt = f"""
Use the following website information to answer the question.

WEBSITE CONTEXT:
{context}

USER QUESTION:
{question}

INSTRUCTIONS:
Answer the question using the website context.
If the context does not contain the answer, say so honestly.
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        options={
            "temperature": 0.2
        }
    )

    return response["message"]["content"]


# --------------------------------
# TEST GENERATOR
# --------------------------------

if __name__ == "__main__":

    question = "What courses does Skill Learning Academy offer?"

    context = """
    Skill Learning Academy offers AI Integrated courses,
    Java Full Stack Development courses and training programs.
    The academy also provides job-oriented training.
    """

    answer = generate_answer(question, context)

    print("\n========== AI GENERATED ANSWER ==========\n")
    print(answer)
