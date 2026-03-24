from abc import ABC, abstractmethod
import os
import json
from src.config import config

class BaseAI(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

class BedrockAI(BaseAI):
    def __init__(self, model_id):
        import boto3
        self.client = boto3.client("bedrock-runtime")
        self.model_id = model_id

    def generate(self, prompt: str) -> str:
        # Example for Titan Text model
        body = json.dumps({
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 512,
                "temperature": 0.7,
            }
        })
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=body,
            contentType="application/json"
        )
        result = json.loads(response["body"].read())
        return result["results"][0]["outputText"]

class AzureOpenAI(BaseAI):
    def __init__(self, deployment_name, endpoint, api_key, api_version="2023-12-01-preview"):
        from openai import AzureOpenAI
        self.client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version
        )
        self.deployment = deployment_name

    def generate(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content

def get_ai_client():
    cloud = config["cloud"]
    ai_cfg = config["ai"]
    if cloud == "aws":
        model_id = ai_cfg["model_id"]
        return BedrockAI(model_id)
    elif cloud == "azure":
        deployment = ai_cfg["deployment_name"]
        endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        api_key = os.environ.get("AZURE_OPENAI_KEY")
        return AzureOpenAI(deployment, endpoint, api_key)
    else:
        raise ValueError(f"Unsupported cloud: {cloud}")