import re
from transformers import pipeline

ner_model = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

text_path = "" #provide the file path

with open(text_path, "r", encoding="utf-8") as file:
    text = file.read()

ner_results = ner_model(text)

# now as this model is a generic NER model, it may not capture all the specific entities that we want
counterparty = None
for ent in ner_results:
    if ent["entity_group"] == "ORG" and "BANK" in ent["word"].upper(): # Looking for org names with bank in this specific scenario
        counterparty = ent["word"]

# for other entities we can use rule based parsing to extract them
notional = re.search(r"\b\d+\s*(mio|million|bn|billion)\b", text, re.I)
isin = re.search(r"\b[A-Z]{2}[A-Z0-9]{9}\d\b", text)
maturity = re.search(r"\b\d+\s*[YMQ]\b", text, re.I)
bid = re.search(r"\bestr\+\d+\s*bps\b", text, re.I)
payment_freq = re.search(r"\b(quarterly|monthly|annual|semi-annual)\b", text, re.I)

entities = {
    "Counterparty": counterparty,
    "Notional": notional.group(0) if notional else None,
    "ISIN": isin.group(0) if isin else None,
    "Maturity": maturity.group(0) if maturity else None,
    "Bid": bid.group(0) if bid else None,
    "PaymentFrequency": payment_freq.group(0).capitalize() if payment_freq else None,
}

print(entities)