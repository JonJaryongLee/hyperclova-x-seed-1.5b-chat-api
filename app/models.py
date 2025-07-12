import torch
from transformers import BitsAndBytesConfig, AutoModelForCausalLM, AutoTokenizer

# 사용할 모델 이름
MODEL_NAME = "naver-hyperclovax/HyperCLOVAX-SEED-Text-Instruct-1.5B"


def load_quantized_model(model_name: str):
    # 8-bit 양자화 + FP32 CPU 오프로드 활성화
    bnb_config = BitsAndBytesConfig(
        load_in_8bit=True,
        llm_int8_enable_fp32_cpu_offload=True,
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto",
        low_cpu_mem_usage=True,
        offload_folder="offload"   # (선택) 오프로드 폴더 지정
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    model.eval()
    return model, tokenizer

# 전역에 모델 로딩
model, tokenizer = load_quantized_model(MODEL_NAME)


def prepare_inputs(messages: list[dict], device: str = "cuda") -> dict:
    """
    chat_history 리스트를 입력 텐서로 변환하고 GPU로 이동합니다.
    """
    encoded = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt"
    )
    return {k: v.to(device) for k, v in encoded.items()}

def generate_response(inputs: dict, max_new_tokens: int = 128) -> str:
    """
    입력 텐서로부터 응답을 생성하고 디코딩합니다.
    inputs: prepare_inputs() 리턴값
    max_new_tokens: 추가로 생성할 토큰 수
    return: 오로지 생성된 텍스트(새 토큰)만
    """
    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            eos_token_id=tokenizer.eos_token_id,
            use_cache=True,
            num_beams=1,
            do_sample=False
        )

    # 1) prompt 길이 계산
    prompt_len = inputs["input_ids"].shape[-1]
    # 2) 새로 생성된 토큰만 슬라이스
    gen_ids = output_ids[0][prompt_len:]
    # 3) 디코딩
    text = tokenizer.decode(gen_ids, skip_special_tokens=True).strip()
    return text
