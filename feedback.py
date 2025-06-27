def check_answer(user_answer, correct_answer):
    return "✅ Correct!" if user_answer.strip() == correct_answer else f"❌ Answer is {correct_answer}"
