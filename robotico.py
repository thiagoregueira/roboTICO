import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

# Configurando a página
st.set_page_config(
    page_title="roboTICO",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# CSS
st.markdown(
    """
    <style>
    p {
        text-align: justify;
        text-indent: 32px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Colocando minhas informações no sidebar
st.sidebar.markdown("<h1>Desenvolvido por:</h1>", unsafe_allow_html=True)
st.sidebar.markdown("[Thiago Regueira](https://bento.me/thiagoregueira)")
st.sidebar.subheader("Breve descrição do roboTICO:")
st.sidebar.markdown(
    """
    <p>O nome roboTICO é uma mistura de robô com o apelido que tenho desde a minha infancia, "TICO", acredito que seja devido ao meu nome, Thiago.</p>
    <p>O projeto é um chatbot desenvolvido em Python, utilizando a biblioteca Streamlit para a interface do usuário e a API do Google Generative AI para a geração de respostas.</p>
    <p>O arquivo principal do projeto é o robotico.py, que configura a interface do usuário, carrega uma imagem de avatar para o bot, configura a chave da API do Google Generative AI e inicializa o modelo e o histórico de bate-papo.</p>
    <p>Além disso, o projeto usa variáveis de ambiente para armazenar informações sensíveis, como a chave da API do Google, e usa a função load_dotenv() para carregá-la.</p>
    """,
    unsafe_allow_html=True,
)

st.title("roboTICO - Seu TICO e TECO virtual!")

# carregando a foto do bot
chatbot_avatar = Image.open(os.path.join("images", "profile-pic.png"))

# Configurando a chave da API
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Selecione o modelo
model = genai.GenerativeModel("gemini-pro")

# Inicialize o histórico de bate-papo
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Oi! Sou o roboTICO, converse comigo!"}
    ]

# Exibe mensagens de bate-papo do histórico na reexecução do aplicativo
for message in st.session_state.messages:
    with st.chat_message(
        message["role"],
        avatar=chatbot_avatar if message["role"] == "assistant" else None,
    ):
        st.markdown(message["content"])


def llm_function(query):
    # Verifica se o input do usuário contém um número
    if any(char.isdigit() for char in query):
        response_text = "Infelizmente, Ainda não aprendi a mexer com números. Favor só enviar palavras."
    else:
        response = model.generate_content(query)
        response_text = " ".join([part.text for part in response.parts])

    # Exibindo a mensagem do assistente com a foto do bot
    with st.chat_message("assistant", avatar=chatbot_avatar):
        st.markdown(response_text, unsafe_allow_html=True)

    # Armazenando a mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": query})

    # Armazenando a mensagem do usuário
    st.session_state.messages.append({"role": "assistant", "content": response_text})


# Aceita entrada do usuário
query = st.chat_input("Manda!")

# Chamando a função quando a entrada é fornecida
if query:
    # Exibindo a mensagem do usuário
    with st.chat_message("user"):
        st.markdown(query)

    llm_function(query)
