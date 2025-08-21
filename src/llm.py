import torch
from tqdm import tqdm
from transformers.models.auto.modeling_auto import AutoModelForCausalLM
from transformers.models.auto.tokenization_auto import AutoTokenizer
from transformers.utils.quantization_config import BitsAndBytesConfig
from transformers.generation.configuration_utils import GenerationConfig


def init_model(model_name: str, token: str) -> tuple:
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        quantization_config=quantization_config,
        token=token,
    )

    return model, tokenizer


def query_model(model, tokenizer, text, max_new_tokens=2000):
    input_ids = tokenizer.encode(text, return_tensors="pt").to("cuda")
    output = model.generate(
        input_ids,
        max_new_tokens=max_new_tokens,
        pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        temperature=10e-10,  # near zero temperature for structured output
    )
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    return response


def create_query(prompt: str, text: str) -> str:
    sent = f"\nInput:\n{text}\nOutput:"

    return prompt + sent


def extract_ner(model, tokenizer, prompt, dataset):
    pred = []
    for sent in tqdm(dataset):
        query = create_query(prompt, sent["text"])
        response = query_model(model, tokenizer, query)

        pred.append(response.split("Output: \n")[-1])

    return pred
