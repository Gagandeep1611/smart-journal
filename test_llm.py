from smart_journal.llm.factory import get_llm_provider


provider = get_llm_provider()

response = provider.generate(
    "In one sentence, explain what a personal journal is."
)

print("\nLLM Response:")
print(response)