import difflib
import ast
import streamlit as st
import google.generativeai as genai
import re

# Access the API key from secrets
Api_key = st.secrets["Api_key"]

# Set up Gemini Model API key
genai.configure(api_key=Api_key)

# Combined list of existing company names in both Arabic and English
existing_companies = [
    "Tech Innovators Inc.", "شركة المبدعين التقنيين",
    "Global Solutions Ltd.", "حلول عالمية",
    "Bright Future Enterprises", "مستقبل مشرق",
    "Creative Minds LLC", "عقول مبتكرة",
    "NextGen Technologies", "تقنيات الجيل القادم",
    "ADNOC", "أدنوك",
    "DP World", "موانئ دبي العالمية",
    "Emirates Group", "مجموعة الإمارات",
    "Emaar Properties", "إعمار العقارية",
    "First Abu Dhabi Bank", "بنك أبوظبي الأول",
    "Mubadala Investment Company", "شركة مبادلة للاستثمار",
    "National Oil Company", "شركة النفط الوطنية",
    "Saudi Aramco", "أرامكو السعودية",
    "Dubai International Financial Centre", "مركز دبي المالي العالمي",
    "Abu Dhabi Commercial Bank", "بنك أبوظبي التجاري"
]

def is_arabic(text):
    """Check if the text is Arabic based on Unicode range."""
    return bool(re.search(r'[\u0600-\u06FF]', text))

def check_name_availability(proposed_name, existing_names):
    """Check if the proposed name is already taken or similar to existing names."""
    similar_names = []
    for name in existing_names:
        if difflib.SequenceMatcher(None, proposed_name, name).ratio() > 0.8:
            similar_names.append(name)
    return similar_names

def filter_similar_names(generated_names, existing_names):
    """Filter out generated names that are too similar to existing names."""
    filtered_names = []
    for generated_name in generated_names:
        if not any(difflib.SequenceMatcher(None, generated_name, existing_name).ratio() > 0.8 for existing_name in existing_names):
            filtered_names.append(generated_name)
    return filtered_names

def generate_name_suggestions(company_info, num_names=10, language="en"):
    """Generate name suggestions using Gemini API."""
    model = genai.GenerativeModel("gemini-pro")
    
    if language == "ar":
        st.write("Detected arabic")
        prompt = (f"Q: اقترح 7 إلى 10 أسماء شركات فريدة بناءً على المعلومات التالية:\n"
                  f"A: الصناعة: {company_info['industry']}\n"
                  f"A: الميزة الفريدة: {company_info['unique_feature']}\n"
                  f"اقترح أسماء تكون مبتكرة ومناسبة لشركة في هذه الصناعة.\n"
                  f"أعد قائمة بأسماء الشركات المقترحة في صيغة Python.")
    else:
        prompt = (f"Q: Generate 7 to 10 unique company names based on the following information:\n"
                  f"A: Industry: {company_info['industry']}\n"
                  f"A: Unique Feature: {company_info['unique_feature']}\n"
                  f"Generate names that are creative and appropriate for a company in this industry.\n"
                  f"Return a python list of the Generated Names.")
    
    response = model.generate_content(prompt)
    generated_text = response.text

    start = generated_text.find("[")
    end = generated_text.rfind("]") + 1
    companies_list = ast.literal_eval(generated_text[start:end])
    
    return filter_similar_names(companies_list, existing_names)

def generate_updated_name(similar_name, language="en"):
    """Generate a slightly updated version of a similar name using Gemini API."""
    model = genai.GenerativeModel("gemini-pro")
    
    if language == "ar":
        prompt = (f"Q: اقترح نسخة محدثة من الاسم التالي بحيث تكون مميزة ولكن لا تزال معروفة:\n"
                  f"A: اسم الشركة الأصلي: {similar_name}\n"
                  f"اقترح أسماء تكون محدثة لاسم الشركة الأصلي.\n"
                  f"أعد قائمة بالأسماء المقترحة في صيغة Python.")
    else:
        prompt = (f"Q: Provide an updated version of the following company name that is still recognizable but distinct:\n"
                  f"A: Original Company Name: {similar_name}\n"
                  f"Generate names that are updated versions of this name.\n"
                  f"Return a python list of the updated names.")
    
    response = model.generate_content(prompt)
    generated_text = response.text

    start = generated_text.find("[")
    end = generated_text.rfind("]") + 1
    updated_names_list = ast.literal_eval(generated_text[start:end])
    
    return filter_similar_names(updated_names_list, existing_companies)

def main():
    # Language selection
    language = st.selectbox("Select Language / اختر اللغة", ("English", "العربية"))

    # Define text for both languages
    text = {
        "English": {
            "title": "Company Name Availability Checker & Generator",
            "instruction": "Enter a proposed company name to check its availability and get suggestions if it's taken.",
            "proposed_name": "Enter the proposed company name:",
            "name_taken": "The proposed name is taken or similar to an existing company name.",
            "similar_names": "Here are some similar names that are already taken:",
            "generating_names": "Generating updated names based on similar names...",
            "updated_suggestions": "Updated name suggestions for",
            "additional_info": "To help generate better names, please answer the following questions:",
            "industry": "Enter the industry of your company:",
            "unique_feature": "Enter a unique feature of your company:",
            "suggested_names": "Here are some suggested names for your new company:",
            "no_suggestions": "Sorry, we couldn't generate any new names at the moment.",
            "name_available": "The proposed name is available. You can use it for your new company."
        },
        "العربية": {
            "title": "مدقق ومولد توفر أسماء الشركات",
            "instruction": "أدخل الاسم المقترح للشركة للتحقق من توفره والحصول على اقتراحات إذا كان الاسم مستخدمًا.",
            "proposed_name": "أدخل الاسم المقترح للشركة:",
            "name_taken": "الاسم المقترح مستخدم أو مشابه لاسم شركة موجودة.",
            "similar_names": "إليك بعض الأسماء المشابهة التي تم استخدامها بالفعل:",
            "generating_names": "جارٍ إنشاء أسماء محدثة بناءً على الأسماء المشابهة...",
            "updated_suggestions": "اقتراحات أسماء محدثة لـ",
            "additional_info": "للمساعدة في إنشاء أسماء أفضل، يرجى الإجابة على الأسئلة التالية:",
            "industry": "أدخل مجال عمل شركتك:",
            "unique_feature": "أدخل ميزة فريدة لشركتك:",
            "suggested_names": "إليك بعض الأسماء المقترحة لشركتك الجديدة:",
            "no_suggestions": "عذرًا، لم نتمكن من إنشاء أي أسماء جديدة في الوقت الحالي.",
            "name_available": "الاسم المقترح متاح. يمكنك استخدامه لشركتك الجديدة."
        }
    }

    # Set the current language
    lang = text[language]

    st.title(lang["title"])
    st.write(lang["instruction"])

    # Step 1: User input for proposed company name
    proposed_name = st.text_input(lang["proposed_name"])

    if proposed_name:
        # Detect the language of the proposed name
        name_language = "ar" if is_arabic(proposed_name) else "en"

        # Step 2: Check if the name is accepted or taken
        similar_names = check_name_availability(proposed_name, existing_companies)
        
        if similar_names:
            # Name is taken, display similar names
            st.warning(lang["name_taken"])
            st.write(lang["similar_names"])
            st.write(similar_names)
            
            # Generate updated names based on similar names
            st.info(lang["generating_names"])
            for similar_name in similar_names:
                updated_names = generate_updated_name(similar_name, language=name_language)
                if updated_names:
                    st.write(f"{lang['updated_suggestions']} '{similar_name}':")
                    st.write(updated_names)

            # Step 3: Ask for additional information to generate new name suggestions
            st.write(lang["additional_info"])
            industry = st.text_input(lang["industry"])
            unique_feature = st.text_input(lang["unique_feature"])

            if industry and unique_feature:
                company_info = {
                    'industry': industry,
                    'unique_feature': unique_feature
                }
                
                # Generate and display new name suggestions
                suggestions = generate_name_suggestions(company_info, language=name_language)
                if suggestions:
                    st.success(lang["suggested_names"])
                    st.write(suggestions)
                else:
                    st.error(lang["no_suggestions"])
        else:
            # Name is available
            st.success(lang["name_available"])

if __name__ == "__main__":
    main()
