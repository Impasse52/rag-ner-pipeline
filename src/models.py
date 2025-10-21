from prompts import default_examples
import sys
import torch
from tqdm.notebook import tqdm
from transformers.models.auto.modeling_auto import AutoModelForCausalLM
from transformers.models.auto.tokenization_auto import AutoTokenizer
from transformers.utils.quantization_config import BitsAndBytesConfig


from haystack import Pipeline
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.embedders import (
    SentenceTransformersTextEmbedder,
    SentenceTransformersDocumentEmbedder,
)

from haystack.components.retrievers.in_memory import InMemoryBM25Retriever


def init_llm(model_name: str, token: str, do_quantization=True) -> tuple:
    quantization_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        quantization_config=quantization_config if do_quantization else None,
        token=token,
    )

    return model, tokenizer


def query_llm(model, tokenizer, text, max_new_tokens=2000):
    inputs = tokenizer(
        text,
        return_tensors="pt",
    ).to("cuda")

    output = model.generate(
        inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
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


def query_relevant_docs_sent_similarity(
    q,
    document_store,
    top_k=3,
    model_name="sentence-transformers/all-MiniLM-L6-v2",
):
    """
    Retrieve the most semantically similar documents to query `q`
    using sentence embeddings.
    """

    # 1️⃣ Create embedding components
    doc_embedder = SentenceTransformersDocumentEmbedder(model=model_name, token=False)
    retriever = InMemoryEmbeddingRetriever(
        document_store=document_store, top_k=top_k + 1
    )
    query_embedder = SentenceTransformersTextEmbedder(model=model_name, token=False)

    query_embedder.warm_up()
    doc_embedder.warm_up()

    # 2️⃣ Build pipeline
    pipeline = Pipeline()
    pipeline.add_component("query_embedder", query_embedder)
    pipeline.add_component("retriever", retriever)
    pipeline.connect("query_embedder.embedding", "retriever.query_embedding")

    # 3️⃣ Ensure documents have embeddings
    # (Only needed once, not every query)
    if not any(d.embedding is not None for d in document_store.filter_documents()):
        docs = document_store.filter_documents()
        doc_embedder.run(docs)
        document_store.write_documents(docs, policy="overwrite")

    # 4️⃣ Run the pipeline
    result = pipeline.run({"query_embedder": {"text": q}})

    # 5️⃣ Extract results
    similar_docs = result["retriever"]["documents"]

    rag_examples = "".join(
        [
            f"\nInput:\n{d.content[:-1]}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\nOutput:\n{d.meta.get('output', '')}<|eot_id|>\n"
            for d in similar_docs[1:]
        ]
    )

    return rag_examples


def query_relevant_docs(q, document_store, top_k=3):
    # Create BM25 retriever
    retriever = InMemoryBM25Retriever(document_store=document_store)

    # Build pipeline
    pipeline = Pipeline()
    pipeline.add_component(name="retriever", instance=retriever)

    # Run the pipeline
    similar_docs = pipeline.run(data={"retriever": {"query": q, "top_k": top_k + 1}})

    # Display results
    for doc in similar_docs["retriever"]["documents"]:
        pass
        # print(
        #     f"Score: {doc.score:.2f} | Content: {doc.content} | Output: {doc.meta['output']}"
        # )

    rag_examples = "".join(
        [
            f"\nInput:\n{d.content[:-1]}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\nOutput:\n{d.meta['output']}<|eot_id|>\n"
            for d in similar_docs["retriever"]["documents"][1:]
        ]
    )

    return rag_examples


def extract_ner(model, tokenizer, prompt, dataset, document_store):
    pred = []
    for sent in tqdm(dataset):
        rag_examples = query_relevant_docs(sent["text"], document_store)
        # query = create_query(prompt + default_examples, sent["text"])
        query = create_query(prompt + rag_examples, sent["text"])

        # DEBUG ONLY
        # print("\nINIZIO ESEMPI\n")
        # print(rag_examples)
        # print("\nFINE ESEMPI\n")
        # print("---------------- INIZIO QUERY ----------------")
        # print(query)
        # print("---------------- FINE QUERY ----------------")

        response = query_llm(model, tokenizer, query)
        output_pred = response.split("Output: \n")[-1]
        print(sent["text"])

        # print("---------------- INIZIO RESPONSE ----------------")
        # print(response)
        # print("---------------- FINE RESPONSE ----------------")

        # Update tqdm output
        output = f"{output_pred}"
        # print(output)
        # print()

        pred.append(output_pred)

        break

    return pred
