import io
import numpy as np
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas

# Constants
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

SUPPORTED_LANGUAGES = {
    "English": "en",
    "中文": "zh"
}

LANGUAGES = {
    "en": {
        "page_title": "🖌️ HTP Online Drawing Board",
        "drawing_settings": "🎨 Drawing Settings",
        "drawing_mode_label": "Drawing Mode:",
        "stroke_width_label": "Stroke Width:",
        "stroke_color_label": "Stroke Color:",
        "bg_color_label": "Background Color:",
        "instructions_title": "📋 Instructions",
        "instructions": """
- Use this board if you don't have paper and pencil.
- **Important**: For best results, we recommend using traditional paper and pencil.
### How to Use:
1. Adjust drawing settings on the left.
2. Draw on the canvas on the right.
3. Click the **Download Drawing** button to save your artwork.
4. Then you can run test analysis.
        """,
        "download_button": "💾 Download Drawing",
        "download_filename": "htp_drawing.png",
        "download_help": "Save your drawing as a PNG image.",
        "reminder_title": "⭕ Reminder",
        "reminder": """
- After finishing your drawing, please download your image.
- Then proceed with test analysis.
        """,
        "language_label": "Language:",
        "run_test": "Run Test Analysis / 运行测试分析",
        "test_result_title": "Test Result / 测试结果",
        "download_result": "Download Test Result / 下载测试结果"
    },
    "zh": {
        "page_title": "🖌️ 房树人在线画板",
        "drawing_settings": "🎨 绘图设置",
        "drawing_mode_label": "绘图模式：",
        "stroke_width_label": "线条宽度：",
        "stroke_color_label": "线条颜色：",
        "bg_color_label": "背景颜色：",
        "instructions_title": "📋 说明",
        "instructions": """
- 如果您没有纸和笔，可以使用此在线画板。
- **重要提示**：若条件允许，我们建议您使用纸和笔以获得最佳效果。
### 使用方法：
1. 在左侧调整绘图设置。
2. 在右侧画布上绘制。
3. 点击 **下载绘画** 按钮保存作品。
4. 然后运行测试分析。
        """,
        "download_button": "💾 下载绘画",
        "download_filename": "htp_drawing.png",
        "download_help": "将您的绘画保存为 PNG 格式图像。",
        "reminder_title": "⭕ 提醒",
        "reminder": """
- 绘画完成后，请下载您的图像。
- 然后运行测试分析获取结果。
        """,
        "language_label": "语言：",
        "run_test": "运行测试分析 / Run Test Analysis",
        "test_result_title": "测试结果 / Test Result",
        "download_result": "下载测试结果 / Download Test Result"
    }
}

def get_text(key):
    return LANGUAGES[st.session_state['language_code']][key]

def numpy_to_bytes(array, format="PNG"):
    if array.dtype != np.uint8:
        array = (array * 255).astype(np.uint8)
    image = Image.fromarray(array)
    byte_io = io.BytesIO()
    image.save(byte_io, format=format)
    return byte_io.getvalue()

def main():
    st.set_page_config(page_title="HTPPDA: HTP Online Drawing Board", page_icon="🖌️", layout="wide")
    
    if 'language' not in st.session_state:
        st.session_state['language'] = 'English'
    if 'language_code' not in st.session_state:
        st.session_state['language_code'] = SUPPORTED_LANGUAGES[st.session_state['language']]
    
    col_lang, _ = st.columns([2,8])
    with col_lang:
        language = st.selectbox(
            get_text("language_label"),
            options=list(SUPPORTED_LANGUAGES.keys()),
            index=list(SUPPORTED_LANGUAGES.keys()).index(st.session_state['language'])
        )
        if language != st.session_state['language']:
            st.session_state['language'] = language
            st.session_state['language_code'] = SUPPORTED_LANGUAGES[language]
            st.experimental_rerun()
    
    st.title(get_text("page_title"))
    col_settings, col_canvas = st.columns(2)
    with col_settings:
        st.header(get_text("drawing_settings"))
        drawing_mode = st.selectbox(get_text("drawing_mode_label"), options=("freedraw", "line", "rect", "circle"), help=get_text("drawing_mode_label"))
        stroke_width = st.slider(get_text("stroke_width_label"), 1, 25, 3)
        stroke_color = st.color_picker(get_text("stroke_color_label"), "#000000")
        bg_color = st.color_picker(get_text("bg_color_label"), "#FFFFFF")
    with col_canvas:
        st.header(get_text("page_title"))
        canvas_result = st_canvas(
            fill_color="rgba(0, 0, 0, 0)",
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_color=bg_color,
            background_image=None,
            update_streamlit=True,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            drawing_mode=drawing_mode,
            key="canvas"
        )
        if canvas_result.image_data is not None:
            img_bytes = numpy_to_bytes(canvas_result.image_data)
            st.download_button(
                label=get_text("download_button"),
                data=img_bytes,
                file_name=get_text("download_filename"),
                mime="image/png",
                help=get_text("download_help")
            )
    st.header(get_text("instructions_title"))
    st.markdown(get_text("instructions"))
    st.header(get_text("reminder_title"))
    st.markdown(get_text("reminder"))
    
    # # 新增：测试分析 – 点击按钮后模拟生成测试结果，并直接显示在页面下方，同时提供下载
    # if st.button(get_text("run_test")):
    #     if canvas_result.image_data is not None:
    #         simulated_result = (
    #             "Analysis Result:\n"
    #             "-----------------\n"
    #             "Your drawing exhibits a balanced layout with vivid colors.\n"
    #             "Detailed features are analyzed here.\n\nFor the full report, please see the downloaded file."
    #         )
    #         st.session_state["test_result"] = simulated_result
    #     else:
    #         st.error("No drawing data available to analyze!")
    
    # if "test_result" in st.session_state:
    #     st.subheader(get_text("test_result_title"))
    #     st.text_area("", st.session_state["test_result"], height=200)
    #     st.download_button(
    #         label=get_text("download_result"),
    #         data=st.session_state["test_result"],
    #         file_name="OnlineBoard_Test_Result.txt",
    #         mime="text/plain"
    #     )

if __name__ == "__main__":
    main()