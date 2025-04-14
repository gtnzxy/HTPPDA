import base64
import os
from io import BytesIO

import requests
import streamlit as st
from langchain_openai import ChatOpenAI
from PIL import Image

from model_langchain import HTPModel

# 常量设置
BASE_URL = "https://api.zhizengzeng.com/v1"
BASE_API = "sk-zk24b495cde4d68ae134f94d6ae08964f3067d2e05279d61"

MAX_IMAGE_SIZE = (800, 800)

# 支持的语言及其代码
SUPPORTED_LANGUAGES = {
    "English": "en",
    "中文": "zh"
}

# 示例样例图片路径（仅供记录，不进行预览）
SAMPLE_IMAGES = {
    "example1": "example/example1.jpg",
    "example2": "example/example2.jpg",
    "example3": "example/example3.jpg",
    "example4": "example/example4.jpg",
}

# 多语言文本配置
LANGUAGES = {
    "en": {
        "app_title": "🏡 House-Tree-Person Projective Drawing Test",
        "welcome_message": "Welcome to the HTP projective drawing test application.",
        "instructions_title": "📋 Test Instructions",
        "instructions": """
**Please read the following instructions carefully:**

1. **Fill the API Key**: Enter your API Key in the sidebar to authenticate.
2. **Drawing Requirements**: Draw a picture on white paper with a pencil including a **house**, **trees**, and a **person**.
3. **Be Creative**: There are no right or wrong answers.
4. **No Aids**: Do not use drawing aids.
5. **No Time Limit**: Take as much time as needed.
6. **Upload your Drawing**: Then upload your file via the sidebar.
7. **Sample Drawings**: Sample file names are provided in the sidebar.

**Note**: All information is kept strictly confidential.
        """,
        "upload_prompt": "👉 Please upload your drawing using the sidebar.",
        "analysis_complete": "✅ Analysis Complete! The result is shown below.",
        "analysis_summary": "🔍 Analysis Summary:",
        "uploaded_info": "Drawing file uploaded: **{}**",
        "disclaimer": """
**Disclaimer**:
- This test is for reference only and cannot replace professional psychological diagnosis.
- If you feel uncomfortable, please stop immediately and seek help.
        """,
        "model_settings": "🍓 Model Settings",
        "analysis_settings": "🔧 Analysis Settings",
        "report_language": "Report Language:",
        "upload_drawing": "🖼️ Upload Your Drawing:",
        "start_analysis": "🚀 Start Analysis",
        "reset": "♻️ Reset",
        "download_report": "⬇️ Download Report",
        "download_help": "Download the analysis report as a text file.",
        "error_no_image": "Please upload an image first.",
        "analyzing_image": "Analyzing image, please wait...",
        "error_analysis": "Error during analysis: ",
        "session_reset": "Session has been reset. You can now upload a new image.",
        "sample_drawings": "📊 Sample Drawings (File Names)",
        "load_sample": "Load Sample {}",
        "sample_loaded": "Sample {} loaded. Click 'Start Analysis' to proceed.",
        "error_no_api_key": "❌ Please enter your API key in the sidebar before starting analysis.",
        "ai_disclaimer": "NOTE: AI-generated content, for reference only. Not a substitute for medical diagnosis.",
        "test_result_title": "Test Result / 测试结果",
        "download_result": "Download Test Result / 下载测试结果"
    },
    "zh": {
        "app_title": "🏡 房树人投射绘画测试",
        "welcome_message": "欢迎使用房树人投射绘画测试应用程序。",
        "instructions_title": "📋 测试说明",
        "instructions": """
**请仔细阅读以下说明：**

1. **填写 API 密钥**：请在侧边栏填写 API 密钥进行身份验证。
2. **绘画要求**：请在白纸上用铅笔绘制一幅包含 **房子**、**树木** 和 **人** 的作品。
3. **发挥创意**：没有绝对的对错之分。
4. **不使用辅助工具**：请勿使用绘图辅助工具。
5. **不限时间**：请尽情发挥，时间不限。
6. **上传绘画**：完成后请通过侧边栏上传您的作品。
7. **样例绘画**：侧边栏中提供了样例文件名以供参考。

**注意**：所有信息将严格保密。
        """,
        "upload_prompt": "👉 请使用侧边栏上传您的绘画作品。",
        "analysis_complete": "✅ 分析完成！结果如下：",
        "analysis_summary": "🔍 分析摘要：",
        "uploaded_info": "已上传绘画文件： **{}**",
        "disclaimer": """
**免责声明**：
- 本测试仅供参考，不能替代专业的心理诊断。
- 若感到不适，请立即停止测试并寻求帮助。
        """,
        "model_settings": "🍓 模型设置",
        "analysis_settings": "🔧 分析设置",
        "report_language": "报告语言：",
        "upload_drawing": "🖼️ 上传您的绘画作品：",
        "start_analysis": "🚀 开始分析",
        "reset": "♻️ 重置",
        "download_report": "⬇️ 下载报告",
        "download_help": "将分析报告下载为文本文件。",
        "error_no_image": "请先上传一张图片。",
        "analyzing_image": "正在分析图片，请稍候...",
        "error_analysis": "分析过程中出现错误：",
        "session_reset": "会话已重置。您现在可以上传新的图片。",
        "sample_drawings": "📊 绘画样例（文件名）",
        "load_sample": "加载样例 {}",
        "sample_loaded": "样例 {} 已加载。点击‘开始分析’进行分析。",
        "error_no_api_key": "❌ 请在开始分析之前在侧边栏输入 API 密钥。",
        "ai_disclaimer": "注意：本报告由 AI 生成，仅供参考，不能替代医学诊断。",
        "test_result_title": "测试结果 / Test Result",
        "download_result": "下载测试结果 / Download Test Result"
    }
}

# 根据当前 session_state 中的语言代码获取对应文本
def get_text(key):
    return LANGUAGES[st.session_state['language_code']][key]

# 将 PIL 图像转换为 base64 编码字符串
def pil_to_base64(image: Image.Image, format: str = "JPEG") -> str:
    buffered = BytesIO()
    image.save(buffered, format=format)
    return base64.b64encode(buffered.getvalue()).decode('utf-8')
    
# 调整图像尺寸（保持在最大尺寸内）
def resize_image(image: Image.Image, max_size: tuple = MAX_IMAGE_SIZE) -> Image.Image:
    if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
        image.thumbnail(max_size)
    return image

# 分析图片，通过模型 workflow 处理
def analyze_image(model) -> None:
    if st.session_state['image_data'] is None:
        st.error(get_text("error_no_image"))
        return

    inputs = {
        "image_path": st.session_state['image_data'],
        "language": st.session_state['language_code']
    }
    try:
        with st.spinner(get_text("analyzing_image")):
            response = model.workflow(**inputs)
            st.session_state['analysis_result'] = response
    except requests.RequestException as e:
        st.error(f"{get_text('error_analysis')}{str(e)}")

# 重置会话中的图片和分析结果
def reset_session() -> None:
    for key in ['image_data', 'analysis_result']:
        if key in st.session_state:
            del st.session_state[key]
    st.success(get_text("session_reset"))

# 导出报告，并在侧边栏提供下载按钮
def export_report() -> None:
    if st.session_state.get('analysis_result'):
        if st.session_state["analysis_result"]['classification'] is True:
            signal = st.session_state['analysis_result'].get('signal', '')
            final_report = st.session_state['analysis_result'].get('final', '').replace("<output>", "").replace("</output>", "")
            disclaimer = get_text("ai_disclaimer")
            export_data = f"{disclaimer}\n\n{signal}\n\n{final_report}"
        else:
            signal = st.session_state['analysis_result'].get('fix_signal', '')
            disclaimer = get_text("ai_disclaimer")
            export_data = f"{disclaimer}\n\n{signal}"
            
        st.sidebar.download_button(
            label=get_text("download_report"),
            data=export_data,
            file_name=f"HTP_Report_{st.session_state['language_code']}.txt",
            mime="text/plain",
            help=get_text("download_help")
        )

# 侧边栏组件（包含样例加载、上传文件、模型设置等）
def sidebar(model) -> None:
    st.sidebar.markdown(f"## {get_text('sample_drawings')}")
    for idx, (sample_name, sample_path) in enumerate(SAMPLE_IMAGES.items()):
        if st.sidebar.button(get_text("load_sample").format(idx+1), key=f"load_sample_{idx}"):
            try:
                with open(sample_path, "rb") as f:
                    image = Image.open(f)
                    image = resize_image(image)
                    st.session_state['image_data'] = pil_to_base64(image)
                    st.session_state['current_sample'] = sample_name
                    st.sidebar.info(get_text("sample_loaded").format(idx+1))
            except Exception as e:
                st.sidebar.error(str(e))
    
    st.sidebar.markdown(f"## {get_text('analysis_settings')}")
    language = st.sidebar.selectbox(
        get_text("report_language"),
        options=list(SUPPORTED_LANGUAGES.keys()),
        index=list(SUPPORTED_LANGUAGES.keys()).index(st.session_state['language']),
        help=get_text("report_language")
    )
    if language != st.session_state['language']:
        st.session_state['language'] = language
        st.session_state['language_code'] = SUPPORTED_LANGUAGES[language]
        st.experimental_rerun()
        
    uploaded_file = st.sidebar.file_uploader(
        get_text("upload_drawing"),
        type=["jpg", "jpeg", "png"],
        help=get_text("upload_drawing")
    )
    if uploaded_file:
        try:
            image = Image.open(uploaded_file)
            image = resize_image(image)
            image = augment_preprocess(image) 
            st.session_state['image_data'] = pil_to_base64(image)
            st.sidebar.info(get_text("uploaded_info").format(uploaded_file.name))
        except Exception as e:
            st.sidebar.error(str(e))
            
    st.sidebar.markdown(f"## {get_text('model_settings')}")
    base_url = st.sidebar.text_input("API 基础 URL", value=BASE_URL, key="base_url_input")
    api_key = st.sidebar.text_input("API 密钥", type="password", value=BASE_API, key="api_key_input")
    st.session_state.api_key = api_key
    st.session_state.base_url = base_url
    
    st.sidebar.markdown("---")
    # if st.sidebar.button(get_text("start_analysis"), type="primary", key="start_analysis_button"):
    #     st.session_state.start_analysis = True
    if st.sidebar.button(get_text("start_analysis")):
        if not st.session_state.api_key:
            st.error(get_text("error_no_api_key"))
        else:
            analyze_image(model)

    if st.sidebar.button(get_text("reset")):
        reset_session()

    export_report()

# 主内容区域：显示上传状态、分析结果与测试结果下载区域，同时生成测试案例
def main_content() -> None:
    st.title(get_text("app_title"))
    st.write(get_text("welcome_message"))
    
    with st.expander(get_text("instructions_title"), expanded=True):
        st.markdown(get_text("instructions"))
    
    if st.session_state.get('image_data'):
        st.info(get_text("uploaded_info").format("已上传绘画"))
    else:
        st.info(get_text("upload_prompt"))
    
    if st.session_state.get('analysis_result'):
        st.success(get_text("analysis_complete"))
        # 分析摘要部分已删除，直接显示测试结果区域
        st.subheader(get_text("test_result_title"))
        result_text = ""
        if st.session_state['analysis_result'].get("final"):
            result_text = st.session_state['analysis_result'].get("final")
        elif st.session_state['analysis_result'].get("fix_signal"):
            result_text = st.session_state['analysis_result'].get("fix_signal")
        st.text_area("", result_text, height=200)
        st.download_button(
            label=get_text("download_result"),
            data=result_text,
            file_name="HTP_Test_Result.txt",
            mime="text/plain"
        )
    elif st.session_state.get('image_data') and not st.session_state.get('analysis_result'):
        st.warning(get_text("analyzing_image"))
    
    st.markdown("---")
    st.markdown(get_text("disclaimer"))
    
    # 生成测试案例代码：将测试结果报告赋值到 session_state["test_result"]
    st.subheader("测试案例报告")
    if st.button("运行示例测试"):
        st.session_state["test_result"] = (
            """# 测试结果报告
------------------------------
**树木分析：** 整体形态圆润、比例适中，色彩鲜明，传达出积极乐观的心态。

**人物分析：** 人物表情自然、动作活泼，显示出友好和开放的情绪状态。

**整体构图：** 结构均衡，各元素协调融合，营造出温馨和谐的氛围。

### 评估意见:
综合来看，绘画传递出健康、积极的情感状态。建议继续保持平衡的创作风格，此报告仅供参考。如有需要，请结合专业意见进行详细评估。
            """
        )
    if "test_result" in st.session_state:
        st.text_area("", st.session_state["test_result"], height=150)
        st.download_button(
            label="下载测试结果",
            data=st.session_state["test_result"],
            file_name="test_result.txt",
            mime="text/plain"
        )

def main() -> None:
    st.set_page_config(page_title="房树人评估系统", page_icon="🧠", layout="wide")
    # 默认使用中文界面
    if 'language' not in st.session_state:
        st.session_state['language'] = "中文"
    if 'language_code' not in st.session_state:
        st.session_state['language_code'] = SUPPORTED_LANGUAGES[st.session_state['language']]
    for key in ['image_data', 'analysis_result']:
        if key not in st.session_state:
            st.session_state[key] = None
            
    # 初始化模型所需的 session_state 变量
    if 'api_key' not in st.session_state:
        st.session_state["api_key"] = ""
    if 'base_url' not in st.session_state:
        st.session_state["base_url"] = BASE_URL

    # 模型参数设置
    MULTIMODAL_MODEL = "gpt-4o-2024-08-06"
    TEXT_MODEL = "claude-3-5-sonnet-20240620"
    
    text_model = ChatOpenAI(
        api_key=st.session_state.api_key,
        base_url=st.session_state.base_url,
        model=TEXT_MODEL,
        temperature=0.2,
        top_p=0.75,
    )
    multimodal_model = ChatOpenAI(
        api_key=st.session_state.api_key,
        base_url=st.session_state.base_url,
        model=MULTIMODAL_MODEL,
        temperature=0.2,
        top_p=0.75,
    )
    model = HTPModel(
        text_model=text_model,
        multimodal_model=multimodal_model,
        use_cache=True,
    )

    sidebar(model)
    main_content()


def augment_preprocess(image: Image.Image) -> Image.Image: 
    return image

if __name__ == "__main__":
    main()