import traceback
import streamlit as st
from PIL import Image
import pandas as pd

def get_text(key):
    return translations[st.session_state.language][key]

translations = {
    "English": {
        "title": "HTPPDA(House Tree Person Psychological Drawing Agent): A Multi-Agent Multimodal System for Mental Health Detection in Left-Behind Children",
        "introduction": "Introduction of HTP Test",
        "introduction_content": "The House-Tree-Person (HTP) test is a projective psychological assessment tool applicable to both children and adults aged 3 and above. This test aims to provide insights into an individual's personality, emotions, and attitudes through the analysis of drawings.",
        "available_features": """
        
        **Available Features:**
        - **Batch Analysis:** Analyze multiple HTP drawings in bulk
        - **HTP Test:** Take the House-Tree-Person test online
        - **Online Board:** Use our digital drawing tool to create HTP drawings
        """,
        "batch_analysis": "Batch Analysis: Analyze multiple HTP drawings in bulk",
        "htp_test": "HTP Test: Take the House-Tree-Person test online",
        "online_board": "Online Board: Use our digital drawing tool to create HTP drawings",
        "contact_admin": "Please contact the administrator for access to these features.",
        "github_link": "Visit our GitHub repository for more information and updates.",
        "abstract": "Abstract",
        "abstract_content": """
    Left-behind children face severe mental health challenges due to parental migration for work. 
    The House-Tree-Person (HTP) test, a psychological assessment method with higher child participation and cooperation, requires expert interpretation, limiting its application in resource-scarce areas. 
    To address this, we propose **HTPPDA**, a multi-agent system based on Multimodal Large Language Models for automated analysis of HTP drawings and assessment of children's mental health status. 
    The system's workflow comprises feature extraction, analysis, and report generation, accomplished by multiple collaborative agents.
        """,
        "system_workflow": "The Workflow of HTPPDA",
        "key_features": "Key Features",
        "automated_analysis": "Automated Analysis",
        "multi_agent_system": "Multi-Agent System",
        "scalable_solution": "Scalable Solution",
        "evaluation_results": "Evaluation Results",
        "matching_rates": "Matching rates of results with teacher feedback.",
        "participants_note": "Note: All test participants were primary school students. This study was conducted with proper authorization from relevant personnel.",
        "limitations": "Limitations",
        "limitation_content": """
    HTPPDA is designed to provide early detection of mental health issues among left-behind children in resource-constrained areas; however, it does not replace professional medical advice. Its main limitations include:

    Cultural Context: The tool has so far been validated only among children in China, which may limit its applicability across different regions.
    Data Protection: Strict mechanisms must be in place to ensure privacy and adhere to ethical standards.
    Potential Biases: As a tool based on multimodal large language models, it may exhibit inherent biases.
    Long-Term Effectiveness: There is currently insufficient longitudinal research to confirm its sustained efficacy.
    Subtle Cue Detection: It may fail to capture the nuanced emotional signals that human experts can identify during face-to-face assessments.
    Technical Constraints: Its performance may be affected by infrastructure limitations and the user's technological proficiency.
        """,
        "case_study": "Case Study",
        "case_study_content": "See the self-conducted test case studies on the HTPTest page.",
        "footer": "2025 HTPPDA",
    },
    "中文": {
        "title": "HTPPDA: 基于房树人测试的心理健康检测多智能体系统",
        "introduction": "房树人介绍",
        "introduction_content": "房-树-人（HTP）测试是一种适用于3岁及以上儿童和成人的投射性心理评估工具。该测试旨在通过分析绘画来深入了解个体的人格、情感和态度。",
        "available_features": """
        
        **可用功能：** 
        - **批量分析：** 批量分析多个HTP绘画
        - **HTP测试：** 在线进行房树人测试
        - **在线画板：** 使用我们的数字绘图工具创建HTP绘画
        """,
        "batch_analysis": "批量分析：批量分析多个HTP绘画",
        "htp_test": "HTP测试：在线进行房树人测试",
        "online_board": "在线画板：使用我们的数字绘图工具创建HTP绘画",
        "contact_admin": "请联系管理员获取相关功能的访问权限。",
        "github_link": "访问我们的GitHub仓库以获取更多信息和更新。",
        "abstract": "摘要",
        "abstract_content": """
        留守儿童因父母外出务工而面临严重的心理健康挑战。房屋-树木-人物（HTP）测试是一种儿童参与度和配合度较高的心理评估方法，但需专家解读，限制了其在资源匮乏地区的应用。 
        为解决这一问题，我们提出了HTPPDA，一个基于多模态大型语言模型的多智能体系统，用于自动分析HTP绘画并评估儿童心理健康。系统包括特征提取、分析及报告生成，由多个协作智能体共同完成。
        """,
        "system_workflow": "HTPPDA工作流程",
        "key_features": "主要特性",
        "automated_analysis": "自动化分析",
        "multi_agent_system": "多智能体系统",
        "scalable_solution": "可扩展解决方案",
        "evaluation_results": "评估结果",
        "matching_rates": "结果与教师反馈的匹配率。",
        "participants_note": "注：所有测试参与者均为小学生，本研究已获得相关授权。",
        "limitations": "局限性",
        "limitation_content": """
        HTPPDA旨在为资源有限地区的留守儿童提供心理健康问题的早期检测，但不能替代专业的医疗建议。其主要局限性包括：

        文化背景：目前该工具仅在中国儿童群体中得到验证，适用性可能存在区域限制。
        数据保护：需要建立严格的机制以确保用户隐私和遵守伦理标准。
        潜在偏见：作为基于多模态大型语言模型的工具，可能存在固有的偏见问题。
        长期有效性：尚缺乏足够的纵向研究来证实其持续效果。
        细微线索捕捉：可能无法识别人际面对面评估中专家所能捕捉到的微妙情感变化。
        技术限制：实际效果可能会受到基础设施条件和用户操作能力的影响。
        """,
        "case_study": "案例研究",
        "case_study_content": "见HTPTest页面中自行测试的案例研究。",
        "footer": "2025 HTPPDA",
    }
}

def sidebar():  
    # 侧边栏
    with st.sidebar:
        st.title("House-Tree-Person Test")
        st.write("## Language / 语言")
        language = st.selectbox("Choose a language / 选择语言", ["English", "中文"], key="language_selector")
        if language != st.session_state.language:
            st.session_state.language = language
            st.rerun()
            
        st.subheader(get_text("introduction"))
        st.write(get_text("introduction_content"))
        
def main_page():
    st.title(get_text('title'))
    
    st.info(get_text('available_features'))
    
    st.write(f"## {get_text('abstract')}")
    st.write(get_text('abstract_content'))

    st.write(f"## {get_text('limitations')}")
    st.write(get_text('limitation_content'))

    st.write(f"## {get_text('case_study')}")
    st.write(get_text('case_study_content'))

    # 页脚
    st.markdown("---")
    st.write(get_text('footer'))

def main() -> None:
    st.set_page_config(page_title="HTPPDA", page_icon=":house::evergreen_tree:", layout="wide")
    if 'language' not in st.session_state:
        st.session_state.language = "English"
    sidebar()
    main_page()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("An error occurred:")
        traceback.print_exc()
    # input("程序运行完毕，按回车键退出……")