import torch
import logging
from transformers import AutoTokenizer, AutoModelForTokenClassification

logger = logging.getLogger(__name__)


class NERExtractor:
    def __init__(self, model_name: str = "yashpwr/resume-ner-bert-v2"):
        self.model_available = False
        self.tokenizer = None
        self.model = None
        
        try:
            logger.info(f"Attempting to load NER model: {model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForTokenClassification.from_pretrained(model_name)
            self.model_available = True
            logger.info("NER model loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load NER model {model_name}: {e}")
            logger.info("Falling back to regex-based skill extraction")
            self.model_available = False

    def extract(self, text: str, confidence_threshold=0.3):
        if not self.model_available:
            logger.debug("NER model not available, returning empty entities")
            return []
        
        try:
            encoded = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=256,
                padding=True,
                return_offsets_mapping=True
            )

            offset_mapping = encoded.pop("offset_mapping")

            with torch.no_grad():
                outputs = self.model(**encoded)
                predictions = torch.argmax(outputs.logits, dim=2)
                probabilities = torch.softmax(outputs.logits, dim=2)

            entities = []
            current_entity = None
            offset_mapping = offset_mapping[0]

            for i, (pred, offset) in enumerate(zip(predictions[0], offset_mapping)):
                label = self.model.config.id2label[pred.item()]
                confidence = probabilities[0][i][pred].item()

                if offset[0] == 0 and offset[1] == 0:
                    continue

                if label.startswith('B-'):
                    if current_entity and current_entity['confidence'] >= confidence_threshold:
                        entities.append(current_entity)

                    entity_type = label[2:]
                    current_entity = {
                        'text': text[offset[0]:offset[1]],
                        'label': entity_type,
                        'start': offset[0],
                        'end': offset[1],
                        'confidence': confidence
                    }
                    confidences = [confidence]

                elif label.startswith('I-') and current_entity:
                    entity_type = label[2:]
                    if entity_type == current_entity['label']:
                        token_text = text[offset[0]:offset[1]]
                        if token_text.startswith('##'):
                            current_entity['text'] += token_text[2:]
                        else:
                            current_entity['text'] += ' ' + token_text
                        
                        current_entity['end'] = offset[1]
                        confidences.append(confidence)
                        current_entity['confidence'] = sum(confidences) / len(confidences)

                elif label == 'O':
                    if current_entity and current_entity['confidence'] >= confidence_threshold:
                        entities.append(current_entity)
                    current_entity = None
                    confidences = []

            if current_entity and current_entity['confidence'] >= confidence_threshold:
                entities.append(current_entity)

            return entities
            
        except Exception as e:
            logger.error(f"Error during NER extraction: {e}")
            return []
