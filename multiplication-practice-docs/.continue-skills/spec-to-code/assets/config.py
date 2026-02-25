from lowcode.decorators import agent_config

@agent_config(key="agent.model", label="LLM Model", description="LLM Model Identifier")
def model_name():
    return "gpt-5"