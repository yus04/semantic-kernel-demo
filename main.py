import asyncio
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.planning.basic_planner import BasicPlanner
from semantic_kernel.planning.basic_planner import Plan
from skills.GetStockPrice.native_function import GetStockPrice
from skills.PredictStockPrice.native_function import PredictStockPrice

# カーネルを作成する関数
def create_kernel() -> sk.Kernel:
    kernel = sk.Kernel()    
    deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()
    completion_service = AzureChatCompletion(deployment, endpoint, api_key)
    kernel.add_chat_service("gpt-35-turbo", completion_service)
    return kernel

# カーネルのスキルを読み込み
def load_skills(kernel: sk.kernel) -> sk.Kernel:
    skill_dir = "skills"
    analyze_skill = kernel.import_semantic_skill_from_directory(skill_dir, "AnalyzeReason")
    get_skill = kernel.import_skill(GetStockPrice(), skill_name="GetStockPrice")
    predict_skill = kernel.import_skill(PredictStockPrice(), skill_name="PredictStockPrice")
    return kernel

async def create_plan(planner: BasicPlanner, kernel: sk.Kernel, use_my_prompt: bool, user_input: str, my_prompt: str) -> Plan:
    if use_my_prompt:
        return await planner.create_plan_async(user_input, kernel, my_prompt)
    else:
        return await planner.create_plan_async(user_input, kernel)

async def execute_plan(planer: BasicPlanner, plan: Plan, kernel: sk.Kernel) -> str:
    response = await planer.execute_plan_async(plan, kernel)
    return response

async def main():
    kernel = create_kernel()
    kernel = load_skills(kernel)

    use_my_prompt = False

    user_input = """
    Get Microsoft's stock price for the last one month,
    If the stock price is likely to rise or fall in the future, you can output a "Buy" or a "Sell",
    Please also tell us why you made this decision.
    """

    my_prompt = """
    You can define any promplt here.
    """

    planner = BasicPlanner()
    plan = await create_plan(planner, kernel, use_my_prompt, user_input, my_prompt)
    response = await execute_plan(planner, plan, kernel)
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
