import streamlit as st, cloudinary, time

from datetime import datetime

from utils.cloudinary_handler import upload_file_cloudinary
from utils.gsheets_handler import get_sheet

cloudinary.config(
    cloud_name = st.secrets["cloudinary"]["cloud_name"],
    api_key = st.secrets["cloudinary"]["api_key"], 
    api_secret = st.secrets["cloudinary"]["api_secret"],
    secure = True
)

if 'form_id' not in st.session_state:
    st.session_state.form_id = 0

def reset_form():
    st.session_state.form_id += 1
    st.rerun()

def main():
    st.set_page_config(page_title="C.A.I. Siena - Manutenzione", page_icon="🏔️")
    st.title("🏔️ MANUTENZIONE SENTIERI C.A.I. SIENA")
    st.info("Il nome e l'indirizzo email associati al tuo account verranno registrati.")

    if True:
        st.header("Operatore e sentiero")
        nome_operatore = st.text_input("Nome e cognome degli operatori *", key=f"nome_{st.session_state.form_id}")
        numero_sentiero = st.text_input("Numero del sentiero *", key=f"numero_{st.session_state.form_id}")
        tratto_sentiero = st.text_input("Tratto del sentiero oggetto di manutenzione *", key=f"tratto_{st.session_state.form_id}")

        tipo_intervento = st.radio("Tipo intervento *", ["Manutenzione ordinaria", "Manutenzione straordinaria"], key=f"intervento_{st.session_state.form_id}")

        descrizione_straordinaria = ""
        if tipo_intervento == "Manutenzione straordinaria":
            st.warning("⚠️ Dettagli Intervento Straordinario")
            descrizione_straordinaria = st.text_area("Descrizione intervento straordinario *", key=f"descrizione_{st.session_state.form_id}")

        st.markdown("---")

        st.header("Dati sull'intervento effettuato e stato del sentiero")
        data_intervento = st.date_input("Data intervento *", datetime.now(), key=f"data_{st.session_state.form_id}")
        
        interventi_effettuati = st.multiselect(
            "Intervento effettuato *",
            [
                "Sopralluogo, verifica", "Posa tabelle segnavia", "Posa pali sostegno",
                "Segnaletica orizzontale", "Sistemazione fondo", "Decespugliamento",
                "Sramatura", "Manutenzione attrezzature", "Rilievo cartografico", "Altro (specificare in note)"
            ],
            key=f"interventi_{st.session_state.form_id}"
        )
        
        stato_tratto = st.radio(
            "Stato attuale del tratto *",
            ["Tratto normalmente percorribile", "Tratto difficilmente percorribile", "Tratto non percorribile"],
            key=f"stato_{st.session_state.form_id}"
        )

        foto_georeferenziate = st.file_uploader(
            "Foto georeferenziate ante e post intervento (Max 10 file)", 
            accept_multiple_files=True,
            key=f"foto_{st.session_state.form_id}"
        )

        st.markdown("---")

        st.header("Spese sostenute")
        km_auto = st.number_input("Km effettuati con la propria auto per l'effettuazione della manutenzione", min_value=0, key=f"km_{st.session_state.form_id}")

        documentazione_spese = st.file_uploader(
            "Upload documentazione comprovante la spesa (Scontrini, fatture, ecc)", 
            type=["pdf", "jpg", "png"],
            accept_multiple_files=True,
            key=f"documentazione_{st.session_state.form_id}"
        )

        st.markdown("---")

        st.header("Note ed osservazioni")
        note = st.text_area("Note ed osservazioni", key=f"note_{st.session_state.form_id}")

        if st.button("INVIA"):
            if not nome_operatore or not numero_sentiero:
                st.error("Per favore, compila i campi obbligatori!")
            else:
                link_foto = []
                if foto_georeferenziate:
                    with st.spinner("Caricamento in corso..."):
                        for i, foto in enumerate(foto_georeferenziate):
                            file_url = upload_file_cloudinary(foto, numero_sentiero, i, prefix="foto")
                            link_foto.append(file_url)
                        
                    # if "image" in upload_result.get("resource_type"):
                    #     st.image(file_url, caption="Anteprima immagine caricata")
                    # else:
                    #     st.write(f"📄 [Clicca qui per visualizzare il PDF]({file_url})")
                       
                link_documentazione = []
                if documentazione_spese:
                    # try:
                        with st.spinner("Caricamento in corso..."):
                            for i, doc in enumerate(documentazione_spese):
                                file_url = upload_file_cloudinary(doc, numero_sentiero, i, prefix="spese")
                                link_documentazione.append(file_url)
                    # except Exception as e:
                    #     st.error(f"Si è verificato un errore durante l'upload: {e}")
 
                nuova_riga = [str(datetime.now()), nome_operatore, numero_sentiero, tratto_sentiero, tipo_intervento, descrizione_straordinaria, 
                              str(data_intervento), ", ".join(interventi_effettuati), km_auto, stato_tratto, note, ", ".join(link_foto), ", ".join(link_documentazione)]
                
                sheet = get_sheet()
                sheet.append_row(nuova_riga)
                                                
                st.success("Dati salvati su Google Sheet e foto caricate su Drive!")
                st.balloons()
                time.sleep(3)
                st.session_state.form_id += 1
                st.rerun()
                      
            #except Exception as e:
            #    print (e)
            #    st.error(f"Errore durante il salvataggio: {e}")                

if __name__ == "__main__":
    main()
