import streamlit as st, pandas as pd

from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Anagrafica Manutentori Sentieri", layout="wide")

st.title("🌲 Gestione Anagrafica Manutentori")
st.markdown("Database centralizzato per la manutenzione dei sentieri.")

conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    return conn.read(ttl="0")

df = load_data()

menu = st.sidebar.radio("Azioni", ["Consulta e Modifica", "Aggiungi Nuovo", "Elimina Record"])

if menu == "Consulta e Modifica":
    st.header("📋 Tabella Anagrafica")
    st.info("Puoi modificare le celle direttamente nella tabella e cliccare 'Salva Modifiche' in fondo.")
    
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="data_editor")
    
    if st.button("💾 Salva Modifiche"):
        try:
            conn.update(data=edited_df)
            st.success("Dati aggiornati correttamente su Google Sheets!")
            st.rerun()
        except Exception as e:
            st.error(f"Errore durante l'aggiornamento: {e}")

elif menu == "Aggiungi Nuovo":
    st.header("👤 Aggiungi un nuovo Manutentore")
    
    with st.form("new_entry_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input("Cognome e Nome*")
            cf = st.text_input("Codice Fiscale")
            telefono = st.text_input("Telefono")
            mail = st.text_input("Mail")
            gilet = st.selectbox("Taglia Gilet", ["", "S", "M", "L", "XL", "XXL"])
            bollino = st.text_input("Anno ultimo bollino")
            
        with col2:
            piattaforma = st.checkbox("In Piattaforma")
            sentiero1 = st.text_input("Sentiero 1")
            sentiero2 = st.text_input("Sentiero 2")
            note_socio = st.text_area("Note Socio")
            note_manutenzione = st.text_area("Note Manutenzione")

        submitted = st.form_submit_button("Aggiungi a Google Sheets")
        
        if submitted:
            if nome:
                new_row = pd.DataFrame([{
                    "cognome e nome": nome,
                    "Codice fiscale": cf,
                    "Gilet": gilet,
                    "In Piattaforma": "X" if piattaforma else "",
                    "note": note_socio,
                    "anno ultimo bollino": bollino,
                    "telefono": telefono,
                    "mail": mail,
                    "note.1": note_manutenzione, # Pandas rinomina le colonne duplicate
                    "sentiero1": sentiero1,
                    "sentiero2": sentiero2
                }])
                
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(data=updated_df)
                st.success(f"Volontario {nome} aggiunto con successo!")
                st.rerun()
            else:
                st.warning("Il campo 'Cognome e Nome' è obbligatorio.")

elif menu == "Elimina Record":
    st.header("🗑️ Elimina un record")
    
    target_row = st.selectbox("Seleziona il manutentore da eliminare:", df["cognome e nome"].tolist())
    
    if st.button("❗ Elimina Definitivamente"):
        updated_df = df[df["cognome e nome"] != target_row]
        conn.update(data=updated_df)
        st.success(f"Record di {target_row} eliminato.")
        st.rerun()