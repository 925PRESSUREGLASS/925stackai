import math
from typing import Optional

import torch
from torch import nn
from transformers import AutoTokenizer


class Llama3QuoteModel(nn.Module):
    """
    A LLaMA 3-style Transformer model for quote prediction.
    This is a decoder-only language model that generates structured quote output given an input description.
    """

    def ollama_chat(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        model: str = "llama3",
        host: str = "http://localhost:11434",
        max_new_tokens: int = 128,
    ) -> str:
        """
        Generate a conversational response using Ollama's Llama 3 model via local API.
        Falls back to local model if Ollama is unavailable.
        """
        import requests

        if system_prompt:
            prompt = (
                f"<|system|> {system_prompt}\n<|user|> {user_message}\n<|assistant|>"
            )
        else:
            prompt = f"User: {user_message}\nAssistant:"
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"num_predict": max_new_tokens},
        }
        try:
            response = requests.post(f"{host}/api/generate", json=data, timeout=60)
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except Exception as e:
            # Fallback to local model if Ollama is not available
            return f"[Ollama unavailable: {e}]\n" + self.chat(
                user_message, system_prompt, max_new_tokens
            )

    def __init__(
        self,
        model_name: str = "meta-llama/Llama-3-8B",
        d_model: int = 512,
        n_heads: int = 8,
        n_layers: int = 6,
        vocab_size: int = 32000,
        max_seq_len: int = 256,
    ):
        super().__init__()
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        except Exception:
            self.tokenizer = None
        self.d_model = d_model
        self.max_seq_len = max_seq_len
        self.vocab_size = vocab_size
        self.token_emb = nn.Embedding(self.vocab_size, d_model)
        self.pos_emb = nn.Parameter(torch.zeros(1, max_seq_len, d_model))
        self.layers = nn.ModuleList(
            [TransformerBlock(d_model, n_heads) for _ in range(n_layers)]
        )
        self.norm = nn.LayerNorm(d_model)
        self.output_proj = nn.Linear(d_model, self.vocab_size)

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        bsz, seq_len = input_ids.shape
        assert seq_len <= self.max_seq_len, "Input sequence too long"
        emb = self.token_emb(input_ids) + self.pos_emb[:, :seq_len, :]
        hidden = emb
        for layer in self.layers:
            hidden = layer(hidden)
        hidden = self.norm(hidden)
        logits = self.output_proj(hidden)
        return logits

    def generate_text(self, prompt: str, max_new_tokens: int = 64) -> str:
        """
        Generate text from a prompt using the model.
        """
        if self.tokenizer:
            input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        else:
            tokens = prompt.split()
            token_to_id = {tok: idx for idx, tok in enumerate(set(tokens), start=1)}
            input_ids = torch.tensor([[token_to_id[tok] for tok in tokens]])
        input_ids = input_ids.to(next(self.parameters()).device)
        self.eval()
        generated_ids = input_ids.tolist()[0]
        for _ in range(max_new_tokens):
            inp = torch.tensor([generated_ids]).to(next(self.parameters()).device)
            logits = self.forward(inp)
            next_token_id = int(torch.argmax(logits[0, -1, :]))
            if self.tokenizer and next_token_id == self.tokenizer.eos_token_id:
                break
            generated_ids.append(next_token_id)
        if self.tokenizer:
            output_text = self.tokenizer.decode(generated_ids[len(input_ids[0]) :])
        else:
            id_to_token = {v: k for k, v in token_to_id.items()}
            output_text = " ".join(
                id_to_token.get(i, "") for i in generated_ids[len(tokens) :]
            )
        return output_text

    def chat(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        max_new_tokens: int = 64,
    ) -> str:
        """
        Generate a conversational response to a user message.
        Uses Ollama Llama 3 if available, otherwise falls back to local model.
        """
        try:
            return self.ollama_chat(
                user_message, system_prompt, max_new_tokens=max_new_tokens
            )
        except Exception:
            # Fallback to local model if ollama_chat fails for any reason
            if system_prompt:
                prompt = f"<|system|> {system_prompt}\n<|user|> {user_message}\n<|assistant|>"
            else:
                prompt = f"User: {user_message}\nAssistant:"
            response = self.generate_text(prompt, max_new_tokens=max_new_tokens)
            return response.strip()


class TransformerBlock(nn.Module):
    def __init__(self, d_model: int, n_heads: int):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.attn = nn.MultiheadAttention(d_model, n_heads, batch_first=True)
        self.attn_ln = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, 4 * d_model), nn.GELU(), nn.Linear(4 * d_model, d_model)
        )
        self.ffn_ln = nn.LayerNorm(d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        seq_len = x.size(1)
        causal_mask = torch.triu(
            torch.ones(seq_len, seq_len, dtype=torch.bool, device=x.device), diagonal=1
        )
        attn_output, _ = self.attn(x, x, x, attn_mask=causal_mask)
        x = x + attn_output
        x = self.attn_ln(x)
        ff_output = self.ffn(x)
        x = x + ff_output
        x = self.ffn_ln(x)
        return x
