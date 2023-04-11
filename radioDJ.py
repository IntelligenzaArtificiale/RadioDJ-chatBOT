# create streamlit app to inference the model with poe
import streamlit as st
st.set_page_config(
    page_title="Il ChatBOT di RADIO Deejay.it 🚀 X Intelligenza Artificiale Italia",
    page_icon="🚀",
    layout="wide",
    menu_items={
        'Get help': 'https://www.intelligenzaartificialeitalia.net/',
        'Report a bug': "mailto:servizi@intelligenzaartificialeitalia.net",
        'About': "# *Il ChatBOT di RADIO Deejay.it 🚀* "
    }
)

from streamlit_chat_media import message
import you

with open('style.css')as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

img_html = " <center><img src='https://static.wixstatic.com/media/3c029f_7bb91a64433b4422aa475a7f200a63db~mv2.png' class='img-fluid' height='250px' width='auto'></center> "
st.markdown(img_html, unsafe_allow_html=True)

if 'bot' not in st.session_state:
        st.session_state['user'] = []
        st.session_state['bot'] = []
        # mostra il messaggio di benvenuto
        st.session_state['bot'].append('Ciao, sono Il ChatBOT di RADIO Deejay.it 🚀 creato da Intelligenza Artificiale Italia 🧠🤖🇮🇹, puoi chiedermi di spiegarti qualunque cosa e ti risponderò il prima possibile in stile rap o trap 🚀 \n\n🤖 Buon divertimento e ricorda usami in modo responsabile!')
        st.session_state['chat'] = []

 # aggiunge il messaggio in chat
def add_message(content, sender):
    if sender == 'bot':
        st.session_state['bot'].append(content)
    else:
        st.session_state['user'].append(content)
        
        
def decodifica_stringa(stringa):
    return bytes(stringa, 'utf-8').decode('unicode-escape')
            

def export_chat():
    if 'bot' in st.session_state:
        if len(st.session_state['bot']) > 1:
            i = len(st.session_state['bot']) - 1
            l = len(st.session_state['user']) - 1
            
            file_chat = ""
            file_chat += 'Il ChatBOT di RADIO Deejay.it 🚀 X Intelligenza Artificiale Italia 🧠🤖🇮🇹\n\n'
            
            if i == 0:
                file_chat += "🤖 " + st.session_state['bot'][i] + "\n\n"
            else:
                while i > 0 :
                    file_chat += "🤖 >>>" + st.session_state['bot'][i] + "\n\n"
                    try:
                        file_chat += "👤 >>>" + st.session_state['user'][l] + "\n\n"
                        l -= 1
                    except:
                        pass
                    i -= 1
            
            file_chat += "\n\n FINE CHAT 🚀\n\n Il CHATBOT stato creato da Intelligenza Artificiale Italia 🧠🤖🇮🇹 \n\nIntelligenzaArtificialeItalia.net"
            
            st.download_button(
                label="Scarica la chat 🚀",
                data=file_chat,
                file_name='chat.txt',
                mime='text/plain'
            )
            
col1, col2 = st.columns([3, 1])
prompt = col1.text_input("🤔 Cosa vuoi che ti spiego ... Ad esempio 'Radio' o 'Intelligenza Artificiale'")
if col2.button("Chiedi 🚀") and prompt != '':
    template = f"Genera una spiegazione in stile RAP o TRAP su {prompt}, utilizzando delle rime in italiano"
    import ora
    with st.spinner('🚀 Sto generando la risposta...'):
        response = you.Completion.create(
            prompt       = template,
            detailed     = True,
            includelinks = False,
            chat=st.session_state['chat'])
    
        
        add_message(prompt, 'user')
        add_message(decodifica_stringa(stringa=response["response"]), 'bot')        
        st.session_state['chat'].append({"question": prompt, "answer": decodifica_stringa(stringa=response["response"])})
        
if 'bot' in st.session_state:
    i = len(st.session_state['bot']) - 1
    l = len(st.session_state['user']) - 1
    if i == 0:
        message(st.session_state['bot'][i], key=str(i))
    else:
        while i > 0 :
            if i % 3 == 0:
                message("🤖 Questa risposta è stata generata con un modello di Intelligenza Artificiale, se vuoi saperne di più puoi andare su [Intelligenza Artificiale Italia](https://www.intelligenzaartificialeitalia.net/)🧠🤖🇮🇹 il primo portale web in italia ad offrire centinaia di risorse gratuite! Come questo CHATBOT", key=str(i) + '_bot')
            message(st.session_state['bot'][i], key=str(i), allow_html=True)
            try :
                message(st.session_state['user'][l], is_user=True, key=str(i) + '_user')
                l -= 1
            except:
                pass
            i -= 1

export_chat()
if len(st.session_state['bot']) > 1:
    if st.button("Cancella la chat 🤖"):
        if 'user' in st.session_state:
            del st.session_state['user']
        if 'bot' in st.session_state:
            del st.session_state['bot']
        if 'token' in st.session_state:
            del st.session_state['token']
        if 'file_csv' in st.session_state:
            del st.session_state['file_csv']
        st.experimental_rerun()