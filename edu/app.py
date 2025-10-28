from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
import random # (주: 이제 random.choice는 사용하지 않습니다)

# Flask 애플리케이션 초기화
app = Flask(__name__)
# 웹 프론트엔드 (다른 출처)의 요청을 허용하기 위해 CORS 설정
CORS(app) 

# --- LangChain 및 Ollama 설정 ---

# OllamaLLM 초기화. gemma3:latest 모델 사용
try:
    llm = OllamaLLM(model="gemma3:latest")
    print("OllamaLLM (gemma3:latest) 초기화 성공.")
except Exception as e:
    print(f"OllamaLLM 초기화 실패. Ollama 서버가 실행 중인지 확인하세요. 오류: {e}")
    # 서버 실행에는 문제가 없지만, 실제 API 호출 시 에러가 발생할 수 있음.

examples = [
    {"question": "Word2Vec가 뭐야?", "answer": "Word2Vec는 단어들 사이의 관계를 숫자로 계산하는 방법이야. 예를 들어 '왕 - 남자 + 여자 = 여왕' 같은 연산이 가능해."},
    {"question": "역전파는 뭐야?", "answer": "역전파는 인공지능이 실수를 찾고 수정하는 과정이야. 마치 틀린 문제 다시 풀어보는 거랑 비슷해."}
]

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=ChatPromptTemplate.from_messages([
        ("human", "{question}"),
        ("ai", "{answer}")
    ]),
    examples=examples
)

styles = [
    "초등학생도 이해할 수 있게 설명해줘.",
    "재밌는 예시로 알려줘.",
    "교과서 스타일로 정리해줘.",
    "블로그 글처럼 설명해줘.",
    "친절한 선생님처럼 말해줘."
]

# LangChain Prompt 구성
prompt = ChatPromptTemplate.from_messages([
    ("system", "넌 친절하고 똑똑한 AI 튜터야. 사용자의 질문에 쉽고 다양한 방식으로 답해줘. 답변은 반드시 한국어로 해줘."),
    *few_shot_prompt.format_messages(),
    MessagesPlaceholder("chat_history"),
    # {style} 변수에 사용자가 선택한 스타일이 들어옵니다.
    ("human", "{question} 스타일: {style}") 
])

# LangChain Chain 구성
chain = prompt | llm | StrOutputParser()

# --- API 엔드포인트 ---

@app.route('/chat', methods=['POST'])
def chat():
    """웹 프론트엔드로부터 질문과 대화 기록, 스타일을 받아 응답을 생성합니다."""
    data = request.json
    user_input = data.get("question")
    selected_style = data.get("style") # <-- 프론트에서 넘어온 스타일을 받습니다.
    chat_history_data = data.get("chat_history", [])

    if not user_input:
        return jsonify({"error": "질문이 제공되지 않았습니다."}), 400
    
    if not selected_style:
         # 스타일이 누락된 경우를 대비한 처리
        return jsonify({"error": "답변 스타일을 선택해야 합니다."}), 400

    # 1. 사용자가 선택한 스타일 사용
    print(f"새 질문: '{user_input}' | 선택된 스타일: {selected_style}")

    # 2. LangChain Chain에 전달할 대화 기록 형식 조정
    formatted_chat_history = []
    for msg in chat_history_data:
        role_map = {'user': 'human', 'ai': 'ai'} 
        lc_role = role_map.get(msg['role'], 'human')
        formatted_chat_history.append((lc_role, msg['content']))
    
    # 3. Chain 호출
    try:
        response_text = chain.invoke({
            "question": user_input,
            "style": selected_style, # <-- 사용자가 선택한 스타일 전달
            "chat_history": formatted_chat_history
        })
        
        # 4. 결과 반환
        return jsonify({
            "response": response_text.strip(),
            "style": selected_style # <-- 사용자가 선택한 스타일을 다시 프론트로 반환
        })
        
    except Exception as e:
        print(f"Chain 호출 중 오류 발생: {e}")
        return jsonify({"error": "AI 모델 응답 생성 중 오류가 발생했습니다. Ollama 서버와 gemma3:latest 모델 상태를 확인해 주세요.", "details": str(e)}), 500

if __name__ == '__main__':
    # Flask 서버 실행 (http://localhost:5000)
    print("Flask 서버를 시작합니다. http://localhost:5000/chat 엔드포인트로 통신합니다.")
    app.run(debug=True, host='0.0.0.0', port=5000)
