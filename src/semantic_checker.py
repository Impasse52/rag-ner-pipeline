import os
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch


def query_model(prompt, max_new_tokens):
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to("cuda")
    output = model.generate(input_ids, max_new_tokens=max_new_tokens)
    response = tokenizer.decode(output[0], skip_special_tokens=True)


# return response


def build_query(prompt, input_sent) -> str:
    return prompt + "\nInput: " + input_sent


def check_semantic_validity(prompt, input_sent):
    query = build_query(prompt, input_sent)
    response = query_model(query, max_new_tokens=2)

    return response[len(query) :]


quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)

# token = os.environ["HF_TOKEN"]
# tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)
# model = AutoModelForCausalLM.from_pretrained(
#     "google/gemma-7b-it",
#     device_map="auto",
#     quantization_config=quantization_config,
#     token=token,
# )

if __name__ == "__main__":
    prompt = """
Sei un eccellente controllatore di frasi: il tuo obiettivo è di verificare che una frase abbia senso o meno. Il tuo unico output è “False” se la frase non ha senso, “True” se ne ha.

Per esempio:
Input: the is chicken. in is a the climb tree. ok
False
Input: REPUBBLICA ITALIANA IN NOME DEL POPOLO ITALIANO TRIBUNALE DI PALERMO Il giudice per l’udienza preliminare, dott. Lorenzo Jannelli, all’udienza del 29 marzo 2010 in camera di consiglio ha pronunciato mediante lettura del dispositivo la seguente SENTENZA (art. 438 e ss.\n'
True 
"""

    input_sent = "Il Riccardo Galli ha specificato di aver conosciuto il Paride Valli presso la macelleria, sita nel quartiere Salamini, dei propri cugini Ettore Vitale, Ottavio Neri ed Leandro Sala (l’altro collaborante già citato), frequentata dal padre Riccardo Galli e da altri uomini d’altri tempi (come Gambino Simone Costa) e che il Paride Valli era persona vicina ed amica di Tullio Conte Di Napoli, circostanza anche personalmente constatata dal collaboratore allorché, in alcune occasioni, aveva incontrato il Paride Valli in compagnia del Di Napoli nella villa di proprietà di Enrico Fontana Gino Basile, altro uomo d’altri tempi della famiglia di Orlando Pace, nonché parente dello stesso Paride Valli ove lo stesso Di Napoli dimorava durante la sua gita."

    res = check_semantic_validity(prompt, input_sent)
    print(res)
