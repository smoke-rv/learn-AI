import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_model_response(prompt: str) -> dict:
    """
    Викликає OpenAI API та повертає структуровану відповідь.
    """
    try:
        # Виклик OpenAI Chat Completions API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Отримуємо відповідь від моделі
        content = response.choices[0].message.content
        
        return {
            "type": "text",
            "content": content,
            "metadata": {
                "model": response.model,
                "tokens": response.usage.total_tokens
            }
        }
    except Exception as e:
        # Викидаємо помилку для обробки у UI
        raise ValueError(f"OpenAI API Error: {str(e)}")

## --- Streamlit UI Section ---

st.title("Prompt-to-Result Service")
st.caption("Введи промпт, і побачиш магію AI")

# Форма для введення промпта
with st.form(key='prompt_form'):
    user_prompt = st.text_area("Ваш Prompt тут:", height=100, key="prompt_input")
    submit_button = st.form_submit_button(label='Отримати Результат')

# Обробка натискання кнопки
if submit_button and user_prompt:
    st.subheader("✅ AI Response:")
    
    # Використовуємо st.spinner для кращого UX (User Experience)
    with st.spinner('Чекаємо на відповідь від моделі...'):
        try:
            # Виклик OpenAI API
            response_data = get_model_response(user_prompt)
            
            # --- Логіка відображення різних типів контенту ---
            
            response_type = response_data.get("type")
            content = response_data.get("content")
            metadata = response_data.get("metadata", {})
            
            if response_type == "text":
                st.success("Отримано текст:")
                st.markdown(content)
                
            else:
                st.error("Помилка: Невідомий тип відповіді від моделі!")
                st.json(response_data) # Показуємо сирий JSON для Debugging
                
            st.markdown("---")
            st.code(f"Metadata: {metadata}", language="json")

        except ValueError as e:
            # Обробка помилок (Error Handling)
            st.error(f"❌ Model Error: {e}")
            st.warning("Щось пішло не так, мабуть виникла якась помилка.")

elif submit_button:
    st.warning("Не забудьте ввести Prompt! Модель не вміє читати ваші думки (поки що).")