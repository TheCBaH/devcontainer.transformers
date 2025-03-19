all: chat

chat:
	(echo '10 + 20 = ?';sleep 20;echo exit)|transformers-cli chat --model_name_or_path HuggingFaceTB/SmolLM2-135M-Instruct
