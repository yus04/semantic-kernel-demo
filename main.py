import asyncio
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureTextCompletion
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.planning.basic_planner import BasicPlanner
from skills.GetStockPrice.native_function import GetStockPrice
from skills.PredictStockPrice.native_function import PredictStockPrice

async def main():
    # カーネルの作成
    kernel = sk.Kernel()    
    deployment, api_key, endpoint = sk.azure_openai_settings_from_dot_env()
    completion_service = AzureChatCompletion(deployment, endpoint, api_key)
    kernel.add_chat_service("gpt-35-turbo", completion_service)

    # スキルの読み込み
    skill_dir = "skills"
    analyze_skill = kernel.import_semantic_skill_from_directory(skill_dir, "AnalyzeReason")
    get_skill = kernel.import_skill(GetStockPrice(), skill_name="GetStockPrice")
    predict_skill = kernel.import_skill(PredictStockPrice(), skill_name="PredictStockPrice")

    # ユーザの入力を基に実行計画を作成
    user_input = """
    Get Microsoft's stock price for the last one month,
    If the stock price is likely to rise or fall in the future, you can output a "Buy" or a "Sell",
    Please also tell us why you made this decision.
    """
    planner = BasicPlanner()
    # my_prompt = """
    # Original promplt is here.
    # """
    # plan = await planner.create_plan_async(user_input, kernel, my_prompt)
    plan = await planner.create_plan_async(user_input, kernel)

    # プランを実行
    response = await planner.execute_plan_async(plan, kernel)
    print(response)

asyncio.run(main())
