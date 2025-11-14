import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_google_vertexai import ChatVertexAI

# --- Cấu hình ---
PROJECT_ID = "sanlaw-477509"
LOCATION = "us-central1"
MODEL_NAME = "gemini-2.5-pro"

# --- Khởi tạo ---
app = FastAPI(
    title="SanLexAi Automated Factory",
    description="Agent for Code Generation and Unit Testing V.1"
)

llm = ChatVertexAI(
    model_name=MODEL_NAME,
    project=PROJECT_ID,
    location=LOCATION
)

# --- Mô hình Dữ liệu ---
class PromptRequest(BaseModel):
    prompt: str

class CodeGenerationResponse(BaseModel):
    functional_code: str
    test_code: str
    message: str

# --- Logic của Agent ---
def _invoke_llm(prompt: str) -> str:
    """Hàm helper để gọi LLM và trả về nội dung."""
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"Error invoking LLM: {e}")
        raise HTTPException(status_code=500, detail=f"Error communicating with the AI model: {e}")

# --- API Endpoints ---
@app.post("/generate-code-and-test", response_model=CodeGenerationResponse)
def generate_code_and_test(request: PromptRequest):
    """
    Endpoint chính: Nhận prompt, sinh mã chức năng, sau đó sinh unit test.
    """
    print(f"Received prompt: {request.prompt}")

    # 1. Sinh mã chức năng (Developer Agent)
    dev_prompt = f"""
    Based on the following request, write a single, complete, and executable Python code snippet.
    Do not add any explanation, comments, or markdown formatting like ```python.
    Only return the raw Python code.

    Request: "{request.prompt}"
    """
    functional_code = _invoke_llm(dev_prompt)
    print(f"Generated functional code:\n{functional_code}")

    # 2. Sinh mã kiểm thử (Tester Agent)
    tester_prompt = f"""
    Based on the following Python code, write a complete unit test for it using the pytest framework.
    Assume the code is in a file named 'generated_code.py'.
    Your test file should be named 'test_generated_code.py'.
    Import the necessary functions from 'generated_code.py'.
    Do not add any explanation or markdown formatting. Only return the raw Python code for the test file.

    Python code to test:
    ---
    {functional_code}
    ---
    """
    test_code = _invoke_llm(tester_prompt)
    print(f"Generated test code:\n{test_code}")

    # 3. (Tùy chọn) Lưu code vào file để kiểm thử trong môi trường CI/CD
    # Tạo thư mục nếu chưa tồn tại
    os.makedirs("generated_code_output", exist_ok=True)
    with open("generated_code_output/generated_code.py", "w") as f:
        f.write(functional_code)
    with open("generated_code_output/test_generated_code.py", "w") as f:
        f.write(test_code)

    return {
        "functional_code": functional_code,
        "test_code": test_code,
        "message": "Code and test generated successfully. Files saved for CI/CD."
    }

@app.get("/")
def read_root():
    return {"status": "Automated Factory is running"}