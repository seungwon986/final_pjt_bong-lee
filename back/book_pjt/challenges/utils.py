import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from .models import BookQuiz, QuizAttempt, ChallengeParticipant

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_quizzes_for_book(book):
    print(f"🔍 [퀴즈 생성 시작] - {book.title}")

    if BookQuiz.objects.filter(book=book).count() >= 10:
        print("✅ 이미 충분한 퀴즈가 존재합니다.")
        return

    prompt = (
        f"'{book.title}' 책을 기반으로 객관식 퀴즈 10문제를 만들어줘. "
        "각 문제는 다음 JSON 형식으로 줘: "
        "[{\"question\": \"...\", \"choices\": {\"A\": \"...\", \"B\": \"...\", \"C\": \"...\", \"D\": \"...\"}, \"answer\": \"A\"}, ...]"
        "추가 설명 없이 JSON만 반환해줘."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=2000
        )

        quiz_text = response.choices[0].message.content.strip()
        print("📦 GPT 응답 일부:", quiz_text[:300])

        json_start = quiz_text.find("[")
        json_end = quiz_text.rfind("]") + 1

        if json_start == -1 or json_end == -1:
            raise ValueError("📛 JSON 형식의 응답을 찾을 수 없습니다.")

        json_string = quiz_text[json_start:json_end]

        try:
            questions = json.loads(json_string)
        except json.JSONDecodeError as je:
            print("❌ JSON 파싱 오류 발생:", je)
            print("⚠️ JSON 문자열:", json_string[:300])
            return

        for q in questions:
            BookQuiz.objects.create(
                book=book,
                question=q['question'],
                choices=q['choices'],
                answer=q['answer']
            )

        print(f"✅ 퀴즈 {len(questions)}개 생성 완료")

    except Exception as e:
        print("❌ 퀴즈 생성 실패:", e)


def generate_dummy_quizzes_for_book(book, count=10):
    for i in range(count):
        BookQuiz.objects.create(
            book=book,
            question=f"{book.title} 관련 예제 문제 {i+1}",
            choices={"A": "선택 A", "B": "선택 B", "C": "선택 C", "D": "선택 D"},
            answer="A"
        )


def record_quiz_attempt(user, challenge, score):
    attempt = QuizAttempt.objects.create(
        user=user,
        challenge=challenge,
        score=score
    )

    if score >= 40:
        participant = ChallengeParticipant.objects.filter(user=user, challenge=challenge).first()
        if participant:
            participant.success = True
            participant.save()
            print("🎉 챌린지 성공 기록됨")

    return attempt
