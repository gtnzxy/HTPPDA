from requests import JSONDecodeError
from src.app.models import HTPInput, HTPOutput, Usage, MethodList, AnalysisOutput
from fastapi import FastAPI, HTTPException, status

# 创建 FastAPI 应用
def create_app(model):
    app = FastAPI(
        title="HTP Test",  # 应用标题
        description="A simple web application that uses the House-Tree-Person test to analyze an image.",  # 应用描述
    )

    # 定义 POST 接口，用于预测分析
    @app.post("/v1/predict", response_model=HTPOutput, status_code=status.HTTP_200_OK)
    async def predict(data: HTPInput):
        """
        接收图像路径和语言参数，调用模型进行分析并返回结果。
        """
        try:
            # 确保语言参数为 "en" 或 "zh"
            assert data.language in ["en", "zh"], "Language must be either 'en' or 'zh'."
            
            # 调用模型的 workflow 方法进行分析
            result = model.workflow(
                image_path=data.image_path,  # 图像路径
                language=data.language       # 分析语言
            )
            
            # 构造返回结果
            result = HTPOutput(
                usage=Usage(
                    total_tokens=result["usage"]["total"],  # 总 token 数
                    prompt_tokens=result["usage"]["prompt"],  # 提示 token 数
                    completion_tokens=result["usage"]["completion"]  # 生成 token 数
                ),
                overall=AnalysisOutput(
                    feature=result["overall"]["feature"],  # 整体特征提取结果
                    analysis=result["overall"]["analysis"],  # 整体分析结果
                ),
                house=AnalysisOutput(
                    feature=result["house"]["feature"],  # 房子特征提取结果
                    analysis=result["house"]["analysis"],  # 房子分析结果
                ),
                tree=AnalysisOutput(
                    feature=result["tree"]["feature"],  # 树木特征提取结果
                    analysis=result["tree"]["analysis"],  # 树木分析结果
                ),
                person=AnalysisOutput(
                    feature=result["person"]["feature"],  # 人物特征提取结果
                    analysis=result["person"]["analysis"],  # 人物分析结果
                ),
                merge=result["merge"],  # 合并分析结果
                final=result["final"],  # 最终分析结果
                signal=result["signal"],  # 信号数据
                classification=result["classification"],  # 分类结果
                fix_signal=result["fix_signal"]  # 修正信号
            )

            return result  # 返回分析结果
        
        except JSONDecodeError as e:
            # 捕获 JSON 解码错误并返回 400 错误
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            # 捕获其他异常并返回 500 错误
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    # 定义 GET 接口，用于列出可用方法
    @app.get("/v1/methods", status_code=status.HTTP_200_OK)
    async def list_methods():
        """
        返回可用的 API 方法列表。
        """
        return MethodList(
            method=["predict"]  # 当前仅支持 "predict" 方法
        )
        
    return app  # 返回 FastAPI 应用实例