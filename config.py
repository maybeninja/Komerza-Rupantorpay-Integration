import yaml

SETTINGS_FILE = "settings.yaml"

with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

KomerzaAPIKey = config.get("KomerzaAPIKey", "")
DiscordWebhookUrl = config.get("DiscordWebhookUrl", "")
BaseURL = config.get("BaseURL", "")
KomerzaStoreID = config.get("KomerzaStoreID", "")
RupantarPayAPIKey = config.get("RupantarPayAPIKey", "")