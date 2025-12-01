import streamlit as st

# Тут ми імітуємо виклик AI моделі.
# В реальному житті, тут був би виклик до OpenAI, Gemini, HuggingFace чи іншого API.
def get_model_response(prompt: str) -> dict:
    """
    Імітує виклик моделі та повертає структуровану відповідь.
    Для демонстрації, якщо prompt містить "image" – повертаємо зображення, інакше – текст.
    """
    st.info(f"AI Model called with prompt: '{prompt}'") # QA-логінг у консоль!

    if "image" in prompt.lower():
        # Імітація відповіді, що містить посилання на зображення (наприклад, від DALL-E)
        return {
            "type": "image",
            "content": "https://upload.wikimedia.org/wikipedia/commons/4/47/PNG_transparency_example.png",
            "metadata": {"source": "DALL-E-like model"}
        }
    elif "error" in prompt.lower():
        # Імітація помилки від моделі
        raise ValueError("Model failed to process the request due to internal server error.")
    else:
        # Імітація текстової відповіді (наприклад, від GPT)
        return {
            "type": "text",
            "content": f"Результат від моделі для запиту: '{prompt}'. Мої вітання, це стандартна текстова відповідь.",
            "metadata": {"source": "LLM-like model"}
        }

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
            # Виклик імітованої моделі
            response_data = get_model_response(user_prompt)
            
            # --- Логіка відображення різних типів контенту ---
            
            response_type = response_data.get("type")
            content = response_data.get("content")
            metadata = response_data.get("metadata", {})
            
            if response_type == "text":
                st.success("Отримано текст:")
                st.markdown(f"**{content}**")
                
            elif response_type == "image":
                st.success("Отримано зображення:")
                st.image(content, caption=f"Згенеровано моделлю: {metadata.get('source')}")
                
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