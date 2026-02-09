from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from PIL import Image
import torch
import re


class OpenSourceVision:
    def __init__(self):
        # Lightweight image captioning model (CPU-friendly)
        self.model = VisionEncoderDecoderModel.from_pretrained(
            "nlpconnect/vit-gpt2-image-captioning"
        )
        self.processor = ViTImageProcessor.from_pretrained(
            "nlpconnect/vit-gpt2-image-captioning"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(
            "nlpconnect/vit-gpt2-image-captioning"
        )
        self.model.eval()

    def sanitize_caption(self, caption: str) -> str:
        """
        Remove hallucinated or sensitive content.
        """
        banned_patterns = [
            r"\bwoman\b", r"\bman\b", r"\bgirl\b", r"\bboy\b",
            r"\bbreast\b", r"\bchest\b", r"\bface\b", r"\bperson\b",
            r"\bchild\b", r"\badult\b", r"\bfemale\b", r"\bmale\b"
        ]

        clean = caption.lower()
        for pat in banned_patterns:
            clean = re.sub(pat, "[redacted]", clean)

        return clean.strip()

    def analyze_image(self, image: Image.Image, injury_type: str):
        pixel_values = self.processor(
            images=image, return_tensors="pt"
        ).pixel_values

        with torch.no_grad():
            output_ids = self.model.generate(
                pixel_values,
                max_length=50,
                num_beams=4
            )

        caption = self.tokenizer.decode(
            output_ids[0], skip_special_tokens=True
        )
        caption = self.sanitize_caption(caption)

        return f"""
VISUAL OBSERVATION (NON-DIAGNOSTIC):
- The image shows surface-level visual features consistent with a {injury_type}.
- Observed characteristics may include discoloration, mild swelling, or texture changes.
- No assumptions are made about identity, age, or specific anatomy.

MODEL NOTE:
- Visual features are extracted using an open-source vision-language model
  and constrained via safety rules to prevent hallucinations.

GENERAL SAFETY GUIDANCE:
- Keep the affected area clean and dry.
- Avoid unnecessary pressure or strain.
- Monitor for worsening pain, swelling, or redness.

IMPORTANT:
- This is NOT a medical diagnosis.
- This system provides informational support only.
"""
