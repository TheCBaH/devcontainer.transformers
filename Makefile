all: chat

MODEL=HuggingFaceTB/SmolLM2-135M-Instruct
chat:
	echo test |transformers-cli run --model ${MODEL}
	(echo '10 + 20 = ?';sleep 20;echo exit)|transformers-cli chat --model_name_or_path ${MODEL}
